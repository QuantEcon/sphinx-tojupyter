import codecs
import os.path
import docutils.io
import docutils

import nbformat
from sphinx.util.osutil import ensuredir, os_path
from ..writers.jupyter import JupyterWriter
from sphinx.builders import Builder
from sphinx.util.console import bold, darkgreen, brown
from sphinx.util.fileutil import copy_asset
from ..writers.execute_nb import ExecuteNotebookWriter
from ..writers.make_site import MakeSiteWriter
from ..writers.convert import convertToHtmlWriter
from dask.distributed import Client, progress
from sphinx.util import logging
import time
from ..writers.utils import copy_dependencies

class JupyterBuilder(Builder):
    """
    Builds Jupyter Notebook
    """
    name = "jupyter"
    format = "ipynb"
    out_suffix = ".ipynb"
    allow_parallel = True

    _writer_class = JupyterWriter
    _make_site_class = MakeSiteWriter
    dask_log = dict()
    futuresInfo = dict()
    futures = []
    threads_per_worker = 1
    n_workers = 1
    logger = logging.getLogger(__name__)

    def init(self):
        ### initializing required classes
        self._execute_notebook_class = ExecuteNotebookWriter(self)
        self._make_site_class = MakeSiteWriter(self)
        self.executedir = str(self.outdir) + '/executed'
        self.reportdir = str(self.outdir) + '/reports/'
        self.errordir = str(self.outdir) + "/reports/{}"
        self.downloadsdir = str(self.outdir) + "/_downloads"
        self.downloadsExecutedir = self.downloadsdir + "/executed"
        self.client = None
        self.execution_status_code = 0

        # Check default language is defined in the jupyter kernels
        def_lng = self.config["tojupyter_default_lang"]
        if  def_lng not in self.config["tojupyter_kernels"]:
            self.logger.warning(
                "Default language defined in conf.py ({}) is not "
                "defined in the tojupyter_kernels in conf.py. "
                "Set default language to python3"
                .format(def_lng))
            self.config["tojupyter_default_lang"] = "python3"

        #threads per worker for dask distributed processing
        if "tojupyter_threads_per_worker" in self.config:
            self.threads_per_worker = self.config["tojupyter_threads_per_worker"]

        #number of workers for dask distributed processing
        if "tojupyter_number_workers" in self.config:
            self.n_workers = self.config["tojupyter_number_workers"]

        # start a dask client to process the notebooks efficiently. 
        # processes = False. This is sometimes preferable if you want to avoid inter-worker communication and your computations release the GIL. This is common when primarily using NumPy or Dask Array.

        if (self.config["tojupyter_execute_notebooks"]):
            self.client = Client(processes=False, threads_per_worker = self.threads_per_worker, n_workers = self.n_workers)
            self.execution_vars = {
                'target': 'website',
                'dependency_lists': self.config["tojupyter_dependency_lists"],
                'executed_notebooks': [],
                'delayed_notebooks': dict(),
                'futures': [],
                'delayed_futures': [],
                'destination': self.executedir
            }

        if (self.config["tojupyter_download_nb_execute"]):
            if self.client is None:
                self.client = Client(processes=False, threads_per_worker = self.threads_per_worker, n_workers = self.n_workers)
            self.download_execution_vars = {
                'target': 'downloads',
                'dependency_lists': self.config["tojupyter_dependency_lists"],
                'executed_notebooks': [],
                'delayed_notebooks': dict(),
                'futures': [],
                'delayed_futures': [],
                'destination': self.downloadsExecutedir
            }

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
        self.writer = self._writer_class(self)

        ## copies the dependencies to the notebook folder
        copy_dependencies(self)

        if (self.config["tojupyter_execute_notebooks"]):
             ## copies the dependencies to the executed folder
            copy_dependencies(self, self.executedir)

        if (self.config["tojupyter_download_nb_execute"]):
            copy_dependencies(self, self.downloadsExecutedir)

    def write_doc(self, docname, doctree):
        # work around multiple string % tuple issues in docutils;
        # replace tuples in attribute values with lists
        self.docname = docname
        doctree = doctree.deepcopy()
        destination = docutils.io.StringOutput(encoding="utf-8")
        ### print an output for downloading notebooks as well with proper links if variable is set
        if "tojupyter_urlpath" in self.config:
            self.writer._set_ref_urlpath(self.config["tojupyter_urlpath"])
        else:
            self.writer._set_ref_urlpath(None)
        if "tojupyter_image_urlpath" in self.config:
            self.writer._set_tojupyter_image_urlpath((self.config["tojupyter_image_urlpath"]))
        else:
            self.writer._set_tojupyter_image_urlpath(None)
        if "tojupyter_download_nb" in self.config and self.config["tojupyter_download_nb"]:

            outfilename = os.path.join(self.downloadsdir, os_path(docname) + self.out_suffix)
            ensuredir(os.path.dirname(outfilename))
            self.writer._set_ref_urlpath(self.config["tojupyter_download_nb_urlpath"])
            self.writer._set_tojupyter_image_urlpath((self.config["tojupyter_download_nb_image_urlpath"]))
            self.writer.write(doctree, destination)

            # get a NotebookNode object from a string
            nb = nbformat.reads(self.writer.output, as_version=4)
            nb = self.update_Metadata(docname, nb)
            try:
                with codecs.open(outfilename, "w", "utf-8") as f:
                    self.writer.output = nbformat.writes(nb, version=4)
                    f.write(self.writer.output)
            except (IOError, OSError) as err:
                self.warn("error writing file %s: %s" % (outfilename, err))

            ### executing downloaded notebooks
            if (self.config['tojupyter_download_nb_execute']):
                strDocname = str(docname)
                if strDocname in self.download_execution_vars['dependency_lists'].keys():
                    self.download_execution_vars['delayed_notebooks'].update({strDocname: nb})
                else:
                    self._execute_notebook_class.execute_notebook(self, nb, docname, self.download_execution_vars, self.download_execution_vars['futures'])

        ### output notebooks for executing
        self.writer.write(doctree, destination)

        # get a NotebookNode object from a string
        nb = nbformat.reads(self.writer.output, as_version=4)
        nb = self.update_Metadata(docname, nb)

        ### execute the notebook
        if (self.config["tojupyter_execute_notebooks"]):
            strDocname = str(docname)
            if strDocname in self.execution_vars['dependency_lists'].keys():
                self.execution_vars['delayed_notebooks'].update({strDocname: nb})
            else:
                self._execute_notebook_class.execute_notebook(self, nb, docname, self.execution_vars, self.execution_vars['futures'])
        else:
            #do not execute
            if (self.config['tojupyter_generate_html']):
                language_info = nb.metadata.kernelspec.language
                self._convert_class = convertToHtmlWriter(self)
                self._convert_class.convert(nb, docname, language_info, self.outdir)

        ### mkdir if the directory does not exist
        outfilename = os.path.join(self.outdir, os_path(docname) + self.out_suffix)
        ensuredir(os.path.dirname(outfilename))

        try:
            with codecs.open(outfilename, "w", "utf-8") as f:
                self.writer.output = nbformat.writes(nb, version=4)
                f.write(self.writer.output)
        except (IOError, OSError) as err:
            self.logger.warning("error writing file %s: %s" % (outfilename, err))

    def update_Metadata(self, docname, nb):
        """Update Metadata for Jupyter Notebook"""
        if "tojupyter_make_site" in self.config and self.config['tojupyter_make_site']:
            # Set Next and Previous
            relations = self.env.collect_relations()
            related = relations.get(docname)
            titles = self.env.titles
            if related and related[2]:
                try:
                    link = self.get_relative_uri(docname, related[2])
                    # link is document uri (i.e. docname) as specified in index
                    if link in self.config.tojupyter_nextprev_ignore:
                        pass
                    else:
                        title_relation = titles[related[2]]
                        # Filter out non-text elements like index entries
                        if len(title_relation.children) > 1:
                            text_nodes = [item for item in title_relation if isinstance(item, docutils.nodes.Text)]
                            title = "".join([item.astext() for item in text_nodes])
                        else:
                            title = title_relation.children[0].astext()
                        # Set next_doc metadata
                        next_doc = {
                            'link': link,
                            'title': title
                        }
                        nb.metadata.next_doc = next_doc
                except KeyError:
                    self.logger.warning(
                        "[NB Metadata] No next_doc relation is found for: {}"
                        .format(docname))
            if related and related[1]:
                try:
                    link = self.get_relative_uri(docname, related[1])
                    # link is document uri (i.e. docname) as specified in index
                    if link in self.config.tojupyter_nextprev_ignore:
                        pass
                    else:
                        title_relation = titles[related[1]]
                        # Filter out non-text elements like index entries
                        if len(title_relation.children) > 1:
                            text_nodes = [item for item in title_relation if isinstance(item, docutils.nodes.Text)]
                            title = "".join([item.astext() for item in text_nodes])
                        else:
                            title = title_relation.children[0].astext()
                        # Set prev_doc metadata
                        prev_doc = {
                            'link': link,
                            'title': title
                        }
                        nb.metadata.prev_doc = prev_doc
                except KeyError:
                    self.logger.warning(
                        "[NB Metadata] No prev_doc relation is found for: {}"
                        .format(docname))
        # Set Compile Datetime
        nb.metadata.date = time.time()
        return nb

    def copy_static_files(self):
        # copy all static files
        self.logger.info(bold("copying static files... "), nonl=True)
        ensuredir(os.path.join(self.outdir, '_static'))
        if (self.config["tojupyter_execute_notebooks"]):
            self.logger.info(bold("copying static files to executed folder... \n"), nonl=True)
            ensuredir(os.path.join(self.executed_notebook_dir, '_static'))


        # excluded = Matcher(self.config.exclude_patterns + ["**/.*"])
        for static_path in self.config["tojupyter_static_file_path"]:
            entry = os.path.join(self.confdir, static_path)
            if not os.path.exists(entry):
                self.logger.warning(
                    "tojupyter_static_path entry {} does not exist"
                    .format(entry))
            else:
                copy_asset(entry, os.path.join(self.outdir, "_static"))
                if (self.config["tojupyter_execute_notebooks"]):
                    copy_asset(entry, os.path.join(self.executed_notebook_dir, "_static"))
        self.logger.info("done")


    def finish(self):
        self.finish_tasks.add_task(self.copy_static_files)

        if self.config["tojupyter_execute_notebooks"]:
            self.save_executed(self.execution_vars,'website')

        if self.config["tojupyter_download_nb_execute"]:
            self.save_executed(self.download_execution_vars, 'downloads')

        if "tojupyter_make_site" in self.config and self.config['tojupyter_make_site']:
            self._make_site_class.build_website(self)

        exit(self.execution_status_code)

    def save_executed(self, params, target):

            # watch progress of the execution of futures
            self.logger.info(bold("Starting notebook execution for %s and html conversion(if set in config)..."), target)
            #progress(self.futures)

            # save executed notebook
            error_results = self._execute_notebook_class.save_executed_notebook(self, params)
