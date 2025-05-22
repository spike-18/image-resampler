# noxfile.py
import nox_poetry

# Default locations to check/format
locations = "src", "tests", "noxfile.py", "docs/conf.py"


@nox_poetry.session(python=["3.13"])
def formatter(session) -> None:
    """Run ruff code formatter."""
    session.run("poetry", "install", external=True)
    session.run("ruff", "format")


@nox_poetry.session(python=["3.13"])
def linter(session) -> None:
    """Lint using ruff."""
    session.run("poetry", "install", external=True)
    session.run("ruff", "check", "--fix")


@nox_poetry.session(python=["3.13"])
def tests(session) -> None:
    """Run the test suite."""
    session.run("poetry", "install", external=True)
    session.run("pytest", "--cov")


@nox_poetry.session(python=["3.13"])
def docs(session) -> None:
    """Build the documentation."""
    # Install main dependencies
    session.run("poetry", "install", "--only", "main", external=True)

    # Install docs dependencies through Poetry
    session.run("poetry", "install", "--only", "docs", external=True)

    # Build the docs
    session.run(
        "sphinx-build",
        "-b",
        "html",
        "-W",  # Treat warnings as errors
        "docs",
        "docs/_build",
    )
