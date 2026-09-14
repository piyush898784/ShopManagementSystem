"""
UI Styling and Theme configuration for Tkinter / ttk widgets.
Provides modern, flat, high-contrast theme definitions.
"""

import tkinter as tk
from tkinter import ttk

class Theme:
    # Color Palette
    PRIMARY = "#1e293b"       # Deep slate navy (Header & Sidebar)
    PRIMARY_DARK = "#0f172a"  # Dark navy background
    SECONDARY = "#3b82f6"     # Accent blue
    SECONDARY_HOVER = "#2563eb"
    SUCCESS = "#10b981"       # Emerald green (Positive / In Stock)
    WARNING = "#f59e0b"       # Amber / Low stock
    DANGER = "#ef4444"        # Red / Out of stock / Delete
    BACKGROUND = "#f8fafc"    # Light grayish white background
    SURFACE = "#ffffff"       # Card / Form white
    TEXT_MAIN = "#1e293b"     # Main dark text
    TEXT_MUTED = "#64748b"    # Secondary text
    BORDER = "#e2e8f0"        # Border line color
    SIDEBAR_BG = "#1e293b"
    SIDEBAR_TEXT = "#f8fafc"
    SIDEBAR_ACTIVE = "#3b82f6"

    # Font definitions
    FONT_HEADER = ("Segoe UI", 16, "bold")
    FONT_TITLE = ("Segoe UI", 12, "bold")
    FONT_SUBTITLE = ("Segoe UI", 10, "bold")
    FONT_BODY = ("Segoe UI", 9)
    FONT_BODY_BOLD = ("Segoe UI", 9, "bold")
    FONT_LARGE_KPI = ("Segoe UI", 20, "bold")
    FONT_MONO = ("Consolas", 9)

    @classmethod
    def apply_ttk_theme(cls, root: tk.Tk):
        """Applies custom modern styling to ttk widgets."""
        style = ttk.Style(root)
        style.theme_use("clam")

        # Global Treeview Style
        style.configure(
            "Treeview",
            background="#ffffff",
            foreground="#1e293b",
            rowheight=28,
            fieldbackground="#ffffff",
            font=cls.FONT_BODY,
            borderwidth=0
        )
        style.configure(
            "Treeview.Heading",
            background="#f1f5f9",
            foreground="#0f172a",
            font=cls.FONT_SUBTITLE,
            padding=(6, 6)
        )
        style.map(
            "Treeview.Heading",
            background=[("active", "#e2e8f0")]
        )
        style.map(
            "Treeview",
            background=[("selected", "#3b82f6")],
            foreground=[("selected", "#ffffff")]
        )

        # Primary Action Button
        style.configure(
            "Primary.TButton",
            background=cls.SECONDARY,
            foreground="#ffffff",
            font=cls.FONT_BODY_BOLD,
            padding=(12, 6),
            borderwidth=0
        )
        style.map(
            "Primary.TButton",
            background=[("active", cls.SECONDARY_HOVER)]
        )

        # Success Action Button
        style.configure(
            "Success.TButton",
            background=cls.SUCCESS,
            foreground="#ffffff",
            font=cls.FONT_BODY_BOLD,
            padding=(12, 6),
            borderwidth=0
        )
        style.map(
            "Success.TButton",
            background=[("active", "#059669")]
        )

        # Danger Action Button
        style.configure(
            "Danger.TButton",
            background=cls.DANGER,
            foreground="#ffffff",
            font=cls.FONT_BODY_BOLD,
            padding=(12, 6),
            borderwidth=0
        )
        style.map(
            "Danger.TButton",
            background=[("active", "#dc2626")]
        )

        # Secondary Button
        style.configure(
            "Secondary.TButton",
            background="#e2e8f0",
            foreground="#334155",
            font=cls.FONT_BODY_BOLD,
            padding=(10, 6),
            borderwidth=0
        )
        style.map(
            "Secondary.TButton",
            background=[("active", "#cbd5e1")]
        )

        # Combobox
        style.configure(
            "TCombobox",
            padding=4,
            font=cls.FONT_BODY
        )
