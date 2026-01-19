"""
Enemy Entity - Hostile creature that can be attacked for Combat XP

Enemies have HP, can be defeated, and respawn after a delay.
"""
import pygame

from src.entities.base import Entity
from src.config import GameBalance, Colors, AssetPaths


class Enemy(Entity):
    """Enemy entity that can be attacked"""

    def __init__(self, x: float, y: float) -> None:
        """
        Initialize enemy at position

        Args:
            x: X coordinate
            y: Y coordinate
        """
        super().__init__(x, y, GameBalance.ENEMY_SIZE)

        # Combat stats
        self.max_hp = GameBalance.ENEMY_MAX_HP
        self.hp = self.max_hp
        self.alive = True

        # Respawn system
        self.respawn_timer = 0

        # Load sprite with fallback to red square
        self.load_sprite(AssetPaths.ENEMY_SPRITE, Colors.RED)

    def take_damage(self, damage: int) -> bool:
        """
        Take damage and check if defeated

        Args:
            damage: Amount of damage to take

        Returns:
            True if enemy was defeated, False otherwise
        """
        self.hp -= damage

        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            self.respawn_timer = GameBalance.ENEMY_RESPAWN_DELAY
            return True  # Defeated

        return False

    def update(self) -> None:
        """Update enemy state and handle respawning"""
        if not self.alive:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.alive = True
                self.hp = self.max_hp

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw enemy to screen with HP bar

        Args:
            screen: Pygame surface to draw on
        """
        if not self.alive:
            return

        # Draw sprite or fallback to red square
        if self.sprite:
            sprite_rect = self.sprite.get_rect(center=(self.x, self.y))
            screen.blit(self.sprite, sprite_rect)
        else:
            pygame.draw.rect(screen, Colors.RED, self.get_rect())

        # Draw HP bar
        self._draw_hp_bar(screen)

    def _draw_hp_bar(self, screen: pygame.Surface) -> None:
        """
        Draw HP bar above enemy

        Args:
            screen: Pygame surface to draw on
        """
        bar_width = self.size
        bar_height = GameBalance.HP_BAR_HEIGHT
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.size // 2 - 10

        # Background (red - damage taken)
        pygame.draw.rect(screen, Colors.RED, (bar_x, bar_y, bar_width, bar_height))

        # Current HP (green)
        hp_width = int(bar_width * (self.hp / self.max_hp))
        pygame.draw.rect(screen, Colors.GREEN, (bar_x, bar_y, hp_width, bar_height))
