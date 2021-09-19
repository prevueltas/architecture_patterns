# Python Architecture

This repo contains my TDD and DDD practice following the exercises of the book
[Architecture Patterns with Python](https://www.cosmicpython.com/).

## Running the tests
It uses pytest, you can run it as a python module to include the CWD in sys.path:

```bash
python -m pytest -v
```

## Coverage reports

Install pytest-cov

```bash
pipenv install pytest-cov
```

Get the coverage report in the terminal:

```bash
python -m pytest -v --cov tests
```

Get the coverage report in html format:

```bash
python -m pytest -v --cov model --cov-report html
```

It creates a folder with name _htmlcov_ with the statics.
