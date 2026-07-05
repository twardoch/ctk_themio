# this_file: tests/test_preferences.py
"""Headless tests for the SQLite preference store.

Each test drives a throwaway database in a ``tmp_path`` so nothing leaks into
the user's real data directory. The module caches "does the DB exist?" in a
global, so we clear it between tests.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from ctk_themio.model import preferences as pref


@pytest.fixture
def db_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    # Reset the module-level existence cache so each test starts clean.
    monkeypatch.setattr(pref, "db_file_found", None, raising=False)
    return tmp_path / "prefs.db"


def test_all_widget_categories_sorted() -> None:
    result = pref.all_widget_categories({"Button": {}, "Almanac": {}, "Canvas": {}})
    assert result == ["Almanac", "Button", "Canvas"]


def test_init_db_creates_tables(db_path: Path) -> None:
    pref.init_db(db_path)
    assert db_path.exists()

    import sqlite3

    conn = sqlite3.connect(db_path)
    tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    conn.close()
    assert {"preferences", "application_control"} <= tables


def test_db_file_exists_initialises_when_missing(db_path: Path) -> None:
    assert not db_path.exists()
    assert pref.db_file_exists(db_path) is True
    assert db_path.exists()


def test_preference_roundtrip(db_path: Path) -> None:
    pref.init_db(db_path)

    row = pref.new_preference_dict(
        scope="user",
        preference_name="theme",
        data_type="str",
        preference_value="Cobalt",
    )
    pref.upsert_preference(db_path, row)

    got = pref.preference_setting(scope="user", preference_name="theme", db_file_path=db_path)
    assert got == "Cobalt"


def test_preference_typed_int(db_path: Path) -> None:
    pref.init_db(db_path)
    pref.upsert_preference(
        db_path,
        pref.new_preference_dict("geometry", "width", "int", 640),
    )
    got = pref.preference_setting(scope="geometry", preference_name="width", db_file_path=db_path)
    assert got == 640
    assert isinstance(got, int)


def test_preference_missing_returns_default(db_path: Path) -> None:
    pref.init_db(db_path)
    got = pref.preference_setting(
        scope="user",
        preference_name="does_not_exist",
        db_file_path=db_path,
        default="fallback",
    )
    assert got == "fallback"


def test_delete_preference(db_path: Path) -> None:
    pref.init_db(db_path)
    pref.upsert_preference(
        db_path,
        pref.new_preference_dict("user", "temp", "str", "value"),
    )
    pref.delete_preference(db_path, "user", "temp")
    got = pref.preference_setting(scope="user", preference_name="temp", db_file_path=db_path)
    assert got == "NO_DATA_FOUND"
