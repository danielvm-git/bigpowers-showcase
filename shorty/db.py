"""SQLite database operations for shorty."""

import os
import sqlite3
from pathlib import Path


DEFAULT_DB_DIR = Path.home() / ".local" / "share" / "shorty"
DEFAULT_DB_PATH = DEFAULT_DB_DIR / "shorty.db"


def _get_db_path(path: str | None = None) -> str:
    """Return the database path, creating the directory if needed."""
    if path is not None:
        return path
    DEFAULT_DB_DIR.mkdir(parents=True, exist_ok=True)
    return str(DEFAULT_DB_PATH)


def init_db(path: str | None = None) -> str:
    """Initialize the SQLite database with the links table. Returns the db path."""
    db_path = _get_db_path(path)
    if db_path != ":memory:":
        os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS links (
                code TEXT PRIMARY KEY,
                url TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                hits INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        conn.commit()
    return db_path


def get_connection(path: str | None = None) -> sqlite3.Connection:
    """Return a connection to the database."""
    db_path = _get_db_path(path)
    return sqlite3.connect(db_path)
