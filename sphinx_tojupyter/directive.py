"""
Sphinx directives for Jupyter notebook generation.

This module provides custom RST directives for controlling notebook generation:
- jupyter: Insert cell breaks and slide markers
- jupyter-dependency: Specify file dependencies
"""
from docutils import nodes
from docutils.parsers.rst import directives, Directive


class jupyter_node(nodes.Structural, nodes.Element):
    """
    Custom docutils node for Jupyter-specific markup.
    
    This node carries metadata about cell breaks, slides, and file dependencies.
    """
    pass


class Jupyter(Directive):
    """
    Directive for controlling notebook cell generation.
    
    Usage::
    
        .. jupyter::
           :cell-break:
           
        .. jupyter::
           :slide: enable
           :slide-type: slide
           
    Options:
        cell-break: Force a new notebook cell
        slide: Enable/disable slide mode (enable/disable)
        slide-type: Type of slide (slide, subslide, fragment, etc.)
    """

    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {'cell-break': directives.flag,
                   'slide': directives.unchanged,
                   'slide-type': directives.unchanged}
    has_content = True
    add_index = False

    def run(self):
        # we create a new cell and we add it to the node tree
        node = jupyter_node()
        if 'cell-break' in self.options:
            node['cell-break'] = True
        if 'slide' in self.options:
            if self.options['slide'] == 'enable':
                node['slide'] = True
            else:
                node['slide'] = False
        if 'slide-type' in self.options:
            #node.parent.append(nodes.literal(self.content.data))
            node['slide-type'] = self.options['slide-type']

        # we return the result
        return [ node ]


class JupyterDependency(Directive):
    """
    Directive for specifying file dependencies.
    
    Usage::
    
        .. jupyter-dependency:: data/dataset.csv
        
    This ensures the specified file is copied to the notebook output directory.
    """
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}
    has_content = False
    add_index = False

    def run(self):
        # we create a new cell and add uri reference to specified file and we add it to the node tree
        node = jupyter_node()
        node['uri'] = directives.uri(self.arguments[0])
        # we return the result
        return [node]

