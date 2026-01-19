"""
Inventory UI - Renders the inventory panel

Pure rendering function with no game logic. Takes inventory data and draws it.
"""
from typing import TYPE_CHECKING
import pygame

from src.config import Colors, GameBalance, SCREEN_WIDTH, SCREEN_HEIGHT

if TYPE_CHECKING:
    from src.systems.inventory import Inventory


def draw_inventory(screen: pygame.Surface, inventory: 'Inventory') -> None:
    """
    Draw inventory UI panel

    Args:
        screen: Pygame surface to draw on
        inventory: Inventory system containing items and visibility state
    """
    if not inventory.visible:
        return

    # Draw semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(Colors.GRAY)
    screen.blit(overlay, (0, 0))

    # Calculate panel position (centered)
    panel_width = GameBalance.INVENTORY_PANEL_WIDTH
    panel_height = GameBalance.INVENTORY_PANEL_HEIGHT
    panel_x = (SCREEN_WIDTH - panel_width) // 2
    panel_y = (SCREEN_HEIGHT - panel_height) // 2

    # Draw inventory panel
    pygame.draw.rect(screen, Colors.LIGHT_GRAY, (panel_x, panel_y, panel_width, panel_height))
    pygame.draw.rect(screen, Colors.BLACK, (panel_x, panel_y, panel_width, panel_height), 3)

    # Draw title
    font = pygame.font.Font(None, 36)
    title = font.render("Inventory (Press I to close)", True, Colors.BLACK)
    screen.blit(title, (panel_x + 20, panel_y + 20))

    # Draw items
    item_font = pygame.font.Font(None, 28)
    y_offset = panel_y + 70

    if not inventory.items:
        # Show "empty" message if no items
        empty_text = item_font.render("(Empty)", True, Colors.GRAY)
        screen.blit(empty_text, (panel_x + 30, y_offset))
    else:
        # Draw each item with quantity
        for item_name, quantity in inventory.items.items():
            text = item_font.render(f"{item_name}: {quantity}", True, Colors.BLACK)
            screen.blit(text, (panel_x + 30, y_offset))
            y_offset += 35
