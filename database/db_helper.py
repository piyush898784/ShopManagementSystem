"""
Optimized Database Helper for ultra-fast, smooth execution.
Maintains persistent connection with automatic reconnection and fallback to prevent GUI freezing.
"""

import os
import sqlite3
from typing import List, Dict, Any, Optional, Tuple
from .db_config import DatabaseConfig, CONNECTOR_TYPE


class DBHelper:
    _mysql_conn = None
    _use_sqlite_fallback = False
    _sqlite_file = os.path.join(os.path.dirname(__file__), "shop_local.db")

    @classmethod
    def get_raw_connection(cls):
        """Returns an active reusable connection or creates one."""
        if cls._use_sqlite_fallback:
            conn = sqlite3.connect(cls._sqlite_file)
            conn.row_factory = sqlite3.Row
            return conn

        try:
            if cls._mysql_conn is None or not cls._is_connection_alive(cls._mysql_conn):
                cls._mysql_conn = DatabaseConfig.get_connection(include_database=True)
            return cls._mysql_conn
        except Exception:
            cls._use_sqlite_fallback = True
            cls._init_sqlite_schema()
            conn = sqlite3.connect(cls._sqlite_file)
            conn.row_factory = sqlite3.Row
            return conn

    @staticmethod
    def _is_connection_alive(conn) -> bool:
        try:
            if hasattr(conn, "is_connected"):
                return conn.is_connected()
            elif hasattr(conn, "ping"):
                conn.ping(reconnect=True)
                return True
            return True
        except Exception:
            return False

    @classmethod
    def _init_sqlite_schema(cls):
        """Initializes fast SQLite schema for smooth standalone operation."""
        conn = sqlite3.connect(cls._sqlite_file)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                barcode TEXT UNIQUE,
                price REAL NOT NULL DEFAULT 0.0,
                cost_price REAL NOT NULL DEFAULT 0.0,
                quantity INTEGER NOT NULL DEFAULT 0,
                min_stock_alert INTEGER NOT NULL DEFAULT 10,
                status TEXT DEFAULT 'In Stock'
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                email TEXT,
                address TEXT
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                invoice_no TEXT PRIMARY KEY,
                customer_id INTEGER,
                customer_name TEXT,
                customer_phone TEXT,
                subtotal REAL,
                tax_percent REAL,
                tax_amount REAL,
                discount_percent REAL,
                discount_amount REAL,
                grand_total REAL,
                payment_mode TEXT,
                invoice_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS invoice_items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_no TEXT,
                product_id INTEGER,
                product_name TEXT,
                unit_price REAL,
                quantity INTEGER,
                line_total REAL
            )
        """)
        conn.commit()
        conn.close()

    @classmethod
    def initialize_database(cls) -> Tuple[bool, str]:
        try:
            conn = DatabaseConfig.get_connection(include_database=False)
            cursor = conn.cursor()
            cfg = DatabaseConfig.load_config()
            db_name = cfg.get("database", "shop_management_db")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4;")
            conn.commit()
            cursor.close()
            conn.close()

            conn = DatabaseConfig.get_connection(include_database=True)
            cursor = conn.cursor()
            schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
            with open(schema_path, "r", encoding="utf-8") as f:
                sql_script = f.read()

            statements = [s.strip() for s in sql_script.split(";") if s.strip()]
            for statement in statements:
                if statement.upper().startswith("CREATE DATABASE") or statement.upper().startswith("USE "):
                    continue
                cursor.execute(statement)

            conn.commit()
            cursor.close()
            cls._mysql_conn = conn
            cls._use_sqlite_fallback = False
            return True, f"Database '{db_name}' ready!"
        except Exception as e:
            cls._use_sqlite_fallback = True
            cls._init_sqlite_schema()
            return True, f"Local database active (MySQL offline: {e})"

    @classmethod
    def execute_query(cls, query: str, params: Optional[Tuple] = None, commit: bool = True) -> int:
        conn = cls.get_raw_connection()
        is_sqlite = isinstance(conn, sqlite3.Connection)
        if is_sqlite:
            query = query.replace("%s", "?")
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            if commit:
                conn.commit()
            last_id = cursor.lastrowid
            conn.close()
            return last_id

        cursor = conn.cursor()
        cursor.execute(query, params or ())
        if commit:
            conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        return last_id

    @classmethod
    def fetch_all(cls, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        conn = cls.get_raw_connection()
        is_sqlite = isinstance(conn, sqlite3.Connection)
        if is_sqlite:
            query = query.replace("%s", "?")
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            rows = [dict(r) for r in cursor.fetchall()]
            conn.close()
            return rows

        if CONNECTOR_TYPE == "mysql.connector":
            cursor = conn.cursor(dictionary=True)
        else:
            cursor = conn.cursor()
        cursor.execute(query, params or ())
        rows = cursor.fetchall()
        cursor.close()
        return rows

    @classmethod
    def fetch_one(cls, query: str, params: Optional[Tuple] = None) -> Optional[Dict[str, Any]]:
        conn = cls.get_raw_connection()
        is_sqlite = isinstance(conn, sqlite3.Connection)
        if is_sqlite:
            query = query.replace("%s", "?")
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            r = cursor.fetchone()
            row = dict(r) if r else None
            conn.close()
            return row

        if CONNECTOR_TYPE == "mysql.connector":
            cursor = conn.cursor(dictionary=True)
        else:
            cursor = conn.cursor()
        cursor.execute(query, params or ())
        row = cursor.fetchone()
        cursor.close()
        return row
