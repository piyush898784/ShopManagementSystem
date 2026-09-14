"""
Bill and BillItem Models for transaction management and invoice generation.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime

class BillItem:
    def __init__(
        self,
        item_id: Optional[int] = None,
        invoice_no: str = "",
        product_id: int = 0,
        product_name: str = "",
        unit_price: float = 0.0,
        quantity: int = 1,
        line_total: float = 0.0
    ):
        self.item_id = item_id
        self.invoice_no = invoice_no
        self.product_id = product_id
        self.product_name = product_name
        self.unit_price = float(unit_price)
        self.quantity = int(quantity)
        self.line_total = round(self.unit_price * self.quantity, 2) if line_total == 0.0 else round(line_total, 2)

    def update_quantity(self, qty: int):
        self.quantity = max(1, qty)
        self.line_total = round(self.unit_price * self.quantity, 2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BillItem":
        return cls(
            item_id=data.get("item_id"),
            invoice_no=data.get("invoice_no", ""),
            product_id=int(data.get("product_id", 0)),
            product_name=data.get("product_name", ""),
            unit_price=float(data.get("unit_price", 0.0)),
            quantity=int(data.get("quantity", 1)),
            line_total=float(data.get("line_total", 0.0))
        )


class Bill:
    def __init__(
        self,
        invoice_no: str = "",
        customer_id: Optional[int] = None,
        customer_name: str = "Walk-in Customer",
        customer_phone: str = "",
        subtotal: float = 0.0,
        tax_percent: float = 5.0,
        tax_amount: float = 0.0,
        discount_percent: float = 0.0,
        discount_amount: float = 0.0,
        grand_total: float = 0.0,
        payment_mode: str = "Cash",
        invoice_date: Optional[str] = None,
        items: Optional[List[BillItem]] = None
    ):
        self.invoice_no = invoice_no or self.generate_invoice_no()
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.tax_percent = float(tax_percent)
        self.discount_percent = float(discount_percent)
        self.payment_mode = payment_mode
        self.invoice_date = invoice_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.items: List[BillItem] = items if items is not None else []
        
        self.subtotal = subtotal
        self.tax_amount = tax_amount
        self.discount_amount = discount_amount
        self.grand_total = grand_total
        
        if self.items and (subtotal == 0.0 and grand_total == 0.0):
            self.recalculate()

    @staticmethod
    def generate_invoice_no() -> str:
        return f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    def add_item(self, product_id: int, product_name: str, unit_price: float, quantity: int = 1) -> BillItem:
        # If product already in items, increment quantity
        for item in self.items:
            if item.product_id == product_id:
                item.update_quantity(item.quantity + quantity)
                self.recalculate()
                return item
        
        new_item = BillItem(
            invoice_no=self.invoice_no,
            product_id=product_id,
            product_name=product_name,
            unit_price=unit_price,
            quantity=quantity
        )
        self.items.append(new_item)
        self.recalculate()
        return new_item

    def remove_item(self, product_id: int) -> bool:
        initial_len = len(self.items)
        self.items = [item for item in self.items if item.product_id != product_id]
        self.recalculate()
        return len(self.items) < initial_len

    def update_item_quantity(self, product_id: int, new_quantity: int):
        for item in self.items:
            if item.product_id == product_id:
                if new_quantity <= 0:
                    self.remove_item(product_id)
                else:
                    item.update_quantity(new_quantity)
                self.recalculate()
                break

    def recalculate(self):
        """Calculates Subtotal, Tax amount, Discount amount, and Grand Total accurately."""
        self.subtotal = sum(item.line_total for item in self.items)
        self.discount_amount = round((self.subtotal * self.discount_percent) / 100.0, 2)
        taxable_amount = max(0.0, self.subtotal - self.discount_amount)
        self.tax_amount = round((taxable_amount * self.tax_percent) / 100.0, 2)
        self.grand_total = round(taxable_amount + self.tax_amount, 2)
