"""
Nox sessions for sphinx-tojupyter testing.

Run all sessions:
    nox

Run specific session:
    nox -s tests
    nox -s tests-3.11
    
Run with specific Sphinx version:
    nox -s "tests-3.11(sphinx='7.0')"

List all sessions:
    nox -l
"""
import nox

# Supported Python versions
PYTHON_VERSIONS = ["3.9", "3.10", "3.11", "3.12", "3.13"]
DEFAULT_PYTHON = "3.11"

# Sphinx versions to test against
SPHINX_VERSIONS = ["5.3", "6.2", "7.4", "8.2"]

nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = ["tests", "lint"]


@nox.session(python=PYTHON_VERSIONS)
@nox.parametrize("sphinx", SPHINX_VERSIONS)
def tests(session, sphinx):
    """
    Run test suite against different Python and Sphinx versions.
    
    Tests basic functionality without optional dependencies.
    """
    # Install package first without dependencies to avoid Sphinx version conflicts
    session.install("-e", ".", "--no-deps")
    # Then install specific Sphinx version
    session.install(f"sphinx=={sphinx}")
    # Install other required dependencies
    session.install("docutils", "myst-parser")
    
    # Run basic tests
    session.run(
        "python", "-m", "sphinx",
        "-b", "jupyter",
        "-W",  # Treat warnings as errors
        "tests/base",
        "tests/base/_build/jupyter",
        env={"PYTHONDONTWRITEBYTECODE": "1"}
    )
    
    session.log("✅ Basic tests passed")


@nox.session(python=DEFAULT_PYTHON, name="tests-full")
def tests_full(session):
    """
    Run full test suite with all optional dependencies.
    
    This includes:
    - myst-parser
    - myst-nb
    - sphinx-exercise
    - sphinx-proof
    """
    session.install(
        "sphinx>=8.0",
        "myst-parser>=4.0",
        "myst-nb>=1.0",
        "sphinx-exercise>=1.0",
        "sphinx-proof>=0.3",
    )
    session.install("-e", ".")
    
    # Test base functionality
    session.log("Testing base functionality...")
    session.run(
        "python", "-m", "sphinx",
        "-b", "jupyter",
        "tests/base",
        "tests/base/_build/jupyter",
    )
    
    # Test glue support (MyST-NB)
    if session.posargs and "skip-glue" not in session.posargs:
        session.log("Testing MyST-NB glue support...")
        session.run(
            "python", "-m", "sphinx",
            "-b", "jupyter",
            "tests/glue",
            "tests/glue/_build/jupyter",
        )
    
    # Test sphinx-proof support
    if session.posargs and "skip-proof" not in session.posargs:
        session.log("Testing sphinx-proof support...")
        session.run(
            "python", "-m", "sphinx",
            "-b", "jupyter",
            "tests/sphinx_proof",
            "tests/sphinx_proof/_build/jupyter",
        )
    
    session.log("✅ Full test suite passed")


@nox.session(python=DEFAULT_PYTHON)
def lint(session):
    """
    Run linting checks.
    
    Checks:
    - flake8 for code style
    - Basic import checks
    """
    session.install("flake8", "flake8-docstrings")
    session.install("-e", ".")
    
    session.log("Running flake8...")
    session.run(
        "flake8",
        "sphinx_tojupyter",
        "--count",
        "--select=E9,F63,F7,F82",  # Critical errors only
        "--show-source",
        "--statistics",
    )
    
    # Check that all modules can be imported
    session.log("Checking imports...")
    session.run(
        "python", "-c",
        "import sphinx_tojupyter; "
        "from sphinx_tojupyter.builders.jupyter import JupyterBuilder; "
        "from sphinx_tojupyter.writers.jupyter import JupyterWriter; "
        "print('✅ All imports successful')"
    )


@nox.session(python=DEFAULT_PYTHON, name="test-glue")
def test_glue(session):
    """Test MyST-NB glue support specifically."""
    session.install(
        "sphinx>=8.0",
        "myst-parser>=4.0",
        "myst-nb>=1.0",
    )
    session.install("-e", ".")
    
    session.log("Testing MyST-NB glue support...")
    session.run(
        "python", "-m", "sphinx",
        "-b", "jupyter",
        "tests/glue",
        "tests/glue/_build/jupyter",
    )
    
    # Verify notebooks were created
    session.run(
        "python", "-c",
        "import os; "
        "assert os.path.exists('tests/glue/_build/jupyter/test_glue_basic.ipynb'), 'Basic glue notebook not found'; "
        "assert os.path.exists('tests/glue/_build/jupyter/test_glue_figures.ipynb'), 'Figures glue notebook not found'; "
        "print('✅ All glue notebooks generated')"
    )


@nox.session(python=DEFAULT_PYTHON, name="test-proof")
def test_proof(session):
    """Test sphinx-proof support specifically."""
    session.install(
        "sphinx>=8.0",
        "myst-parser>=4.0",
        "sphinx-proof>=0.3",
    )
    session.install("-e", ".")
    
    session.log("Testing sphinx-proof support...")
    session.run(
        "python", "-m", "sphinx",
        "-b", "jupyter",
        "tests/sphinx_proof",
        "tests/sphinx_proof/_build/jupyter",
    )
    
    # Verify notebooks were created
    session.run(
        "python", "-c",
        "import os; "
        "assert os.path.exists('tests/sphinx_proof/_build/jupyter/test_basic_directives.ipynb'), 'Basic directives notebook not found'; "
        "assert os.path.exists('tests/sphinx_proof/_build/jupyter/test_numbered_directives.ipynb'), 'Numbered directives notebook not found'; "
        "assert os.path.exists('tests/sphinx_proof/_build/jupyter/test_proofs.ipynb'), 'Proofs notebook not found'; "
        "print('✅ All sphinx-proof notebooks generated')"
    )


@nox.session(python=DEFAULT_PYTHON)
def docs(session):
    """Build documentation."""
    session.install(
        "sphinx>=8.0",
        "myst-parser>=4.0",
        "sphinx-rtd-theme",
    )
    session.install("-e", ".")
    
    session.log("Building documentation...")
    session.run(
        "python", "-m", "sphinx",
        "-b", "html",
        "docs",
        "docs/_build/html",
        "-W",  # Treat warnings as errors
    )
    
    session.log(f"✅ Documentation built successfully")
    session.log(f"📖 View at: file://{session.posargs[0] if session.posargs else 'docs/_build/html/index.html'}")


@nox.session(python=DEFAULT_PYTHON, name="build-package")
def build_package(session):
    """Build distribution packages."""
    session.install("build", "twine")
    
    session.log("Building package...")
    session.run("python", "-m", "build")
    
    session.log("Checking package...")
    session.run("twine", "check", "dist/*")
    
    session.log("✅ Package built successfully")


@nox.session(python=DEFAULT_PYTHON)
def clean(session):
    """Clean build artifacts and caches."""
    import shutil
    from pathlib import Path
    
    patterns = [
        "**/_build",
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/.pytest_cache",
        "build",
        "dist",
        "*.egg-info",
        ".nox",
    ]
    
    for pattern in patterns:
        for path in Path(".").glob(pattern):
            if path.exists():
                session.log(f"Removing {path}")
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
    
    session.log("✅ Cleanup complete")


@nox.session(python=DEFAULT_PYTHON, name="dev-install")
def dev_install(session):
    """
    Install package in development mode with all dependencies.
    
    Useful for local development setup.
    """
    session.install(
        "sphinx>=8.0",
        "myst-parser>=4.0",
        "myst-nb>=1.0",
        "sphinx-exercise>=1.0",
        "sphinx-proof>=0.3",
        "sphinx-book-theme",
        "jupyterlab",
        "ipykernel",
    )
    session.install("-e", ".")
    
    session.log("✅ Development environment ready")
    session.log("Run 'jupyter lab' to start working with notebooks")


@nox.session(python=DEFAULT_PYTHON, name="check-manifest")
def check_manifest(session):
    """
    Check that MANIFEST.in includes all necessary files.
    """
    session.install("check-manifest")
    session.run("check-manifest")
