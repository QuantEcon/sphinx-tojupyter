from __future__ import unicode_literals
import re
import nbformat.v4
from docutils import nodes, writers
from .code import JupyterCodeTranslator
from ..utils import JupyterOutputCellGenerators
from shutil import copyfile
import copy
import os
import base64
import mimetypes
from sphinx.util import logging

logger = logging.getLogger(__name__)


class JupyterTranslator(JupyterCodeTranslator, object):
    """ Jupyter Translator for Text and Code
    """

    SPLIT_URI_ID_REGEX = re.compile(r"([^\#]*)\#?(.*)")

    def __init__(self, builder, document):
        super(JupyterTranslator, self).__init__(builder, document)

        # Settings
        self.sep_lines = "  \n"
        self.sep_paras = "\n\n"
        self.indent_char = " "
        self.indent = self.indent_char * 4
        self.default_ext = ".ipynb"
        self.urlpath = builder.urlpath
        # Variables used in visit/depart
        self.in_code_block = False  # if False, it means in markdown_cell
        self.in_block_quote = False
        self.block_quote_type = "block-quote"
        self.in_note = False
        self.in_attribution = False
        self.in_rubric = False
        self.in_footnote = False
        self.in_footnote_reference = False
        self.in_download_reference = False
        self.in_inpage_reference = False
        self.in_caption = False
        self.in_toctree = False
        self.in_list = False
        self.in_math = False
        self.in_math_block = False

        self.code_lines = []
        self.markdown_lines = []

        self.indents = []
        self.section_level = 0
        self.bullets = []
        self.list_item_starts = []
        self.in_topic = False
        self.reference_text_start = 0
        self.in_reference = False
        self.list_level = 0
        self.remove_next_content = False
        self.in_citation = False
        self.math_block_label = None

        self.images = []
        self.files = []
        self.table_builder = None

        # Slideshow option
        self.metadata_slide = False  #False is the value by default for all the notebooks
        self.slide = "slide" #value by default

    def _image_to_base64(self, image_path):
        """
        Convert an image file to a base64-encoded data URI.
        
        Parameters
        ----------
        image_path : str
            Path to the image file (can be relative to source or build directory)
        
        Returns
        -------
        str
            Base64-encoded data URI (e.g., 'data:image/png;base64,...') or None if file not found
        """
        # Try to find the image file
        # First try relative to the build directory
        full_path = os.path.join(self.builder.outdir, image_path)
        if not os.path.exists(full_path):
            # Try relative to source directory
            full_path = os.path.join(self.builder.srcdir, image_path)
        if not os.path.exists(full_path):
            # Try as absolute path
            full_path = image_path
        
        if not os.path.exists(full_path):
            return None
        
        try:
            # Read the image file as binary
            with open(full_path, 'rb') as f:
                image_data = f.read()
            
            # Encode as base64
            encoded = base64.b64encode(image_data).decode('ascii')
            
            # Determine MIME type
            mime_type, _ = mimetypes.guess_type(full_path)
            if mime_type is None:
                # Default to PNG if we can't determine
                mime_type = 'image/png'
            
            # Create data URI
            data_uri = f"data:{mime_type};base64,{encoded}"
            return data_uri
        except Exception as e:
            # If anything goes wrong, return None to fall back to file path
            print(f"Warning: Could not embed image {image_path}: {e}")
            return None

    def _copy_glued_image(self, image_path, filename):
        """
        Copy a glued image to the _build/jupyter/glue/ directory for URL-based references.
        
        Parameters
        ----------
        image_path : str
            Original path to the image file
        filename : str
            Filename to use in the destination directory
        
        Returns
        -------
        bool
            True if copy was successful, False otherwise
        """
        # Try to find the source image file
        full_path = os.path.join(self.builder.outdir, image_path)
        if not os.path.exists(full_path):
            full_path = os.path.join(self.builder.srcdir, image_path)
        if not os.path.exists(full_path):
            full_path = image_path
        
        if not os.path.exists(full_path):
            print(f"Warning: Could not find glued image to copy: {image_path}")
            return False
        
        try:
            # Create the glue directory
            glue_dir = os.path.join(self.builder.outdir, 'glue')
            os.makedirs(glue_dir, exist_ok=True)
            
            # Copy the file
            dest_path = os.path.join(glue_dir, filename)
            copyfile(full_path, dest_path)
            
            # Log for user
            rel_dest = os.path.relpath(dest_path, self.builder.outdir)
            print(f"Copied glued image: {rel_dest}")
            
            return True
        except Exception as e:
            print(f"Warning: Failed to copy glued image {image_path}: {e}")
            return False

    # specific visit and depart methods
    # ---------------------------------

    def visit_document(self, node):
        """at start
        """
        JupyterCodeTranslator.visit_document(self, node)

    def depart_document(self, node):
        """at end
        Almost the exact same implementation as that of the superclass.


        Notes
        -----
        [1] if copyfile is not graceful should catch exception if file not found / issue warning in sphinx
        [2] should this be moved to CodeTranslator for support files when producing code only notebooks?
        """
        self.add_markdown_cell()
        #Parse .. jupyter-dependency::
        if len(self.files) > 0:
            for fl in self.files:
                src_fl = os.path.join(self.builder.srcdir, fl)
                out_fl = os.path.join(self.builder.outdir, os.path.basename(fl))   #copy file to same location as notebook (remove dir structure)
                #Check if output directory exists
                out_dir = os.path.dirname(out_fl)
                if not os.path.exists(out_dir):
                    os.makedirs(out_dir)
                print("Copying {} to {}".format(src_fl, out_fl))
                copyfile(src_fl, out_fl)
        JupyterCodeTranslator.depart_document(self, node)
    
    # =========
    # Sections
    # =========

    def visit_only(self, node):
        pass

    def depart_only(self, node):
        pass

    def visit_topic(self, node):
        self.in_topic = True

    def depart_topic(self, node):
        self.in_topic = False

    def visit_section(self, node):
        self.section_level += 1

    def depart_section(self, node):
        self.section_level -= 1

    #=================
    # Inline elements
    #=================
    def visit_Text(self, node):

        text = node.astext()

        #Escape Special markdown chars except in code block
        if self.in_code_block == False:
            text = text.replace("$", r"\$")

        if self.in_math:
            text = '$ {} $'.format(text.strip())
        elif self.in_math_block and self.math_block_label:
            text = "$$\n{0}{1}$${2}".format(
                        text.strip(), self.math_block_label, self.sep_paras
                    )
            self.math_block_label = None
        elif self.in_math_block:
            text = "$$\n{0}\n$${1}".format(text.strip(), self.sep_paras)

        if self.in_code_block:
            self.code_lines.append(text)
        elif self.table_builder:
            self.table_builder['line_pending'] += text
        elif self.in_block_quote or self.in_note:
            if self.block_quote_type == "epigraph":
                self.markdown_lines.append(text.replace("\n", "\n> ")) #Ensure all lines are indented
            else:
                self.markdown_lines.append(text)
        elif self.in_caption and self.in_toctree:
            self.markdown_lines.append("# {}".format(text))
        else:
            self.markdown_lines.append(text)

    def depart_Text(self, node):
        pass

    def visit_attribution(self, node):
        self.in_attribution = True
        self.markdown_lines.append("> ")

    def depart_attribution(self, node):
        self.in_attribution = False
        self.markdown_lines.append("\n")

    # image
    def visit_image(self, node):
        """
        Notes
        -----
        1. Should this use .has_attrs()?
        2. the scale, height and width properties are not combined in this
        implementation as is done in http://docutils.sourceforge.net/docs/ref/rst/directives.html#image

        """
        uri = node.attributes["uri"]
        self.images.append(uri)             #TODO: list of image files
        
        # Check if this is a glued image (from jupyter_execute or _build/jupyter_execute)
        original_uri = uri
        is_glued_image = "jupyter_execute" in uri or "_build/jupyter_execute" in uri
        
        if is_glued_image:
            # Check if user wants to use a URL path for glued images
            if hasattr(self.builder.config, 'tojupyter_glue_urlpath') and self.builder.config.tojupyter_glue_urlpath:
                # Copy image to glue directory and reference with base URL + /glue/filename
                filename = os.path.basename(uri)
                self._copy_glued_image(original_uri, filename)
                base_url = self.builder.config.tojupyter_glue_urlpath.rstrip('/')
                uri = f"{base_url}/glue/{filename}"
            elif hasattr(self.builder.config, 'tojupyter_glue_images_urlpath') and self.builder.config.tojupyter_glue_images_urlpath:
                # Alternative config name for clarity
                filename = os.path.basename(uri)
                self._copy_glued_image(original_uri, filename)
                base_url = self.builder.config.tojupyter_glue_images_urlpath.rstrip('/')
                uri = f"{base_url}/glue/{filename}"
            else:
                # Default: embed as base64 for standalone notebooks
                data_uri = self._image_to_base64(uri)
                if data_uri:
                    uri = data_uri
        
        if self.tojupyter_image_urlpath and uri == original_uri:
            for file_path in self.tojupyter_static_file_path:
                if file_path in uri:
                    uri = uri.replace(file_path +"/", self.tojupyter_image_urlpath)
                    break  #don't need to check other matches
        attrs = node.attributes
        if self.tojupyter_images_markdown:
            #-Construct MD image
            image = "![{0}]({0})".format(uri)
        else:
            # Construct HTML image
            image = '<img src="{}" '.format(uri)
            if "alt" in attrs.keys():
                image += 'alt="{}" '.format(attrs["alt"])
            style = ""
            if "width" in attrs.keys():
                style += "width:{};".format(attrs["width"])
            if "height" in attrs.keys():
                style += "height:{};".format(attrs["height"])
            if "scale" in attrs.keys():
                style = "width:{0}%;height:{0}%".format(attrs["scale"])
            image += 'style="{}" '.format(style)
            if "align" in attrs.keys():
                image += 'align="{}"'.format(attrs["align"])
            image = image.rstrip() + ">\n\n"  #Add double space for html
        self.markdown_lines.append(image)
    
    def depart_image(self, node):
        if self.tojupyter_images_markdown:
            self.markdown_lines.append("\n\n")

    # math
    def visit_math(self, node):
        """inline math"""

        # With sphinx < 1.8, a math node has a 'latex' attribute, from which the
        # formula can be obtained and added to the text.

        # With sphinx >= 1.8, a math node has no 'latex' attribute, which mean
        # that a flag has to be raised, so that the in visit_Text() we know that
        # we are dealing with a formula.

        try: # sphinx < 1.8
            math_text = node.attributes["latex"].strip()
        except KeyError:
            # sphinx >= 1.8
            self.in_math = True

            # the flag is raised, the function can be exited.
            return

        formatted_text = "$ {} $".format(math_text)

        if self.table_builder:
            self.table_builder['line_pending'] += formatted_text
        else:
            self.markdown_lines.append(formatted_text)

    def depart_math(self, node):
        self.in_math = False

    def visit_displaymath(self, node):
        """directive math"""
        # displaymath is called with sphinx < 1.8 only

        math_text = node.attributes["latex"].strip()

        if self.in_list and node["label"]:
            self.markdown_lines.pop()  #remove entry \n from table builder

        if self.list_level == 0:
            formatted_text = "$$\n{0}\n$${1}".format(
                math_text, self.sep_paras)
        else:
            formatted_text = "$$\n{0}\n$${1}".format(
                math_text, self.sep_paras)

        #check for labelled math
        if node["label"]:
            #Use \tags in the LaTeX environment
            referenceBuilder = " \\tag{" + str(node["number"]) + "}\n"                  #node["ids"] should always exist for labelled displaymath
            formatted_text = formatted_text.rstrip("$$\n") + referenceBuilder + "$${}".format(self.sep_paras)

        self.markdown_lines.append(formatted_text)

    def depart_displaymath(self, node):
        if self.in_list:
            self.markdown_lines[-1] = self.markdown_lines[-1][:-1]  #remove excess \n

    def visit_math_block(self, node):
        """directive math"""
        # visit_math_block is called only with sphinx >= 1.8

        self.in_math_block = True

        if self.in_list and "label" in node and node["label"]:
            self.markdown_lines.pop()  #remove entry \n from table builder

        #check for labelled math
        if "label" in node and node["label"]:
            #Use \tags in the LaTeX environment
            try:
                docname = node['docname']
                chapter = self.builder.env.toc_secnumbers[docname][''][0]
                tag = str(chapter) + "." + str(node["number"])
            except KeyError:
                tag = str(node["number"])
            referenceBuilder = " \\tag{" + tag + "}\n"
            #node["ids"] should always exist for labelled displaymath
            self.math_block_label = referenceBuilder

    def depart_math_block(self, node):
        if self.in_list:
            self.markdown_lines[-1] = self.markdown_lines[-1][:-1]  #remove excess \n

        self.in_math_block = False

    def visit_table(self, node):
        self.table_builder = dict()
        self.table_builder['column_widths'] = []
        self.table_builder['lines'] = []
        self.table_builder['line_pending'] = ""

        if 'align' in node:
            self.table_builder['align'] = node['align']
        else:
            self.table_builder['align'] = "center"

    def depart_table(self, node):
        table_lines = "".join(self.table_builder['lines'])
        self.markdown_lines.append(table_lines)
        self.table_builder = None

    def visit_thead(self, node):
        """ Table Header """
        self.table_builder['current_line'] = 0

    def depart_thead(self, node):
        """ create the header line which contains the alignment for each column """
        header_line = "|"
        for col_width in self.table_builder['column_widths']:
            header_line += self.generate_alignment_line(
                col_width, self.table_builder['align'])
            header_line += "|"

        self.table_builder['lines'].append(header_line + "\n")

    def generate_alignment_line(self, line_length, alignment):
        left = ":" if alignment != "right" else "-"
        right = ":" if alignment != "left" else "-"
        return left + "-" * (int(line_length) - 2) + right

    def visit_colspec(self, node):
        self.table_builder['column_widths'].append(node['colwidth'])

    def visit_row(self, node):
        self.table_builder['line_pending'] = "|"

    def depart_row(self, node):
        finished_line = self.table_builder['line_pending'] + "\n"
        self.table_builder['lines'].append(finished_line)

    def visit_entry(self, node):
        pass

    def depart_entry(self, node):
        self.table_builder['line_pending'] += "|"

    def visit_raw(self, node):
        """
        Handle raw HTML/script blocks.
        
        By default (tojupyter_drop_raw_html=True), skip raw HTML nodes to prevent
        web-specific content like Thebe configuration from appearing in notebooks.
        Set tojupyter_drop_raw_html=False to preserve raw HTML if needed.
        """
        if self.tojupyter_drop_raw_html:
            if node.attributes.get('format') == 'html':
                raise nodes.SkipNode
        # Otherwise pass through
        pass


    def visit_rubric(self, node):
        self.in_rubric = True
        self.add_markdown_cell()
        if len(node.children) == 1 and node.children[0].astext() in ['Footnotes']:
            self.markdown_lines.append('**{}**\n\n'.format(node.children[0].astext()))
            raise nodes.SkipNode

    def depart_rubric(self, node):
        self.add_markdown_cell()
        self.in_rubric = False

    def visit_footnote_reference(self, node):
        self.in_footnote_reference = True
        refid = node.attributes['refid']
        ids = node.astext()
        # Use Markdown-style link for footnotes
        link = "<sup>[{}](#{})</sup>".format(ids, refid)
        self.markdown_lines.append(link)
        raise nodes.SkipNode

    def depart_footnote_reference(self, node):
        self.in_footnote_reference = False

    def visit_footnote(self, node):
        self.in_footnote = True

    def depart_footnote(self, node):
        self.in_footnote = False

    def visit_download_reference(self, node):
        self.in_download_reference = True
        html = "<a href={} download>".format(node["reftarget"])
        self.markdown_lines.append(html)

    def depart_download_reference(self, node):
        self.markdown_lines.append("</a>")
        self.in_download_reference = False

    #================
    # markdown cells
    #================

    # general paragraph
    def visit_paragraph(self, node):
        pass

    def depart_paragraph(self, node):
        if self.list_level > 0:
            self.markdown_lines.append(self.sep_lines)
        elif self.table_builder:
            pass
        elif self.block_quote_type == "epigraph":
            try:
                attribution = node.parent.children[1]
                self.markdown_lines.append("\n>\n")   #Continue block for attribution
            except:
                self.markdown_lines.append(self.sep_paras)
        else:
            self.markdown_lines.append(self.sep_paras)

    # title(section)
    def visit_title(self, node):
        JupyterCodeTranslator.visit_title(self, node)

        self.add_markdown_cell()
        if self.in_topic:
            # In topic (TOC), increase heading level by 1
            self.markdown_lines.append(
                "{} ".format("#" * (self.section_level + 1)))
        elif self.table_builder:
            self.markdown_lines.append(
                "### {}\n".format(node.astext()))
        else:
            self.markdown_lines.append(
                "{} ".format("#" * self.section_level))

    def depart_title(self, node):
        if not self.table_builder:
            self.markdown_lines.append(self.sep_paras)

    # emphasis(italic)
    def visit_emphasis(self, node):
        self.markdown_lines.append("*")

    def depart_emphasis(self, node):
        self.markdown_lines.append("*")

    # strong(bold)
    def visit_strong(self, node):
        self.markdown_lines.append("**")

    def depart_strong(self, node):
        self.markdown_lines.append("**")

    def visit_literal(self, node):
        if self.in_download_reference:
            return
        self.markdown_lines.append("`")

    def depart_literal(self, node):
        if self.in_download_reference:
            return
        self.markdown_lines.append("`")

    # inline nodes (including glued text from myst-nb)
    def visit_inline(self, node):
        """
        Handle inline nodes, including glued text from MyST-NB.
        
        MyST-NB's {glue:text} creates nodes.inline with class 'pasted-text'.
        These nodes contain the glued variable value as text children.
        We just let the text flow through normally.
        """
        # Glued text will have 'pasted-text' class
        # No special formatting needed - text children are handled by visit_Text
        pass

    def depart_inline(self, node):
        pass

    # figures
    def visit_figure(self, node):
        pass

    def depart_figure(self, node):
        self.markdown_lines.append(self.sep_lines)

    # reference
    def visit_reference(self, node):
        """anchor link"""
        self.in_reference = True
        self.markdown_lines.append("[")
        self.reference_text_start = len(self.markdown_lines)

    def depart_reference(self, node):
        if self.in_topic:
            # Jupyter Notebook uses the target text as its id
            uri_text = "".join(
                self.markdown_lines[self.reference_text_start:]).strip()
            uri_text = re.sub(
                self.URI_SPACE_REPLACE_FROM, self.URI_SPACE_REPLACE_TO, uri_text)
            # Sanitise special characters from links
            special_chars = ["`"]
            for char in special_chars:
                uri_text = uri_text.replace(char, "")
            formatted_text = "](#{})".format(uri_text)
            self.markdown_lines.append(formatted_text)
        else:
            # if refuri exists, then it includes id reference(#hoge)
            if "refuri" in node.attributes:
                refuri = node["refuri"]
                # add default extension(.ipynb) for internal links
                if "internal" in node.attributes and node.attributes["internal"] == True:
                    refuri = self.add_extension_to_inline_link(refuri, self.default_ext)
                    # If a base urlpath is configured, and the refuri is neither an absolute
                    # URL nor an anchor nor an absolute path, prefix it so cross-document
                    # links point to the configured site URL.
                    try:
                        base_url = self.urlpath
                    except AttributeError:
                        base_url = None
                    if base_url:
                        is_external = refuri.startswith("http://") or refuri.startswith("https://")
                        is_anchor = refuri.startswith("#")
                        is_abs_path = refuri.startswith("/")
                        if not (is_external or is_anchor or is_abs_path):
                            base = base_url.rstrip('/')
                            # strip any leading ./ from refuri to avoid duplicate dots
                            refuri = f"{base}/{refuri.lstrip('./')}"
            else:
                # in-page link
                if "refid" in node:
                    refid = node["refid"]
                    self.in_inpage_reference = True
                    # Markdown doesn't handle closing brackets very well
                    refid = refid.replace("(", "%28")
                    refid = refid.replace(")", "%29")
                    refuri = "#{}".format(refid)
                # error
                else:
                    self.error("Invalid reference")
                    refuri = ""

            # Handle special characters in refuri
            refuri = refuri.replace("(", "%28")
            refuri = refuri.replace(")", "%29")
            
            self.markdown_lines.append("]({})".format(refuri))

        if self.in_toctree:
            self.markdown_lines.append("\n")

        self.in_reference = False

    def visit_target(self, node):
        if "refid" in node.attributes:
            refid = node.attributes["refid"]
            self.markdown_lines.append("\n<a id='{}'></a>\n".format(refid))

    # list items
    def visit_bullet_list(self, node):
        self.list_level += 1

        # markdown does not have option changing bullet chars
        self.bullets.append("-")
        self.indents.append(len(self.bullets[-1] * 2))  #add two per level

    def depart_bullet_list(self, node):
        self.list_level -= 1
        if self.list_level == 0:
            self.markdown_lines.append(self.sep_paras)
            if self.in_topic:
                self.add_markdown_cell()
        if len(self.bullets):
            self.bullets.pop()
            self.indents.pop()
        

    def visit_enumerated_list(self, node):
        self.list_level += 1
        # markdown does not have option changing bullet chars
        self.bullets.append("1.")
        self.indents.append(len(self.bullets[-1]))

    def depart_enumerated_list(self, node):
        self.list_level -= 1
        if self.list_level == 0:
            self.markdown_lines.append(self.sep_paras)
        if len(self.bullets):
            self.bullets.pop()
            self.indents.pop()

    def visit_list_item(self, node):
        ## check if there is a list level
        if not len(self.bullets):
            return
        self.in_list = True
        head = "{} ".format(self.bullets[-1])
        self.markdown_lines.append(head)
        self.list_item_starts.append(len(self.markdown_lines))

    def depart_list_item(self, node):
        ## check if there is a list level
        if not len(self.list_item_starts):
            return
        self.in_list = False
        list_item_start = self.list_item_starts.pop()
        indent = self.indent_char * self.indents[-1]
        br_removed_flag = False

        # remove last breakline
        if self.markdown_lines and self.markdown_lines[-1][-1] == "\n":
            br_removed_flag = True
            self.markdown_lines[-1] = self.markdown_lines[-1][:-1]

        for i in range(list_item_start, len(self.markdown_lines)):
            self.markdown_lines[i] = self.markdown_lines[i].replace(
                "\n", "\n{}".format(indent))

        # add breakline
        if br_removed_flag:
            self.markdown_lines.append("\n")

    # definition list
    def visit_definition_list(self, node):
        self.markdown_lines.append("\n<dl style='margin: 20px 0;'>\n")

    def depart_definition_list(self, node):
        self.markdown_lines.append("\n</dl>{}".format(self.sep_paras))

    def visit_term(self, node):
        self.markdown_lines.append("<dt>")

    def depart_term(self, node):
        self.markdown_lines.append("</dt>\n")

    def visit_definition(self, node):
        self.markdown_lines.append("<dd>\n")

    def depart_definition(self, node):
        self.markdown_lines.append("</dd>\n")

    # field list
    def visit_field_list(self, node):
        self.visit_definition_list(node)

    def depart_field_list(self, node):
        self.depart_definition_list(node)

    def visit_field_name(self, node):
        self.visit_term(node)

    def depart_field_name(self, node):
        self.depart_term(node)

    def visit_field_body(self, node):
        self.visit_definition(node)

    def depart_field_body(self, node):
        self.depart_definition(node)

    # citation
    def visit_citation(self, node):
        self.in_citation = True
        if "ids" in node.attributes:
            ids = node.attributes["ids"]
            id_text = ""
            for id_ in ids:
                id_text += "{} ".format(id_)
            else:
                id_text = id_text[:-1]

            self.markdown_lines.append(
                "<a id='{}'></a>\n".format(id_text))

    def depart_citation(self, node):
        self.in_citation = False

    # label
    def visit_label(self, node):
        if self.in_footnote:
            ids = node.parent.attributes["ids"]
            id_text = ""
            for id_ in ids:
                id_text += "{} ".format(id_)
            else:
                id_text = id_text[:-1]
            # Use Markdown-style anchor
            self.markdown_lines.append("<a id='{}'></a>\n**[{}]** ".format(id_text, node.astext()))
            raise nodes.SkipNode
        if self.in_citation:
            self.markdown_lines.append(r"\[")

    def depart_label(self, node):
        if self.in_citation:
            self.markdown_lines.append(r"\] ")

    # ===============================================
    #  code blocks are implemented in the superclass
    # ===============================================

    def visit_block_quote(self, node):
        if self.in_list:               #allow for 4 spaces interpreted as block_quote
            self.markdown_lines.append("\n")
            return
        self.in_block_quote = True
        if "epigraph" in node.attributes["classes"]:
            self.block_quote_type = "epigraph"
        self.markdown_lines.append("> ")

    def depart_block_quote(self, node):
        if "epigraph" in node.attributes["classes"]:
            self.block_quote_type = "block-quote"
        self.markdown_lines.append("\n")
        self.in_block_quote = False

    def visit_literal_block(self, node):
        JupyterCodeTranslator.visit_literal_block(self, node)
        if self.in_code_block:
            self.add_markdown_cell()

    def depart_literal_block(self, node):
        JupyterCodeTranslator.depart_literal_block(self, node)

    def visit_note(self, node):
        self.in_note = True
        self.markdown_lines.append(">**Note**\n>\n>")

    def depart_note(self, node):
        self.in_note = False

    def depart_raw(self, node):
        # Pass through raw content
        self.markdown_lines.append("\n\n")
        

    # =============
    # Jupyter Nodes
    # =============

    def visit_jupyter_node(self, node):
        try:
            if 'cell-break' in node.attributes:
                self.add_markdown_cell()
            if 'slide' in node.attributes:
                self.metadata_slide = node['slide'] # this activates the slideshow metadata for the notebook
            if 'slide-type' in node.attributes:
                if "fragment" in node['slide-type']:
                    self.add_markdown_cell(slide_type=node['slide-type'])   #start a new cell
                self.slide = node['slide-type'] # replace the default value
        except:
            pass
        #Parse tojupyter_dependency directive (TODO: Should this be a separate node type?)
        try:
            self.files.append(node['uri'])
        except:
            pass

    def depart_jupyter_node(self, node):
        if 'cell-break' in node.attributes:
            pass
        if 'slide' in node.attributes:
            pass
        if 'slide-type' in node.attributes:
            pass

    # ==================
    # MyST-NB Glue Nodes
    # ==================

    def visit_PendingGlueReference(self, node):
        """
        Handle unresolved glue references from MyST-NB.
        
        PendingGlueReference nodes should be resolved by Sphinx's 
        ReplacePendingGlueReferences post-transform before reaching the writer.
        If we encounter one, it means the post-transform didn't run or failed.
        
        This can happen if:
        - MyST-NB is not properly configured
        - The referenced document doesn't exist
        - The glue key doesn't exist in the referenced document
        """
        # Try to get useful info for warning
        key = getattr(node, 'key', 'unknown')
        refdoc = getattr(node, 'refdoc', 'unknown')
        
        # Warn the user
        if hasattr(self, 'builder'):
            self.builder.warn(
                f"Unresolved glue reference to key '{key}' in document '{refdoc}'. "
                "This may indicate that MyST-NB's post-transform didn't run, or the "
                "referenced glue key doesn't exist. Check that myst-nb is properly "
                "configured and the glue key exists in the source document."
            )
        
        # Output placeholder text so the issue is visible
        self.markdown_lines.append(f"[Unresolved glue: {refdoc}::{key}]")
        
        # Skip children (if any)
        raise nodes.SkipNode

    def depart_PendingGlueReference(self, node):
        # Should never be called due to SkipNode, but include for completeness
        pass

    def visit_comment(self, node):
        raise nodes.SkipNode

    def visit_compact_paragraph(self, node):
        try:
            if node.attributes['toctree']:
                self.in_toctree = True
        except:
            pass  #Should this execute visit_compact_paragragh in BaseTranslator?

    def depart_compact_paragraph(self, node):
        try:
            if node.attributes['toctree']:
                self.in_toctree = False
        except:
            pass

    def visit_caption(self, node):
        self.in_caption = True

    def depart_caption(self, node):
        self.in_caption = False
        if self.in_toctree:
            self.markdown_lines.append("\n")

    # ==================
    # sphinx-proof Nodes
    # ==================
    
    def _get_proof_node_number(self, node, node_type):
        """
        Helper to get the number for a sphinx-proof enumerable node.
        Returns formatted number string or empty string if unnumbered.
        """
        try:
            # Check if node is unnumbered
            if 'nonumber' in node.attributes or node.get('nonumber', False):
                return ""
            
            label = node.get('label', '')
            if not label:
                return ""
            
            docname = self.builder.docname
            fig_num = self.builder.env.toc_fignumbers.get(docname, {})
            
            if node_type in fig_num and label in fig_num[node_type]:
                number = fig_num[node_type][label]
                return ".".join(map(str, number))
        except Exception:
            pass
        
        return ""

    def _format_proof_title(self, node, directive_name, display_name=None):
        """
        Helper to format the title/header for sphinx-proof directives.
        
        Args:
            node: The docutils node
            directive_name: The directive type (e.g., 'theorem', 'axiom')
            display_name: Optional custom display name (defaults to title-cased directive_name)
        """
        if display_name is None:
            display_name = directive_name.title()
        
        # Get number if available
        number = self._get_proof_node_number(node, directive_name)
        
        # Get title from node's title child if present
        title_text = ""
        if node.children:
            for child in node.children:
                if isinstance(child, nodes.title):
                    title_text = child.astext()
                    break
                elif child.tagname == 'title':
                    title_text = child.astext()
                    break
        
        # sphinx-proof may wrap titles in parentheses already - strip them
        if title_text:
            title_text = title_text.strip()
            if title_text.startswith('(') and title_text.endswith(')'):
                title_text = title_text[1:-1].strip()
        
        # Build the header
        header = f"**{display_name}"
        if number:
            header += f" {number}"
        header += "**"
        
        if title_text:
            header += f" ({title_text})"
        
        return header + "\n\n"

    def visit_theorem_node(self, node):
        """Handle sphinx-proof theorem directive."""
        self.add_markdown_cell()
        header = self._format_proof_title(node, 'theorem', 'Theorem')
        self.markdown_lines.append(header)
        # Remove title node from children to avoid duplicate processing
        self._remove_title_node(node)

    def depart_theorem_node(self, node):
        self.add_markdown_cell()
    
    def _remove_title_node(self, node):
        """Helper to remove title node from children to prevent duplicate rendering."""
        if node.children:
            node.children = [child for child in node.children 
                           if not (isinstance(child, nodes.title) or child.tagname == 'title')]

    def visit_axiom_node(self, node):
        """Handle sphinx-proof axiom directive."""
        self.add_markdown_cell()
        header = self._format_proof_title(node, 'axiom', 'Axiom')
        self.markdown_lines.append(header)
        self._remove_title_node(node)

    def depart_axiom_node(self, node):
        self.add_markdown_cell()

    def visit_lemma_node(self, node):
        """Handle sphinx-proof lemma directive."""
        self.add_markdown_cell()
        header = self._format_proof_title(node, 'lemma', 'Lemma')
        self.markdown_lines.append(header)
        self._remove_title_node(node)

    def depart_lemma_node(self, node):
        self.add_markdown_cell()

    def visit_definition_node(self, node):
        """Handle sphinx-proof definition directive."""
        self.add_markdown_cell()
        header = self._format_proof_title(node, 'definition', 'Definition')
        self.markdown_lines.append(header)
        self._remove_title_node(node)

    def depart_definition_node(self, node):
        self.add_markdown_cell()

    def visit_remark_node(self, node):
        """Handle sphinx-proof remark directive."""
        self.add_markdown_cell()
        header = self._format_proof_title(node, 'remark', 'Remark')
        self.markdown_lines.append(header)
        self._remove_title_node(node)

    def depart_remark_node(self, node):
        self.add_markdown_cell()

    def visit_conjecture_node(self, node):
        """Handle sphinx-proof conjecture directive."""
        self.add_markdown_cell()
        header = self._format_proof_title(node, 'conjecture', 'Conjecture')
        self.markdown_lines.append(header)
        self._remove_title_node(node)

    def depart_conjecture_node(self, node):
        self.add_markdown_cell()

    def visit_corollary_node(self, node):
        """Handle sphinx-proof corollary directive."""
        self.add_markdown_cell()
        header = self._format_proof_title(node, 'corollary', 'Corollary')
        self.markdown_lines.append(header)
        self._remove_title_node(node)

    def depart_corollary_node(self, node):
        self.add_markdown_cell()

    def visit_algorithm_node(self, node):
        """Handle sphinx-proof algorithm directive."""
        self.add_markdown_cell()
        header = self._format_proof_title(node, 'algorithm', 'Algorithm')
        self.markdown_lines.append(header)
        self._remove_title_node(node)

    def depart_algorithm_node(self, node):
        self.add_markdown_cell()

    def visit_criterion_node(self, node):
        """Handle sphinx-proof criterion directive."""
        self.add_markdown_cell()
        header = self._format_proof_title(node, 'criterion', 'Criterion')
        self.markdown_lines.append(header)
        self._remove_title_node(node)

    def depart_criterion_node(self, node):
        self.add_markdown_cell()

    def visit_example_node(self, node):
        """Handle sphinx-proof example directive."""
        self.add_markdown_cell()
        header = self._format_proof_title(node, 'example', 'Example')
        self.markdown_lines.append(header)
        self._remove_title_node(node)

    def depart_example_node(self, node):
        self.add_markdown_cell()

    def visit_property_node(self, node):
        """Handle sphinx-proof property directive."""
        self.add_markdown_cell()
        header = self._format_proof_title(node, 'property', 'Property')
        self.markdown_lines.append(header)
        self._remove_title_node(node)

    def depart_property_node(self, node):
        self.add_markdown_cell()

    def visit_observation_node(self, node):
        """Handle sphinx-proof observation directive."""
        self.add_markdown_cell()
        header = self._format_proof_title(node, 'observation', 'Observation')
        self.markdown_lines.append(header)
        self._remove_title_node(node)

    def depart_observation_node(self, node):
        self.add_markdown_cell()

    def visit_proposition_node(self, node):
        """Handle sphinx-proof proposition directive."""
        self.add_markdown_cell()
        header = self._format_proof_title(node, 'proposition', 'Proposition')
        self.markdown_lines.append(header)
        self._remove_title_node(node)

    def depart_proposition_node(self, node):
        self.add_markdown_cell()

    def visit_assumption_node(self, node):
        """Handle sphinx-proof assumption directive."""
        self.add_markdown_cell()
        header = self._format_proof_title(node, 'assumption', 'Assumption')
        self.markdown_lines.append(header)
        self._remove_title_node(node)

    def depart_assumption_node(self, node):
        self.add_markdown_cell()

    def visit_notation_node(self, node):
        """Handle sphinx-proof notation directive."""
        self.add_markdown_cell()
        header = self._format_proof_title(node, 'notation', 'Notation')
        self.markdown_lines.append(header)
        self._remove_title_node(node)

    def depart_notation_node(self, node):
        self.add_markdown_cell()

    def visit_proof_node(self, node):
        """Handle sphinx-proof proof directive (unenumerable)."""
        self.add_markdown_cell()
        # Proof directives are typically not numbered
        self.markdown_lines.append("**Proof.**\n\n")

    def depart_proof_node(self, node):
        self.add_markdown_cell()

    def visit_unenumerable_node(self, node):
        """
        Handle sphinx-proof unenumerable nodes (directives with :nonumber: option).
        These still have a type but no numbering.
        """
        self.add_markdown_cell()
        node_type = node.get('type', '')
        
        # Get title if present
        title_text = ""
        if node.children:
            for child in node.children:
                if isinstance(child, nodes.title):
                    title_text = child.astext()
                    break
                elif child.tagname == 'title':
                    title_text = child.astext()
                    break
        
        # Format header
        display_name = node_type.title() if node_type else "Note"
        header = f"**{display_name}**"
        
        if title_text:
            header += f" ({title_text})"
        
        self.markdown_lines.append(header + "\n\n")
        self._remove_title_node(node)

    def depart_unenumerable_node(self, node):
        self.add_markdown_cell()

    # 
    # Support for sphinx-exercise (enumberable nodes)
    # This work in sphinx-exercise is done in a post_transform
    # and relies on html translator to populate the numref
    # targets
    #

    def visit_exercise_enumerable_node(self, node):
        """
        TODO: This should be moved to spinx-exercise visit_ and depart_ methods
        """
        title = node.children[0].get("title", "")
        label = node.get("label", "")
        docname = self.builder.docname
        fig_num = self.builder.env.toc_fignumbers.get(docname, {})
        try:
            number = fig_num["exercise"][label]
            number = ".".join(map(str, number))
            title_text = self.builder.config.numfig_format["exercise"] % number
        except:
            logger.warn("[sphinx-tojupyter] Unable to parse enumerable exercise node with numfig format")
        title = node.children[0]
        title += nodes.Text(title_text)

    # ================
    # general methods
    # ================
    def add_markdown_cell(self, slide_type="slide", title=False):
        """split a markdown cell here

        * add the slideshow metadata
        * append `markdown_lines` to notebook
        * reset `markdown_lines`
        """
        line_text = "".join(self.markdown_lines)
        formatted_line_text = self.strip_blank_lines_in_end_of_block(line_text)
        slide_info = {'slide_type': self.slide}

        if len(formatted_line_text.strip()) > 0:
            new_md_cell = nbformat.v4.new_markdown_cell(formatted_line_text)
            if self.metadata_slide:  # modify the slide metadata on each cell
                new_md_cell.metadata["slideshow"] = slide_info
                self.slide = slide_type
            if title:
                new_md_cell.metadata["hide-input"] = True
            self.output["cells"].append(new_md_cell)
            self.markdown_lines = []


    @classmethod
    def split_uri_id(cls, uri):
        return re.search(cls.SPLIT_URI_ID_REGEX, uri).groups()

    @classmethod
    def add_extension_to_inline_link(cls, uri, ext):
        if "." not in uri:
            if len(uri) > 0 and uri[0] == "#":
                return uri
            uri, id_ = cls.split_uri_id(uri)
            if len(id_) == 0:
                return "{}{}".format(uri, ext)
            else:
                return "{}{}#{}".format(uri, ext, id_)
        #adjust relative references
        elif "../" in uri:
            # uri = uri.replace("../", "")
            uri, id_ = cls.split_uri_id(uri)
            if len(id_) == 0:
                return "{}{}".format(uri, ext)
            else:
                return "{}{}#{}".format(uri, ext, id_)

        return uri

    @classmethod
    def get_filename(cls,path):
        if "." in path and "/" in path:
            index = path.rfind('/')
            index1 = path.rfind('.')
            return path[index + 1:index1]
        else:
            return path
