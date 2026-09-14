"""
Utility to generate and export formatted printable invoice receipts.
"""

import os
from typing import Dict, Any, List
from models.bill import Bill


class InvoiceGenerator:
    INVOICES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "invoices_saved")

    @classmethod
    def generate_receipt_text(cls, bill_data: Dict[str, Any], items: List[Dict[str, Any]]) -> str:
        """
        Generates a clean, monospaced thermal-printer styled text receipt.
        """
        width = 46
        lines = []
        lines.append("=" * width)
        lines.append("        SMART SHOP RETAIL STORE         ")
        lines.append("     123 Market Street, Main City       ")
        lines.append("         Phone: +91 98765 43210         ")
        lines.append("=" * width)
        
        inv_no = bill_data.get("invoice_no", "N/A")
        date_str = bill_data.get("formatted_date") or bill_data.get("invoice_date", "")
        cust_name = bill_data.get("customer_name", "Walk-in Customer")
        cust_phone = bill_data.get("customer_phone", "N/A")
        pay_mode = bill_data.get("payment_mode", "Cash")

        lines.append(f"Invoice No : {inv_no}")
        lines.append(f"Date & Time: {date_str}")
        lines.append(f"Customer   : {cust_name}")
        lines.append(f"Phone      : {cust_phone}")
        lines.append(f"Payment    : {pay_mode}")
        lines.append("-" * width)
        lines.append(f"{'Item Description':<20} {'Qty':>4} {'Price':>9} {'Total':>9}")
        lines.append("-" * width)

        for item in items:
            name = item.get("product_name", "")
            qty = item.get("quantity", 0)
            price = float(item.get("unit_price", 0.0))
            tot = float(item.get("line_total", 0.0))
            
            # Shorten name if needed
            short_name = (name[:18] + "..") if len(name) > 20 else name
            lines.append(f"{short_name:<20} {qty:>4} {price:>9.2f} {tot:>9.2f}")

        lines.append("-" * width)
        subtotal = float(bill_data.get("subtotal", 0.0))
        discount = float(bill_data.get("discount_amount", 0.0))
        tax = float(bill_data.get("tax_amount", 0.0))
        grand_total = float(bill_data.get("grand_total", 0.0))
        tax_pct = float(bill_data.get("tax_percent", 0.0))
        disc_pct = float(bill_data.get("discount_percent", 0.0))

        lines.append(f"{'Subtotal:':<30} {subtotal:>15.2f}")
        if discount > 0:
            lines.append(f"{f'Discount ({disc_pct}%):':<30} {-discount:>15.2f}")
        if tax > 0:
            lines.append(f"{f'GST / Tax ({tax_pct}%):':<30} {tax:>15.2f}")
        lines.append("=" * width)
        lines.append(f"{'GRAND TOTAL (INR):':<30} {grand_total:>15.2f}")
        lines.append("=" * width)
        lines.append("      THANK YOU FOR SHOPPING WITH US!   ")
        lines.append("         PLEASE VISIT US AGAIN!         ")
        lines.append("=" * width)
        
        return "\n".join(lines)

    @classmethod
    def save_receipt_to_file(cls, bill_data: Dict[str, Any], items: List[Dict[str, Any]]) -> str:
        """Saves receipt text to disk in invoices_saved folder."""
        if not os.path.exists(cls.INVOICES_DIR):
            os.makedirs(cls.INVOICES_DIR, exist_ok=True)
        
        receipt_text = cls.generate_receipt_text(bill_data, items)
        inv_no = bill_data.get("invoice_no", "invoice").replace(":", "_").replace("/", "_")
        filepath = os.path.join(cls.INVOICES_DIR, f"{inv_no}.txt")
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(receipt_text)
            
        return filepath
