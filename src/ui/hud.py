"""
HUD (Heads-Up Display) - Renders game UI elements

Pure rendering function for skills display and game instructions.
"""
from typing import TYPE_CHECKING
import pygame

from src.config import Colors, SCREEN_HEIGHT

if TYPE_CHECKING:
    from src.systems.xp_system import XPSystem


def draw_hud(screen: pygame.Surface, xp_system: 'XPSystem') -> None:
    """
    Draw HUD elements (skills and instructions)

    Args:
        screen: Pygame surface to draw on
        xp_system: XP system containing skill levels and XP data
    """
    # Draw skills
    _draw_skills(screen, xp_system)

    # Draw instructions
    _draw_instructions(screen)


def _draw_skills(screen: pygame.Surface, xp_system: 'XPSystem') -> None:
    """
    Draw skill levels and XP

    Args:
        screen: Pygame surface to draw on
        xp_system: XP system containing skill data
    """
    font = pygame.font.Font(None, 24)
    y_offset = 10

    for skill in ['Woodcutting', 'Combat']:
        level, xp = xp_system.get_skill_info(skill)
        text = font.render(f"{skill}: Lv {level} ({xp} XP)", True, Colors.WHITE)
        screen.blit(text, (10, y_offset))
        y_offset += 30


def _draw_instructions(screen: pygame.Surface) -> None:
    """
    Draw game instructions

    Args:
        screen: Pygame surface to draw on
    """
    font = pygame.font.Font(None, 20)
    instructions = [
        "Click to move",
        "Click trees to chop",
        "Click enemies to attack",
        "Press I for inventory"
    ]

    y_offset = SCREEN_HEIGHT - 90

    for instruction in instructions:
        text = font.render(instruction, True, Colors.WHITE)
        screen.blit(text, (10, y_offset))
        y_offset += 22
