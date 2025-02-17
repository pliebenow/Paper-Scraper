import pytest
import logging

@pytest.fixture(autouse=True)
def setup_logging():
    """Configure logging for tests"""
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)