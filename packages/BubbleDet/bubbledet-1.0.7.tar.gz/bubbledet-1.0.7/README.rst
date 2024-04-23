===========================================
BubbleDet
===========================================

Computes the one-loop functional determinant entering the bubble nucleation
rate, or vacuum decay rate.

|

Documentation
===========================================
For complete package documentation, see the
`BubbleDet homepage <https://bubbledet.readthedocs.io/>`_. For more information
about the mathematics behind BubbleDet, see the accompanying paper on
`arXiv <https://arxiv.org/abs/2308.15652>`_.

|


Requirements
===========================================

Based on Python 3. Package dependencies are automatically installed with pip or
conda. For a list, see `pyproject.toml` in the
`git respository <https://bitbucket.org/og113/bubbledet/>`_.

|


Installation
===========================================

Pip
---

The latest stable version can be installed as a package with
`pip <https://pypi.org/project/BubbleDet/>`_ (or pip3)
using::

    pip install BubbleDet

Alternatively, for the development version, one can clone the
`git respository <https://bitbucket.org/og113/bubbledet/>`_.
and install with::

    pip install -e .

from the base directory of the repository. To install also optional dependencies
for the docs and tests, instead run::

    pip install -e .[docs,tests]


Conda
-----

The latest stable version can also be installed as a package with
`conda <https://anaconda.org/conda-forge/bubbledet/>`_, from the
`conda-forge <https://github.com/conda-forge/bubbledet-feedstock>`_ repository::

    conda install -c conda-forge BubbleDet

|

Tests
===========================================

After installation of the development version, the tests can be run with::

    pytest -v

from the base directory of the git repository.

|

Examples
===========================================

A number of examples are collected in the directory `examples/` of the git repo,
including a simple real scalar model and a comparison to analytic results in the
thin-wall limit. The examples can also be found on the
`BubbleDet homepage <https://bubbledet.readthedocs.io/>`_. After installing the
package, these can be run directly with Python, as in::

    python3 first_example.py
