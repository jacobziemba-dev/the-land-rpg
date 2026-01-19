"""
The Land RPG - Configuration and Constants

This module centralizes all game configuration values, eliminating magic numbers
and making balance adjustments easier.
"""
from typing import Tuple


# ============================================================================
# Screen Settings
# ============================================================================

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60


# ============================================================================
# Colors
# ============================================================================

class Colors:
    """Color constants used throughout the game"""
    BLACK: Tuple[int, int, int] = (0, 0, 0)
    WHITE: Tuple[int, int, int] = (255, 255, 255)
    GREEN: Tuple[int, int, int] = (0, 200, 0)
    BROWN: Tuple[int, int, int] = (139, 69, 19)
    RED: Tuple[int, int, int] = (200, 0, 0)
    GRAY: Tuple[int, int, int] = (128, 128, 128)
    LIGHT_GRAY: Tuple[int, int, int] = (200, 200, 200)


# ============================================================================
# Game Balance
# ============================================================================

class GameBalance:
    """Game balance constants for entities and systems"""

    # Player settings
    PLAYER_SIZE = 30
    PLAYER_SPEED = 3
    PLAYER_ATTACK_DAMAGE = 10
    PLAYER_ATTACK_DELAY = 60  # frames between attacks (1 second at 60 FPS)

    # Tree settings
    TREE_SIZE = 40
    TREE_RESPAWN_DELAY = 300  # frames (5 seconds at 60 FPS)
    TREE_XP_PER_LOG = 25

    # Enemy settings
    ENEMY_SIZE = 35
    ENEMY_MAX_HP = 100
    ENEMY_RESPAWN_DELAY = 600  # frames (10 seconds at 60 FPS)
    ENEMY_XP_PER_KILL = 50

    # XP System settings
    XP_PER_LEVEL = 100  # XP required per level (level = xp // 100 + 1)

    # UI settings
    INVENTORY_PANEL_WIDTH = 400
    INVENTORY_PANEL_HEIGHT = 400
    HP_BAR_HEIGHT = 5


# ============================================================================
# Asset Paths
# ============================================================================

class AssetPaths:
    """Paths to game assets (sprites, sounds, etc.)"""

    # Sprite paths
    PLAYER_SPRITE = "assets/sprites/player.png"
    TREE_ACTIVE_SPRITE = "assets/sprites/tree_active.png"
    TREE_CHOPPED_SPRITE = "assets/sprites/tree_chopped.png"
    ENEMY_SPRITE = "assets/sprites/enemy.png"
