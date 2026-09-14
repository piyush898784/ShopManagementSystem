"""
Ultra-fast, smooth Inventory Management View (CRUD).
Features instant in-memory search (zero keystroke latency) and direct database sync.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ui.theme import Theme
from services.inventory_service import InventoryService
from models.product import Product


class InventoryView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=Theme.BACKGROUND)
        self.category_map = {}
        self.products_cache = []
        self.create_widgets()
        self.load_categories()
        self.load_products()

    def create_widgets(self):
        # Header Bar
        header_frame = tk.Frame(self, bg=Theme.BACKGROUND)
        header_frame.pack(fill="x", padx=16, pady=(10, 8))

        tk.Label(
            header_frame,
            text="📦 Inventory & Product Stock Manager",
            font=Theme.FONT_TITLE,
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT_MAIN
        ).pack(side="left")

        self.lbl_product_count = tk.Label(
            header_frame,
            text="0 products",
            font=Theme.FONT_BODY_BOLD,
            bg="#e2e8f0",
            fg=Theme.TEXT_MAIN,
            padx=10,
            pady=3
        )
        self.lbl_product_count.pack(side="right")

        # Main Workspace
        main_pane = tk.Frame(self, bg=Theme.BACKGROUND)
        main_pane.pack(fill="both", expand=True, padx=16, pady=(0, 10))

        # --- LEFT PANEL: Product Entry Form ---
        form_card = tk.Frame(main_pane, bg=Theme.SURFACE, bd=1, relief="solid", padx=14, pady=14)
        form_card.pack(side="left", fill="y", padx=(0, 10))

        tk.Label(form_card, text="Product Information", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE, fg=Theme.TEXT_MAIN).pack(anchor="w", pady=(0, 10))

        fields_frame = tk.Frame(form_card, bg=Theme.SURFACE)
        fields_frame.pack(fill="x")

        # 1. Product ID
        tk.Label(fields_frame, text="ID:", font=Theme.FONT_BODY_BOLD, bg=Theme.SURFACE, fg=Theme.TEXT_MUTED).grid(row=0, column=0, sticky="w", pady=3)
        self.ent_id = ttk.Entry(fields_frame, width=22, state="readonly")
        self.ent_id.grid(row=0, column=1, sticky="w", pady=3)

        # 2. Category
        tk.Label(fields_frame, text="Category *:", font=Theme.FONT_BODY_BOLD, bg=Theme.SURFACE).grid(row=1, column=0, sticky="w", pady=3)
        self.combo_category = ttk.Combobox(fields_frame, width=20, state="readonly")
        self.combo_category.grid(row=1, column=1, sticky="w", pady=3)

        # 3. Product Name
        tk.Label(fields_frame, text="Name *:", font=Theme.FONT_BODY_BOLD, bg=Theme.SURFACE).grid(row=2, column=0, sticky="w", pady=3)
        self.ent_name = ttk.Entry(fields_frame, width=22)
        self.ent_name.grid(row=2, column=1, sticky="w", pady=3)

        # 4. Barcode
        tk.Label(fields_frame, text="Barcode:", font=Theme.FONT_BODY_BOLD, bg=Theme.SURFACE).grid(row=3, column=0, sticky="w", pady=3)
        self.ent_barcode = ttk.Entry(fields_frame, width=22)
        self.ent_barcode.grid(row=3, column=1, sticky="w", pady=3)

        # 5. Price
        tk.Label(fields_frame, text="Price (₹) *:", font=Theme.FONT_BODY_BOLD, bg=Theme.SURFACE).grid(row=4, column=0, sticky="w", pady=3)
        self.ent_price = ttk.Entry(fields_frame, width=22)
        self.ent_price.grid(row=4, column=1, sticky="w", pady=3)

        # 6. Cost Price
        tk.Label(fields_frame, text="Cost (₹):", font=Theme.FONT_BODY_BOLD, bg=Theme.SURFACE).grid(row=5, column=0, sticky="w", pady=3)
        self.ent_cost = ttk.Entry(fields_frame, width=22)
        self.ent_cost.grid(row=5, column=1, sticky="w", pady=3)

        # 7. Quantity
        tk.Label(fields_frame, text="Stock Qty *:", font=Theme.FONT_BODY_BOLD, bg=Theme.SURFACE).grid(row=6, column=0, sticky="w", pady=3)
        self.ent_qty = ttk.Entry(fields_frame, width=22)
        self.ent_qty.grid(row=6, column=1, sticky="w", pady=3)

        # 8. Min Stock Alert
        tk.Label(fields_frame, text="Min Alert:", font=Theme.FONT_BODY_BOLD, bg=Theme.SURFACE).grid(row=7, column=0, sticky="w", pady=3)
        self.ent_min_alert = ttk.Entry(fields_frame, width=22)
        self.ent_min_alert.grid(row=7, column=1, sticky="w", pady=3)
        self.ent_min_alert.insert(0, "10")

        # Action Buttons
        btn_grid = tk.Frame(form_card, bg=Theme.SURFACE)
        btn_grid.pack(fill="x", pady=(14, 0))

        self.btn_add = ttk.Button(btn_grid, text="➕ Add", style="Success.TButton", command=self.handle_add_product)
        self.btn_add.grid(row=0, column=0, padx=2, pady=3, sticky="ew")

        self.btn_update = ttk.Button(btn_grid, text="✏️ Update", style="Primary.TButton", command=self.handle_update_product)
        self.btn_update.grid(row=0, column=1, padx=2, pady=3, sticky="ew")

        self.btn_delete = ttk.Button(btn_grid, text="🗑️ Delete", style="Danger.TButton", command=self.handle_delete_product)
        self.btn_delete.grid(row=1, column=0, padx=2, pady=3, sticky="ew")

        self.btn_clear = ttk.Button(btn_grid, text="🧹 Clear", style="Secondary.TButton", command=self.clear_form)
        self.btn_clear.grid(row=1, column=1, padx=2, pady=3, sticky="ew")

        btn_grid.columnconfigure(0, weight=1)
        btn_grid.columnconfigure(1, weight=1)

        # --- RIGHT PANEL: Search & Table ---
        table_card = tk.Frame(main_pane, bg=Theme.SURFACE, bd=1, relief="solid", padx=12, pady=12)
        table_card.pack(side="right", fill="both", expand=True)

        filter_bar = tk.Frame(table_card, bg=Theme.SURFACE)
        filter_bar.pack(fill="x", pady=(0, 8))

        tk.Label(filter_bar, text="🔍 Search:", font=Theme.FONT_BODY_BOLD, bg=Theme.SURFACE).pack(side="left", padx=(0, 4))
        self.ent_search = ttk.Entry(filter_bar, width=20)
        self.ent_search.pack(side="left", padx=(0, 8))
        self.ent_search.bind("<KeyRelease>", lambda e: self.render_filtered_table())

        tk.Label(filter_bar, text="Category:", font=Theme.FONT_BODY_BOLD, bg=Theme.SURFACE).pack(side="left", padx=(4, 4))
        self.combo_filter_category = ttk.Combobox(filter_bar, width=18, state="readonly")
        self.combo_filter_category.pack(side="left", padx=(0, 8))
        self.combo_filter_category.bind("<<ComboboxSelected>>", lambda e: self.render_filtered_table())

        ttk.Button(filter_bar, text="Reset", style="Secondary.TButton", command=self.reset_filters).pack(side="left")

        # Treeview Table
        table_container = tk.Frame(table_card, bg=Theme.SURFACE)
        table_container.pack(fill="both", expand=True)

        columns = ("id", "name", "category", "barcode", "price", "quantity", "status")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Product Name")
        self.tree.heading("category", text="Category")
        self.tree.heading("barcode", text="Barcode")
        self.tree.heading("price", text="Price (₹)")
        self.tree.heading("quantity", text="Stock")
        self.tree.heading("status", text="Status")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("name", width=220, anchor="w")
        self.tree.column("category", width=130, anchor="w")
        self.tree.column("barcode", width=110, anchor="center")
        self.tree.column("price", width=75, anchor="e")
        self.tree.column("quantity", width=60, anchor="center")
        self.tree.column("status", width=95, anchor="center")

        v_scroll = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=v_scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        v_scroll.pack(side="right", fill="y")

        self.tree.tag_configure("in_stock", foreground="#0f172a")
        self.tree.tag_configure("low_stock", foreground="#d97706", font=Theme.FONT_BODY_BOLD)
        self.tree.tag_configure("out_of_stock", foreground="#dc2626", font=Theme.FONT_BODY_BOLD)

        self.tree.bind("<<TreeviewSelect>>", self.on_product_select)

    def load_categories(self):
        try:
            categories = InventoryService.get_all_categories()
            self.category_map = {c.name: c.category_id for c in categories}
            cat_names = [c.name for c in categories]

            self.combo_category["values"] = cat_names
            if cat_names:
                self.combo_category.current(0)

            self.combo_filter_category["values"] = ["All Categories"] + cat_names
            self.combo_filter_category.current(0)
        except Exception:
            pass

    def load_products(self):
        """Fetches all products once into memory."""
        try:
            self.products_cache = InventoryService.get_all_products()
            self.render_filtered_table()
        except Exception as e:
            self.lbl_product_count.config(text="Disconnected")

    def render_filtered_table(self):
        """Ultra-fast instant filtering from in-memory cache."""
        query = self.ent_search.get().strip().lower()
        selected_cat = self.combo_filter_category.get()
        cat_id = self.category_map.get(selected_cat) if (selected_cat and selected_cat != "All Categories") else None

        for row in self.tree.get_children():
            self.tree.delete(row)

        filtered_count = 0
        for p in self.products_cache:
            if cat_id and p.category_id != cat_id:
                continue
            if query:
                match_name = query in p.name.lower()
                match_barcode = p.barcode and query in p.barcode.lower()
                match_id = query == str(p.product_id)
                if not (match_name or match_barcode or match_id):
                    continue

            tag = "in_stock"
            if p.status == "Out of Stock":
                tag = "out_of_stock"
            elif p.status == "Low Stock":
                tag = "low_stock"

            self.tree.insert(
                "",
                "end",
                values=(
                    p.product_id,
                    p.name,
                    p.category_name,
                    p.barcode or "N/A",
                    f"{p.price:.2f}",
                    p.quantity,
                    p.status
                ),
                tags=(tag,)
            )
            filtered_count += 1

        self.lbl_product_count.config(text=f"{filtered_count} / {len(self.products_cache)} items")

    def on_product_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        if not values:
            return

        prod_id = int(values[0])
        # Find product in cache
        p = next((x for x in self.products_cache if x.product_id == prod_id), None)
        if not p:
            return

        self.clear_form()
        self.ent_id.config(state="normal")
        self.ent_id.delete(0, tk.END)
        self.ent_id.insert(0, str(p.product_id))
        self.ent_id.config(state="readonly")

        self.ent_name.insert(0, p.name)
        if p.category_name in self.combo_category["values"]:
            self.combo_category.set(p.category_name)

        if p.barcode:
            self.ent_barcode.insert(0, p.barcode)

        self.ent_price.insert(0, f"{p.price:.2f}")
        self.ent_cost.insert(0, f"{p.cost_price:.2f}")
        self.ent_qty.insert(0, str(p.quantity))
        self.ent_min_alert.delete(0, tk.END)
        self.ent_min_alert.insert(0, str(p.min_stock_alert))

    def clear_form(self):
        self.ent_id.config(state="normal")
        self.ent_id.delete(0, tk.END)
        self.ent_id.config(state="readonly")

        self.ent_name.delete(0, tk.END)
        self.ent_barcode.delete(0, tk.END)
        self.ent_price.delete(0, tk.END)
        self.ent_cost.delete(0, tk.END)
        self.ent_qty.delete(0, tk.END)
        self.ent_min_alert.delete(0, tk.END)
        self.ent_min_alert.insert(0, "10")

        if self.combo_category["values"]:
            self.combo_category.current(0)
        self.tree.selection_remove(self.tree.selection())

    def reset_filters(self):
        self.ent_search.delete(0, tk.END)
        self.combo_filter_category.current(0)
        self.render_filtered_table()

    def validate_inputs(self):
        name = self.ent_name.get().strip()
        if not name:
            return False, "Product Name is required.", {}

        cat_name = self.combo_category.get()
        cat_id = self.category_map.get(cat_name)
        if not cat_id:
            return False, "Please select a Category.", {}

        try:
            price = float(self.ent_price.get().strip())
            if price < 0:
                return False, "Price cannot be negative.", {}
        except ValueError:
            return False, "Please enter a valid numeric Price.", {}

        cost = 0.0
        if self.ent_cost.get().strip():
            try:
                cost = float(self.ent_cost.get().strip())
            except ValueError:
                pass

        try:
            qty = int(self.ent_qty.get().strip())
            if qty < 0:
                return False, "Stock Quantity cannot be negative.", {}
        except ValueError:
            return False, "Please enter a valid whole number for Stock Quantity.", {}

        min_alert = 10
        if self.ent_min_alert.get().strip():
            try:
                min_alert = int(self.ent_min_alert.get().strip())
            except ValueError:
                pass

        barcode = self.ent_barcode.get().strip() or None

        return True, "", {
            "name": name,
            "category_id": cat_id,
            "barcode": barcode,
            "price": price,
            "cost_price": cost,
            "quantity": qty,
            "min_stock_alert": min_alert
        }

    def handle_add_product(self):
        valid, msg, data = self.validate_inputs()
        if not valid:
            messagebox.showwarning("Validation", msg)
            return

        try:
            prod = Product(
                category_id=data["category_id"],
                name=data["name"],
                barcode=data["barcode"],
                price=data["price"],
                cost_price=data["cost_price"],
                quantity=data["quantity"],
                min_stock_alert=data["min_stock_alert"]
            )
            prod_id = InventoryService.add_product(prod)
            messagebox.showinfo("Success", f"Product '{prod.name}' added successfully!")
            self.clear_form()
            self.load_products()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def handle_update_product(self):
        prod_id_str = self.ent_id.get().strip()
        if not prod_id_str:
            messagebox.showwarning("Selection", "Please select a product from the table first.")
            return

        valid, msg, data = self.validate_inputs()
        if not valid:
            messagebox.showwarning("Validation", msg)
            return

        try:
            prod = Product(
                product_id=int(prod_id_str),
                category_id=data["category_id"],
                name=data["name"],
                barcode=data["barcode"],
                price=data["price"],
                cost_price=data["cost_price"],
                quantity=data["quantity"],
                min_stock_alert=data["min_stock_alert"]
            )
            InventoryService.update_product(prod)
            messagebox.showinfo("Success", f"Product ID {prod.product_id} updated!")
            self.clear_form()
            self.load_products()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def handle_delete_product(self):
        prod_id_str = self.ent_id.get().strip()
        if not prod_id_str:
            messagebox.showwarning("Selection", "Please select a product to delete.")
            return

        prod_id = int(prod_id_str)
        if messagebox.askyesno("Delete", f"Delete Product ID {prod_id}?"):
            try:
                InventoryService.delete_product(prod_id)
                self.clear_form()
                self.load_products()
            except Exception as e:
                messagebox.showerror("Error", str(e))
