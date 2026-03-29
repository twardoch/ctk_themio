# this_file: src/ctk_themio/paths.py
"""Centralized path definitions for CTk Theme Builder.

Bundled (read-only) assets live inside the package directory.
User-writable data (DB, logs, palettes, themes, temp) lives in
OS-appropriate locations via platformdirs.
"""

import shutil
from pathlib import Path

from platformdirs import user_cache_dir, user_data_dir, user_log_dir

APP_NAME = "ctk_themio"
APP_AUTHOR = "twardoch"
APP_ID = "com.twardoch.ctk_themio"

# ---------------------------------------------------------------------------
# Package directory (read-only bundled assets)
# ---------------------------------------------------------------------------
PKG_DIR = Path(__file__).parent
ASSETS_DIR = PKG_DIR / "assets"
CONFIG_DIR = ASSETS_DIR / "config"
ETC_DIR = ASSETS_DIR / "etc"
VIEWS_DIR = ASSETS_DIR / "views"
APP_THEMES_DIR = ASSETS_DIR / "themes"
APP_IMAGES = ASSETS_DIR / "images"
BUNDLED_USER_THEMES_DIR = PKG_DIR / "user_themes"

# ---------------------------------------------------------------------------
# User-writable directories (OS-appropriate via platformdirs)
# ---------------------------------------------------------------------------
USER_DATA_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))
USER_LOG_DIR = Path(user_log_dir(APP_NAME, APP_AUTHOR))
USER_CACHE_DIR = Path(user_cache_dir(APP_NAME, APP_AUTHOR))

# Mapped names (compatible with old code expectations)
APP_DATA_DIR = USER_DATA_DIR
DB_FILE_PATH = USER_DATA_DIR / "ctk_theme_builder.db"
PALETTES_DIR = USER_DATA_DIR / "palettes"
LOG_DIR = USER_LOG_DIR
TEMP_DIR = USER_CACHE_DIR / "tmp"

# ---------------------------------------------------------------------------
# Ensure all writable directories exist
# ---------------------------------------------------------------------------
for _d in (USER_DATA_DIR, USER_LOG_DIR, USER_CACHE_DIR, PALETTES_DIR, LOG_DIR, TEMP_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# First-run: seed user themes from bundled defaults
# ---------------------------------------------------------------------------
_user_themes_dir_default = USER_DATA_DIR / "user_themes"
if not _user_themes_dir_default.exists() and BUNDLED_USER_THEMES_DIR.exists():
    shutil.copytree(BUNDLED_USER_THEMES_DIR, _user_themes_dir_default)
