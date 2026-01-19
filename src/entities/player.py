"""
Player Entity - Player character with movement, combat, and progression

Manages player movement, combat mechanics, inventory, and skill progression.
"""
from typing import TYPE_CHECKING, Optional
import pygame
import math

from src.entities.base import Entity
from src.systems.xp_system import XPSystem
from src.systems.inventory import Inventory
from src.config import GameBalance, Colors, AssetPaths

if TYPE_CHECKING:
    from src.entities.enemy import Enemy


class Player(Entity):
    """Player character with movement, stats, and combat abilities"""

    def __init__(self, x: float, y: float) -> None:
        """
        Initialize player at position

        Args:
            x: Starting X coordinate
            y: Starting Y coordinate
        """
        super().__init__(x, y, GameBalance.PLAYER_SIZE)

        # Movement
        self.speed = GameBalance.PLAYER_SPEED
        self.target_x = x
        self.target_y = y

        # Systems
        self.xp_system = XPSystem()
        self.inventory = Inventory()

        # Combat
        self.attacking_enemy: Optional['Enemy'] = None
        self.attack_cooldown = 0

        # Load sprite with fallback to green square
        self.load_sprite(AssetPaths.PLAYER_SPRITE, Colors.GREEN)

    def move_to(self, x: float, y: float) -> None:
        """
        Set movement target position

        Args:
            x: Target X coordinate
            y: Target Y coordinate
        """
        self.target_x = x
        self.target_y = y

    def start_attack(self, enemy: 'Enemy') -> None:
        """
        Begin attacking an enemy

        Args:
            enemy: Enemy entity to attack
        """
        self.attacking_enemy = enemy
        self.attack_cooldown = 0

    def stop_attack(self) -> None:
        """Stop attacking current enemy"""
        self.attacking_enemy = None

    def update(self) -> None:
        """Update player position and combat state"""
        self._update_movement()
        self._update_combat()

    def _update_movement(self) -> None:
        """Update player movement towards target"""
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.sqrt(dx**2 + dy**2)

        if dist > self.speed:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
        else:
            self.x = self.target_x
            self.y = self.target_y

    def _update_combat(self) -> None:
        """Handle auto-attack logic"""
        if not self.attacking_enemy:
            return

        # Count down attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            return

        # Attack the enemy
        if self.attacking_enemy.take_damage(GameBalance.PLAYER_ATTACK_DAMAGE):
            # Enemy defeated
            self.xp_system.add_xp('Combat', GameBalance.ENEMY_XP_PER_KILL)
            self.attacking_enemy = None
        else:
            # Reset cooldown for next attack
            self.attack_cooldown = GameBalance.PLAYER_ATTACK_DELAY

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw player to screen

        Args:
            screen: Pygame surface to draw on
        """
        if self.sprite:
            # Draw sprite centered on position
            sprite_rect = self.sprite.get_rect(center=(self.x, self.y))
            screen.blit(self.sprite, sprite_rect)
        else:
            # Fallback: draw green square
            pygame.draw.rect(screen, Colors.GREEN, self.get_rect())
