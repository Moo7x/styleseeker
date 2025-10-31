# backend/app/core/config.py

from pathlib import Path

# Define the root directory of the project.
# Path(__file__) is the path to the current file (config.py)
# .parent gives us the directory containing it (core/)
# .parent again gives us the directory containing that (app/)
# .parent again gives us the backend/ directory
# .parent again gives us the root 'styleseeker' directory
ROOT_DIR = Path(__file__).parent.parent.parent.parent

DATA_DIR = ROOT_DIR / "data"
IMAGE_DIR = DATA_DIR / "images"

# We can add more settings here later
