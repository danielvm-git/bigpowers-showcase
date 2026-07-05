# shorty — URL Shortener CLI

A command-line URL shortener with local SQLite storage. Shorten URLs, manage links, resolve short codes, and serve redirects locally — all from the terminal.

## Stack

Python 3.13+, SQLite (stdlib), Click (CLI framework), pytest (tests)

## Commands

| Action | Command |
|--------|---------|
| Install deps | `pip install -r requirements.txt` |
| Run CLI | `python -m shorty <command>` |
| Run tests | `pytest -q` |
| Lint | `ruff check .` |
| Typecheck | `mypy shorty/` |
| Format | `ruff format .` |

## Architecture

```
shorty/
  __init__.py
  __main__.py      # entry point
  cli.py           # Click commands
  db.py            # SQLite CRUD
  models.py        # dataclasses
  shortener.py     # short-code generation + URL validation
  server.py        # local redirect HTTP server
tests/
  test_cli.py
  test_db.py
  test_shortener.py
  test_server.py
```

## Conventions

- Functions: 4–20 lines
- Files: under 300 lines
- Types: explicit, no `Any`
- Tests: pytest, F.I.R.S.T
- Format: ruff

## Never

- Never work directly on `main`
- Never push without running tests first
- Never commit secrets or `.env` files
