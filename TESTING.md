# Testing with Nox

This project uses [Nox](https://nox.thea.codes/) for automated testing across multiple Python and Sphinx versions.

## Quick Start

Install nox:
```bash
pip install nox
```

Run all tests:
```bash
nox
```

## Available Sessions

List all available test sessions:
```bash
nox -l
```

### Core Testing Sessions

**`tests`** - Run basic tests against multiple Python/Sphinx versions:
```bash
nox -s tests                                    # Run all Python/Sphinx combinations
nox -s tests-3.11                              # Run Python 3.11 only
nox -s "tests-3.11(sphinx='8.2')"             # Specific Python + Sphinx version
```

**Supported Versions:**
- Python: 3.11, 3.12, 3.13
- Sphinx: 7.4, 8.2

**`tests-full`** - Run complete test suite with all optional dependencies:
```bash
nox -s tests-full                              # Tests all features
nox -s tests-full -- skip-glue                # Skip MyST-NB glue tests
nox -s tests-full -- skip-proof               # Skip sphinx-proof tests
```

**`test-glue`** - Test MyST-NB glue support specifically:
```bash
nox -s test-glue
```

**`test-proof`** - Test sphinx-proof support specifically:
```bash
nox -s test-proof
```

### Development Sessions

**`lint`** - Run code linting checks:
```bash
nox -s lint
```

**`docs`** - Build documentation:
```bash
nox -s docs
```

**`dev-install`** - Set up development environment:
```bash
nox -s dev-install
```

**`build-package`** - Build distribution packages:
```bash
nox -s build-package
```

**`clean`** - Clean all build artifacts:
```bash
nox -s clean
```

## Test Matrix

The project is tested against:

- **Python versions:** 3.9, 3.10, 3.11, 3.12, 3.13
- **Sphinx versions:** 5.3, 6.2, 7.4, 8.2
- **Optional extensions:**
  - myst-parser
  - myst-nb (glue support)
  - sphinx-exercise
  - sphinx-proof

## CI/CD Integration

GitHub Actions automatically runs tests on:
- Every push to main branch
- Every pull request
- Multiple OS: Ubuntu, macOS, Windows
- Full matrix of Python + Sphinx versions

See `.github/workflows/tests.yml` for details.

## Local Development Workflow

1. **Set up environment:**
   ```bash
   nox -s dev-install
   ```

2. **Make changes to code**

3. **Run relevant tests:**
   ```bash
   nox -s test-proof           # If you changed sphinx-proof support
   nox -s test-glue           # If you changed MyST-NB support
   nox -s tests-3.11          # Run core tests
   ```

4. **Check code quality:**
   ```bash
   nox -s lint
   ```

5. **Build docs to verify:**
   ```bash
   nox -s docs
   ```

6. **Before committing, run full suite:**
   ```bash
   nox -s tests-full
   ```

## Troubleshooting

**Session fails with import errors:**
```bash
nox -s clean                   # Clean cached environments
nox -s tests-full --reuse-existing-virtualenvs=no
```

**Run tests in verbose mode:**
```bash
nox -s tests-3.11 -- -v
```

**Keep environment for debugging:**
```bash
nox -s tests-3.11 --no-venv-reuse
# Then activate: .nox/tests-3-11/bin/activate
```

## Configuration

Nox behavior can be customized in `noxfile.py`:
- `PYTHON_VERSIONS` - List of Python versions to test
- `SPHINX_VERSIONS` - List of Sphinx versions to test  
- `nox.options.reuse_existing_virtualenvs` - Reuse virtual environments (faster)

## Tips

- Use `--reuse-existing-virtualenvs` (default) for faster subsequent runs
- Use `--no-reuse-existing-virtualenvs` when dependency versions change
- Run `nox -s clean` periodically to free disk space
- CI runs all tests; locally focus on relevant sessions for your changes
