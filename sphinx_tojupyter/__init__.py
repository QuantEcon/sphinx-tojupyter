import yaml

try:
    yaml.warnings({'YAMLLoadWarning': False})  # not all versions of YAML support this
except AttributeError:
    pass

from .builders.jupyter import JupyterBuilder
from .directive.jupyter import jupyter_node
from .directive.jupyter import Jupyter as JupyterDirective
from .directive.jupyter import JupyterDependency

try:
    from importlib.metadata import version as get_version
except ImportError:
    from importlib_metadata import version as get_version

try:
    VERSION = get_version('sphinx-tojupyter')
except Exception:
    VERSION = 'unknown'

import sphinx
SPHINX_VERSION = sphinx.version_info

JUPYTER_KERNELS = {
    "python3": {
        "kernelspec": {
            "display_name": "Python",
            "language": "python3",
            "name": "python3"
            },
        "file_extension": ".py",
    },
}

NB_RENDER_PRIORITY = [
  ["jupyter", "application/vnd.jupyter.widget-view+json", 10],
  ["jupyter", "application/javascript", 20],
  ["jupyter", "text/html", 30],
  ["jupyter", "image/svg+xml", 40],
  ["jupyter", "image/png", 50],
  ["jupyter", "image/jpeg", 60],
  ["jupyter", "text/markdown", 70],
  ["jupyter", "text/latex", 80],
  ["jupyter", "text/plain", 90],
]

def _noop(*args, **kwargs):
    pass

def setup(app):
    """Setup the sphinx-tojupyter extension"""
    
    # Add Sphinx version to environment configuration
    app.add_config_value('SPHINX_VERSION', SPHINX_VERSION, 'env')

    # Register Jupyter builder
    app.add_builder(JupyterBuilder)

    # Core notebook generation options
    app.add_config_value("tojupyter_kernels", JUPYTER_KERNELS, "jupyter")
    app.add_config_value("tojupyter_default_lang", "python3", "jupyter")
    app.add_config_value("tojupyter_lang_synonyms", [], "jupyter")
    app.add_config_value("tojupyter_conversion_mode", "all", "jupyter")

    # Content control options
    app.add_config_value("tojupyter_drop_solutions", True, "jupyter")
    app.add_config_value("tojupyter_drop_tests", True, "jupyter")

    # Asset handling options
    app.add_config_value("tojupyter_static_file_path", [], "jupyter")
    app.add_config_value("tojupyter_images_markdown", True, "jupyter")

    # URL path options
    app.add_config_value("tojupyter_urlpath", None, "jupyter")
    app.add_config_value("tojupyter_image_urlpath", None, "jupyter")
    app.add_config_value("tojupyter_glue_urlpath", None, "jupyter")

    # Advanced options
    app.add_config_value("tojupyter_latex_macros", None, "jupyter")
    app.add_config_value("tojupyter_dependency_lists", {}, "jupyter")
    app.add_config_value("tojupyter_nextprev_ignore", [], "jupyter")

    # Register Jupyter directives
    app.add_node(jupyter_node, html=(_noop, _noop), latex=(_noop, _noop))
    app.add_directive("jupyter", JupyterDirective)
    app.add_directive("jupyter-dependency", JupyterDependency)

    # Configure myst-nb integration
    if "nb_mime_priority_overrides" in app.config:
        app.config["nb_mime_priority_overrides"] = NB_RENDER_PRIORITY
    else:
        app.add_config_value("nb_mime_priority_overrides", NB_RENDER_PRIORITY, "env")

    return {
        "version": VERSION,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
