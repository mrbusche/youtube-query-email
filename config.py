import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# YouTube API Configuration
API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_USERNAME = os.getenv("YOUTUBE_USERNAME")

# Email Configuration
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Convert comma-separated emails to list
RECIPIENT_EMAILS = os.getenv("RECIPIENT_EMAILS", "").split(",")

# Search Configuration
SEARCH_TERMS = os.getenv("SEARCH_TERMS", "AI agents").split(",")

# Search Parameters
MAX_RESULTS = 5
SORT_ORDER = "viewCount"
DAYS_BACK = 7

print("Loaded configuration:")
print(f"MAX_RESULTS: {MAX_RESULTS}")
print(f"DAYS_BACK: {DAYS_BACK}")
print(f"SORT_ORDER: {SORT_ORDER}")
print(f"SEARCH_TERMS: {SEARCH_TERMS}")
print(f"RECIPIENT_EMAILS: {RECIPIENT_EMAILS}")

# Validate required environment variables
required_vars = ["YOUTUBE_API_KEY", "SENDER_EMAIL"]
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
