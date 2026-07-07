""""Tests for shorty shortener module — resolve, list, delete."""

import pathlib

import pytest

from shorty.db import init_db
from shorty.shortener import resolve, list_links, delete_link, shorten


def _setup_db(tmp_path: pathlib.Path) -> str:
    db_path = str(tmp_path / "test.db")
    init_db(db_path)
    return db_path


class TestResolve:
    def test_resolve_returns_link(self, tmp_path: pathlib.Path) -> None:
        db_path = _setup_db(tmp_path)
        created = shorten("https://example.com", db_path)
        found = resolve(created.code, db_path)
        assert found.url == "https://example.com"

    def test_resolve_unknown_raises(self, tmp_path: pathlib.Path) -> None:
        db_path = _setup_db(tmp_path)
        with pytest.raises(ValueError, match="not found"):
            resolve("zzzzzz", db_path)


class TestListLinks:
    def test_list_empty_returns_empty(self, tmp_path: pathlib.Path) -> None:
        db_path = _setup_db(tmp_path)
        assert list_links(db_path) == []

    def test_list_returns_all(self, tmp_path: pathlib.Path) -> None:
        db_path = _setup_db(tmp_path)
        shorten("https://a.example.com", db_path)
        shorten("https://b.example.com", db_path)
        result = list_links(db_path)
        assert len(result) == 2
        urls = {link.url for link in result}
        assert urls == {"https://a.example.com", "https://b.example.com"}


class TestDeleteLink:
    def test_delete_removes_link(self, tmp_path: pathlib.Path) -> None:
        db_path = _setup_db(tmp_path)
        created = shorten("https://example.com", db_path)
        delete_link(created.code, db_path)
        with pytest.raises(ValueError, match="not found"):
            resolve(created.code, db_path)

    def test_delete_unknown_raises(self, tmp_path: pathlib.Path) -> None:
        db_path = _setup_db(tmp_path)
        with pytest.raises(ValueError, match="not found"):
            delete_link("zzzzzz", db_path)
