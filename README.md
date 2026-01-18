# The Land RPG

A top-down RPG adventure game set in 'The Land' with skilling and combat, built in Python with Pygame.

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

1. Install Python 3.12 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Play

Run the game with:
```bash
python game.py
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
