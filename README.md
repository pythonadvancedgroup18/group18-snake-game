# Snake — Group 18
## Project Summary
This project is our implementation of the classic Snake Game developed as part of the Advanced Python Cohort. The game features a clean dark-themed user interface, responsive controls, and dynamic gameplay where the snake grows longer as it eats food and gradually increases in speed. High scores are tracked locally and displayed on the game screen, with the top 5 scores recorded for replayability. 
The codebase follows best practices with a clear project structure (src/, data/, tests/), dependency management handled through Pipenv (Pipfile + Pipfile.lock), and testing using Pytest.

## Assigned Roles
*Coordinator/Lead:*
1. Uche Ebubechukwu Uche Uduma - branch: uche_ebube_changes/main

*Developers (Core Logic):*
2. Success Oluwafemi Ali
3. Oyedokun Yusuf - oyedokun_yusuf

*QA/CI & Tests:* 
4. Farid Abdurrahman 
5. Ali Garba Muazu - Muazu_test

*Docs/Presenters:* 
6. Richmond Adoki
7. Ike-Onuigbo Gideon Ikechi
8. Muhammad Najibullah Abubakar
9. Mohammed Mustapha Shehu

## Demo Video
link: https://drive.google.com/file/d/1JMHhyiCuv40jp_xRVoq-WvXqMO_SUkaZ/view?usp=drivesdk

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

## Demo Gif

![Snake Game Demo](demo.gif)


## Notes
- Game uses high_score.json locally. A sample data/high_score.example.json is included.
- Python version used: 3.13.5
