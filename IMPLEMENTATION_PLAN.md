# The Land RPG: Cleanup & MVP Implementation Plan

## Overview

This plan transforms The Land RPG from a 397-line monolithic [game.py](game.py) into a well-organized, maintainable MVP with basic sprite support. The game currently works but needs code organization and visual improvements.

**Goals:**
1. Reorganize codebase into modular structure
2. Add basic sprites/icons to replace colored squares
3. Improve code quality (type hints, constants extraction, better architecture)
4. Maintain 100% feature compatibility
5. Ensure all tests pass

**Estimated Time:** 4-5 hours

---

## Current State

**Working Game** - Fully functional top-down RPG with:
- Point-and-click movement
- Woodcutting skill (chop trees for logs + XP)
- Combat system (auto-attack enemies)
- Inventory system (toggle with 'I' key)
- XP/leveling for 2 skills

**Code Structure:**
- Single file: [game.py](game.py) (397 lines)
- Classes: XPSystem, Inventory, Player, Tree, Enemy, Game
- Tests: [test_game.py](test_game.py) validates core mechanics
- Graphics: Colored squares (green player, brown trees, red enemies)

**Issues:**
- All code in one file (hard to maintain)
- Magic numbers scattered throughout
- No type hints
- No sprite support
- UI rendering mixed with game logic

---

## Target Architecture

### New Directory Structure

```
the-land-rpg/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Main game controller & entry point
│   ├── config.py               # All constants & configuration
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── base.py             # Entity base class (DRY)
│   │   ├── player.py           # Player class
│   │   ├── tree.py             # Tree class
│   │   └── enemy.py            # Enemy class
│   ├── systems/
│   │   ├── __init__.py
│   │   ├── xp_system.py        # XP & leveling
│   │   └── inventory.py        # Item storage
│   └── ui/
│       ├── __init__.py
│       ├── hud.py              # Skills & instructions display
│       └── inventory_ui.py     # Inventory panel rendering
├── assets/
│   ├── sprites/
│   │   ├── player.png          # 30x30 sprite
│   │   ├── tree_active.png     # 40x40 active tree
│   │   ├── tree_chopped.png    # 40x40 stump
│   │   └── enemy.png           # 35x35 enemy
│   └── README.md               # Asset attribution
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── test_xp_system.py       # XP tests
│   ├── test_inventory.py       # Inventory tests
│   ├── test_entities.py        # Entity tests
│   └── test_integration.py     # Full game tests
├── game_legacy.py              # Original game.py (backup)
├── test_game_legacy.py         # Original tests (backup)
├── run_game.py                 # New entry point
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Implementation Phases

### Phase 1: Setup & Configuration (15 min)

**1.1 Create Directory Structure**
```bash
mkdir -p src/entities src/systems src/ui tests assets/sprites
touch src/__init__.py src/entities/__init__.py src/systems/__init__.py src/ui/__init__.py tests/__init__.py
```

**1.2 Create src/config.py** - Extract all constants from game.py

Extract:
- Screen settings (SCREEN_WIDTH, SCREEN_HEIGHT, FPS)
- Colors class (BLACK, WHITE, GREEN, BROWN, RED, GRAY, LIGHT_GRAY)
- GameBalance class:
  - Player: size=30, speed=3, attack damage=10, attack delay=60 frames
  - Tree: size=40, respawn=300 frames, XP per log=25
  - Enemy: size=35, max HP=100, respawn=600 frames, XP per kill=50
  - XP: 100 XP per level
  - UI: inventory panel 400x400, HP bar height=5
- AssetPaths class: paths to sprite files

**Critical:** This eliminates magic numbers from lines 11-23 and scattered throughout methods.

---

### Phase 2: Core Systems (20 min)

**2.1 Create src/systems/xp_system.py**

Refactor XPSystem from game.py:26-49:
- Add type hints: `Dict[str, Dict[str, int]]` for skills
- Return type `bool` for `add_xp()` (True if leveled up)
- Return type `Tuple[int, int]` for `get_skill_info()`
- Extract level calculation to static method `_calculate_level()`

**2.2 Create src/systems/inventory.py**

Refactor Inventory from game.py:52-68:
- Move rendering logic to separate UI module
- Add utility methods: `remove_item()`, `has_item()`
- Type hints: `Dict[str, int]` for items
- Keep only data logic (no pygame/rendering code)

---

### Phase 3: Entity Base & Refactoring (45 min)

**3.1 Create src/entities/base.py**

Abstract base class to eliminate code duplication:
- Constructor: `__init__(x, y, size)`
- Shared method: `get_rect()` → `pygame.Rect` (centered on x,y)
- Sprite loading: `load_sprite(path, fallback_color)` with graceful degradation
- Abstract methods: `update()`, `draw(screen)`

**3.2 Create src/entities/player.py**

Refactor Player from game.py:103-158:
- Inherit from Entity base class
- Split `update()` into `_update_movement()` and `_update_combat()`
- Add methods: `start_attack(enemy)`, `stop_attack()`
- Load sprite with fallback to green square
- Type hints: `Optional[Enemy]` for attacking_enemy
- Import config constants instead of hardcoding

**3.3 Create src/entities/tree.py**

Refactor Tree from game.py:160-198:
- Inherit from Entity
- Load two sprites: `tree_active.png` and `tree_chopped.png`
- `chop(player)` returns `bool` (success/failure)
- Draw appropriate sprite based on active state
- Use config constants for respawn time, XP values

**3.4 Create src/entities/enemy.py**

Refactor Enemy from game.py:200-250:
- Inherit from Entity
- Extract HP bar rendering to `_draw_hp_bar(screen)` private method
- `take_damage(damage)` returns `bool` (True if defeated)
- Load enemy sprite with fallback to red square
- Use config constants for HP, respawn, damage

---

### Phase 4: UI Modules (20 min)

**4.1 Create src/ui/inventory_ui.py**

Extract from game.py:69-101:
- Pure function: `draw_inventory(screen, inventory)`
- No class, just rendering logic
- Use constants from config
- Use `TYPE_CHECKING` guard to avoid circular imports

**4.2 Create src/ui/hud.py**

Extract from game.py:356-380:
- Pure function: `draw_hud(screen, xp_system)`
- Renders skill levels and instructions
- Easy to modify layout later

---

### Phase 5: Main Game Controller (30 min)

**5.1 Create src/main.py**

Refactor Game class from game.py:252-396:
- Import all entity, system, and UI modules
- Split `handle_events()` into:
  - `_handle_keypress(key)`
  - `_handle_left_click(pos)`
  - `_try_chop_tree(x, y)` → returns bool
  - `_try_attack_enemy(x, y)` → returns bool
- Use new `draw_hud()` and `draw_inventory()` functions
- Use `player.start_attack()` / `stop_attack()` methods
- Keep `update()` and `draw()` simple and clean

**5.2 Create Entry Point**

Create run_game.py:
```python
from src.main import main

if __name__ == "__main__":
    main()
```

---

### Phase 6: Asset Integration (1-2 hours)

**6.1 Find/Create Sprites**

Get basic sprites from:
- **Kenney.nl** (recommended - free CC0 assets)
- **OpenGameArt.org** - community assets
- **itch.io** - game asset packs
- **Create simple ones** with Piskel.app or GIMP

Required sprites (PNG with transparency):
- `player.png` - 30x30 (or larger, scaled in code)
- `tree_active.png` - 40x40 leafy tree
- `tree_chopped.png` - 40x40 stump
- `enemy.png` - 35x35 hostile creature

**6.2 Create assets/README.md**

Document sprite sources and licenses:
```markdown
# The Land RPG - Assets

All sprites licensed under CC0 or equivalent.

## Sprites
- player.png: [Source/Creator]
- tree_active.png: [Source/Creator]
- tree_chopped.png: [Source/Creator]
- enemy.png: [Source/Creator]
```

**6.3 Test Graceful Fallback**

Verify game works:
- With all sprites present
- With sprites missing (falls back to colored squares)

---

### Phase 7: Testing (1 hour)

**7.1 Create tests/conftest.py**

Shared pytest fixtures:
```python
import os
import pytest
os.environ['SDL_VIDEODRIVER'] = 'dummy'
import pygame

@pytest.fixture(scope="session", autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()
```

**7.2 Create Unit Tests**

- tests/test_xp_system.py: Test XP gain, levelups, multiple skills
- tests/test_inventory.py: Test add/remove items, stacking, has_item
- tests/test_entities.py: Test player movement, tree chopping, enemy combat

**7.3 Create tests/test_integration.py**

Test complete game flow:
- Game initialization
- Movement → Chop tree → Attack enemy
- Verify XP gains, inventory updates

**7.4 Update requirements.txt**

Add testing dependencies:
```
pygame>=2.5.0
pytest>=7.4.0
pytest-cov>=4.1.0
```

**7.5 Run Tests**

```bash
pytest tests/ -v
pytest --cov=src tests/  # With coverage report
```

Target: >80% code coverage

---

### Phase 8: Documentation & Cleanup (20 min)

**8.1 Update README.md**

Update sections:
- Installation: Add `pytest` to dependencies
- How to Play: Update to use `python run_game.py`
- Development: Add section on running tests
- Project Structure: Document new modular layout

**8.2 Deprecate Legacy Files**

```bash
# Rename old files for reference
mv game.py game_legacy.py
mv test_game.py test_game_legacy.py
```

Add note at top of legacy files:
```python
# DEPRECATED: This file is kept for reference only.
# Use the new modular structure in src/ instead.
```

**8.3 Update .gitignore**

Ensure `__pycache__`, `*.pyc`, `.pytest_cache` are ignored (already present in current .gitignore)

---

## Implementation Order Checklist

Execute in this exact order:

1. ☐ Create directory structure
2. ☐ Create src/config.py
3. ☐ Create src/entities/base.py
4. ☐ Create src/systems/xp_system.py
5. ☐ Create src/systems/inventory.py
6. ☐ Create src/entities/player.py
7. ☐ Create src/entities/tree.py
8. ☐ Create src/entities/enemy.py
9. ☐ Create src/ui/hud.py
10. ☐ Create src/ui/inventory_ui.py
11. ☐ Create src/main.py
12. ☐ Create run_game.py
13. ☐ Test game runs: `python run_game.py`
14. ☐ Find/create sprites for assets/sprites/
15. ☐ Create assets/README.md
16. ☐ Create tests/conftest.py
17. ☐ Create tests/test_xp_system.py
18. ☐ Create tests/test_inventory.py
19. ☐ Create tests/test_entities.py
20. ☐ Create tests/test_integration.py
21. ☐ Run tests: `pytest tests/ -v`
22. ☐ Update README.md
23. ☐ Rename legacy files
24. ☐ Final verification: game runs, tests pass

---

## Critical Files

These files are most important for the refactoring:

1. **src/config.py** - Foundation; centralizes all constants
2. **src/entities/base.py** - DRY principle; prevents duplication
3. **src/entities/player.py** - Core gameplay entity
4. **src/main.py** - Orchestrates all systems
5. **tests/test_integration.py** - Validates no regression

---

## Key Architecture Decisions

**1. Entity Base Class**
- Eliminates duplicate `get_rect()` across Player/Tree/Enemy
- Provides consistent sprite loading with fallback
- Abstract methods enforce consistent interface

**2. Separation of UI from Logic**
- Inventory class: data only (no rendering)
- inventory_ui.py: rendering only (pure function)
- Benefits: easier testing, swappable UI styles

**3. Configuration Centralization**
- All magic numbers in config.py
- Easy balance adjustments
- Clear documentation of game values

**4. Type Hints Throughout**
- Improves IDE autocomplete
- Catches bugs at development time
- Self-documenting function signatures

**5. Graceful Sprite Degradation**
- Game works with or without sprites
- Falls back to colored squares if PNG missing
- Allows phased asset integration

---

## Verification Plan

After implementation, verify:

### Functional Testing
- ☐ Game launches without errors
- ☐ Player moves on click
- ☐ Trees can be chopped (logs added, XP gained)
- ☐ Trees respawn after 5 seconds
- ☐ Enemies can be attacked
- ☐ Auto-attack works (1 second delay)
- ☐ Enemies respawn after 10 seconds
- ☐ Inventory toggles with 'I' key
- ☐ Skills display XP and levels correctly
- ☐ Sprites load (or fall back to colored squares)

### Code Quality
- ☐ No file exceeds 200 lines
- ☐ All functions have type hints
- ☐ No magic numbers in code (all in config)
- ☐ Docstrings on all classes and public methods

### Testing
- ☐ All tests pass: `pytest tests/`
- ☐ Code coverage >80%: `pytest --cov=src tests/`
- ☐ Legacy tests still pass on old code

### Documentation
- ☐ README reflects new structure
- ☐ Asset sources documented
- ☐ Clear instructions for running game and tests

---

## Success Criteria

Implementation is complete when:

1. ✓ Game runs identically to original (no feature regression)
2. ✓ Code is organized into logical modules (src/entities, src/systems, src/ui)
3. ✓ Basic sprites replace colored squares (with fallback)
4. ✓ All tests pass with >80% coverage
5. ✓ No magic numbers (all in config.py)
6. ✓ Type hints on all functions
7. ✓ Documentation is accurate and up-to-date
8. ✓ New developer can understand structure in <15 minutes

---

## Out of Scope (Post-MVP)

These features are intentionally excluded but documented for future:

- Save/load system
- Additional skills (Fishing, Mining, Crafting)
- Quest system
- Sound effects and music
- Multiple enemy types
- Equipment system (weapons, armor)
- Multiplayer

---

## Estimated Timeline

| Phase | Time |
|-------|------|
| Setup & Config | 15 min |
| Core Systems | 20 min |
| Entity Refactoring | 45 min |
| UI Modules | 20 min |
| Main Controller | 30 min |
| Asset Integration | 1-2 hours |
| Testing | 1 hour |
| Documentation | 20 min |
| **Total** | **4-5 hours** |

---

## Risk Mitigation

**Risk: Breaking existing functionality**
- Mitigation: Keep game.py as game_legacy.py for reference
- Test frequently during refactoring
- Run legacy tests to verify behavior matches

**Risk: Circular import dependencies**
- Mitigation: Use TYPE_CHECKING guard for type hints
- Keep dependencies unidirectional (entities → systems)

**Risk: Sprite loading failures**
- Mitigation: Graceful fallback to colored squares built-in
- Test with missing sprite files

**Risk: Tests breaking during refactor**
- Mitigation: Create new tests for new structure
- Keep legacy tests for comparison
- Use pytest fixtures to share setup code
