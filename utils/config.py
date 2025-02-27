# utils/config.py
# store all the configuration settings for the project

# Base URL for the API
API_BASE_URL = "http://localhost:8000"

# Authentication credentials (for secured APIs)
# USERNAME = "admin"
# PASSWORD = "password123"

# Timeout settings (for API requests)
REQUEST_TIMEOUT = 10  # In seconds

# Headers (default headers for API requests)
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}