# conftest.py
# PyTest configuration file where you define shared fixtures and hooks.
# A fixture in PyTest is a function that provides setup and teardown functionality for tests.
# •	Fixtures help initialize test data, set up database connections, create API clients, configure browsers, etc.
# •	Fixtures can have different scopes (function, class, module, session).
import json
import pytest
from utils.config import API_BASE_URL, USERNAME, PASSWORD, REQUEST_TIMEOUT, DEFAULT_HEADERS, API_HEADERS, TOKEN_HEADERS

# Fixture to load the test data
@pytest.fixture
def set_ror_data():
    with open('data/set_ror_data.json', 'r') as json_file:
        return json.load(json_file)

@pytest.fixture(scope="session")
def api_base_url():
    return API_BASE_URL # Returns the API base URL

@pytest.fixture(scope="session")
def env_username():
    return USERNAME # Returns the API USERNAME

@pytest.fixture(scope="session")
def env_password():
    return PASSWORD # Returns the API PASSWORD

@pytest.fixture(scope="session")
def request_timeout():
    return REQUEST_TIMEOUT # Returns the API

@pytest.fixture(scope="session")
def request_default_headers():
    return DEFAULT_HEADERS # Returns default token auth headers 

@pytest.fixture(scope="session")
def request_api_headers():
    return API_HEADERS # Returns api key auth headers

@pytest.fixture(scope="session")
def request_token_headers():
    return TOKEN_HEADERS # Returns oauth token auth headers