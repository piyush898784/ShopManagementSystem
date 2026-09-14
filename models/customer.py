"""
Customer Model for recording customer information and contact details.
"""

from typing import Optional, Dict, Any

class Customer:
    def __init__(
        self,
        customer_id: Optional[int] = None,
        phone: str = "",
        name: str = "Walk-in Customer",
        email: Optional[str] = "",
        address: Optional[str] = ""
    ):
        self.customer_id = customer_id
        self.phone = phone.strip()
        self.name = name.strip() if name else "Walk-in Customer"
        self.email = email.strip() if email else ""
        self.address = address.strip() if address else ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Customer":
        return cls(
            customer_id=data.get("customer_id"),
            phone=data.get("phone", ""),
            name=data.get("name", "Walk-in Customer"),
            email=data.get("email", ""),
            address=data.get("address", "")
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "phone": self.phone,
            "name": self.name,
            "email": self.email,
            "address": self.address
        }
