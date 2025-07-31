import subprocess

def test():
    """
    Run all unittests. Equivalent to:
    `poetry run python -u -m unittest discover -v -s ./test -p test_*.py`
    """
    subprocess.run(
        ['python', '-u', '-m', 'unittest', 'discover', '-v', '-s', './test', '-p', 'test_*.py']
    )
