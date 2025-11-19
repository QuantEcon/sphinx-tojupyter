import codecs
import os.path
import docutils.io
import docutils

import nbformat
from sphinx.util.osutil import ensuredir, os_path
from ..writers.jupyter import JupyterWriter
from sphinx.builders import Builder
from sphinx.util.console import bold
from sphinx.util.fileutil import copy_asset
from sphinx.util import logging
import time
from ..writers.utils import copy_dependencies

class JupyterBuilder(Builder):
    """
    Builds Jupyter Notebooks from RST/MyST source files
    """
    name = "jupyter"
    format = "ipynb"
    out_suffix = ".ipynb"
    allow_parallel = True

    _writer_class = JupyterWriter
    logger = logging.getLogger(__name__)

    def init(self):
        """Initialize the Jupyter notebook builder"""
        # Check default language is defined in the jupyter kernels
        def_lng = self.config["tojupyter_default_lang"]
        if def_lng not in self.config["tojupyter_kernels"]:
            self.logger.warning(
                "Default language defined in conf.py ({}) is not "
                "defined in the tojupyter_kernels in conf.py. "
                "Set default language to python3"
                .format(def_lng))
            self.config["tojupyter_default_lang"] = "python3"

    def get_outdated_docs(self):
        for docname in self.env.found_docs:
            if docname not in self.env.all_docs:
                yield docname
                continue
            targetname = os.path.join(self.outdir, docname)
            targetname += self.out_suffix
            try:
                targetmtime = os.path.getmtime(targetname)
            except OSError:
                targetmtime = 0
            try:
                srcmtime = os.path.getmtime(self.env.doc2path(docname))
                if srcmtime > targetmtime:
                    yield docname
            except EnvironmentError:
                pass

    def get_target_uri(self, docname, typ=None):
        return docname

    def prepare_writing(self, docnames):
        """Prepare the writer for notebook generation"""
        self.writer = self._writer_class(self)
        # Copy dependencies to the notebook folder
        copy_dependencies(self)

    def write_doc(self, docname, doctree):
        """Write a document as a Jupyter notebook"""
        self.docname = docname
        doctree = doctree.deepcopy()
        destination = docutils.io.StringOutput(encoding="utf-8")
        
        # Set URL paths for links and images
        if "tojupyter_urlpath" in self.config:
            self.writer._set_ref_urlpath(self.config["tojupyter_urlpath"])
        else:
            self.writer._set_ref_urlpath(None)
            
        if "tojupyter_image_urlpath" in self.config:
            self.writer._set_tojupyter_image_urlpath(self.config["tojupyter_image_urlpath"])
        else:
            self.writer._set_tojupyter_image_urlpath(None)

        # Write the notebook
        self.writer.write(doctree, destination)

        # Get a NotebookNode object from the output string
        nb = nbformat.reads(self.writer.output, as_version=4)
        nb = self.update_Metadata(docname, nb)

        # Write notebook to file
        outfilename = os.path.join(self.outdir, os_path(docname) + self.out_suffix)
        ensuredir(os.path.dirname(outfilename))

        try:
            with codecs.open(outfilename, "w", "utf-8") as f:
                self.writer.output = nbformat.writes(nb, version=4)
                f.write(self.writer.output)
        except (IOError, OSError) as err:
            self.logger.warning("error writing file %s: %s" % (outfilename, err))

    def update_Metadata(self, docname, nb):
        """Update metadata for Jupyter Notebook"""
        # Set compilation datetime
        nb.metadata.date = time.time()
        return nb

    def copy_static_files(self):
        """Copy static files to the output directory"""
        self.logger.info(bold("copying static files... "), nonl=True)
        ensuredir(os.path.join(self.outdir, '_static'))

        for static_path in self.config["tojupyter_static_file_path"]:
            entry = os.path.join(self.confdir, static_path)
            if not os.path.exists(entry):
                self.logger.warning(
                    "tojupyter_static_path entry {} does not exist"
                    .format(entry))
            else:
                copy_asset(entry, os.path.join(self.outdir, "_static"))
        self.logger.info("done")

    def finish(self):
        """Finish the build process"""
        self.finish_tasks.add_task(self.copy_static_files)
