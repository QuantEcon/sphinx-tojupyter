# Copilot Instructions for sphinx-tojupyter

This document guides automated and human contributors on how to work within this repository efficiently and safely.

## Purpose
- Keep changes small, readable, and aligned with project conventions.
- Prefer maintainability and clarity over cleverness.
- Integrate changes into existing docs and workflows.

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
- Before opening a PR, ensure:
  - Build: Sphinx-related builders run without errors for affected docs.
  - Lint/Typecheck: No obvious style or typing regressions; keep imports tidy.
  - Tests: Run repository tests and spot-check affected paths.
- Green-before-done: don’t leave the tree red. If a non-trivial issue remains, document it clearly in the PR description.

## Commits and Pull Requests
- Commits: crisp messages, imperative mood, scope in the subject (e.g., "writers: simplify site generation path").
- PRs: link issues, summarize user-facing changes, add screenshots or short before/after snippets for docs.
- Keep PRs focused. If a change grows, split logically.

## Working in this Repository
- Prefer editing these locations:
  - Core logic: `sphinx_tojupyter/`
  - Builders/writers: `sphinx_tojupyter/builders/` and `sphinx_tojupyter/writers/`
  - Docs: `docs/` (do not add extra summary files; integrate into existing pages)
  - Tests: `tests/`
- Avoid ad-hoc new top-level folders or parallel doc trees.

## Practical Tips
- Favor clarity over micro-optimizations. Readability wins.
- If a change introduces complexity, consider adding a small comment describing the trade-off.
- Reuse utility functions in `writers/utils.py` and related modules before introducing new helpers.
- If using `gh` in automation or scripts, always redirect outputs to `/tmp` and reference those files in your notes or PR.

## Definition of Done
- Code/doc changes are simple and understandable.
- Existing docs updated; no redundant summary files added.
- Local checks pass (build/lint/tests as applicable).
- PR description clearly states what changed and why, with any `/tmp` output files referenced if used.
