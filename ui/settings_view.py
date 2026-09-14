"""
Settings View for MySQL connection configuration, schema initialization, and database diagnostics.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ui.theme import Theme
from database.db_config import DatabaseConfig
from database.db_helper import DBHelper
from seed_data import seed_database


class SettingsView(tk.Frame):
    def __init__(self, parent, on_config_saved=None):
        super().__init__(parent, bg=Theme.BACKGROUND)
        self.on_config_saved = on_config_saved
        self.create_widgets()
        self.load_current_config()

    def create_widgets(self):
        header_frame = tk.Frame(self, bg=Theme.BACKGROUND)
        header_frame.pack(fill="x", padx=25, pady=(20, 10))

        title_lbl = tk.Label(
            header_frame,
            text="⚙️ Database Settings & Configuration",
            font=Theme.FONT_HEADER,
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT_MAIN
        )
        title_lbl.pack(side="left")

        # Main Layout Frame
        container = tk.Frame(self, bg=Theme.BACKGROUND)
        container.pack(fill="both", expand=True, padx=25, pady=10)

        # Config Card
        card = tk.Frame(container, bg=Theme.SURFACE, bd=1, relief="solid", padx=25, pady=20)
        card.pack(side="left", fill="both", expand=True, padx=(0, 15))

        tk.Label(card, text="MySQL Connection Parameters", font=Theme.FONT_TITLE, bg=Theme.SURFACE, fg=Theme.TEXT_MAIN).pack(anchor="w", pady=(0, 15))

        form_grid = tk.Frame(card, bg=Theme.SURFACE)
        form_grid.pack(fill="x")

        # 1. Host
        tk.Label(form_grid, text="Host / Server:", font=Theme.FONT_BODY_BOLD, bg=Theme.SURFACE).grid(row=0, column=0, sticky="w", pady=6)
        self.ent_host = ttk.Entry(form_grid, width=28)
        self.ent_host.grid(row=0, column=1, sticky="w", pady=6, padx=(10, 0))

        # 2. Port
        tk.Label(form_grid, text="Port:", font=Theme.FONT_BODY_BOLD, bg=Theme.SURFACE).grid(row=1, column=0, sticky="w", pady=6)
        self.ent_port = ttk.Entry(form_grid, width=28)
        self.ent_port.grid(row=1, column=1, sticky="w", pady=6, padx=(10, 0))

        # 3. User
        tk.Label(form_grid, text="Username:", font=Theme.FONT_BODY_BOLD, bg=Theme.SURFACE).grid(row=2, column=0, sticky="w", pady=6)
        self.ent_user = ttk.Entry(form_grid, width=28)
        self.ent_user.grid(row=2, column=1, sticky="w", pady=6, padx=(10, 0))

        # 4. Password
        tk.Label(form_grid, text="Password:", font=Theme.FONT_BODY_BOLD, bg=Theme.SURFACE).grid(row=3, column=0, sticky="w", pady=6)
        self.ent_password = ttk.Entry(form_grid, width=28, show="*")
        self.ent_password.grid(row=3, column=1, sticky="w", pady=6, padx=(10, 0))

        # 5. Database Name
        tk.Label(form_grid, text="Database Name:", font=Theme.FONT_BODY_BOLD, bg=Theme.SURFACE).grid(row=4, column=0, sticky="w", pady=6)
        self.ent_database = ttk.Entry(form_grid, width=28)
        self.ent_database.grid(row=4, column=1, sticky="w", pady=6, padx=(10, 0))

        # Buttons
        btn_box = tk.Frame(card, bg=Theme.SURFACE)
        btn_box.pack(fill="x", pady=(20, 10))

        btn_test = ttk.Button(btn_box, text="🔌 Test Connection", style="Secondary.TButton", command=self.handle_test_connection)
        btn_test.pack(side="left", padx=(0, 10))

        btn_save = ttk.Button(btn_box, text="💾 Save Configuration", style="Primary.TButton", command=self.handle_save_config)
        btn_save.pack(side="left")

        self.lbl_status = tk.Label(card, text="Status: Ready", font=Theme.FONT_BODY_BOLD, bg=Theme.SURFACE, fg=Theme.TEXT_MUTED)
        self.lbl_status.pack(anchor="w", pady=(10, 0))

        # Right Card: Database Management & Seeding
        db_card = tk.Frame(container, bg=Theme.SURFACE, bd=1, relief="solid", padx=20, pady=20)
        db_card.pack(side="right", fill="both", expand=True)

        tk.Label(db_card, text="Database Initialization & Seed", font=Theme.FONT_TITLE, bg=Theme.SURFACE, fg=Theme.TEXT_MAIN).pack(anchor="w", pady=(0, 10))

        desc_text = (
            "Click below to set up tables in MySQL and automatically populate "
            "over 200 realistic inventory products across 8 retail categories."
        )
        tk.Label(db_card, text=desc_text, font=Theme.FONT_BODY, bg=Theme.SURFACE, fg=Theme.TEXT_MUTED, wraplength=280, justify="left").pack(anchor="w", pady=(0, 15))

        btn_init = ttk.Button(db_card, text="🛠️ Initialize Schema & Tables", style="Secondary.TButton", command=self.handle_init_database)
        btn_init.pack(fill="x", pady=6)

        btn_seed = ttk.Button(db_card, text="🌱 Populate 200+ Products", style="Success.TButton", command=self.handle_seed)
        btn_seed.pack(fill="x", pady=6)

    def load_current_config(self):
        cfg = DatabaseConfig.load_config()
        self.ent_host.delete(0, tk.END)
        self.ent_host.insert(0, cfg.get("host", "localhost"))

        self.ent_port.delete(0, tk.END)
        self.ent_port.insert(0, str(cfg.get("port", 3306)))

        self.ent_user.delete(0, tk.END)
        self.ent_user.insert(0, cfg.get("user", "root"))

        self.ent_password.delete(0, tk.END)
        self.ent_password.insert(0, cfg.get("password", ""))

        self.ent_database.delete(0, tk.END)
        self.ent_database.insert(0, cfg.get("database", "shop_management_db"))

    def get_form_config(self):
        return {
            "host": self.ent_host.get().strip(),
            "port": int(self.ent_port.get().strip() or 3306),
            "user": self.ent_user.get().strip(),
            "password": self.ent_password.get(),
            "database": self.ent_database.get().strip()
        }

    def handle_test_connection(self):
        try:
            cfg = self.get_form_config()
            success, msg = DatabaseConfig.test_connection(cfg)
            if success:
                self.lbl_status.config(text="Status: Connected Successfully! ✅", fg=Theme.SUCCESS)
                messagebox.showinfo("Connection Test", "Successfully connected to MySQL server!")
            else:
                self.lbl_status.config(text=f"Status: Failed ❌", fg=Theme.DANGER)
                messagebox.showerror("Connection Failed", msg)
        except Exception as e:
            self.lbl_status.config(text=f"Status: Error ❌", fg=Theme.DANGER)
            messagebox.showerror("Error", str(e))

    def handle_save_config(self):
        try:
            cfg = self.get_form_config()
            DatabaseConfig.save_config(cfg)
            self.lbl_status.config(text="Configuration Saved! ✅", fg=Theme.SUCCESS)
            messagebox.showinfo("Saved", "Database configuration saved successfully!")
            if self.on_config_saved:
                self.on_config_saved()
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    def handle_init_database(self):
        try:
            self.handle_save_config()
            success, msg = DBHelper.initialize_database()
            if success:
                messagebox.showinfo("Database Initialized", msg)
            else:
                messagebox.showerror("Initialization Failed", msg)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def handle_seed(self):
        try:
            self.handle_save_config()
            success = seed_database(verbose=False)
            if success:
                messagebox.showinfo("Seeding Complete", "Successfully loaded 200+ demo products into MySQL!")
                if self.on_config_saved:
                    self.on_config_saved()
            else:
                messagebox.showerror("Seeding Failed", "Could not seed data into MySQL.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
