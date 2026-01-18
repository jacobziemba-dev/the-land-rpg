"""
Screenshot utility for The Land RPG
Takes a screenshot after a few seconds of gameplay
"""
import pygame
import sys
import os

# Set environment for headless mode
os.environ['SDL_VIDEODRIVER'] = 'dummy'

# Import the game module
exec(open('game.py').read())
