# Smart Shop Management System 🛒

A desktop-based retail inventory and Point of Sale (POS) billing system built with **Python**, **Tkinter**, and **MySQL**.

---

## 📌 Project Highlights & Resume Alignment

- **200+ Products Managed**: Pre-seeded with over 200 distinct retail items across 8 categories (Groceries, Dairy & Bakery, Beverages, Snacks, Personal Care, Household Cleaning, Electronics, and Stationery).
- **Complete CRUD Functionality**: Built using strict Object-Oriented Programming (OOP) principles with separate Model, Service, and UI layers.
- **MySQL Integration & Data Integrity**: Leverages relational schemas with foreign key constraints, indexing, and ACID transactions for bill generation to prevent stock overselling and eliminate data redundancy.
- **Modern Tkinter GUI**: Features responsive layouts, real-time search & barcode lookups, dynamic cart management, and automatic invoice receipt generation.

---

## 🛠️ Tech Stack

- **Language:** Python 3.x
- **GUI Framework:** Tkinter & `tkinter.ttk` (Standard Library)
- **Database:** MySQL (using `mysql-connector-python` / `pymysql`)

---

## 📁 Project Architecture

```
ShopManagementSystem/
│
├── database/
│   ├── db_config.py          # MySQL connection loader & credential management
│   ├── db_helper.py          # OOP Database execution, queries & transactions
│   ├── schema.sql            # DDL script for categories, products, customers, invoices
│   └── config.json           # Active MySQL connection settings
│
├── models/
│   ├── product.py            # Product entity model with status calculations
│   ├── category.py           # Category entity model
│   ├── customer.py           # Customer entity model
│   └── bill.py               # Bill and BillItem transaction models
│
├── services/
│   ├── inventory_service.py  # Inventory CRUD, stock filters & category operations
│   └── billing_service.py    # Atomic checkout transactions & sales metrics
│
├── ui/
│   ├── theme.py              # Visual color palette, fonts & ttk styles
│   ├── main_window.py        # Main application frame & navigation sidebar
│   ├── dashboard_view.py     # KPI summary cards & stock alert indicators
│   ├── inventory_view.py     # Product CRUD management & search table
│   ├── billing_view.py       # POS checkout screen, live cart & bill generator
│   └── settings_view.py      # MySQL configuration & database seeder screen
│
├── utils/
│   └── invoice_generator.py  # Printable thermal-styled ASCII receipt formatter
│
├── invoices_saved/           # Directory where invoice receipts (.txt) are saved
├── main.py                   # Application launch script
├── seed_data.py              # 200+ demo products generator script
└── requirements.txt          # Python dependencies
```

---

## 🚀 Setup and Execution Instructions

### 1. Install Dependencies
Make sure you have Python 3.8+ installed. Then install the required MySQL driver:
```bash
pip install -r requirements.txt
```

### 2. Configure MySQL Database
Make sure your MySQL server (such as MySQL Server or XAMPP) is running.
The default connection settings are:
- **Host:** `localhost`
- **Port:** `3306`
- **User:** `root`
- **Password:** `""` (blank)
- **Database:** `shop_management_db`

*(You can modify these credentials anytime inside the application under the **Database Settings** tab).*

### 3. Seed Database with 200+ Products
Run the seed script directly from the terminal or click **"Populate 200+ Products"** from the app's Settings tab:
```bash
python seed_data.py
```

### 4. Launch the Application
```bash
python main.py
```

---

## 📋 Features Overview

1. **Dashboard:**
   - Real-time KPI cards: Total SKUs, Total Units in Stock, Low Stock Warnings, Today's Sales Revenue, and Invoice Count.
   - Live low stock table alerting cashiers when items drop below threshold.

2. **Inventory Management (CRUD):**
   - **Create:** Add new items with automated status tracking.
   - **Read:** Search dynamically by product name, ID, or barcode with category filtering.
   - **Update:** Edit prices, stock levels, or category assignments.
   - **Delete:** Remove discontinued items with safety confirmation.

3. **Point of Sale (POS) & Billing:**
   - Real-time catalog search and single-click or barcode-scan cart insertion.
   - Dynamic quantity adjustments and stock limits checking.
   - Automatic calculation of Subtotal, customizable GST/Tax %, and Discount %.
   - Multi-mode payment support (Cash, UPI / QR, Debit/Credit Card).
   - Atomic checkout transaction that writes invoice headers, invoice line items, and deducts inventory stock simultaneously.
   - Instant receipt viewer with automatic export to `invoices_saved/`.

4. **Settings & Diagnostics:**
   - Test MySQL connection directly within the GUI.
   - Initialize schema with one click.
