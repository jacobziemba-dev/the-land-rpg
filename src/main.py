"""
The Land RPG - Main Game Controller

Orchestrates all game systems, entities, and rendering.
"""
import pygame
import sys
from typing import List

from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, Colors
from src.entities.player import Player
from src.entities.tree import Tree
from src.entities.enemy import Enemy
from src.ui.hud import draw_hud
from src.ui.inventory_ui import draw_inventory


class Game:
    """Main game class that orchestrates all systems"""

    def __init__(self) -> None:
        """Initialize game and create all game objects"""
        # Initialize Pygame
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("The Land RPG")
        self.clock = pygame.time.Clock()
        self.running = True

        # Create player
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # Create trees
        self.trees: List[Tree] = [
            Tree(150, 150),
            Tree(650, 150),
            Tree(150, 450),
            Tree(650, 450),
            Tree(400, 100),
        ]

        # Create enemies
        self.enemies: List[Enemy] = [
            Enemy(300, 300),
            Enemy(500, 300),
            Enemy(400, 400),
        ]

    def handle_events(self) -> None:
        """Handle all game events (keyboard, mouse, etc.)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self._handle_keypress(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self._handle_left_click(event.pos)

    def _handle_keypress(self, key: int) -> None:
        """
        Handle keyboard input

        Args:
            key: Pygame key constant
        """
        if key == pygame.K_i:
            self.player.inventory.toggle()

    def _handle_left_click(self, pos: tuple[int, int]) -> None:
        """
        Handle left mouse click

        Args:
            pos: Mouse position (x, y)
        """
        mouse_x, mouse_y = pos

        # Don't process clicks if inventory is open
        if self.player.inventory.visible:
            return

        # Try to chop a tree
        if self._try_chop_tree(mouse_x, mouse_y):
            return

        # Try to attack an enemy
        if self._try_attack_enemy(mouse_x, mouse_y):
            return

        # If not clicking on interactive object, move player
        self.player.move_to(mouse_x, mouse_y)
        self.player.stop_attack()

    def _try_chop_tree(self, x: int, y: int) -> bool:
        """
        Try to chop a tree at the clicked position

        Args:
            x: Click X coordinate
            y: Click Y coordinate

        Returns:
            True if a tree was clicked and chopped, False otherwise
        """
        for tree in self.trees:
            if tree.get_rect().collidepoint(x, y):
                if tree.active:
                    tree.chop(self.player)
                return True
        return False

    def _try_attack_enemy(self, x: int, y: int) -> bool:
        """
        Try to attack an enemy at the clicked position

        Args:
            x: Click X coordinate
            y: Click Y coordinate

        Returns:
            True if an enemy was clicked and attacked, False otherwise
        """
        for enemy in self.enemies:
            if enemy.get_rect().collidepoint(x, y):
                if enemy.alive:
                    self.player.start_attack(enemy)
                return True
        return False

    def update(self) -> None:
        """Update all game entities"""
        self.player.update()

        for tree in self.trees:
            tree.update()

        for enemy in self.enemies:
            enemy.update()

    def draw(self) -> None:
        """Draw all game elements"""
        # Clear screen
        self.screen.fill(Colors.BLACK)

        # Draw trees
        for tree in self.trees:
            tree.draw(self.screen)

        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Draw player
        self.player.draw(self.screen)

        # Draw HUD (skills and instructions)
        draw_hud(self.screen, self.player.xp_system)

        # Draw inventory (on top of everything)
        draw_inventory(self.screen, self.player.inventory)

        # Update display
        pygame.display.flip()

    def run(self) -> None:
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


def main() -> None:
    """Entry point for the game"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
