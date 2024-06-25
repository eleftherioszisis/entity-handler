import json
import pytest
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"



@pytest.fixture(scope="session")
def cell_composition_config_distribution_file():
    return DATA_DIR / "cell_composition_config_distribution.json"


@pytest.fixture(scope="session")
def cell_composition_config_distribution_dict(cell_composition_config_distribution_file):
    return json.loads(Path(cell_composition_config_distribution_file).read_bytes())


