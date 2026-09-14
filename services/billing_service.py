"""
Billing Service managing customers, point-of-sale transactions, and invoice history.
Ensures transaction consistency for bill generation and stock reduction.
"""

from typing import List, Dict, Any, Optional, Tuple
import sqlite3
from database.db_helper import DBHelper
from models.bill import Bill, BillItem
from models.customer import Customer


class BillingService:
    @staticmethod
    def get_or_create_customer(phone: str, name: str = "Walk-in Customer", email: str = "", address: str = "") -> Customer:
        """Finds existing customer by phone number or creates a new customer."""
        if not phone or not phone.strip():
            return Customer(phone="N/A", name=name or "Walk-in Customer")

        phone_clean = phone.strip()
        query = "SELECT customer_id, phone, name, email, address FROM customers WHERE phone = %s"
        row = DBHelper.fetch_one(query, (phone_clean,))
        if row:
            return Customer.from_dict(row)

        insert_query = "INSERT INTO customers (phone, name, email, address) VALUES (%s, %s, %s, %s)"
        cust_id = DBHelper.execute_query(insert_query, (phone_clean, name.strip() or "Customer", email.strip(), address.strip()), commit=True)
        return Customer(customer_id=cust_id, phone=phone_clean, name=name, email=email, address=address)

    @staticmethod
    def process_sale_transaction(bill: Bill) -> Tuple[bool, str]:
        """
        Processes a full sale transaction atomically:
        1. Checks sufficient stock for all line items.
        2. Inserts record into `invoices` table.
        3. Inserts all `invoice_items`.
        4. Decrements product stock quantity in `products` table.
        """
        if not bill.items:
            return False, "Cannot process empty bill. Please add items to cart."

        conn = DBHelper.get_raw_connection()
        is_sqlite = isinstance(conn, sqlite3.Connection)
        try:
            cursor = conn.cursor()

            # 1. Validate stock
            for item in bill.items:
                sel_sql = "SELECT name, quantity FROM products WHERE product_id = ?" if is_sqlite else "SELECT name, quantity FROM products WHERE product_id = %s FOR UPDATE"
                cursor.execute(sel_sql, (item.product_id,))
                prod = cursor.fetchone()
                if not prod:
                    conn.rollback()
                    if is_sqlite:
                        conn.close()
                    return False, f"Product ID {item.product_id} not found."

                avail_qty = prod["quantity"] if isinstance(prod, (dict, sqlite3.Row)) else prod[1]
                prod_title = prod["name"] if isinstance(prod, (dict, sqlite3.Row)) else prod[0]

                if avail_qty < item.quantity:
                    conn.rollback()
                    if is_sqlite:
                        conn.close()
                    return False, f"Insufficient stock for '{prod_title}'. Available: {avail_qty}"

            # 2. Insert invoice header
            inv_sql = (
                "INSERT INTO invoices (invoice_no, customer_id, customer_name, customer_phone, subtotal, tax_percent, tax_amount, discount_percent, discount_amount, grand_total, payment_mode) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                if is_sqlite else
                "INSERT INTO invoices (invoice_no, customer_id, customer_name, customer_phone, subtotal, tax_percent, tax_amount, discount_percent, discount_amount, grand_total, payment_mode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )
            cursor.execute(inv_sql, (
                bill.invoice_no,
                bill.customer_id,
                bill.customer_name,
                bill.customer_phone,
                bill.subtotal,
                bill.tax_percent,
                bill.tax_amount,
                bill.discount_percent,
                bill.discount_amount,
                bill.grand_total,
                bill.payment_mode
            ))

            # 3. Insert invoice items & 4. Deduct stock
            item_sql = (
                "INSERT INTO invoice_items (invoice_no, product_id, product_name, unit_price, quantity, line_total) VALUES (?, ?, ?, ?, ?, ?)"
                if is_sqlite else
                "INSERT INTO invoice_items (invoice_no, product_id, product_name, unit_price, quantity, line_total) VALUES (%s, %s, %s, %s, %s, %s)"
            )
            update_sql = (
                "UPDATE products SET quantity = quantity - ? WHERE product_id = ?"
                if is_sqlite else
                "UPDATE products SET quantity = quantity - %s WHERE product_id = %s"
            )

            for item in bill.items:
                cursor.execute(item_sql, (
                    bill.invoice_no,
                    item.product_id,
                    item.product_name,
                    item.unit_price,
                    item.quantity,
                    item.line_total
                ))
                cursor.execute(update_sql, (item.quantity, item.product_id))

            conn.commit()
            cursor.close()
            if is_sqlite:
                conn.close()
            return True, f"Invoice {bill.invoice_no} completed successfully!"

        except Exception as e:
            conn.rollback()
            if is_sqlite:
                conn.close()
            return False, f"Transaction failed: {str(e)}"
