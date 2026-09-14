"""
Product Model representing inventory items with validation and calculation methods.
"""

from typing import Optional, Dict, Any

class Product:
    def __init__(
        self,
        product_id: Optional[int] = None,
        category_id: int = 1,
        category_name: str = "",
        name: str = "",
        barcode: Optional[str] = None,
        price: float = 0.0,
        cost_price: float = 0.0,
        quantity: int = 0,
        min_stock_alert: int = 10,
        status: str = "In Stock"
    ):
        self.product_id = product_id
        self.category_id = category_id
        self.category_name = category_name
        self.name = name.strip()
        self.barcode = barcode.strip() if barcode else None
        self.price = float(price)
        self.cost_price = float(cost_price)
        self.quantity = int(quantity)
        self.min_stock_alert = int(min_stock_alert)
        self.status = self.calculate_status()

    def calculate_status(self) -> str:
        if self.quantity <= 0:
            return "Out of Stock"
        elif self.quantity <= self.min_stock_alert:
            return "Low Stock"
        return "In Stock"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Product":
        return cls(
            product_id=data.get("product_id"),
            category_id=data.get("category_id", 1),
            category_name=data.get("category_name", ""),
            name=data.get("name", ""),
            barcode=data.get("barcode"),
            price=float(data.get("price", 0.0)),
            cost_price=float(data.get("cost_price", 0.0)),
            quantity=int(data.get("quantity", 0)),
            min_stock_alert=int(data.get("min_stock_alert", 10)),
            status=data.get("status", "In Stock")
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "product_id": self.product_id,
            "category_id": self.category_id,
            "category_name": self.category_name,
            "name": self.name,
            "barcode": self.barcode,
            "price": self.price,
            "cost_price": self.cost_price,
            "quantity": self.quantity,
            "min_stock_alert": self.min_stock_alert,
            "status": self.calculate_status()
        }
