import os
from dotenv import load_dotenv

load_dotenv()

TWITTER_URL = "https://x.com/login"
TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")
TWITTER_MAIL = os.getenv("TWITTER_MAIL")
PROXY_URI = os.getenv("PROXY_URI")
