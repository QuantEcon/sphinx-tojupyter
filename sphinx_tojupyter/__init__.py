import yaml

try:
    yaml.warnings({'YAMLLoadWarning': False})  # not all versions of YAML support this
except AttributeError:
    pass

from .builders.jupyter import JupyterBuilder
from .builders.jupyterpdf import JupyterPDFBuilder
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
  ["jupyterpdf", "application/pdf", 10],
  ["jupyterpdf", "image/png", 20],  
  ["jupyterpdf", "image/jpeg", 30],  
  ["jupyterpdf", "text/latex", 40],  
  ["jupyterpdf", "text/markdown", 50],  
  ["jupyterpdf", "text/plain", 60],  
]

def _noop(*args, **kwargs):
    pass

def setup(app):
    execute_nb_obj = {
        "no-text": True,
        "timeout": 600,
        "text_reports": True,
    }

    #Add Sphinx Version to ENV Configuration
    app.add_config_value('SPHINX_VERSION', SPHINX_VERSION, 'env')

    # Jupyter Builder and Options
    app.add_builder(JupyterPDFBuilder)
    app.add_builder(JupyterBuilder)
    app.add_config_value("tojupyter_kernels", JUPYTER_KERNELS, "jupyter")
    app.add_config_value("tojupyter_conversion_mode", "all", "jupyter")
    app.add_config_value("tojupyter_static_file_path", [], "jupyter")
    app.add_config_value("tojupyter_default_lang", "python3", "jupyter")
    app.add_config_value("tojupyter_lang_synonyms", [], "jupyter")
    app.add_config_value("tojupyter_drop_solutions", True, "jupyter")
    app.add_config_value("tojupyter_drop_tests", True, "jupyter")
    app.add_config_value("tojupyter_execute_nb", execute_nb_obj, "jupyter")
    app.add_config_value("tojupyter_generate_html", False, "jupyter")
    app.add_config_value("tojupyter_html_template", None, "jupyter")
    app.add_config_value("tojupyter_execute_notebooks", False, "jupyter")
    app.add_config_value("tojupyter_make_site", False, "jupyter")
    app.add_config_value("tojupyter_dependency_lists", {}, "jupyter")
    app.add_config_value("tojupyter_threads_per_worker", 1, "jupyter")
    app.add_config_value("tojupyter_number_workers", 1, "jupyter")
    app.add_config_value("tojupyter_target_pdf", False, "jupyter")
    app.add_config_value("tojupyter_theme", None, "jupyter")
    app.add_config_value("tojupyter_theme_path", "theme", "jupyter")
    app.add_config_value("tojupyter_template_path", "templates", "jupyter")
    app.add_config_value("tojupyter_dependencies", None, "jupyter")
    app.add_config_value("tojupyter_download_nb_execute", None, "jupyter")
    app.add_config_value("tojupyter_nextprev_ignore", [], "jupyter")
    app.add_config_value("tojupyter_target_html", False, "jupyter")
    app.add_config_value("tojupyter_download_nb", False, "jupyter")
    app.add_config_value("tojupyter_download_nb_urlpath", None, "jupyter")
    app.add_config_value("tojupyter_download_nb_image_urlpath", None, "jupyter")
    app.add_config_value("tojupyter_images_markdown", True, "jupyter")
    app.add_config_value("tojupyter_urlpath", None, "jupyter")
    app.add_config_value("tojupyter_image_urlpath", None, "jupyter")
    app.add_config_value("tojupyter_glue_urlpath", None, "jupyter")
    app.add_config_value("tojupyter_glue_images_urlpath", None, "jupyter")  # Alternative name for clarity
    app.add_config_value("tojupyter_latex_macros", None, "jupyter")  # LaTeX macros for MathJax
    app.add_config_value("tojuyter_drop_html_raw", True, "jupyter")

    # Jupyter pdf options
    app.add_config_value("tojupyter_latex_template", None, "jupyter")
    app.add_config_value("tojupyter_latex_template_book", None, "jupyter")
    app.add_config_value("tojupyter_pdf_logo", None, "jupyter")
    app.add_config_value("tojupyter_bib_file", None, "jupyter")
    app.add_config_value("tojupyter_pdf_author", None, "jupyter")
    app.add_config_value("tojupyter_pdf_showcontentdepth", 2, "jupyter")
    app.add_config_value("tojupyter_pdf_urlpath", None, "jupyter")
    app.add_config_value("tojupyter_pdf_excludepatterns", [], "jupyter")
    app.add_config_value("tojupyter_pdf_book", False, "jupyter")
    app.add_config_value("tojupyter_pdf_book_index", None, "jupyter")
    app.add_config_value("tojupyter_pdf_book_title", None, "jupyter")
    app.add_config_value("tojupyter_pdf_book_name", None, "jupyter")

    # Jupyter Directives
    app.add_node(jupyter_node, html=(_noop, _noop), latex=(_noop, _noop))
    app.add_directive("jupyter", JupyterDirective)
    app.add_directive("jupyter-dependency", JupyterDependency)

    #Add config to support myst_nb
    if "nb_mime_priority_overrides" in app.config:
        app.config["nb_mime_priority_overrides"] = NB_RENDER_PRIORITY
    else:
        app.add_config_value("nb_mime_priority_overrides", NB_RENDER_PRIORITY, "env")

    return {
        "version": VERSION,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
