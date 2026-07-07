"""URL shortening logic — code generation + URL validation + persistence."""

import secrets
import string
import sqlite3
from datetime import datetime

from shorty.db import get_connection
from shorty.models import Link

_ALPHABET = string.ascii_lowercase + string.digits
_CODE_LENGTH = 6
_MAX_ATTEMPTS = 10


def _generate_code() -> str:
    """Generate a random URL-safe short code."""
    return "".join(secrets.choice(_ALPHABET) for _ in range(_CODE_LENGTH))


def shorten(url: str, db_path: str | None = None) -> Link:
    """Shorten a URL. Returns existing link if URL already stored, otherwise creates a new one."""
    conn = get_connection(db_path)
    try:
        _validate_url(url)

        existing = conn.execute(
            "SELECT code, url, created_at, hits FROM links WHERE url = ?", (url,)
        ).fetchone()
        if existing is not None:
            return Link(
                code=existing[0],
                url=existing[1],
                created_at=datetime.fromisoformat(existing[2]),
                hits=existing[3],
            )

        for _ in range(_MAX_ATTEMPTS):
            code = _generate_code()
            try:
                conn.execute(
                    "INSERT INTO links (code, url) VALUES (?, ?)", (code, url)
                )
                conn.commit()
                return Link(
                    code=code,
                    url=url,
                    created_at=datetime.now(),
                    hits=0,
                )
            except sqlite3.IntegrityError:
                continue

        raise RuntimeError(f"Failed to generate unique code after {_MAX_ATTEMPTS} attempts")
    finally:
        conn.close()


def resolve(code: str, db_path: str | None = None) -> Link:
    """Resolve a short code to its original URL. Raises ValueError if not found."""
    conn = get_connection(db_path)
    try:
        row = conn.execute(
            "SELECT code, url, created_at, hits FROM links WHERE code = ?", (code,)
        ).fetchone()
        if row is None:
            raise ValueError(f"Short code not found: {code}")
        return Link(
            code=row[0],
            url=row[1],
            created_at=datetime.fromisoformat(row[2]),
            hits=row[3],
        )
    finally:
        conn.close()


def _validate_url(url: str) -> None:
    """Raise ValueError if url is not a valid HTTP/HTTPS URL."""
    if not url.startswith(("http://", "https://")):
        raise ValueError(f"URL must start with http:// or https://, got: {url}")
    if len(url) > 2048:
        raise ValueError(f"URL too long: {len(url)} chars (max 2048)")


def list_links(db_path: str | None = None) -> list[Link]:
    """Return all stored links, ordered by creation date (newest first)."""
    conn = get_connection(db_path)
    try:
        rows = conn.execute(
            "SELECT code, url, created_at, hits FROM links ORDER BY created_at DESC"
        ).fetchall()
        return [
            Link(
                code=r[0],
                url=r[1],
                created_at=datetime.fromisoformat(r[2]),
                hits=r[3],
            )
            for r in rows
        ]
    finally:
        conn.close()


def delete_link(code: str, db_path: str | None = None) -> None:
    """Delete a link by short code. Raises ValueError if not found."""
    conn = get_connection(db_path)
    try:
        cursor = conn.execute("DELETE FROM links WHERE code = ?", (code,))
        conn.commit()
        if cursor.rowcount == 0:
            raise ValueError(f"Short code not found: {code}")
    finally:
        conn.close()
