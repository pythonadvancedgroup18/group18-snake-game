# Snake — Group 18

## Quickstart (Windows / PowerShell)
REQUIRES PYTHON 3.13 OR GREATER 
1. Clone the repo:
   git clone https://github.com/pythonadvancedgroup18/group18-snake-game.git
   cd group18-snake-game

2. Install pipenv (if not already installed):
   py -m pip install --user pipenv

3. Install dependencies from Pipfile.lock
   py -m pipenv sync --dev

4. Run:
   py -m pipenv run python src/main.py

5. Run tests:
   py -m pipenv run pytest

## Notes
- Game uses high_score.json locally. A sample data/high_score.example.json is included.
- Python version used: 3.13.5
