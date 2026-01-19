"""
Create simple placeholder sprites for The Land RPG

This script generates basic sprites programmatically until proper art assets are added.
"""
import pygame
import os

# Initialize Pygame
pygame.init()

# Create assets directory
os.makedirs("assets/sprites", exist_ok=True)

def create_player_sprite():
    """Create a simple player sprite (30x30)"""
    size = 30
    surface = pygame.Surface((size, size), pygame.SRCALPHA)

    # Draw a simple character (green circle with darker outline)
    pygame.draw.circle(surface, (0, 200, 0), (size // 2, size // 2), size // 2 - 2)
    pygame.draw.circle(surface, (0, 150, 0), (size // 2, size // 2), size // 2 - 2, 2)

    # Add eyes
    pygame.draw.circle(surface, (255, 255, 255), (size // 2 - 5, size // 2 - 3), 3)
    pygame.draw.circle(surface, (255, 255, 255), (size // 2 + 5, size // 2 - 3), 3)
    pygame.draw.circle(surface, (0, 0, 0), (size // 2 - 5, size // 2 - 3), 2)
    pygame.draw.circle(surface, (0, 0, 0), (size // 2 + 5, size // 2 - 3), 2)

    pygame.image.save(surface, "assets/sprites/player.png")
    print("Created player.png")

def create_tree_active_sprite():
    """Create an active tree sprite (40x40)"""
    size = 40
    surface = pygame.Surface((size, size), pygame.SRCALPHA)

    # Draw trunk (brown rectangle)
    trunk_width = 8
    trunk_height = 15
    trunk_x = (size - trunk_width) // 2
    trunk_y = size - trunk_height - 2
    pygame.draw.rect(surface, (101, 67, 33), (trunk_x, trunk_y, trunk_width, trunk_height))

    # Draw foliage (green circles)
    pygame.draw.circle(surface, (34, 139, 34), (size // 2, size // 2 - 5), 12)
    pygame.draw.circle(surface, (34, 139, 34), (size // 2 - 8, size // 2), 10)
    pygame.draw.circle(surface, (34, 139, 34), (size // 2 + 8, size // 2), 10)
    pygame.draw.circle(surface, (46, 125, 50), (size // 2, size // 2 - 5), 12, 2)

    pygame.image.save(surface, "assets/sprites/tree_active.png")
    print("Created tree_active.png")

def create_tree_chopped_sprite():
    """Create a chopped tree sprite / stump (40x40)"""
    size = 40
    surface = pygame.Surface((size, size), pygame.SRCALPHA)

    # Draw stump (brown with rings)
    stump_size = 14
    stump_x = (size - stump_size) // 2
    stump_y = size - stump_size - 2

    # Outer circle (darker brown)
    pygame.draw.circle(surface, (101, 67, 33), (size // 2, stump_y + stump_size // 2), stump_size // 2)
    # Inner rings (lighter brown)
    pygame.draw.circle(surface, (139, 90, 43), (size // 2, stump_y + stump_size // 2), stump_size // 2 - 2, 2)
    pygame.draw.circle(surface, (101, 67, 33), (size // 2, stump_y + stump_size // 2), stump_size // 2 - 4, 1)

    pygame.image.save(surface, "assets/sprites/tree_chopped.png")
    print("Created tree_chopped.png")

def create_enemy_sprite():
    """Create a simple enemy sprite (35x35)"""
    size = 35
    surface = pygame.Surface((size, size), pygame.SRCALPHA)

    # Draw a simple skull-like shape (red/dark red)
    # Main head circle
    pygame.draw.circle(surface, (200, 0, 0), (size // 2, size // 2), size // 2 - 2)
    pygame.draw.circle(surface, (150, 0, 0), (size // 2, size // 2), size // 2 - 2, 2)

    # Eyes (dark holes)
    pygame.draw.circle(surface, (100, 0, 0), (size // 2 - 6, size // 2 - 4), 4)
    pygame.draw.circle(surface, (100, 0, 0), (size // 2 + 6, size // 2 - 4), 4)

    # Menacing mouth
    pygame.draw.arc(surface, (100, 0, 0), (size // 2 - 8, size // 2, 16, 10), 0, 3.14, 2)

    pygame.image.save(surface, "assets/sprites/enemy.png")
    print("Created enemy.png")

if __name__ == "__main__":
    print("Creating placeholder sprites...")
    create_player_sprite()
    create_tree_active_sprite()
    create_tree_chopped_sprite()
    create_enemy_sprite()
    print("\nAll sprites created successfully in assets/sprites/")
    print("These are simple placeholders - you can replace them with better art later!")
