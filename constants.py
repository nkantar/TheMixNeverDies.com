from os import getenv
from pathlib import Path

from dotenv import load_dotenv


##################################################
# secrets

load_dotenv()  # see .env


##################################################
# configuration

HOMEPAGE_DATES = 7


##################################################
# paths

CURRENT_DIR_PATH = Path.cwd()

INPUT_FILE_PATH = CURRENT_DIR_PATH / "input"

TEMPLATE_DIR_PATH = CURRENT_DIR_PATH / "templates"
INPUT_TEMPLATE_PATH = TEMPLATE_DIR_PATH / "input"
STATIC_DIR_PATH = CURRENT_DIR_PATH / "static"
OUTPUT_DIR_PATH = CURRENT_DIR_PATH / "output"
ARCHIVE_DIR_PATH = OUTPUT_DIR_PATH / "archive"
OUTPUT_STATIC_DIR_PATH = OUTPUT_DIR_PATH / "static"

HOMEPAGE_PATH = OUTPUT_DIR_PATH / "index.html"
ARCHIVE_PATH = ARCHIVE_DIR_PATH / "index.html"
ERROR_404_PATH = OUTPUT_DIR_PATH / "404.html"


##################################################
# template names

HOMEPAGE_TEMPLATE_NAME = "home.html"
ARCHIVE_TEMPLATE_NAME = "archive.html"
PAGE_TEMPLATE_NAME = "page.html"
ERROR_404_TEMPLATE_NAME = "404.html"


##################################################
# Spotify

SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = getenv("SPOTIFY_REDIRECT_URI")

SPOTIFY_ACCESS_TOKEN = getenv("SPOTIFY_ACCESS_TOKEN")
SPOTIFY_REFRESH_TOKEN = getenv("SPOTIFY_REFRESH_TOKEN")

SPOTIFY_SCOPE = "user-library-read"
SPOTIFY_USERNAME = "nkantar"
SPOTIFY_CACHE_PATH = CURRENT_DIR_PATH / f".cache-{SPOTIFY_USERNAME}"
