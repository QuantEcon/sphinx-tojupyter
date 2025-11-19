# GitHub Actions Workflows

## Documentation Deployment (`docs.yml`)

Automatically builds and deploys the Sphinx documentation to GitHub Pages.

**Note:** Documentation is also built and validated by `ci.yml` on all PRs and branches.

### Triggers
- **Push to `main`**: Builds and deploys documentation to GitHub Pages
- **Manual trigger**: Via GitHub Actions UI

### Requirements

Before the workflow can deploy, you need to configure GitHub Pages:

1. Go to repository **Settings** → **Pages**
2. Under **Source**, select **GitHub Actions**
3. The workflow will automatically deploy on the next push to `main`

### What it does

**Build Job:**
- Checks out the repository
- Sets up Python 3.11
- Installs Sphinx and dependencies (myst-parser, myst-nb, sphinx-proof, alabaster)
- Builds documentation with warnings as errors (`-W`)
- Creates `.nojekyll` file (prevents Jekyll processing)
- Uploads documentation artifact

**Deploy Job:**
- Only runs on push to `main` branch (not PRs)
- Deploys the built documentation to GitHub Pages
- Available at: `https://quantecon.github.io/sphinx-tojupyter/`

### Local Testing

Test the build locally before pushing:

```bash
cd docs
sphinx-build -b html . _build/html -W
```

### Troubleshooting

**Build Failures:**
- Check that all MyST syntax is valid
- Ensure all cross-references are correct
- Verify all toctree entries exist

**Deployment Not Working:**
- Verify GitHub Pages is configured to use "GitHub Actions" source
- Check that the workflow has `pages: write` permission
- Ensure the branch is `main` (deploy job won't run on other branches)

**404 on GitHub Pages:**
- Wait 1-2 minutes after deployment
- Clear browser cache
- Check the deployment URL in Actions → Deploy logs
