# AI-Powered Adaptive NPC Behavior System Using Python

## Description
This is a 2D game project where the player can move around, and NPCs patrol and detect the player. The NPC behavior is controlled using a Finite State Machine (FSM), which allows them to patrol, chase, and eventually attack or flee based on conditions. The project is developed using Python and Pygame.

## Features Implemented
- Player movement using WASD keys
- NPC patrolling behavior
- Distance-based player detection
- Collision detection between player and NPC
- Modular code structure with separate modules:
  - `main.py` → Game loop and control
  - `player.py` → Player logic
  - `npc.py` → NPC logic (FSM ready)
  - `settings.py` → Game settings (colors, speed, screen size)

## Requirements
- Python 3.x
- Pygame

## Setup Instructions
1. Install Python 3.x if not already installed: https://www.python.org/downloads/
2. Clone the repository:
   ```bash
   git clone <repository_link>
