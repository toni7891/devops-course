from copy import deepcopy
from pathlib import Path
import sys

import pytest


APP_DIR = Path(__file__).resolve().parents[1] 
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from app import app  # noqa: E402
from models import tasks  # noqa: E402


INITIAL_TASKS = deepcopy(tasks)


@pytest.fixture(autouse=True)
def reset_tasks():
    tasks.clear()
    tasks.extend(deepcopy(INITIAL_TASKS))
    yield
    tasks.clear()
    tasks.extend(deepcopy(INITIAL_TASKS))


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client