# Configuration file for testing sphinx-thebe integration

project = 'Thebe Integration Test'
author = 'Test'
release = '1.0'

# Enable sphinx-thebe extension (if available)
extensions = [
    'sphinx_tojupyter',
]

# Try to add sphinx-thebe if available
try:
    import sphinx_thebe
    extensions.append('sphinx_thebe')
    print("✅ sphinx-thebe extension loaded")
except ImportError:
    print("⚠️  sphinx-thebe not available - install with: pip install sphinx-thebe")

# Jupyter builder configuration
tojupyter_default_lang = "python3"
tojupyter_kernels = {
    "python3": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python3",
            "name": "python3"
        },
        "file_extension": ".py",
    }
}

# This is the key configuration - should drop raw HTML by default
tojupyter_drop_raw_html = True  # Default, but explicitly set for testing

# Thebe configuration (if sphinx-thebe is loaded)
thebe_config = {
    "repository_url": "https://github.com/binder-examples/jupyter-stacks-datascience",
    "repository_branch": "master",
}
