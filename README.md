# Snake — Group 18

## Quickstart (Windows / PowerShell)
1. Install pipenv (if needed):
   py -m pip install --user pipenv
2. Create environment & install deps:
   py -m pipenv --python 3.13.5
   py -m pipenv install
3. Run:
   py -m pipenv run python src/main.py

## Tests
4. Run tests:
   py -m pipenv run pytest

Snake initial length and starting position Snake movement logic Snake growth when eating food Food spawn logic (not on snake, respawns correctly) Snake reset after game over Collision rules (wall, self, direction restrictions)

All tests are located inside the tests/ folder.

## Notes
- Game uses high_score.json locally. A sample data/high_score.example.json is included.
- Python version used: 3.13.5