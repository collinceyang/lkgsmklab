# conftest.py
# PyTest configuration file where you define shared fixtures and hooks.
# A fixture in PyTest is a function that provides setup and teardown functionality for tests.
# •	Fixtures help initialize test data, set up database connections, create API clients, configure browsers, etc.
# •	Fixtures can have different scopes (function, class, module, session).

import pytest
from utils.config import API_BASE_URL

@pytest.fixture(scope="session")
def api_base_url():
    return API_BASE_URL # Returns the API base URL