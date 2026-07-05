""""Tests for shorty database module."""

import pathlib
import sqlite3

import pytest

from shorty.db import init_db, get_connection


def test_init_db_creates_table(tmp_path: pathlib.Path) -> None:
    """init_db should create the links table in a fresh database."""
    db_path = str(tmp_path / "test.db")
    result = init_db(db_path)
    assert result == db_path

    conn = sqlite3.connect(db_path)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='links'")
    assert cursor.fetchone() is not None


def test_init_db_returns_path() -> None:
    """init_db should return the db path it was given."""
    assert init_db(":memory:") == ":memory:"


def test_get_connection_returns_connection() -> None:
    """get_connection should return a working sqlite3.Connection."""
    conn = get_connection(":memory:")
    assert isinstance(conn, sqlite3.Connection)
    conn.close()


def test_init_db_idempotent() -> None:
    """Calling init_db twice on the same db should not error."""
    db_path = ":memory:"
    init_db(db_path)
    init_db(db_path)  # should not raise


def test_init_db_file_path(tmp_path: pathlib.Path) -> None:
    """init_db with a file path should create the database file."""
    db_file = tmp_path / "test.db"
    result = init_db(str(db_file))
    assert result == str(db_file)
    assert db_file.exists()
