"""Scripts for running various development tasks."""
import subprocess


def pylint():
    """
    Run pylint linter. Equivalent to:
    `poetry run pylint . --ignore .venv`
    """
    subprocess.run(["pylint", ".", "--ignore", ".venv", "--ignore", "test"], check=True)


def bandit():
    """
    Run bandit security linter. Equivalent to:
    `poetry run bandit -r . --exclude .venv`
    """
    subprocess.run(["bandit", "-r", ".", "--exclude", "./.venv"], check=True)


def unittest():
    """
    Run all unit tests. Equivalent to:
    `poetry run python -u -m unittest discover -v -s ./test -p test_*.py`
    """
    subprocess.run(
        [
            "python",
            "-u",
            "-m",
            "unittest",
            "discover",
            "-v",
            "-s",
            "./test",
            "-p",
            "test_*.py",
        ],
        check=True,
    )


def app():
    """
    Run the application. Equivalent to:
    `poetry run python -u -m app`
    """
    subprocess.run(["python", "-u", "-m", "fastapi", "run"], check=False)
