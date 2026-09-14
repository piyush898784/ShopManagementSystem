"""
Fast & Smooth Shop Management System Main Window.
Streamlined to core essentials: 📦 Inventory Management (CRUD) and ⚡ Billing & POS.
"""

import tkinter as tk
from tkinter import ttk
from ui.theme import Theme
from ui.inventory_view import InventoryView
from ui.billing_view import BillingView


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Shop Management System - Inventory & POS Billing")
        self.geometry("1100x680")
        self.minsize(980, 580)
        self.configure(bg=Theme.BACKGROUND)

        # Apply global TTK styles
        Theme.apply_ttk_theme(self)

        self.create_layout()

    def create_layout(self):
        # 1. Clean Top Header
        top_bar = tk.Frame(self, bg=Theme.PRIMARY_DARK, height=48)
        top_bar.pack(side="top", fill="x")

        tk.Label(
            top_bar,
            text="🛒 SMART SHOP MANAGEMENT SYSTEM",
            font=Theme.FONT_TITLE,
            bg=Theme.PRIMARY_DARK,
            fg="#ffffff",
            padx=16,
            pady=10
        ).pack(side="left")

        # 2. Smooth Tab Navigation (Notebook)
        style = ttk.Style()
        style.configure("TNotebook", background=Theme.BACKGROUND, borderwidth=0)
        style.configure("TNotebook.Tab", font=Theme.FONT_SUBTITLE, padding=(18, 8))
        style.map("TNotebook.Tab", background=[("selected", Theme.SECONDARY)], foreground=[("selected", "#ffffff")])

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=10)

        # Tab 1: Billing & POS
        self.tab_billing = BillingView(self.notebook)
        self.notebook.add(self.tab_billing, text="  ⚡ Billing & POS Checkout  ")

        # Tab 2: Inventory Management (CRUD)
        self.tab_inventory = InventoryView(self.notebook)
        self.notebook.add(self.tab_inventory, text="  📦 Inventory Management (CRUD)  ")

        # Tab change event to sync data instantly
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def on_tab_changed(self, event):
        selected_index = self.notebook.index("current")
        if selected_index == 0:
            # Switched to Billing -> refresh catalog
            if hasattr(self.tab_billing, "load_inventory_catalog"):
                self.tab_billing.load_inventory_catalog()
        elif selected_index == 1:
            # Switched to Inventory -> refresh table
            if hasattr(self.tab_inventory, "load_products"):
                self.tab_inventory.load_products()
