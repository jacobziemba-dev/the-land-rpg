# The Land RPG

A top-down RPG adventure game set in 'The Land' with skilling and combat, built in Python with Pygame.

## Screenshots

### Gameplay
![The Land RPG Gameplay](https://github.com/user-attachments/assets/6ae9e690-ca19-428c-944c-4894373f8c10)

### Inventory System
![Inventory UI](https://github.com/user-attachments/assets/d8401a5f-e9ae-483b-b4dd-09964e95df4c)

## Features

- **Point-and-click movement**: Click anywhere to move your character
- **Woodcutting skill**: Click on trees to gather logs and gain Woodcutting XP
- **Combat system**: Click on enemies to initiate auto-attacks and gain Combat XP
- **Inventory system**: Press 'I' to toggle your inventory
- **XP and Leveling**: Track your progress in Woodcutting and Combat skills
- **Simple graphics**: Colored squares representing game entities
  - Green: Player character
  - Brown: Trees
  - Red: Enemies

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or using a virtual environment (recommended):
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
# or
source .venv/bin/activate  # On macOS/Linux

pip install -r requirements.txt
```

## How to Play

Run the game with:
```bash
python run_game.py
```

Or with the virtual environment:
```bash
.venv\Scripts\python run_game.py  # On Windows
# or
.venv/bin/python run_game.py  # On macOS/Linux
```

### Controls

- **Left Click**: Move to location, chop trees, or attack enemies
- **I Key**: Toggle inventory

### Gameplay

1. **Movement**: Click anywhere on the screen to move your character
2. **Woodcutting**: Click on brown trees to chop them and collect logs. Trees respawn after 5 seconds.
3. **Combat**: Click on red enemies to start attacking them. Auto-attacks occur every second.
4. **Inventory**: Press 'I' to view your collected items
5. **Skills**: Watch your Woodcutting and Combat levels increase as you gain XP

## Game Mechanics

- **Woodcutting**: Gain 25 XP per log chopped
- **Combat**: Gain 50 XP per enemy defeated
- **Leveling**: Every 100 XP grants 1 level
- **Auto-combat**: Once you click an enemy, attacks continue automatically
- **Enemy HP**: Enemies have 100 HP and take 10 damage per hit
- **Respawning**: Trees respawn after 5 seconds, enemies after 10 seconds

## Project Structure

The game has been refactored into a clean, modular architecture:

```
the-land-rpg/
├── src/                        # Main source code
│   ├── config.py               # All game constants and configuration
│   ├── main.py                 # Main game controller & entry point
│   ├── entities/               # Game entities (Player, Tree, Enemy)
│   │   ├── base.py             # Abstract Entity base class
│   │   ├── player.py           # Player character
│   │   ├── tree.py             # Harvestable trees
│   │   └── enemy.py            # Hostile enemies
│   ├── systems/                # Game systems
│   │   ├── xp_system.py        # XP and leveling system
│   │   └── inventory.py        # Item storage system
│   └── ui/                     # UI rendering
│       ├── hud.py              # Skills & instructions display
│       └── inventory_ui.py     # Inventory panel rendering
├── assets/                     # Game assets
│   ├── sprites/                # Sprite images (PNG)
│   │   ├── player.png          # Player sprite
│   │   ├── tree_active.png     # Active tree sprite
│   │   ├── tree_chopped.png    # Chopped tree/stump sprite
│   │   └── enemy.png           # Enemy sprite
│   └── README.md               # Asset attribution and sources
├── scripts/                    # Helper scripts
│   └── create_sprites.py       # Regenerate placeholder sprites
├── tests/                      # Test suite (for future implementation)
├── run_game.py                 # Game entry point (run this!)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

### Key Architecture Features:

- **Modular Design**: Code organized into logical modules (entities, systems, UI)
- **DRY Principle**: Entity base class eliminates code duplication
- **Separation of Concerns**: UI rendering separated from game logic
- **Type Hints**: Full type annotations throughout
- **Configuration Centralization**: All constants in `config.py`
- **Sprite Support**: Graceful fallback to colored squares if sprites missing

## Development

### Regenerating Sprites

If sprite files are missing, regenerate them with:

```bash
python scripts/create_sprites.py
```

This creates simple placeholder sprites. You can replace them with better artwork from sources like [Kenney.nl](https://kenney.nl/assets) (see [assets/README.md](assets/README.md) for details).
