# story: e43s01

# Conventions

## Conventional Commits

All commits follow Conventional Commits 1.0.0: `<type>(<scope>): <description>`

- `feat`: Minor bump
- `fix`: Patch bump
- `perf`: Patch bump  
- `docs`, `chore`, `style`, `refactor`, `test`: No bump
- `BREAKING CHANGE:` or `!`: Major bump

## Git & GitHub

- No direct work on `main`
- Feature branches via `kickoff-branch`
- Use `gh` CLI for repo operations
- Conventional Commits for all messages
- No `Co-authored-by` footers

## Code Style

- Functions: 4–20 lines
- Files: under 300 lines
- One thing per function (SRP)
- Explicit types, no `Any`
- Early returns over nested ifs (max 2 levels)
- No magic strings — extract to named constants
- No commented-out code — delete it
- Inject dependencies through constructor/parameter

## Tests (F.I.R.S.T)

- Fast, Independent, Repeatable, Self-Validating, Timely
- Every new function gets a test
- Every bug fix gets a regression test
- Mocks for external I/O only
- Never skip/@ignore a test without documented reason

## Dependencies

- Inject through constructor/parameter
- Wrap third-party libs behind project-owned interface

## Formatting

- `ruff format .` (default settings)
- Configured in pre-commit

## specs/ — All Planning Output Goes Here

- `specs/state.yaml` — session state
- `specs/release-plan.yaml` — release index
- `specs/execution-status.yaml` — story status
- `specs/product/SCOPE_LATEST.yaml` — what the product does
- `specs/product/VISION_LATEST.yaml` — north star
- `specs/product/GLOSSARY_LATEST.yaml` — domain terms
- `specs/epics/` — epic capsules
- `specs/tech-architecture/` — stack, plans, ADRs
- `specs/bugs/` — bug investigation trails
- `specs/verifications/` — UAT records, audit reports
- `specs/metrics/` — cycle-time metrics

## Defensive Code

- Retry with backoff (API/network calls)
- Timeout (long-running operations)
- Graceful degradation (external service failures)
