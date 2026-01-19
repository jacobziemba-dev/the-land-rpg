"""
Inventory System - Manages player item storage

This module handles inventory data logic only. Rendering is handled by the UI module.
"""
from typing import Dict


class Inventory:
    """Manages player inventory items"""

    def __init__(self) -> None:
        """Initialize empty inventory"""
        self.items: Dict[str, int] = {}
        self.visible: bool = False

    def add_item(self, item_name: str, quantity: int = 1) -> None:
        """
        Add items to inventory

        Args:
            item_name: Name of the item to add
            quantity: Number of items to add (default: 1)
        """
        if item_name in self.items:
            self.items[item_name] += quantity
        else:
            self.items[item_name] = quantity

    def remove_item(self, item_name: str, quantity: int = 1) -> bool:
        """
        Remove items from inventory

        Args:
            item_name: Name of the item to remove
            quantity: Number of items to remove (default: 1)

        Returns:
            True if items were removed successfully, False if not enough items
        """
        if item_name not in self.items:
            return False

        if self.items[item_name] < quantity:
            return False

        self.items[item_name] -= quantity

        # Remove item from dict if quantity reaches 0
        if self.items[item_name] == 0:
            del self.items[item_name]

        return True

    def has_item(self, item_name: str, quantity: int = 1) -> bool:
        """
        Check if inventory contains specified quantity of an item

        Args:
            item_name: Name of the item to check
            quantity: Required quantity (default: 1)

        Returns:
            True if inventory has at least the specified quantity
        """
        return self.items.get(item_name, 0) >= quantity

    def toggle(self) -> None:
        """Toggle inventory visibility"""
        self.visible = not self.visible

    def get_item_count(self, item_name: str) -> int:
        """
        Get the quantity of a specific item

        Args:
            item_name: Name of the item

        Returns:
            Quantity of the item (0 if not in inventory)
        """
        return self.items.get(item_name, 0)
