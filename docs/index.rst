===================
Typelets for Python
===================

Typelets is a Python typing utility module designed to augment some of the
types provided in Python and third-party libraries.

This includes general Python additions, including:

* :py:mod:`typelets.funcs`: Typing for general keyword arguments in functions.

* :py:mod:`typelets.json`: Typing for JSON structures, and for
  application-defined data that can be serialized to JSON.

* :py:mod:`typelets.symbols`: Symbols for marking types as unset/unsettable.

Plus typing useful for Django developers:

* :py:mod:`typelets.django.auth`: Types for accepting users.
* :py:mod:`typelets.django.forms`: Types for forms and form fields.
* :py:mod:`typelets.django.json`: Types for Django's JSON serialization.
* :py:mod:`typelets.django.models`: Types for working with Django models.
* :py:mod:`typelets.django.strings`: Types for localized strings.
* :py:mod:`typelets.django.urls`: Types for URL management.


Installation
============

To install Typelets, run:

.. code-block:: console

   $ pip install typelets

Typelets follows `semantic versioning`_, meaning no surprises when you
upgrade.

.. _semantic versioning: https://semver.org/


Documentation
=============

.. toctree::
   :maxdepth: 3

   coderef/index
   releasenotes/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
