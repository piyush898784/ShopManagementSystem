"""
Category Model class representing product categories.
"""

from typing import Optional, Dict, Any

class Category:
    def __init__(self, category_id: Optional[int], name: str, description: Optional[str] = ""):
        self.category_id = category_id
        self.name = name.strip()
        self.description = description.strip() if description else ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Category":
        return cls(
            category_id=data.get("category_id"),
            name=data.get("name", ""),
            description=data.get("description", "")
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description
        }
