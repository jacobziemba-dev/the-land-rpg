"""
Base Entity Class - DRY foundation for all game entities

This abstract base class provides shared functionality for Player, Tree, and Enemy,
eliminating code duplication and ensuring consistent interface.
"""
from abc import ABC, abstractmethod
from typing import Optional, Tuple
import pygame
import os


class Entity(ABC):
    """Abstract base class for all game entities"""

    def __init__(self, x: float, y: float, size: int) -> None:
        """
        Initialize entity with position and size

        Args:
            x: X coordinate (center)
            y: Y coordinate (center)
            size: Size of the entity (width and height)
        """
        self.x = x
        self.y = y
        self.size = size
        self.sprite: Optional[pygame.Surface] = None

    def get_rect(self) -> pygame.Rect:
        """
        Get entity collision rectangle centered on position

        Returns:
            pygame.Rect centered on entity's x, y position
        """
        return pygame.Rect(
            self.x - self.size // 2,
            self.y - self.size // 2,
            self.size,
            self.size
        )

    def load_sprite(self, path: str, fallback_color: Tuple[int, int, int]) -> None:
        """
        Load sprite from file with graceful fallback to colored square

        Args:
            path: Path to sprite image file
            fallback_color: RGB color tuple to use if sprite fails to load
        """
        if os.path.exists(path):
            try:
                self.sprite = pygame.image.load(path).convert_alpha()
                # Scale sprite to entity size
                self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))
            except pygame.error:
                # If loading fails, sprite stays None (will use fallback)
                self.sprite = None
        # If file doesn't exist or loading failed, sprite remains None
        # Subclasses will handle fallback rendering

    @abstractmethod
    def update(self) -> None:
        """Update entity state - must be implemented by subclasses"""
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """Draw entity to screen - must be implemented by subclasses"""
        pass
