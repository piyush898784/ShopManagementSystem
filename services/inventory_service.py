"""
Inventory Service encapsulating all business logic and CRUD queries for Products and Categories.
"""

from typing import List, Dict, Any, Optional, Tuple
from database.db_helper import DBHelper
from models.product import Product
from models.category import Category


class InventoryService:
    @staticmethod
    def get_all_categories() -> List[Category]:
        """Fetches all product categories."""
        query = "SELECT category_id, name, description FROM categories ORDER BY name ASC"
        rows = DBHelper.fetch_all(query)
        return [Category.from_dict(row) for row in rows]

    @staticmethod
    def add_category(name: str, description: str = "") -> int:
        """Adds a new category."""
        query = "INSERT INTO categories (name, description) VALUES (%s, %s)"
        return DBHelper.execute_query(query, (name.strip(), description.strip()), commit=True)

    @staticmethod
    def get_all_products(category_id: Optional[int] = None, search_query: Optional[str] = None) -> List[Product]:
        """
        Retrieves products with category names joined, optionally filtered by category or search string.
        """
        query = """
            SELECT 
                p.product_id,
                p.category_id,
                c.name AS category_name,
                p.name,
                p.barcode,
                p.price,
                p.cost_price,
                p.quantity,
                p.min_stock_alert,
                p.status
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
            WHERE 1=1
        """
        params = []
        if category_id and category_id > 0:
            query += " AND p.category_id = %s"
            params.append(category_id)
        
        if search_query and search_query.strip():
            term = f"%{search_query.strip()}%"
            query += " AND (p.name LIKE %s OR p.barcode LIKE %s OR CAST(p.product_id AS CHAR) LIKE %s)"
            params.extend([term, term, term])

        query += " ORDER BY p.product_id DESC"
        rows = DBHelper.fetch_all(query, tuple(params))
        return [Product.from_dict(row) for row in rows]

    @staticmethod
    def get_product_by_id(product_id: int) -> Optional[Product]:
        """Fetches single product by ID."""
        query = """
            SELECT 
                p.product_id, p.category_id, c.name AS category_name,
                p.name, p.barcode, p.price, p.cost_price, p.quantity,
                p.min_stock_alert, p.status
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
            WHERE p.product_id = %s
        """
        row = DBHelper.fetch_one(query, (product_id,))
        return Product.from_dict(row) if row else None

    @staticmethod
    def get_product_by_barcode(barcode: str) -> Optional[Product]:
        """Fetches single product by Barcode."""
        query = """
            SELECT 
                p.product_id, p.category_id, c.name AS category_name,
                p.name, p.barcode, p.price, p.cost_price, p.quantity,
                p.min_stock_alert, p.status
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
            WHERE p.barcode = %s
        """
        row = DBHelper.fetch_one(query, (barcode,))
        return Product.from_dict(row) if row else None

    @staticmethod
    def add_product(product: Product) -> int:
        """Inserts a new product into the database."""
        query = """
            INSERT INTO products 
            (category_id, name, barcode, price, cost_price, quantity, min_stock_alert)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            product.category_id,
            product.name,
            product.barcode if product.barcode else None,
            product.price,
            product.cost_price,
            product.quantity,
            product.min_stock_alert
        )
        return DBHelper.execute_query(query, params, commit=True)

    @staticmethod
    def update_product(product: Product) -> bool:
        """Updates product information."""
        query = """
            UPDATE products 
            SET category_id = %s,
                name = %s,
                barcode = %s,
                price = %s,
                cost_price = %s,
                quantity = %s,
                min_stock_alert = %s
            WHERE product_id = %s
        """
        params = (
            product.category_id,
            product.name,
            product.barcode if product.barcode else None,
            product.price,
            product.cost_price,
            product.quantity,
            product.min_stock_alert,
            product.product_id
        )
        DBHelper.execute_query(query, params, commit=True)
        return True

    @staticmethod
    def delete_product(product_id: int) -> bool:
        """Deletes a product by ID."""
        query = "DELETE FROM products WHERE product_id = %s"
        DBHelper.execute_query(query, (product_id,), commit=True)
        return True

    @staticmethod
    def get_inventory_summary() -> Dict[str, Any]:
        """Calculates dashboard summary metrics for inventory."""
        query = """
            SELECT 
                COUNT(*) AS total_products,
                IFNULL(SUM(quantity), 0) AS total_units,
                IFNULL(SUM(price * quantity), 0) AS retail_valuation,
                IFNULL(SUM(cost_price * quantity), 0) AS cost_valuation,
                SUM(CASE WHEN quantity <= 0 THEN 1 ELSE 0 END) AS out_of_stock_count,
                SUM(CASE WHEN quantity > 0 AND quantity <= min_stock_alert THEN 1 ELSE 0 END) AS low_stock_count
            FROM products
        """
        row = DBHelper.fetch_one(query)
        if not row:
            return {
                "total_products": 0,
                "total_units": 0,
                "retail_valuation": 0.0,
                "cost_valuation": 0.0,
                "out_of_stock_count": 0,
                "low_stock_count": 0
            }
        return {
            "total_products": int(row.get("total_products", 0)),
            "total_units": int(row.get("total_units", 0)),
            "retail_valuation": float(row.get("retail_valuation", 0.0)),
            "cost_valuation": float(row.get("cost_valuation", 0.0)),
            "out_of_stock_count": int(row.get("out_of_stock_count", 0)),
            "low_stock_count": int(row.get("low_stock_count", 0))
        }
