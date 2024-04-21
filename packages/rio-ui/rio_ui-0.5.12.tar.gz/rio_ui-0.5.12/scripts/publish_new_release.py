import subprocess
from pathlib import Path

import requests
import revel

import rio

PROJECT_DIR = Path(__file__).absolute().parent.parent


def main() -> None:
    # Make sure we're on the correct branch
    process = subprocess.run(
        ["git", "branch", "--show-current"], check=True, capture_output=True, text=True
    )
    if process.stdout.strip("\n") != "dev":
        revel.fatal("You must checkout the 'dev' branch")

    # Make sure the version number got bumped
    if rio.__version__ == get_latest_published_version():
        revel.fatal("You forgot to increment the version number")

    # Build the TS code
    subprocess.run(["rye", "run", "build"], check=True)

    # Run the test suite
    if not tests_pass():
        revel.fatal("The test don't pass")

    # Merge dev into main and push
    subprocess.run(["git", "fetch", ".", "dev:main"], check=True)
    subprocess.run(["git", "push", "-u", "origin", "main"], check=True)

    # Publish
    subprocess.run(["rye", "build", "--clean"], check=True)
    subprocess.run(["rye", "publish"], check=True)


def get_latest_published_version() -> str:
    response = requests.get(f"https://pypi.org/pypi/rio-ui/json")
    return response.json()["info"]["version"]


def tests_pass() -> bool:
    return subprocess.run(["rye", "test", "--", "-x"], check=True) == 0


main()
