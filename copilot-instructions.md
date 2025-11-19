# Copilot Instructions for sphinx-tojupyter

This document guides automated and human contributors on how to work within this repository efficiently and safely.

## Purpose
- Keep changes small, readable, and aligned with project conventions.
- Prefer maintainability and clarity over cleverness.
- Integrate changes into existing docs and workflows.

## Project Overview (v1.0+)
**sphinx-tojupyter** converts Sphinx documentation to Jupyter notebooks, supporting both RST and MyST Markdown formats.

### Core Focus
- ✅ Convert RST and MyST source files to `.ipynb` format
- ✅ Support MyST-NB features (glue, code cells, etc.)
- ✅ Support sphinx-proof directives (theorems, proofs, algorithms)
- ✅ Support LaTeX macros (MathJax 2 & 3)
- ✅ Maintain compatibility with Sphinx 7+ and Python 3.11+

### Not In Scope
Use these tools instead:
- **Notebook execution** → `myst-nb` or Jupyter Book
- **PDF generation** → `jupyter nbconvert` or Jupyter Book
- **Website building** → Jupyter Book

### Package Structure
```
sphinx_tojupyter/
├── __init__.py          # Extension setup
├── builders/
│   ├── jupyter.py       # Main notebook builder
│   └── jupyterpdf.py    # PDF builder (legacy, may be removed)
├── directive/
│   └── jupyter.py       # jupyter directive for inclusion control
└── writers/
    ├── jupyter.py       # Main notebook writer
    ├── translate_all.py # RST→Notebook translator (core logic)
    ├── translate_code.py # Code block handling
    ├── convert.py       # Deprecated entry point
    ├── execute_nb.py    # Deprecated execution (removed)
    ├── make_pdf.py      # Deprecated PDF generation (removed)
    ├── make_site.py     # Deprecated site generation (removed)
    └── utils.py         # Shared utilities
```

## Additional Rules (project-specific)
1. Do not create summary files; update existing docs where possible. Prefer editing files under `docs/` (or other relevant existing files) rather than adding parallel “summary” artifacts.
2. The GitHub CLI (`gh`) is installed. When interacting with GitHub via terminal, capture interactive or long outputs to files under `/tmp` so results can be viewed reliably (e.g., `/tmp/gh_pr_list.txt`).
3. Write code that is easy to understand and deliberately simple. Reduce complexity to lower long‑term maintenance costs.

## Coding Style and Design
- Simplicity first: small, focused functions; clear names; avoid premature abstraction.
- Prefer standard library and existing utilities in `sphinx_tojupyter/` over new dependencies.
- Python style: follow PEP 8; add type hints where obvious; include concise docstrings with examples when appropriate.
- Error handling: fail fast with helpful messages; avoid silent passes. Log or surface actionable errors.
- Data contracts (lightweight):
  - Inputs: validate early (types/expected shape).
  - Outputs: document return values and invariants.
  - Edge cases: empty inputs, large inputs, missing files, permission issues, network timeouts.

## Documentation Policy
- Update existing content rather than creating new overview/summary docs.
- Co-locate documentation with the feature being changed:
  - Sphinx config and build behavior: update relevant pages in `docs/` (e.g., builders, writers, config topics).
  - User-facing behavior: reflect it in the appropriate `.md` or `.rst` under `docs/`.
- Keep examples minimal and runnable. Prefer incremental diffs and short guidance.

## Using GitHub CLI (gh) with /tmp outputs
- Always redirect output to a file under `/tmp` to avoid lossy interactive formatting and to preserve results for review.
- Examples (zsh):
  - List PRs:
    gh pr list > /tmp/gh_pr_list.txt
  - View a PR in detail (replace 123):
    gh pr view 123 --json title,number,author,state,mergeStateStatus,labels,files,commits > /tmp/gh_pr_123.json
  - List issues with a query:
    gh issue list --label bug --limit 50 > /tmp/gh_issues_bug.txt
  - Create a PR (non-interactive example):
    gh pr create --fill --base main --head feature/branch --draft > /tmp/gh_pr_create.txt 2>&1
- Notes:
  - Use explicit flags to avoid interactive prompts when possible.
  - Capture stderr when relevant with `2>&1`.
  - Prefer JSON output (`--json ...`) when you plan to parse results.

## Tests, Quality Gates, and CI

### Project Focus (v1.0+)
This project focuses **solely on converting RST and MyST source files to Jupyter notebooks**. Removed features include:
- Notebook execution (use `myst-nb` or Jupyter Book)
- PDF generation (use `jupyter nbconvert`)
- Website building (use Jupyter Book or `jupyter-book`)

### Testing Setup
All tests use **nox** for environment management and are defined in `noxfile.py`:

**Core Test Sessions (run by default):**
- `tests` - Core test suite across Python 3.11, 3.12, 3.13 × Sphinx 7.4, 8.2 (6 combinations)
- `lint` - Code quality checks (flake8, imports, formatting)

**Optional Feature Tests:**
- `test-glue` - MyST-NB glue support (inline references, figures)
- `test-proof` - sphinx-proof directives (theorems, proofs, algorithms)
- `test-macros` - LaTeX macro support (MathJax 2 & 3)

**Other Sessions:**
- `tests-full` - Full test suite with all optional dependencies
- `docs` - Build documentation with Sphinx
- `build-package` - Build distribution packages
- `clean` - Clean build artifacts and caches
- `dev-install` - Development environment setup
- `check-manifest` - Verify MANIFEST.in completeness
- `test-config` - Configuration validation tests

**Running Tests:**
```bash
# Run default sessions (tests + lint)
nox

# Run specific session
nox -s tests
nox -s test-glue
nox -s docs

# Run with specific Python/Sphinx version
nox -s "tests-3.11(sphinx='7.4')"

# List all available sessions
nox -l
```

### Dependencies
**Required:**
- `sphinx>=7.0` - Documentation framework
- `docutils` - RST parsing
- `nbformat` - Notebook format handling
- `nbconvert` - Notebook conversion utilities
- `pyyaml` - YAML configuration

**Optional (for specific features):**
- `myst-parser` - MyST Markdown support
- `myst-nb>=0.14` - MyST-NB features (glue, etc.)
- `sphinx-proof` - Theorem/proof directives

**Development:**
- `nox` - Test automation
- `flake8` - Linting

### CI/CD Workflows
**`.github/workflows/ci.yml`** (runs on all PRs and branches):
- Tests: 6 combinations (Python 3.11/3.12/3.13 × Sphinx 7.4/8.2)
- Full tests: Multiple OS (Ubuntu, macOS, Windows)
- Lint checks
- Documentation build
- Package build verification

**`.github/workflows/docs.yml`** (runs on push to `main`):
- Builds documentation with Sphinx
- Deploys to GitHub Pages at `https://quantecon.github.io/sphinx-tojupyter/`

### Before Opening a PR
- **Tests**: Run `nox` to verify core tests and linting pass
- **Feature Tests**: If touching MyST/glue/proof/macros, run relevant `test-*` session
- **Documentation**: If docs changed, run `nox -s docs` to verify build
- **Local Build**: Test `make jupyter` in relevant test directories
- **CI**: All PRs automatically run the full test matrix via GitHub Actions
- Green-before-done: don't leave the tree red. If a non-trivial issue remains, document it clearly in the PR description.

## Commits and Pull Requests
- Commits: crisp messages, imperative mood, scope in the subject (e.g., "writers: simplify site generation path").
- PRs: link issues, summarize user-facing changes, add screenshots or short before/after snippets for docs.
- Keep PRs focused. If a change grows, split logically.

## Working in this Repository
- Prefer editing these locations:
  - Core logic: `sphinx_tojupyter/`
  - Builders/writers: `sphinx_tojupyter/builders/` and `sphinx_tojupyter/writers/`
  - Docs: `docs/` (do not add extra summary files; integrate into existing pages)
  - Tests: `tests/` - organized by feature
- Avoid ad-hoc new top-level folders or parallel doc trees.

### Test Structure
```
tests/
├── base/          # Core RST functionality tests
├── glue/          # MyST-NB glue integration tests
├── sphinx_proof/  # sphinx-proof directive tests
├── latex_macros/  # LaTeX macro support tests
└── project/       # Large project integration tests
```

Each test directory typically contains:
- `conf.py` - Sphinx configuration for the test
- Test source files (`.rst` or `.md`)
- `Makefile` - Build commands (`make jupyter`)
- `ipynb/` - Expected output notebooks (for comparison)
- `README.md` - Test documentation

### Adding New Tests
1. Create test source files in appropriate `tests/` subdirectory
2. Update `conf.py` if special configuration needed
3. Run `make jupyter` to generate notebooks
4. Verify output notebooks are correct
5. Add nox session if testing new optional dependency
6. Document any special setup in test directory README

## Common Development Tasks

### Quick Start (Development Setup)
```bash
# Install in development mode with all dependencies
nox -s dev-install

# Or manually
pip install -e ".[dev]"
```

### Running Tests Locally
```bash
# Run all default tests (6 Python/Sphinx combos + lint)
nox

# Quick test with your current Python
nox -s "tests-3.11(sphinx='8.2')"

# Test specific feature
nox -s test-glue
nox -s test-proof

# Build and test docs
nox -s docs
```

### Building Notebooks from Tests
```bash
# Navigate to test directory
cd tests/base

# Build notebooks
make jupyter

# Clean and rebuild
make clean
make jupyter

# Compare with expected output
diff -r ipynb/ _build/jupyter/
```

### Making Changes
1. **Small translator changes** (`translate_all.py`, `translate_code.py`):
   - Edit the visitor methods
   - Test with `cd tests/base && make jupyter`
   - Verify notebooks render correctly
   
2. **New MyST feature support**:
   - Add visitor methods to `translate_all.py`
   - Create test in `tests/glue/` or appropriate directory
   - Add nox session if new dependency needed
   
3. **Documentation updates**:
   - Edit files in `docs/`
   - Build locally: `nox -s docs`
   - Check `docs/_build/html/` output

### Debugging Tips
- **Verbose Sphinx output**: Add `-v` or `-vv` to sphinx-build commands in Makefile
- **Inspect intermediate doctree**: Use `make pickle` then inspect `.doctree` files
- **Check node types**: Print `node.__class__.__name__` in visitor methods
- **Compare outputs**: Use `diff` or `nbdiff` to compare generated vs expected notebooks

## Practical Tips
- Favor clarity over micro-optimizations. Readability wins.
- If a change introduces complexity, consider adding a small comment describing the trade-off.
- Reuse utility functions in `writers/utils.py` and related modules before introducing new helpers.
- If using `gh` in automation or scripts, always redirect outputs to `/tmp` and reference those files in your notes or PR.
- When adding new node visitor methods, implement both `visit_*` and `depart_*` for consistency.

## Definition of Done
- Code/doc changes are simple and understandable.
- Existing docs updated; no redundant summary files added.
- Local checks pass (build/lint/tests as applicable).
- PR description clearly states what changed and why, with any `/tmp` output files referenced if used.
