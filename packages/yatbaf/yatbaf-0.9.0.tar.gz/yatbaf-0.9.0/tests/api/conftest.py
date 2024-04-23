import json as jsonlib
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def api_spec():
    api_json_file = Path(__file__).parent / "data" / "api.json"
    with api_json_file.open("rb") as f:
        return jsonlib.load(f)
