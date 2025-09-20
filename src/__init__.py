"""
Snake Game - Group 18
A classic Snake game implementation using Pygame.
"""

__version__ = "1.0.0"
__author__ = "Group 18"

# Import main components for easy access
from .main import main, Game, Snake, Food, HighScoreManager

# Define what gets imported with "from src import *"
__all__ = ["main", "Game", "Snake", "Food", "HighScoreManager"]