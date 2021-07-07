# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

VERSION = 'v0.1.2'

LONG_DESCRIPTION = """
This package contains a [Sphinx](http://www.sphinx-doc.org/en/master/) extension 
for building Jupyter notebooks.

The default behavior of the `jupyter` builder is to provide notebooks that are readable
with an emphasis on supporting basic markdown into the notebooks.

This project is maintained and supported by [QuantEcon](http://quantecon.org/)
"""

requires = ['Sphinx>=3.0']

setup(
    name='sphinx-tojupyter',
    version=VERSION,
    url='https://github.com/QuantEcon/sphinx-tojupyter',
    download_url='https://github.com/QuantEcon/sphinx-tojupyter/archive/{}.tar.gz'.format(VERSION),
    license='BSD',
    author='QuantEcon',
    author_email='contact@quantecon.org',
    description='Sphinx "Jupyter" extension to build Jupyter notebooks.',
    long_description=LONG_DESCRIPTION,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Sphinx',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Framework :: Sphinx :: Extension',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['sphinx', 'pyyaml', 'nbformat', 'nbconvert', 'dask[distributed]', 'nbdime'],
)
