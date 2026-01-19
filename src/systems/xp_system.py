"""
XP System - Manages experience points and leveling for different skills

This module handles all skill progression logic, separated from game entities.
"""
from typing import Dict, Tuple
from src.config import GameBalance


class XPSystem:
    """Manages experience and levels for different skills"""

    def __init__(self) -> None:
        """Initialize XP system with default skills"""
        self.skills: Dict[str, Dict[str, int]] = {
            'Woodcutting': {'xp': 0, 'level': 1},
            'Combat': {'xp': 0, 'level': 1}
        }

    def add_xp(self, skill: str, amount: int) -> bool:
        """
        Add XP to a skill and level up if needed

        Args:
            skill: Name of the skill (e.g., 'Woodcutting', 'Combat')
            amount: Amount of XP to add

        Returns:
            True if the skill leveled up, False otherwise
        """
        if skill not in self.skills:
            return False

        self.skills[skill]['xp'] += amount
        new_level = self._calculate_level(self.skills[skill]['xp'])

        if new_level > self.skills[skill]['level']:
            self.skills[skill]['level'] = new_level
            return True  # Leveled up

        return False

    def get_skill_info(self, skill: str) -> Tuple[int, int]:
        """
        Get skill level and XP

        Args:
            skill: Name of the skill

        Returns:
            Tuple of (level, xp). Returns (0, 0) if skill doesn't exist
        """
        if skill in self.skills:
            return self.skills[skill]['level'], self.skills[skill]['xp']
        return 0, 0

    @staticmethod
    def _calculate_level(xp: int) -> int:
        """
        Calculate level from XP amount

        Args:
            xp: Total experience points

        Returns:
            Calculated level (minimum 1)
        """
        return xp // GameBalance.XP_PER_LEVEL + 1
