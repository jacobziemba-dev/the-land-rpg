"""
The Land RPG - A top-down adventure game with skilling and combat
"""
import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BROWN = (139, 69, 19)
RED = (200, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)


class XPSystem:
    """Manages experience and levels for different skills"""
    def __init__(self):
        self.skills = {
            'Woodcutting': {'xp': 0, 'level': 1},
            'Combat': {'xp': 0, 'level': 1}
        }
    
    def add_xp(self, skill, amount):
        """Add XP to a skill and level up if needed"""
        if skill in self.skills:
            self.skills[skill]['xp'] += amount
            # Simple level calculation: level = xp // 100 + 1
            new_level = self.skills[skill]['xp'] // 100 + 1
            if new_level > self.skills[skill]['level']:
                self.skills[skill]['level'] = new_level
                return True  # Leveled up
        return False
    
    def get_skill_info(self, skill):
        """Get skill level and XP"""
        if skill in self.skills:
            return self.skills[skill]['level'], self.skills[skill]['xp']
        return 0, 0


class Inventory:
    """Manages player inventory"""
    def __init__(self):
        self.items = {}
        self.visible = False
    
    def add_item(self, item_name, quantity=1):
        """Add items to inventory"""
        if item_name in self.items:
            self.items[item_name] += quantity
        else:
            self.items[item_name] = quantity
    
    def toggle(self):
        """Toggle inventory visibility"""
        self.visible = not self.visible
    
    def draw(self, screen):
        """Draw inventory UI"""
        if not self.visible:
            return
        
        # Draw semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(GRAY)
        screen.blit(overlay, (0, 0))
        
        # Draw inventory panel
        panel_width = 400
        panel_height = 400
        panel_x = (SCREEN_WIDTH - panel_width) // 2
        panel_y = (SCREEN_HEIGHT - panel_height) // 2
        
        pygame.draw.rect(screen, LIGHT_GRAY, (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(screen, BLACK, (panel_x, panel_y, panel_width, panel_height), 3)
        
        # Draw title
        font = pygame.font.Font(None, 36)
        title = font.render("Inventory (Press I to close)", True, BLACK)
        screen.blit(title, (panel_x + 20, panel_y + 20))
        
        # Draw items
        font = pygame.font.Font(None, 28)
        y_offset = panel_y + 70
        for item_name, quantity in self.items.items():
            text = font.render(f"{item_name}: {quantity}", True, BLACK)
            screen.blit(text, (panel_x + 30, y_offset))
            y_offset += 35


class Player:
    """Player character with movement and stats"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 30
        self.color = GREEN
        self.speed = 3
        self.target_x = x
        self.target_y = y
        self.xp_system = XPSystem()
        self.inventory = Inventory()
        self.attacking_enemy = None
        self.attack_cooldown = 0
        self.attack_delay = 60  # frames between attacks (1 second at 60 FPS)
    
    def move_to(self, x, y):
        """Set movement target"""
        self.target_x = x
        self.target_y = y
    
    def update(self):
        """Update player position and combat"""
        # Move towards target
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.sqrt(dx**2 + dy**2)
        
        if dist > self.speed:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
        else:
            self.x = self.target_x
            self.y = self.target_y
        
        # Handle auto-attack
        if self.attacking_enemy and self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        if self.attacking_enemy and self.attack_cooldown == 0:
            # Attack the enemy
            if self.attacking_enemy.take_damage(10):
                # Enemy defeated
                self.xp_system.add_xp('Combat', 50)
                self.attacking_enemy = None
            else:
                self.attack_cooldown = self.attack_delay
    
    def get_rect(self):
        """Get player collision rectangle"""
        return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)
    
    def draw(self, screen):
        """Draw player"""
        pygame.draw.rect(screen, self.color, self.get_rect())


class Tree:
    """Tree entity that can be chopped for logs"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 40
        self.color = BROWN
        self.respawn_timer = 0
        self.respawn_delay = 300  # 5 seconds at 60 FPS
        self.active = True
    
    def chop(self, player):
        """Player chops the tree"""
        if self.active:
            player.inventory.add_item("Logs", 1)
            player.xp_system.add_xp('Woodcutting', 25)
            self.active = False
            self.respawn_timer = self.respawn_delay
    
    def update(self):
        """Update tree state"""
        if not self.active:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.active = True
    
    def get_rect(self):
        """Get tree collision rectangle"""
        return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)
    
    def draw(self, screen):
        """Draw tree"""
        if self.active:
            pygame.draw.rect(screen, self.color, self.get_rect())
        else:
            # Draw faded tree when chopped
            faded_color = (self.color[0] // 2, self.color[1] // 2, self.color[2] // 2)
            pygame.draw.rect(screen, faded_color, self.get_rect())


class Enemy:
    """Enemy entity that can be attacked"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 35
        self.color = RED
        self.max_hp = 100
        self.hp = self.max_hp
        self.alive = True
        self.respawn_timer = 0
        self.respawn_delay = 600  # 10 seconds at 60 FPS
    
    def take_damage(self, damage):
        """Take damage and check if defeated"""
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            self.respawn_timer = self.respawn_delay
            return True  # Defeated
        return False
    
    def update(self):
        """Update enemy state"""
        if not self.alive:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.alive = True
                self.hp = self.max_hp
    
    def get_rect(self):
        """Get enemy collision rectangle"""
        return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)
    
    def draw(self, screen):
        """Draw enemy"""
        if self.alive:
            pygame.draw.rect(screen, self.color, self.get_rect())
            # Draw HP bar
            bar_width = self.size
            bar_height = 5
            bar_x = self.x - bar_width // 2
            bar_y = self.y - self.size // 2 - 10
            
            # Background (red)
            pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
            # Current HP (green)
            hp_width = int(bar_width * (self.hp / self.max_hp))
            pygame.draw.rect(screen, GREEN, (bar_x, bar_y, hp_width, bar_height))


class Game:
    """Main game class"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("The Land RPG")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Create game objects
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Create trees
        self.trees = [
            Tree(150, 150),
            Tree(650, 150),
            Tree(150, 450),
            Tree(650, 450),
            Tree(400, 100),
        ]
        
        # Create enemies
        self.enemies = [
            Enemy(300, 300),
            Enemy(500, 300),
            Enemy(400, 400),
        ]
    
    def handle_events(self):
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    self.player.inventory.toggle()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_x, mouse_y = event.pos
                    
                    # Don't process clicks if inventory is open
                    if self.player.inventory.visible:
                        continue
                    
                    # Check if clicking on a tree
                    clicked_tree = False
                    for tree in self.trees:
                        if tree.get_rect().collidepoint(mouse_x, mouse_y):
                            if tree.active:
                                tree.chop(self.player)
                                clicked_tree = True
                            break
                    
                    # Check if clicking on an enemy
                    clicked_enemy = False
                    if not clicked_tree:
                        for enemy in self.enemies:
                            if enemy.get_rect().collidepoint(mouse_x, mouse_y):
                                if enemy.alive:
                                    self.player.attacking_enemy = enemy
                                    self.player.attack_cooldown = 0
                                    clicked_enemy = True
                                break
                    
                    # If not clicking on interactive object, move player
                    if not clicked_tree and not clicked_enemy:
                        self.player.move_to(mouse_x, mouse_y)
                        self.player.attacking_enemy = None
    
    def update(self):
        """Update game state"""
        self.player.update()
        
        for tree in self.trees:
            tree.update()
        
        for enemy in self.enemies:
            enemy.update()
    
    def draw(self):
        """Draw game"""
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw trees
        for tree in self.trees:
            tree.draw(self.screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
        # Draw inventory (on top of everything)
        self.player.inventory.draw(self.screen)
        
        pygame.display.flip()
    
    def draw_ui(self):
        """Draw UI elements"""
        font = pygame.font.Font(None, 24)
        y_offset = 10
        
        # Draw skills
        for skill in ['Woodcutting', 'Combat']:
            level, xp = self.player.xp_system.get_skill_info(skill)
            text = font.render(f"{skill}: Lv {level} ({xp} XP)", True, WHITE)
            self.screen.blit(text, (10, y_offset))
            y_offset += 30
        
        # Draw instructions
        inst_font = pygame.font.Font(None, 20)
        instructions = [
            "Click to move",
            "Click trees to chop",
            "Click enemies to attack",
            "Press I for inventory"
        ]
        y_offset = SCREEN_HEIGHT - 90
        for inst in instructions:
            text = inst_font.render(inst, True, WHITE)
            self.screen.blit(text, (10, y_offset))
            y_offset += 22
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
