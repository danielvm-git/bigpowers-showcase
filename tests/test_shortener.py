""""Tests for shorty shortener module."""

import pathlib

import pytest

from shorty.shortener import shorten, _validate_url


def test_shorten_returns_link(tmp_path: pathlib.Path) -> None:
    """shorten should return a Link with a 6-char code."""
    db_path = str(tmp_path / "test.db")
    from shorty.db import init_db

    init_db(db_path)
    link = shorten("https://example.com", db_path)
    assert len(link.code) == 6
    assert link.url == "https://example.com"
    assert link.hits == 0


def test_shorten_idempotent(tmp_path: pathlib.Path) -> None:
    """Shortening the same URL twice should return the same code."""
    db_path = str(tmp_path / "test.db")
    from shorty.db import init_db

    init_db(db_path)
    link1 = shorten("https://example.com", db_path)
    link2 = shorten("https://example.com", db_path)
    assert link1.code == link2.code


def test_shorten_different_urls_different_codes(tmp_path: pathlib.Path) -> None:
    """Different URLs should get different short codes."""
    db_path = str(tmp_path / "test.db")
    from shorty.db import init_db

    init_db(db_path)
    link1 = shorten("https://example.com", db_path)
    link2 = shorten("https://other.example.com", db_path)
    assert link1.code != link2.code


def test_shorten_invalid_url_raises() -> None:
    """shorten should raise ValueError for non-HTTP URLs."""
    with pytest.raises(ValueError, match="http:// or https://"):
        shorten("ftp://files.example.com", ":memory:")


def test_shorten_no_scheme_raises() -> None:
    """shorten should raise ValueError for URLs without scheme."""
    with pytest.raises(ValueError, match="http:// or https://"):
        shorten("example.com", ":memory:")


def test_validate_url_accepts_https() -> None:
    """_validate_url should accept https URLs."""
    _validate_url("https://example.com")  # should not raise


def test_validate_url_accepts_http() -> None:
    """_validate_url should accept http URLs."""
    _validate_url("http://example.com")  # should not raise


def test_validate_url_rejects_no_scheme() -> None:
    """_validate_url should reject URLs without scheme."""
    with pytest.raises(ValueError, match="http:// or https://"):
        _validate_url("example.com/path")
