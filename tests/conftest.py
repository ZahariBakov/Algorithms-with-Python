import importlib.util
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def load_module(folder, filename):
    """Load an exercise file by its path.

    The file names start with a digit and have spaces and apostrophes,
    so a normal import does not work.
    """
    path = ROOT / folder / filename
    module_name = re.sub(r'\W', '_', f'{folder}_{filename}')

    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


@pytest.fixture(scope='session')
def load():
    cache = {}

    def loader(folder, filename):
        key = (folder, filename)
        if key not in cache:
            cache[key] = load_module(folder, filename)
        return cache[key]

    return loader


@pytest.fixture(autouse=True)
def no_input(monkeypatch):
    def fail(*args, **kwargs):
        raise AssertionError('input() must not be called in a test')

    monkeypatch.setattr('builtins.input', fail)
