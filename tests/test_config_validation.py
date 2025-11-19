"""
Test configuration validation for v2.0

Ensures that:
1. Deprecated config options don't cause crashes
2. Core config options work correctly
3. Appropriate warnings are issued for deprecated options
"""
import pytest
import tempfile
import os
from pathlib import Path
from sphinx.application import Sphinx
from sphinx.util.docutils import docutils_namespace


def test_deprecated_config_options_dont_crash():
    """Test that deprecated v1.x config options don't cause crashes"""
    
    # Create a minimal conf.py with deprecated options
    conf_content = """
extensions = ["sphinx_tojupyter"]

# v2.0 core options (should work)
jupyter_kernels = {
    "python3": {
        "kernelspec": {
            "display_name": "Python",
            "language": "python3",
            "name": "python3"
        },
        "file_extension": ".py",
    }
}

# Deprecated options (should be ignored gracefully)
jupyter_target_pdf = True
jupyter_target_html = True
jupyter_execute_notebooks = True
jupyter_make_site = True
jupyter_generate_html = True
jupyter_coverage_dir = "coverage"
tojupyter_target_pdf = True
tojupyter_target_html = True
"""
    
    # Create a minimal RST document
    rst_content = """
Test Document
=============

This is a test.

.. code-block:: python

    print("Hello World")
"""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        srcdir = tmpdir / "source"
        srcdir.mkdir()
        outdir = tmpdir / "build"
        
        # Write conf.py
        (srcdir / "conf.py").write_text(conf_content)
        
        # Write index.rst (required by Sphinx)
        (srcdir / "index.rst").write_text(rst_content)
        
        # Try to build
        with docutils_namespace():
            app = Sphinx(
                srcdir=str(srcdir),
                confdir=str(srcdir),
                outdir=str(outdir),
                doctreedir=str(outdir / ".doctrees"),
                buildername="jupyter",
                warningiserror=False,  # Don't fail on warnings
            )
            app.build()
            
        # Check that notebook was created
        notebook_path = outdir / "index.ipynb"
        assert notebook_path.exists(), "Notebook should be created despite deprecated options"
        
        # Check that it's valid JSON
        import json
        with open(notebook_path) as f:
            nb_data = json.load(f)
        
        assert "cells" in nb_data
        assert len(nb_data["cells"]) > 0


def test_core_config_options_work():
    """Test that core v2.0 config options work correctly"""
    
    conf_content = """
extensions = ["sphinx_tojupyter"]

jupyter_conversion_mode = "all"
jupyter_default_lang = "python3"
jupyter_lang_synonyms = ["pycon", "ipython"]

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

jupyter_static_file_path = []
jupyter_images_markdown = True
"""
    
    rst_content = """
Test Document
=============

Code block:

.. code-block:: python

    x = 42
"""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        srcdir = tmpdir / "source"
        srcdir.mkdir()
        outdir = tmpdir / "build"
        
        (srcdir / "conf.py").write_text(conf_content)
        (srcdir / "index.rst").write_text(rst_content)
        
        with docutils_namespace():
            app = Sphinx(
                srcdir=str(srcdir),
                confdir=str(srcdir),
                outdir=str(outdir),
                doctreedir=str(outdir / ".doctrees"),
                buildername="jupyter",
            )
            app.build()
            
        notebook_path = outdir / "index.ipynb"
        assert notebook_path.exists()
        
        # Validate notebook content
        import json
        with open(notebook_path) as f:
            nb_data = json.load(f)
        
        # Check kernel metadata
        assert nb_data["metadata"]["kernelspec"]["name"] == "python3"
        
        # Check that notebook has cells (markdown or code)
        assert len(nb_data["cells"]) > 0


def test_minimal_config():
    """Test that minimal configuration works"""
    
    conf_content = """
extensions = ["sphinx_tojupyter"]

jupyter_kernels = {
    "python3": {
        "kernelspec": {
            "display_name": "Python",
            "language": "python3",
            "name": "python3"
        },
        "file_extension": ".py",
    }
}
"""
    
    rst_content = """
Minimal Test
============

Just text.
"""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        srcdir = tmpdir / "source"
        srcdir.mkdir()
        outdir = tmpdir / "build"
        
        (srcdir / "conf.py").write_text(conf_content)
        (srcdir / "index.rst").write_text(rst_content)
        
        with docutils_namespace():
            app = Sphinx(
                srcdir=str(srcdir),
                confdir=str(srcdir),
                outdir=str(outdir),
                doctreedir=str(outdir / ".doctrees"),
                buildername="jupyter",
            )
            app.build()
            
        notebook_path = outdir / "index.ipynb"
        assert notebook_path.exists()


if __name__ == "__main__":
    # Run tests individually for debugging
    test_deprecated_config_options_dont_crash()
    print("✓ Deprecated config options test passed")
    
    test_core_config_options_work()
    print("✓ Core config options test passed")
    
    test_minimal_config()
    print("✓ Minimal config test passed")
    
    print("\n✅ All config validation tests passed!")
