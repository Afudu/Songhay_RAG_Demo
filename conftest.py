# conftest.py — runs before all tests
# Mocks python-decouple so tests don't require a .env file in CI.

import pytest
from unittest.mock import patch


@pytest.fixture(autouse=True)
def mock_config():
    """Provide dummy config values for all tests."""
    with patch("decouple.config",
               side_effect=lambda key, **kwargs: kwargs.get("default", f"mock-{key}")):
        yield
