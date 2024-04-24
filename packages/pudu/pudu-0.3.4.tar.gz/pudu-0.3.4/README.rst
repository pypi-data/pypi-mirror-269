====
pudu
====

.. image:: https://img.shields.io/pypi/v/pudu.svg
        :target: https://pypi.python.org/pypi/pudu
.. image:: https://anaconda.org/conda-forge/pudu/badges/version.svg   
        :target: https://anaconda.org/conda-forge/pudu
.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
        :target: https://opensource.org/licenses/MIT
.. image:: https://github.com/pudu-py/pudu/actions/workflows/codeql.yml/badge.svg
        :target: https://github.com/pudu-py/pudu/actions/workflows/codeql.yml
.. image:: https://github.com/pudu-py/pudu/workflows/docs/badge.svg
        :target: https://pudu-py.github.io/pudu
.. image:: https://codecov.io/gh/pudu-py/pudu/branch/main/graph/badge.svg?token=DC0QIwuYel
        :target: https://codecov.io/gh/pudu-py/pudu
.. image:: https://static.pepy.tech/personalized-badge/pudu?period=total&units=international_system&left_color=grey&left_text=pypi%20downloads&right_color=blue
        :target: https://pepy.tech/project/pudu
.. image:: https://img.shields.io/conda/dn/conda-forge/pudu.svg?color=blue&label=conda%20downloads
        :target: https://pepy.tech/project/pudu
.. image:: https://img.shields.io/badge/stackoverflow-Ask%20a%20question-brown
        :target: https://stackoverflow.com/questions/tagged/pudu
.. image:: https://joss.theoj.org/papers/cacb5b6520209b0c940bf46638df251d/status.svg
        :target: https://joss.theoj.org/papers/cacb5b6520209b0c940bf46638df251d

**A Python library for explainability of machine learning algorithms for spectroscopic data in an agnostic, deterministic, and simple way.**
* GitHub repo: https://github.com/pudu-py/pudu
* Documentation: https://pudu-py.github.io/pudu
* PyPI: https://pypi.python.org/pypi/pudu
* Conda-forge: https://anaconda.org/conda-forge/pudu
* Free software: MIT license

Introduction
============

**pudu** is a Python package that helps interpret and explore the results of machine learning algorithms 
with spectroscopic data. It does this by quantifying the change in the prediction according to the change 
in the features. This library works with classification and regression problems with both 1-d and 2-d problems. 
In order to see the exact procedure and format needed, please refer to the examples in the ``docs``.

Features
--------

The following is a list of the main features that **pudu** package enables.

- Importance: measures the change in prediction according to perturbations in the features.
- Speed: calculates how fast a prediction changes according to different perturbation levels.
- Synergy: tests the synergy between features and the change in classification probability.
- Re-activations: Evaluates how activations maps from CNNs change according to perturbations in the data.
- Easy plotting with ample personalization options for all the cases above.


Quickstart
----------

1. Install this library using ``pip``:

        pip install pudu

2. Install this library using ``conda-forge``:

        conda install -c conda-forge pudu

3. Test it by running one of the examples in the ``docs``.

4. If you find this library useful, please consider a reference or citation as:

        @misc{Grau-Luque2023Pudu,
        author = {E. Grau-Luque, I. Becerril-Romero, A. Perez-Rodriguez, M. Guc, V. Izquierdo-Roca},
        title = {pudu},
        year = {2023},
        publisher = {GitHub},
        journal = {GitHub repository},
        howpublished = {\url{https://github.com/pudu-py/pudu}},
        }


5. Stay up-to-date by updating the library using:

       conda update pudu
       pip install --update pudu

6. If you encounter problems when updating, try uninstalling and then re-installing::

        pip uninstall pudu
        conda remove pudu

Credits
-------

This package was created with `Cookiecutter <https://github.com/audreyr/cookiecutter>`__ and the `giswqs/pypackage <https://github.com/giswqs/pypackage>`__ project template.
