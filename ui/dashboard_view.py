"""
Dashboard View displaying key performance indicators, stock alerts, and quick actions.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ui.theme import Theme
from services.inventory_service import InventoryService
from services.billing_service import BillingService
from seed_data import seed_database


class DashboardView(tk.Frame):
    def __init__(self, parent, nav_callback=None):
        super().__init__(parent, bg=Theme.BACKGROUND)
        self.nav_callback = nav_callback
        self.card_widgets = {}
        self.create_widgets()
        self.refresh_data()

    def create_widgets(self):
        # Header title
        header_frame = tk.Frame(self, bg=Theme.BACKGROUND)
        header_frame.pack(fill="x", padx=25, pady=(20, 10))

        title_lbl = tk.Label(
            header_frame,
            text="Executive Dashboard & Overview",
            font=Theme.FONT_HEADER,
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT_MAIN
        )
        title_lbl.pack(side="left")

        refresh_btn = ttk.Button(
            header_frame,
            text="🔄 Refresh Data",
            style="Secondary.TButton",
            command=self.refresh_data
        )
        refresh_btn.pack(side="right")

        # KPI Metrics Grid (Cards)
        kpi_container = tk.Frame(self, bg=Theme.BACKGROUND)
        kpi_container.pack(fill="x", padx=25, pady=10)

        # Card configs: (Key, Title, BgColor, FgColor)
        cards = [
            ("total_products", "Total Products (SKUs)", "#3b82f6", "#ffffff"),
            ("total_units", "Total Units in Stock", "#0ea5e9", "#ffffff"),
            ("low_stock_count", "Low Stock Alerts", "#f59e0b", "#ffffff"),
            ("out_of_stock_count", "Out of Stock Items", "#ef4444", "#ffffff"),
            ("today_revenue", "Today's Revenue (₹)", "#10b981", "#ffffff"),
            ("today_invoices", "Today's Invoices", "#8b5cf6", "#ffffff"),
        ]

        for i, (key, title, bg_col, fg_col) in enumerate(cards):
            card = tk.Frame(kpi_container, bg=bg_col, bd=0, relief="flat", padx=15, pady=12)
            card.grid(row=i // 3, column=i % 3, padx=8, pady=8, sticky="nsew")
            kpi_container.columnconfigure(i % 3, weight=1)

            t_lbl = tk.Label(card, text=title, font=Theme.FONT_SUBTITLE, bg=bg_col, fg=fg_col)
            t_lbl.pack(anchor="w")

            val_lbl = tk.Label(card, text="--", font=Theme.FONT_LARGE_KPI, bg=bg_col, fg=fg_col)
            val_lbl.pack(anchor="w", pady=(5, 0))

            self.card_widgets[key] = val_lbl

        # Quick Actions & Recent Low Stock Frame
        content_frame = tk.Frame(self, bg=Theme.BACKGROUND)
        content_frame.pack(fill="both", expand=True, padx=25, pady=10)

        # Left Column: Quick Action Center
        actions_card = tk.Frame(content_frame, bg=Theme.SURFACE, bd=1, relief="solid", padx=20, pady=15)
        actions_card.pack(side="left", fill="both", expand=False, padx=(0, 10))

        tk.Label(actions_card, text="Quick Management Actions", font=Theme.FONT_TITLE, bg=Theme.SURFACE, fg=Theme.TEXT_MAIN).pack(anchor="w", pady=(0, 15))

        btn_pos = ttk.Button(
            actions_card,
            text="⚡ Start New Billing (POS)",
            style="Success.TButton",
            command=lambda: self.nav_callback("billing") if self.nav_callback else None
        )
        btn_pos.pack(fill="x", pady=6)

        btn_inv = ttk.Button(
            actions_card,
            text="📦 Manage Inventory (CRUD)",
            style="Primary.TButton",
            command=lambda: self.nav_callback("inventory") if self.nav_callback else None
        )
        btn_inv.pack(fill="x", pady=6)

        btn_seed = ttk.Button(
            actions_card,
            text="🌱 Seed 200+ Demo Products",
            style="Secondary.TButton",
            command=self.handle_seed_database
        )
        btn_seed.pack(fill="x", pady=6)

        # Right Column: Low Stock Alert Table
        low_stock_card = tk.Frame(content_frame, bg=Theme.SURFACE, bd=1, relief="solid", padx=15, pady=12)
        low_stock_card.pack(side="right", fill="both", expand=True)

        tk.Label(
            low_stock_card,
            text="⚠️ Low Stock & Out of Stock Warnings",
            font=Theme.FONT_TITLE,
            bg=Theme.SURFACE,
            fg=Theme.DANGER
        ).pack(anchor="w", pady=(0, 8))

        columns = ("id", "name", "category", "price", "qty", "status")
        self.tree = ttk.Treeview(low_stock_card, columns=columns, show="headings", height=8)
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Product Name")
        self.tree.heading("category", text="Category")
        self.tree.heading("price", text="Price (₹)")
        self.tree.heading("qty", text="Stock Qty")
        self.tree.heading("status", text="Status")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("name", width=180, anchor="w")
        self.tree.column("category", width=120, anchor="w")
        self.tree.column("price", width=70, anchor="e")
        self.tree.column("qty", width=70, anchor="center")
        self.tree.column("status", width=90, anchor="center")

        tree_scroll = ttk.Scrollbar(low_stock_card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")

        # Color tags
        self.tree.tag_configure("out_of_stock", foreground=Theme.DANGER, font=Theme.FONT_BODY_BOLD)
        self.tree.tag_configure("low_stock", foreground=Theme.WARNING, font=Theme.FONT_BODY_BOLD)

    def refresh_data(self):
        try:
            inv_summary = InventoryService.get_inventory_summary()
            sales_summary = BillingService.get_sales_summary()

            self.card_widgets["total_products"].config(text=f"{inv_summary.get('total_products', 0)}")
            self.card_widgets["total_units"].config(text=f"{inv_summary.get('total_units', 0):,}")
            self.card_widgets["low_stock_count"].config(text=f"{inv_summary.get('low_stock_count', 0)}")
            self.card_widgets["out_of_stock_count"].config(text=f"{inv_summary.get('out_of_stock_count', 0)}")
            
            today_rev = sales_summary.get("today_revenue", 0.0)
            self.card_widgets["today_revenue"].config(text=f"₹{today_rev:,.2f}")
            self.card_widgets["today_invoices"].config(text=f"{sales_summary.get('today_invoices', 0)}")

            # Load low stock table
            for row in self.tree.get_children():
                self.tree.delete(row)

            products = InventoryService.get_all_products()
            low_stock_items = [p for p in products if p.status in ("Low Stock", "Out of Stock")]

            for p in low_stock_items[:50]:
                tag = "out_of_stock" if p.status == "Out of Stock" else "low_stock"
                self.tree.insert(
                    "",
                    "end",
                    values=(p.product_id, p.name, p.category_name, f"₹{p.price:.2f}", p.quantity, p.status),
                    tags=(tag,)
                )

        except Exception as e:
            # If database not configured or connected yet, show placeholder
            for key in self.card_widgets:
                self.card_widgets[key].config(text="--")

    def handle_seed_database(self):
        answer = messagebox.askyesno(
            "Seed Database",
            "This will create categories and insert 200+ realistic products into MySQL.\nDo you wish to proceed?"
        )
        if answer:
            try:
                success = seed_database(verbose=False)
                if success:
                    messagebox.showinfo("Success", "Successfully initialized database and seeded 200+ products!")
                    self.refresh_data()
                else:
                    messagebox.showerror("Error", "Could not seed database. Please check MySQL Settings.")
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to seed: {str(e)}")
