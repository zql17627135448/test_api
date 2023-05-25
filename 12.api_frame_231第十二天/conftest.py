from pathlib import Path

import pytest

from commons.yaml_util import clear_extract_yaml

@pytest.fixture(scope="session",autouse=True)
def auto_clear_extract_yaml():
    clear_extract_yaml()
