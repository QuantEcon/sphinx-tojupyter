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
PYTHON_VERSIONS = ["3.11", "3.12", "3.13"]
DEFAULT_PYTHON = "3.11"

# Sphinx versions to test against
SPHINX_VERSIONS = ["7.4", "8.2"]

nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = ["tests", "lint"]


@nox.session(python=PYTHON_VERSIONS)
@nox.parametrize("sphinx", SPHINX_VERSIONS)
def tests(session, sphinx):
    """
    Run test suite against different Python and Sphinx versions.
    
    Tests basic functionality without optional dependencies.
    """
    # Install with specific Sphinx version constraint to prevent upgrades
    # Create a temporary constraints file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(f"sphinx=={sphinx}\n")
        constraints_file = f.name
    
    try:
        session.install("-c", constraints_file, f"sphinx=={sphinx}")
        session.install("-c", constraints_file, "-e", ".")
    finally:
        import os
        os.unlink(constraints_file)
    
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


@nox.session(name="tests-full")
def tests_full(session):
    """
    Run full test suite with all optional dependencies.
    
    Uses the current Python interpreter to create a virtualenv.
    In CI, this will be the Python version set up by the workflow matrix.
    
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
    if not session.posargs or "skip-glue" not in session.posargs:
        session.log("Testing MyST-NB glue support...")
        session.run(
            "python", "-m", "sphinx",
            "-b", "jupyter",
            "tests/glue",
            "tests/glue/_build/jupyter",
        )
    
    # Test sphinx-proof support
    if not session.posargs or "skip-proof" not in session.posargs:
        session.log("Testing sphinx-proof support...")
        session.run(
            "python", "-m", "sphinx",
            "-b", "jupyter",
            "tests/sphinx_proof",
            "tests/sphinx_proof/_build/jupyter",
        )
    
    # Test LaTeX macros support
    if not session.posargs or "skip-macros" not in session.posargs:
        session.log("Testing LaTeX macros support...")
        session.run(
            "python", "-m", "sphinx",
            "-b", "jupyter",
            "tests/latex_macros",
            "tests/latex_macros/_build/jupyter",
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
        "from sphinx_tojupyter.builder import JupyterBuilder; "
        "from sphinx_tojupyter.writer import JupyterWriter; "
        "from sphinx_tojupyter.translators import JupyterTranslator, JupyterCodeTranslator; "
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


@nox.session(python=DEFAULT_PYTHON, name="test-macros")
def test_macros(session):
    """Test LaTeX macros support specifically."""
    session.install(
        "sphinx>=8.0",
        "myst-parser>=4.0",
    )
    session.install("-e", ".")
    
    session.log("Testing LaTeX macros support...")
    session.run(
        "python", "-m", "sphinx",
        "-b", "jupyter",
        "tests/latex_macros",
        "tests/latex_macros/_build/jupyter",
    )
    
    # Verify notebooks were created
    session.run(
        "python", "-c",
        "import os; "
        "assert os.path.exists('tests/latex_macros/_build/jupyter/test_macros.ipynb'), 'Macros notebook not found'; "
        "print('✅ LaTeX macros notebooks generated')"
    )


@nox.session(python=DEFAULT_PYTHON, name="test-urlpath")
def test_urlpath(session):
    """Test tojupyter_urlpath configuration for cross-document links."""
    session.install(
        "sphinx>=8.0",
        "myst-parser>=4.0",
    )
    session.install("-e", ".")
    
    session.log("Testing tojupyter_urlpath configuration...")
    session.run(
        "python", "-m", "sphinx",
        "-b", "jupyter",
        "tests/urlpath",
        "tests/urlpath/_build/jupyter",
    )
    
    # Verify notebooks were created
    session.run(
        "python", "-c",
        "import os; "
        "assert os.path.exists('tests/urlpath/_build/jupyter/doc_a.ipynb'), 'doc_a notebook not found'; "
        "assert os.path.exists('tests/urlpath/_build/jupyter/doc_b.ipynb'), 'doc_b notebook not found'; "
        "print('✅ URL path test notebooks generated')"
    )
    
    # Verify link patterns
    session.log("Verifying link patterns...")
    session.run(
        "python", "-c",
        """
import json
import os

def check_links(notebook_path, doc_name):
    with open(notebook_path, 'r') as f:
        nb = json.load(f)
    
    issues = []
    base_url = 'https://continuous-time-mcs.quantecon.org/'
    
    for i, cell in enumerate(nb.get('cells', [])):
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            
            # Check for cross-document links (should have base URL)
            if 'doc_a.ipynb' in source and doc_name != 'doc_a':
                if base_url not in source:
                    issues.append(f"Cell {i}: Cross-doc link to doc_a.ipynb missing base URL")
            if 'doc_b.ipynb' in source and doc_name != 'doc_b':
                if base_url not in source:
                    issues.append(f"Cell {i}: Cross-doc link to doc_b.ipynb missing base URL")
            
            # Check that in-page anchors don't have base URL
            import re
            local_anchors = re.findall(r'\\]\\(#[^)]+\\)', source)
            for anchor in local_anchors:
                if base_url in anchor:
                    issues.append(f"Cell {i}: In-page anchor has base URL: {anchor}")
    
    return issues

# Check doc_a
issues_a = check_links('tests/urlpath/_build/jupyter/doc_a.ipynb', 'doc_a')
if issues_a:
    print("⚠️  Issues in doc_a.ipynb:")
    for issue in issues_a:
        print(f"  - {issue}")
else:
    print("✅ doc_a.ipynb links verified")

# Check doc_b  
issues_b = check_links('tests/urlpath/_build/jupyter/doc_b.ipynb', 'doc_b')
if issues_b:
    print("⚠️  Issues in doc_b.ipynb:")
    for issue in issues_b:
        print(f"  - {issue}")
else:
    print("✅ doc_b.ipynb links verified")

if issues_a or issues_b:
    raise AssertionError("Link verification failed - see issues above")

print("\\n✅ All URL path tests passed!")
"""
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


@nox.session(python=PYTHON_VERSIONS, name="test-config")
@nox.parametrize("sphinx", SPHINX_VERSIONS)
def test_config(session, sphinx):
    """
    Run configuration validation tests.
    
    Tests that:
    - Deprecated config options don't cause crashes
    - Core config options work correctly
    - Minimal configuration works
    """
    # Install with specific Sphinx version
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(f"sphinx=={sphinx}\n")
        constraints_file = f.name
    
    try:
        session.install("-c", constraints_file, f"sphinx=={sphinx}")
        session.install("-c", constraints_file, "pytest")
        session.install("-c", constraints_file, "-e", ".")
    finally:
        import os
        os.unlink(constraints_file)
    
    # Run pytest on config validation tests
    session.run(
        "pytest",
        "tests/test_config_validation.py",
        "-v",
        env={"PYTHONDONTWRITEBYTECODE": "1"}
    )
    
    session.log("✅ Config validation tests passed")
