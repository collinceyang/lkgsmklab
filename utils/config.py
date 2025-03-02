# utils/config.py
# store all the configuration settings for the project
import os
from dotenv import load_dotenv

# Load the correct .env file based on the ENV_TYPE variable
env_type = os.getenv("ENV_TYPE", "dev")  # Default to 'dev' if ENV_TYPE is not set

# Dynamically load the appropriate .env file
if env_type == "dev":
    load_dotenv(".env.dev")
elif env_type == "qa":
    load_dotenv(".env.qa")
elif env_type == "prod":
    load_dotenv(".env.prod")
else:
    raise ValueError("Invalid ENV_TYPE specified")

# Fetch configuration variables from the loaded .env file
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
USERNAME = os.getenv("USERNAME", "default_user")
PASSWORD = os.getenv("PASSWORD", "default_password")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 10))


# # Base URL for the API
# API_BASE_URL = "http://localhost:8000"

# Authentication credentials (for secured APIs)
# USERNAME = "admin"
# PASSWORD = "password123"

# Timeout settings (for API requests)
# REQUEST_TIMEOUT = 10  # In seconds

# Headers (default headers for API requests)
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

API_HEADERS = {
    "X-API-Key": "my_secure_api_key",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

TOKEN_HEADERS = {
    "Authorization": "Bearer valid_oauth_token_example",
    "Content-Type": "application/json",
    "Accept": "application/json"
}