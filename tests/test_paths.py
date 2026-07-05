# this_file: tests/test_paths.py
"""Sanity tests for the centralized path map.

We confirm the read-only asset roots live inside the package and the writable
roots hang off the platformdirs data directory, so the two never collide.
"""

from __future__ import annotations

from pathlib import Path

from ctk_themio import paths


def test_asset_dirs_are_inside_package() -> None:
    assert paths.ASSETS_DIR.parent == paths.PKG_DIR
    assert paths.CONFIG_DIR.parent == paths.ASSETS_DIR
    assert paths.APP_THEMES_DIR.parent == paths.ASSETS_DIR


def test_db_path_under_user_data() -> None:
    assert paths.DB_FILE_PATH.parent == paths.USER_DATA_DIR
    assert paths.DB_FILE_PATH.name == "ctk_theme_builder.db"


def test_writable_dirs_exist() -> None:
    # paths.py creates these at import time.
    for d in (paths.USER_DATA_DIR, paths.USER_LOG_DIR, paths.PALETTES_DIR, paths.TEMP_DIR):
        assert isinstance(d, Path)
        assert d.exists()


def test_user_and_asset_roots_are_distinct() -> None:
    assert paths.USER_DATA_DIR != paths.PKG_DIR
    assert paths.PKG_DIR not in paths.USER_DATA_DIR.parents
