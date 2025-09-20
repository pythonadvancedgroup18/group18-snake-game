# Snake — Group 18

## Quickstart (Windows / PowerShell)
REQUIRES PYTHON 3.13 OR GREATER 
Testing

This project includes automated tests written with pytest to ensure that the Snake game functions correctly.

Running the tests

1. Install pytest (if not already installed):

pip install pytest


2. From the root of the project, run:

pytest

Test Coverage

The tests currently cover:

Snake initial length and starting position
Snake movement logic
Snake growth when eating food
Food spawn logic (not on snake, respawns correctly)
Snake reset after game over
Collision rules (wall, self, direction restrictions)

All tests are located inside the tests/ folder.