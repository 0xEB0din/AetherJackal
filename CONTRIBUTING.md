# Contributing to AetherJackal

Thanks for your interest in contributing. This document explains how to get involved.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/<your-username>/AetherJackal.git`
3. Install dependencies: `./scripts/migrate.sh setup`
4. Create a feature branch: `git checkout -b feature/my-feature`

## Development Setup

```bash
# Backend (Flask on port 5000)
cd backend
pip install -r requirements.txt
flask run

# Frontend (React on port 3000)
cd frontend
npm install
npm start

# Or run both at once
./scripts/migrate.sh dev
```

Copy `.env.example` to `.env` and adjust values as needed.

## Code Style

**Python (backend):**
- Follow PEP 8
- Run `pylint app.py routes/ services/ models/` before committing
- Use type hints where they add clarity

**JavaScript (frontend):**
- Run `npm run lint` before committing
- Use functional components and hooks (no class components)

## Running Tests

```bash
# Backend
cd backend && python -m pytest tests/ -v --cov=.

# Frontend
cd frontend && npm test -- --watchAll=false

# Or both
./scripts/migrate.sh test
```

All tests must pass before submitting a PR.

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org):

- `feat: add resource tagging` — new feature
- `fix: correct cost calculation rounding` — bug fix
- `docs: update API reference` — documentation only
- `test: add migration rollback tests` — test changes
- `refactor: extract pricing logic` — code restructuring
- `chore: update dependencies` — maintenance

## Pull Requests

1. Keep PRs focused — one feature or fix per PR
2. Fill out the PR template
3. Ensure all CI checks pass
4. Update documentation if your change affects the API or user-facing behavior

## Reporting Bugs

Use the [bug report template](https://github.com/0xEB0din/AetherJackal/issues/new?template=bug_report.md). Include steps to reproduce, expected vs. actual behavior, and your environment details.

## Suggesting Features

Use the [feature request template](https://github.com/0xEB0din/AetherJackal/issues/new?template=feature_request.md). Describe the problem, proposed solution, and any alternatives you considered.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
