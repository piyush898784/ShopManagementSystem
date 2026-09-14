"""
Fast & Smooth Point of Sale (POS) and Billing View.
Optimized for high-speed checkout and responsive UI.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ui.theme import Theme
from services.inventory_service import InventoryService
from services.billing_service import BillingService
from models.bill import Bill
from utils.invoice_generator import InvoiceGenerator


class BillingView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=Theme.BACKGROUND)
        self.current_bill = Bill()
        self.catalog_cache = []
        self.create_widgets()
        self.load_inventory_catalog()

    def create_widgets(self):
        # Top Header Bar
        header_frame = tk.Frame(self, bg=Theme.BACKGROUND)
        header_frame.pack(fill="x", padx=16, pady=(10, 8))

        tk.Label(
            header_frame,
            text="⚡ Point of Sale (POS) & Billing",
            font=Theme.FONT_TITLE,
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT_MAIN
        ).pack(side="left")

        self.lbl_inv_number = tk.Label(
            header_frame,
            text=f"Bill No: {self.current_bill.invoice_no}",
            font=Theme.FONT_BODY_BOLD,
            bg="#dbeafe",
            fg="#1d4ed8",
            padx=10,
            pady=3
        )
        self.lbl_inv_number.pack(side="right")

        # Main 2-Column Split
        body_frame = tk.Frame(self, bg=Theme.BACKGROUND)
        body_frame.pack(fill="both", expand=True, padx=16, pady=(0, 10))

        # --- LEFT: Catalog Selection ---
        left_card = tk.Frame(body_frame, bg=Theme.SURFACE, bd=1, relief="solid", padx=12, pady=12)
        left_card.pack(side="left", fill="both", expand=True, padx=(0, 8))

        tk.Label(left_card, text="Product Catalog", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE, fg=Theme.TEXT_MAIN).pack(anchor="w", pady=(0, 6))

        # Search Bar
        search_box = tk.Frame(left_card, bg=Theme.SURFACE)
        search_box.pack(fill="x", pady=(0, 6))

        tk.Label(search_box, text="🔍 Search:", font=Theme.FONT_BODY_BOLD, bg=Theme.SURFACE).pack(side="left", padx=(0, 4))
        self.ent_search = ttk.Entry(search_box, width=18)
        self.ent_search.pack(side="left", fill="x", expand=True, padx=(0, 4))
        self.ent_search.bind("<KeyRelease>", lambda e: self.filter_catalog())
        self.ent_search.bind("<Return>", lambda e: self.add_selected_or_first())

        # Catalog Table
        cat_frame = tk.Frame(left_card, bg=Theme.SURFACE)
        cat_frame.pack(fill="both", expand=True, pady=(0, 8))

        cols = ("id", "name", "price", "stock")
        self.tree_catalog = ttk.Treeview(cat_frame, columns=cols, show="headings", height=8, selectmode="browse")
        self.tree_catalog.heading("id", text="ID")
        self.tree_catalog.heading("name", text="Product Description")
        self.tree_catalog.heading("price", text="Price (₹)")
        self.tree_catalog.heading("stock", text="Stock")

        self.tree_catalog.column("id", width=38, anchor="center")
        self.tree_catalog.column("name", width=190, anchor="w")
        self.tree_catalog.column("price", width=70, anchor="e")
        self.tree_catalog.column("stock", width=55, anchor="center")

        cat_scroll = ttk.Scrollbar(cat_frame, orient="vertical", command=self.tree_catalog.yview)
        self.tree_catalog.configure(yscrollcommand=cat_scroll.set)

        self.tree_catalog.pack(side="left", fill="both", expand=True)
        cat_scroll.pack(side="right", fill="y")
        self.tree_catalog.bind("<Double-1>", lambda e: self.handle_add_to_cart())

        # Add to Cart Controls
        add_ctrl = tk.Frame(left_card, bg=Theme.SURFACE)
        add_ctrl.pack(fill="x")

        tk.Label(add_ctrl, text="Qty:", font=Theme.FONT_BODY_BOLD, bg=Theme.SURFACE).pack(side="left", padx=(0, 4))
        self.spin_qty = ttk.Spinbox(add_ctrl, from_=1, to=999, width=5)
        self.spin_qty.set(1)
        self.spin_qty.pack(side="left", padx=(0, 8))

        btn_add = ttk.Button(add_ctrl, text="🛒 Add to Cart", style="Primary.TButton", command=self.handle_add_to_cart)
        btn_add.pack(side="left", fill="x", expand=True)

        # --- RIGHT: Cart & Checkout ---
        right_card = tk.Frame(body_frame, bg=Theme.SURFACE, bd=1, relief="solid", padx=12, pady=12)
        right_card.pack(side="right", fill="both", expand=True)

        # Customer Row
        cust_row = tk.Frame(right_card, bg=Theme.SURFACE)
        cust_row.pack(fill="x", pady=(0, 6))

        tk.Label(cust_row, text="Phone:", font=Theme.FONT_BODY_BOLD, bg=Theme.SURFACE).pack(side="left", padx=(0, 2))
        self.ent_phone = ttk.Entry(cust_row, width=12)
        self.ent_phone.pack(side="left", padx=(0, 8))

        tk.Label(cust_row, text="Name:", font=Theme.FONT_BODY_BOLD, bg=Theme.SURFACE).pack(side="left", padx=(0, 2))
        self.ent_name = ttk.Entry(cust_row, width=14)
        self.ent_name.insert(0, "Walk-in Customer")
        self.ent_name.pack(side="left", fill="x", expand=True)

        # Cart Table
        cart_frame = tk.Frame(right_card, bg=Theme.SURFACE)
        cart_frame.pack(fill="both", expand=True, pady=(0, 6))

        cart_cols = ("id", "name", "price", "qty", "total")
        self.tree_cart = ttk.Treeview(cart_frame, columns=cart_cols, show="headings", height=5, selectmode="browse")
        self.tree_cart.heading("id", text="ID")
        self.tree_cart.heading("name", text="Item")
        self.tree_cart.heading("price", text="Price")
        self.tree_cart.heading("qty", text="Qty")
        self.tree_cart.heading("total", text="Total (₹)")

        self.tree_cart.column("id", width=32, anchor="center")
        self.tree_cart.column("name", width=150, anchor="w")
        self.tree_cart.column("price", width=60, anchor="e")
        self.tree_cart.column("qty", width=40, anchor="center")
        self.tree_cart.column("total", width=65, anchor="e")

        cart_scroll = ttk.Scrollbar(cart_frame, orient="vertical", command=self.tree_cart.yview)
        self.tree_cart.configure(yscrollcommand=cart_scroll.set)

        self.tree_cart.pack(side="left", fill="both", expand=True)
        cart_scroll.pack(side="right", fill="y")

        # Cart Action Buttons
        cart_btns = tk.Frame(right_card, bg=Theme.SURFACE)
        cart_btns.pack(fill="x", pady=(0, 6))

        ttk.Button(cart_btns, text="Remove Item", style="Danger.TButton", command=self.handle_remove_cart_item).pack(side="left", padx=(0, 4))
        ttk.Button(cart_btns, text="Clear Cart", style="Secondary.TButton", command=self.handle_clear_cart).pack(side="left")

        # Calculation Panel
        calc_card = tk.Frame(right_card, bg="#f1f5f9", bd=1, relief="solid", padx=10, pady=8)
        calc_card.pack(fill="x", pady=(0, 6))

        r1 = tk.Frame(calc_card, bg="#f1f5f9")
        r1.pack(fill="x", pady=2)
        tk.Label(r1, text="Subtotal: ₹", font=Theme.FONT_BODY_BOLD, bg="#f1f5f9").pack(side="left")
        self.lbl_subtotal = tk.Label(r1, text="0.00", font=Theme.FONT_BODY_BOLD, bg="#f1f5f9")
        self.lbl_subtotal.pack(side="left", padx=(0, 15))

        tk.Label(r1, text="Disc (%):", font=Theme.FONT_BODY_BOLD, bg="#f1f5f9").pack(side="left")
        self.ent_discount = ttk.Entry(r1, width=4)
        self.ent_discount.insert(0, "0")
        self.ent_discount.pack(side="left", padx=(2, 0))
        self.ent_discount.bind("<KeyRelease>", lambda e: self.recalculate_totals())

        r2 = tk.Frame(calc_card, bg="#f1f5f9")
        r2.pack(fill="x", pady=2)
        tk.Label(r2, text="Tax (%):", font=Theme.FONT_BODY_BOLD, bg="#f1f5f9").pack(side="left")
        self.ent_tax = ttk.Entry(r2, width=4)
        self.ent_tax.insert(0, "5.0")
        self.ent_tax.pack(side="left", padx=(2, 15))
        self.ent_tax.bind("<KeyRelease>", lambda e: self.recalculate_totals())

        tk.Label(r2, text="Payment:", font=Theme.FONT_BODY_BOLD, bg="#f1f5f9").pack(side="left")
        self.combo_payment = ttk.Combobox(r2, values=["Cash", "UPI / QR", "Card"], state="readonly", width=10)
        self.combo_payment.current(0)
        self.combo_payment.pack(side="left", padx=(2, 0))

        r3 = tk.Frame(calc_card, bg="#f1f5f9")
        r3.pack(fill="x", pady=(4, 0))
        tk.Label(r3, text="TOTAL:", font=Theme.FONT_SUBTITLE, bg="#f1f5f9", fg="#0f172a").pack(side="left")
        self.lbl_grand_total = tk.Label(r3, text="₹ 0.00", font=Theme.FONT_LARGE_KPI, bg="#f1f5f9", fg=Theme.SUCCESS)
        self.lbl_grand_total.pack(side="right")

        # Checkout Button
        self.btn_checkout = ttk.Button(
            right_card,
            text="💳 Complete Sale & Generate Bill",
            style="Success.TButton",
            command=self.handle_checkout
        )
        self.btn_checkout.pack(fill="x", pady=(2, 0))

    def load_inventory_catalog(self):
        try:
            self.catalog_cache = InventoryService.get_all_products()
            self.filter_catalog()
        except Exception:
            pass

    def filter_catalog(self):
        query = self.ent_search.get().strip().lower()
        for row in self.tree_catalog.get_children():
            self.tree_catalog.delete(row)

        for p in self.catalog_cache:
            if not query or (query in p.name.lower() or (p.barcode and query in p.barcode.lower()) or query == str(p.product_id)):
                self.tree_catalog.insert(
                    "",
                    "end",
                    values=(p.product_id, p.name, f"₹{p.price:.2f}", p.quantity)
                )

    def add_selected_or_first(self):
        sel = self.tree_catalog.selection()
        if not sel:
            children = self.tree_catalog.get_children()
            if children:
                self.tree_catalog.selection_set(children[0])
        self.handle_add_to_cart()

    def handle_add_to_cart(self):
        selected = self.tree_catalog.selection()
        if not selected:
            messagebox.showwarning("Selection", "Please select a product from catalog.")
            return

        values = self.tree_catalog.item(selected[0], "values")
        prod_id = int(values[0])
        prod_name = values[1]
        prod_price = float(values[2].replace("₹", ""))
        stock_avail = int(values[3])

        try:
            qty = int(self.spin_qty.get().strip())
            if qty <= 0:
                return
        except ValueError:
            return

        if stock_avail < qty:
            messagebox.showwarning("Stock Alert", f"Only {stock_avail} units available.")
            return

        self.current_bill.add_item(
            product_id=prod_id,
            product_name=prod_name,
            unit_price=prod_price,
            quantity=qty
        )
        self.spin_qty.set(1)
        self.refresh_cart_view()

    def handle_remove_cart_item(self):
        selected = self.tree_cart.selection()
        if not selected:
            return
        values = self.tree_cart.item(selected[0], "values")
        prod_id = int(values[0])
        self.current_bill.remove_item(prod_id)
        self.refresh_cart_view()

    def handle_clear_cart(self):
        if not self.current_bill.items:
            return
        self.current_bill = Bill()
        self.lbl_inv_number.config(text=f"Bill No: {self.current_bill.invoice_no}")
        self.refresh_cart_view()

    def recalculate_totals(self):
        try:
            tax = float(self.ent_tax.get().strip() or "0")
            self.current_bill.tax_percent = max(0.0, tax)
        except ValueError:
            self.current_bill.tax_percent = 0.0

        try:
            disc = float(self.ent_discount.get().strip() or "0")
            self.current_bill.discount_percent = max(0.0, min(100.0, disc))
        except ValueError:
            self.current_bill.discount_percent = 0.0

        self.current_bill.recalculate()
        self.lbl_subtotal.config(text=f"{self.current_bill.subtotal:,.2f}")
        self.lbl_grand_total.config(text=f"₹ {self.current_bill.grand_total:,.2f}")

    def refresh_cart_view(self):
        for row in self.tree_cart.get_children():
            self.tree_cart.delete(row)

        for item in self.current_bill.items:
            self.tree_cart.insert(
                "",
                "end",
                values=(
                    item.product_id,
                    item.product_name,
                    f"₹{item.unit_price:.2f}",
                    item.quantity,
                    f"₹{item.line_total:.2f}"
                )
            )

        self.recalculate_totals()

    def handle_checkout(self):
        if not self.current_bill.items:
            messagebox.showwarning("Empty", "Cart is empty.")
            return

        phone = self.ent_phone.get().strip()
        name = self.ent_name.get().strip() or "Walk-in Customer"

        cust = BillingService.get_or_create_customer(phone=phone, name=name)
        self.current_bill.customer_id = cust.customer_id
        self.current_bill.customer_name = cust.name
        self.current_bill.customer_phone = cust.phone
        self.current_bill.payment_mode = self.combo_payment.get()

        self.recalculate_totals()

        success, msg = BillingService.process_sale_transaction(self.current_bill)
        if not success:
            messagebox.showerror("Error", msg)
            return

        bill_dict = {
            "invoice_no": self.current_bill.invoice_no,
            "customer_name": self.current_bill.customer_name,
            "customer_phone": self.current_bill.customer_phone,
            "subtotal": self.current_bill.subtotal,
            "tax_percent": self.current_bill.tax_percent,
            "tax_amount": self.current_bill.tax_amount,
            "discount_percent": self.current_bill.discount_percent,
            "discount_amount": self.current_bill.discount_amount,
            "grand_total": self.current_bill.grand_total,
            "payment_mode": self.current_bill.payment_mode,
            "invoice_date": self.current_bill.invoice_date
        }
        item_dicts = [
            {"product_name": it.product_name, "quantity": it.quantity, "unit_price": it.unit_price, "line_total": it.line_total}
            for it in self.current_bill.items
        ]

        saved_path = InvoiceGenerator.save_receipt_to_file(bill_dict, item_dicts)
        self.show_receipt_popup(bill_dict, item_dicts, saved_path)

        # Reset
        self.current_bill = Bill()
        self.lbl_inv_number.config(text=f"Bill No: {self.current_bill.invoice_no}")
        self.ent_phone.delete(0, tk.END)
        self.ent_name.delete(0, tk.END)
        self.ent_name.insert(0, "Walk-in Customer")
        self.refresh_cart_view()
        self.load_inventory_catalog()

    def show_receipt_popup(self, bill_dict, item_dicts, saved_path):
        popup = tk.Toplevel(self)
        popup.title(f"Receipt - {bill_dict['invoice_no']}")
        popup.geometry("480x560")
        popup.configure(bg=Theme.BACKGROUND)
        popup.transient(self)
        popup.grab_set()

        receipt_text = InvoiceGenerator.generate_receipt_text(bill_dict, item_dicts)

        txt_frame = tk.Frame(popup, bg=Theme.BACKGROUND, padx=12, pady=8)
        txt_frame.pack(fill="both", expand=True)

        txt = tk.Text(txt_frame, font=Theme.FONT_MONO, bg="#ffffff", fg="#0f172a", wrap="none")
        txt.insert("1.0", receipt_text)
        txt.config(state="disabled")

        scroll = ttk.Scrollbar(txt_frame, orient="vertical", command=txt.yview)
        txt.configure(yscrollcommand=scroll.set)

        txt.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        lbl_info = tk.Label(popup, text=f"Saved to: {saved_path}", font=Theme.FONT_BODY, bg=Theme.BACKGROUND, fg=Theme.TEXT_MUTED)
        lbl_info.pack(pady=3)

        btn_close = ttk.Button(popup, text="Close Receipt", style="Primary.TButton", command=popup.destroy)
        btn_close.pack(pady=(0, 10))
