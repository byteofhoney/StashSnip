# Contributing to StashSnip

Thanks for your interest in contributing to StashSnip! Whether it's fixing a bug, adding a feature, improving docs or just cleaning up code, contributions are welcome.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Branch Naming](#branch-naming)
- [Commit Messages](#commit-messages)
- [Running Tests](#running-tests)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Style Guidelines](#style-guidelines)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

## Code of Conduct

This project follows a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold it. Please read it before contributing.

## Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/byteofhoney/StashSnip.git
   cd StashSnip
   ```
3. Set up your development environment (see below).
4. Look through the [Issues](../../issues) tab; issues labeled `good first issue` are a great place to start.
5. If you want to work on something that doesn't already have an issue, **open one first** and describe what you would like to do. This avoids duplicate work and lets us discuss the approach before you invest time in it.

## How to Contribute

You can contribute in several ways:

- Fix a bug
- Add a new feature
- Improve documentation (README, docstrings, comments)
- Add or improve tests
- Improve UI/UX or styling
- Refactor existing code for clarity or performance

## Development Setup

```bash
# Create a virtual environment
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your own MongoDB Atlas URI and a secret key

# Run the app
python run.py
```

Visit `http://127.0.0.1:5000` to confirm it's running.

You'll need a free [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) cluster for local development, the free tier is enough.

## Branch Naming

Create a new branch off `main` for your work:

```bash
git checkout -b feature/short-description
git checkout -b fix/short-description
git checkout -b docs/short-description
```

Examples: `feature/export-to-json`, `fix/search-case-sensitivity`, `docs/update-setup-guide`.

## Commit Messages

Keep commit messages short, present tense and descriptive:

```
Add tag filter to search route
Fix delete modal not closing on cancel
Update README with deployment instructions
```

Avoid vague messages like `fix stuff` or `update`.

## Running Tests

StashSnip uses `pytest`. Before submitting a PR, make sure existing tests pass and add new tests for any new functionality:

```bash
pytest
```

If you're adding a new route or feature, please include at least a basic test covering it (see the `tests/` folder for examples of the existing style).

## Submitting a Pull Request

1. Make sure your branch is up to date with `main`:
   ```bash
   git fetch origin
   git rebase origin/main
   ```
2. Push your branch and open a PR against `main`.
3. In your PR description, include:
   - What the change does and why
   - Related issue number (e.g. `Closes #12`)
   - Screenshots, if it's a UI change
4. Make sure `pytest` passes and there are no obvious linting issues.
5. Be responsive to review feedback; small back-and-forth is normal and expected.

PRs that are large, unscoped or don't match a discussed issue may take longer to review or be asked to be split up. When in doubt, open an issue first to discuss the approach.

## Style Guidelines

- Follow existing patterns in the codebase (Flask app factory + Blueprints structure).
- Keep functions small and focused; prefer readability over cleverness.
- Use descriptive variable and function names.
- Match the existing HTML/CSS/JS style in the frontend.
- Comment non-obvious logic, especially around MongoDB queries.

## Reporting Bugs

Open an issue using the **Bug Report** template. Include:

- Steps to reproduce
- Expected vs actual behavior
- Environment (OS, Python version, browser if UI related)
- Screenshots or error logs if applicable

## Suggesting Features

Open an issue using the **Feature Request** template. Describe the problem you are trying to solve, not just the solution.

---

Thanks again for taking the time to contribute, every bit helps even a typo fix. 
