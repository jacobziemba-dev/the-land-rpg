"""
Tree Entity - Harvestable resource for Woodcutting skill

Trees can be chopped for logs and XP, then respawn after a delay.
"""
from typing import TYPE_CHECKING
import pygame

from src.entities.base import Entity
from src.config import GameBalance, Colors, AssetPaths

if TYPE_CHECKING:
    from src.entities.player import Player


class Tree(Entity):
    """Tree entity that can be chopped for logs"""

    def __init__(self, x: float, y: float) -> None:
        """
        Initialize tree at position

        Args:
            x: X coordinate
            y: Y coordinate
        """
        super().__init__(x, y, GameBalance.TREE_SIZE)

        # State
        self.active = True
        self.respawn_timer = 0

        # Load sprites for both states
        self.sprite_active: pygame.Surface | None = None
        self.sprite_chopped: pygame.Surface | None = None
        self._load_tree_sprites()

    def _load_tree_sprites(self) -> None:
        """Load sprites for active and chopped states"""
        # Load active tree sprite
        self.load_sprite(AssetPaths.TREE_ACTIVE_SPRITE, Colors.BROWN)
        self.sprite_active = self.sprite

        # Load chopped tree sprite (stump)
        self.load_sprite(AssetPaths.TREE_CHOPPED_SPRITE, Colors.BROWN)
        self.sprite_chopped = self.sprite

        # Set current sprite to active
        self.sprite = self.sprite_active

    def chop(self, player: 'Player') -> bool:
        """
        Player chops the tree

        Args:
            player: Player entity chopping the tree

        Returns:
            True if tree was successfully chopped, False if already chopped
        """
        if not self.active:
            return False

        # Give player logs and XP
        player.inventory.add_item("Logs", 1)
        player.xp_system.add_xp('Woodcutting', GameBalance.TREE_XP_PER_LOG)

        # Tree becomes inactive
        self.active = False
        self.respawn_timer = GameBalance.TREE_RESPAWN_DELAY
        self.sprite = self.sprite_chopped

        return True

    def update(self) -> None:
        """Update tree state and handle respawning"""
        if not self.active:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.active = True
                self.sprite = self.sprite_active

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw tree to screen

        Args:
            screen: Pygame surface to draw on
        """
        if self.sprite:
            # Draw appropriate sprite (active or chopped)
            sprite_rect = self.sprite.get_rect(center=(self.x, self.y))
            screen.blit(self.sprite, sprite_rect)
        else:
            # Fallback: draw brown square (faded if chopped)
            if self.active:
                pygame.draw.rect(screen, Colors.BROWN, self.get_rect())
            else:
                # Draw faded brown when chopped
                faded_color = (
                    Colors.BROWN[0] // 2,
                    Colors.BROWN[1] // 2,
                    Colors.BROWN[2] // 2
                )
                pygame.draw.rect(screen, faded_color, self.get_rect())
