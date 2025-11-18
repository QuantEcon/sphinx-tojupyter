# sphinx-proof Test Suite

This directory contains tests for sphinx-proof directive support in sphinx-tojupyter.

## Running Tests

To build the Jupyter notebooks from the test documents:

```bash
make jupyter
```

The generated notebooks will be in `_build/jupyter/`.

## Test Files

- `test_basic_directives.md` - Tests all 15 basic directive types (theorem, axiom, lemma, etc.)
- `test_numbered_directives.md` - Tests numbered directives with titles and cross-references
- `test_proofs.md` - Tests the proof directive

## What to Check

After building, verify that the generated notebooks contain:

1. **Proper Headers**: Each directive should have a bold header like "**Theorem 1.1** (Title)"
2. **Numbering**: Directives with labels should be numbered correctly
3. **Content**: The mathematical content and text should be preserved
4. **Formatting**: Markdown should be clean and readable

## Expected Output Format

A theorem like:

```markdown
{prf:theorem} Pythagorean Theorem
:label: pythagoras

In a right triangle...
```

Should generate:

```markdown
**Theorem 1** (Pythagorean Theorem)

In a right triangle...
```
