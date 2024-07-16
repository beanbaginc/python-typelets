"""Typelets for Python.

Version Added:
    1.0
"""

from typelets._version import (VERSION,
                               __version__,
                               __version_info__,
                               get_package_version,
                               get_version_string,
                               is_release)


__all__ = [
    'VERSION',
    '__version__',
    '__version_info__',
    'get_package_version',
    'get_version_string',
    'is_release',
]


__autodoc_excludes__ = __all__
