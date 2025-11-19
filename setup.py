# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

VERSION = 'v1.0.0'

LONG_DESCRIPTION = """
sphinx-tojupyter v1.0 - Generate High-Quality Jupyter Notebooks from Sphinx Projects

A focused Sphinx extension for converting RST and MyST source files into executable 
Jupyter notebooks (.ipynb). 

v1.0 is the first stable release, specializing in notebook generation and delegating 
execution, HTML, and PDF features to Jupyter Book for seamless integration.

Features:
- Convert RST/MyST to Jupyter notebooks
- MyST-NB glue support
- sphinx-proof directive support
- sphinx-exercise directive support
- Multi-language kernel support
- LaTeX macro support

For execution, HTML generation, and PDF export, use Jupyter Book.

This project is maintained and supported by [QuantEcon](http://quantecon.org/)
"""

setup(
    name='sphinx-tojupyter',
    version=VERSION,
    url='https://github.com/QuantEcon/sphinx-tojupyter',
    download_url='https://github.com/QuantEcon/sphinx-tojupyter/archive/{}.tar.gz'.format(VERSION),
    license='BSD',
    author='QuantEcon',
    author_email='contact@quantecon.org',
    description='Sphinx extension to generate Jupyter notebooks from RST/MyST source files',
    long_description=LONG_DESCRIPTION,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Framework :: Sphinx',
        'Framework :: Sphinx :: Extension',
        'Framework :: Jupyter',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Documentation',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Software Development :: Documentation',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.11',
    install_requires=[
        'sphinx>=7.0',
        'myst-nb>=0.14',
        'pyyaml',
        'nbformat',
        'nbconvert',
    ],
    extras_require={
        'test': [
            'pytest>=7.0',
            'myst-parser>=4.0',
            'sphinx-exercise>=1.0',
            'sphinx-proof>=0.3',
        ],
        'dev': [
            'pytest>=7.0',
            'myst-parser>=4.0',
            'sphinx-exercise>=1.0',
            'sphinx-proof>=0.3',
            'flake8',
            'jupyterlab',
            'ipykernel',
        ],
    },
)
