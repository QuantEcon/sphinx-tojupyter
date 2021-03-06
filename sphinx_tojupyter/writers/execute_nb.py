import nbformat
from sphinx.util.osutil import ensuredir
import os.path
import shutil
import time
import json
from nbconvert.preprocessors import ExecutePreprocessor
from ..writers.convert import convertToHtmlWriter
from sphinx.util import logging
import dask
from dask.distributed import as_completed
from packaging import version
from io import open
import sys


class ExecuteNotebookWriter():
    
    """
    Executes jupyter notebook written in python or julia
    """
    logger = logging.getLogger(__name__)
    startFlag = 0
    def __init__(self, builderSelf):
        pass
    def execute_notebook(self, builderSelf, nb, filename, params, futures):
        execute_nb_config = builderSelf.config["tojupyter_execute_nb"]
        timeout = execute_nb_config["timeout"]
        filename = filename
        subdirectory = ''
        full_path = filename
        # check if there are subdirectories
        index = filename.rfind('/')
        if index > 0:
            subdirectory = filename[0:index]
            filename = filename[index + 1:]

        language = nb.metadata.kernelspec.language
        if (language.lower().find('python') != -1):
            language = 'python'
        elif (language.lower().find('julia') != -1):
            language = 'julia'

        ## adding latex metadata
        if builderSelf.config["tojupyter_target_pdf"]:
            nb = self.add_latex_metadata(builderSelf, nb, subdirectory, filename)

        # - Parse Directories and execute them - #
        self.execution_cases(builderSelf, params['destination'], True, subdirectory, language, futures, nb, filename, full_path)

    def add_latex_metadata(self, builder, nb, subdirectory, filename=""):

        ## initialize latex metadata
        if 'latex_metadata' not in nb['metadata']:
            nb['metadata']['latex_metadata'] = {}

        ## check for relative paths
        path = ''
        if subdirectory != '':
            path = "../"
            slashes = subdirectory.count('/')
            for i in range(slashes):
                path += "../"

        ## add check for logo here as well
        if nb.metadata.title:
            nb.metadata.latex_metadata.title = nb.metadata.title
        if "tojupyter_pdf_logo" in builder.config and builder.config['tojupyter_pdf_logo']:
            nb.metadata.latex_metadata.logo = path + builder.config['tojupyter_pdf_logo']
        
        if builder.config["tojupyter_bib_file"]:
            nb.metadata.latex_metadata.bib = path + builder.config["tojupyter_bib_file"]

        if builder.config["tojupyter_pdf_author"]:
            nb.metadata.latex_metadata.author = builder.config["tojupyter_pdf_author"]
        
        if builder.config["tojupyter_pdf_book_index"] is not None and (filename and builder.config["tojupyter_pdf_book_index"] in filename):
            nb.metadata.latex_metadata.tojupyter_pdf_book_title = builder.config["tojupyter_pdf_book_title"]

        # nb_string = json.dumps(nb_obj, indent=2, sort_keys=True)
        return nb

    def execution_cases(self, builderSelf, directory, allow_errors, subdirectory, language, futures, nb, filename, full_path):
        if subdirectory != '':
            builderSelf.executed_notebook_dir = directory + "/" + subdirectory
        else:
            builderSelf.executed_notebook_dir = directory

        ## ensure that executed notebook directory
        ensuredir(builderSelf.executed_notebook_dir)
        ## specifying kernels
        if language == 'python':
            if (sys.version_info > (3, 0)):
                # Python 3 code in this block
                ep = ExecutePreprocessor(timeout=-1, allow_errors=allow_errors, kernel_name='python3')
            else:
                # Python 2 code in this block
                ep = ExecutePreprocessor(timeout=-1, allow_errors=allow_errors, kernel_name='python2')
        elif language == 'julia':
            ep = ExecutePreprocessor(timeout=-1, allow_errors=allow_errors)

        ### calling this function before starting work to ensure it starts recording
        if (self.startFlag == 0):
            self.startFlag = 1
            builderSelf.client.get_task_stream()

        future = builderSelf.client.submit(ep.preprocess, nb, {"metadata": {"path": builderSelf.executed_notebook_dir, "filename": filename, "filename_with_path": full_path}})

        ### dictionary to store info for errors in future
        future_dict = { "filename": full_path, "filename_with_path": full_path, "language_info": nb['metadata']['kernelspec']}
        builderSelf.futuresInfo[future.key] = future_dict

        futures.append(future)


    def task_execution_time(self, builderSelf):
        ## calculates execution time of each task in client using get task stream
        task_Info_latest = builderSelf.client.get_task_stream()[-1]
        time_tuple = task_Info_latest['startstops'][0]

        if version.parse(dask.__version__) <  version.parse("2.10.0"):
            computing_time = time_tuple[2] - time_tuple[1]
        else:
            computing_time = time_tuple['stop'] - time_tuple['start']
        return computing_time

    def check_execution_completion(self, builderSelf, future, nb, error_results, count, total_count, futures_name, params):
        error_result = []
        builderSelf.dask_log['futures'].append(str(future))
        status = 'pass'

        # computing time for each task 
        computing_time = self.task_execution_time(builderSelf)

        # store the exceptions in an error result array
        if future.status == 'error':
            status = 'fail'
            try:
                builderSelf.execution_status_code = 1
            except:
                self.logger.warning("No execution status code defined in builder")

            for key,val in builderSelf.futuresInfo.items():
                if key == future.key:
                    filename_with_path = val['filename_with_path']
                    filename = val['filename']
                    language_info = val['language_info']
            error_result.append(future.exception())

        else:
            passed_metadata = nb[1]['metadata'] 
            filename = passed_metadata['filename']
            filename_with_path = passed_metadata['filename_with_path']
            executed_nb = nb[0]
            language_info = executed_nb['metadata']['kernelspec']
            executed_nb['metadata']['filename_with_path'] = filename_with_path
            executed_nb['metadata']['download_nb'] = builderSelf.config['tojupyter_download_nb']
            if "tojupyter_pdf_book_title" in builderSelf.config and builderSelf.config['tojupyter_pdf_book_title']:
                executed_nb['metadata']['site_title'] = builderSelf.config['tojupyter_pdf_book_title']
            if "tojupyter_download_nb" in builderSelf.config and builderSelf.config['tojupyter_download_nb']:
                executed_nb['metadata']['download_nb_path'] = builderSelf.config['tojupyter_download_nb_urlpath']
            if (futures_name.startswith('delayed') != -1):
                # adding in executed notebooks list
                params['executed_notebooks'].append(filename)
                key_to_delete = False
                for nb, arr in params['dependency_lists'].items():
                    executed = 0
                    for elem in arr:
                        if elem in params['executed_notebooks']:
                            executed += 1
                    if (executed == len(arr)):
                        key_to_delete = nb
                        notebook = params['delayed_notebooks'].get(nb)
                        builderSelf._execute_notebook_class.execute_notebook(builderSelf, notebook, nb, params, params['delayed_futures'])
                if (key_to_delete):
                    del params['dependency_lists'][str(key_to_delete)]
                    key_to_delete = False
            notebook_name = "{}.ipynb".format(filename)
            executed_notebook_path = os.path.join(passed_metadata['path'], notebook_name)

            #Parse Executed notebook to remove hide-output blocks
            for cell in executed_nb['cells']:
                if cell['cell_type'] == "code":
                    if cell['metadata']['hide-output']:
                        cell['outputs'] = []
            #Write Executed Notebook as File
            with open(executed_notebook_path, "wt", encoding="UTF-8") as f:
                nbformat.write(executed_nb, f)
            
            ## generate html if needed
            if (builderSelf.config['tojupyter_generate_html'] and params['target'] == 'website'):
                builderSelf._convert_class.convert(executed_nb, filename, language_info, params['destination'], passed_metadata['path'])
            
            ## generate pdfs if set to true
            if (builderSelf.config['tojupyter_target_pdf']):
                builderSelf._pdf_class.convert_to_latex(builderSelf, filename_with_path, executed_nb['metadata']['latex_metadata'])
                builderSelf._pdf_class.move_pdf(builderSelf)
            
        print('({}/{})  {} -- {} -- {:.2f}s'.format(count, total_count, filename, status, computing_time))
            


        # storing error info if any execution throws an error
        results = dict()
        results['runtime']  = computing_time
        results['filename'] = filename_with_path
        results['errors']   = error_result
        results['language'] = language_info
        error_results.append(results)
        return filename

    def save_executed_notebook(self, builderSelf, params):
        error_results = []

        builderSelf.dask_log['scheduler_info'] = builderSelf.client.scheduler_info()
        builderSelf.dask_log['futures'] = []

        ## create an instance of the class id config set
        if (builderSelf.config['tojupyter_generate_html'] and params['target'] == 'website'):
            builderSelf._convert_class = convertToHtmlWriter(builderSelf)

        # this for loop gathers results in the background
        total_count = len(params['futures'])
        count = 0
        update_count_delayed = 1
        for future, nb in as_completed(params['futures'], with_results=True, raise_errors=False):
            count += 1
            builderSelf._execute_notebook_class.check_execution_completion(builderSelf, future, nb, error_results, count, total_count, 'futures', params)

        for future, nb in as_completed(params['delayed_futures'], with_results=True, raise_errors=False):
            count += 1
            if update_count_delayed == 1:
                update_count_delayed = 0
                total_count += len(params['delayed_futures'])
            builderSelf._execute_notebook_class.check_execution_completion(builderSelf, future, nb, error_results, count, total_count,  'delayed_futures', params)

        return error_results

    def produce_code_execution_report(self, builderSelf, error_results, params, fln = "code-execution-results.json"):
        """
        Updates the JSON file that contains the results of the execution of each notebook.
        """
        ensuredir(builderSelf.reportdir)
        json_filename = builderSelf.reportdir + fln

        if os.path.isfile(json_filename):
            with open(json_filename, encoding="UTF-8") as json_file:
                json_data = json.load(json_file)
                temp_dictionary = dict()
                for item in json_data['results']:
                    name = item['filename']
                    language = item['language']
                    if name not in temp_dictionary:
                        temp_dictionary[name] = dict()
                    temp_dictionary[name][language] = item
                json_data['results'] = []

        else:
            temp_dictionary = dict()
            json_data = dict()
            json_data['results'] = []

        # Generate the data for the JSON file.
        for notebook_errors in error_results:
            runtime = int(notebook_errors['runtime'] * 10)
            name = notebook_errors['filename']
            language = notebook_errors['language']['name']
            seconds = (runtime % 600) / 10
            minutes = int(runtime / 600)

            extension = ''
            if (language.lower().find('python') != -1):
                extension = 'py'
            elif (language.lower().find('julia') != -1):
                extension = 'jl'

            nicer_runtime = str(minutes) + ":" + ("0" + str(seconds) if seconds < 10 else str(seconds))
            new_dictionary = {
                'filename': name,
                'runtime': nicer_runtime,
                'num_errors': len(notebook_errors['errors']),
                'extension': extension,
                'language': language
            }

            if name not in temp_dictionary:
                temp_dictionary[name] = dict()
            temp_dictionary[name][language] = new_dictionary

        temp_list = []
        for key in temp_dictionary:
            for second_key in temp_dictionary[key]:
                temp_list.append(temp_dictionary[key][second_key])

        for item in sorted(temp_list, key=lambda k: k['filename']):
            json_data['results'].append(item)
        json_data['run_time'] = time.strftime("%d-%m-%Y %H:%M:%S")

        try:
            if (sys.version_info > (3, 0)):
                with open(json_filename, "w") as json_file:
                    json.dump(json_data, json_file)
            else:
                with open(json_filename, "w") as json_file:
                    x = json.dumps(json_data, ensure_ascii=False)
                    if isinstance(x,str):
                        x = unicode(x, 'UTF-8')
                    json_file.write(x)
        except IOError:
            self.logger.warning("Unable to save lecture status JSON file. Does the {} directory exist?".format(builderSelf.reportdir))

    def produce_dask_processing_report(self, builderSelf, params, fln= "dask-reports.json"):
        """
            produces a report of dask execution
        """
        ensuredir(builderSelf.reportdir)
        json_filename = builderSelf.reportdir + fln

        try:
            if (sys.version_info > (3, 0)):
                with open(json_filename, "w") as json_file:
                    json.dump(builderSelf.dask_log, json_file)
            else:
               with open(json_filename, "w") as json_file:
                    x = json.dumps(builderSelf.dask_log, ensure_ascii=False)
                    if isinstance(x,str):
                        x = unicode(x, 'UTF-8')
                    json_file.write(x)
        except IOError:
            self.logger.warning("Unable to save dask reports JSON file. Does the {} directory exist?".format(builderSelf.reportdir))
