# shorty — URL Shortener CLI

A local-first URL shortener. Shorten URLs, manage links, resolve short codes, and serve redirects — all from your terminal, all stored in SQLite on your machine.

*Built with [bigpowers](https://github.com/danielvm-git/bigpowers) — browse the `specs/` directory to see the full spec-driven development trail.*

## Quick Start

```bash
pip install -r requirements.txt
python -m shorty shorten https://example.com/very/long/url
python -m shorty resolve abc123
python -m shorty list
```

## Commands

| Command | Description |
|---------|-------------|
| `shorten <url>` | Create a short code for a URL |
| `resolve <code>` | Get the original URL from a short code |
| `list` | Show all stored links |
| `delete <code>` | Remove a stored link |
| `serve` | Start local redirect server (default :8080) |

## Spec Trail

This repo's `specs/` directory is the real product — a complete bigpowers trail from day one:

- `specs/product/SCOPE_LATEST.yaml` — what shorty does
- `specs/release-plan.yaml` — epics and stories, WSJF-scored
- `specs/state.yaml` — session state and handoff
- `specs/epics/` — epic capsules with tasks and verify commands
- `specs/bugs/` — bug investigation trails

Read the trail commit-by-commit to see spec-driven development in action.
