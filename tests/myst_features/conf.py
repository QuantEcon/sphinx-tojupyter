extensions = ["sphinx_tojupyter", "myst_parser"]

# Jupyter kernel configuration
jupyter_kernels = {
    "python3": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python3",
            "name": "python3"
        },
        "file_extension": ".py",
    }
}

# MyST configuration
myst_enable_extensions = [
    "colon_fence",  # Allow ::: style directives
    "deflist",      # Definition lists
    "substitution", # Text substitutions
]

# Project information
project = 'MyST Features Test'
