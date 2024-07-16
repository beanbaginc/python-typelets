# Typelets for Python

[Typelets](https://pypi.org/project/typelets) is a Python typing utility module
designed to augment some of the types provided in Python and third-party
libraries. It was built to help develop
[Review Board](https://www.reviewboard.org), our premier code review product
from [Beanbag](https://www.beanbaginc.com), and we're making it available for
use in other projects.

This includes general Python additions, including:

* [typelets.funcs](https://typelets.readthedocs.io/en/latest/coderef/python/typelets.funcs.html):
  Typing for general keyword arguments in functions.

* [typelets.json](https://typelets.readthedocs.io/en/latest/coderef/python/typelets.json.html):
  Typing for JSON structures, and for application-defined data that can be
  serialized to JSON.

* [typelets.symbols](https://typelets.readthedocs.io/en/latest/coderef/python/typelets.symbols.html):
  Symbols for marking types as unset/unsettable.

Plus typing useful for Django developers:

* [typelets.django.auth](https://typelets.readthedocs.io/en/latest/coderef/python/typelets.django.auth.html):
  Types for accepting users.

* [typelets.django.forms](https://typelets.readthedocs.io/en/latest/coderef/python/typelets.django.forms.html):
  Types for forms and form fields.

* [typelets.django.json](https://typelets.readthedocs.io/en/latest/coderef/python/typelets.django.json.html):
  Types for Django's JSON serialization.

* [typelets.django.models](https://typelets.readthedocs.io/en/latest/coderef/python/typelets.django.models.html):
  Types for working with Django models.

* [typelets.django.strings](https://typelets.readthedocs.io/en/latest/coderef/python/typelets.django.strings.html):
  Types for localized strings.

* [typelets.django.urls](https://typelets.readthedocs.io/en/latest/coderef/python/typelets.django.urls.html):
  Types for URL management.


## Installation

To install typelets, run:

```console
$ pip install typelets
```

Typelets follows [semantic versioning](https://semver.org/), meaning no
surprises when you upgrade.


## Documentation

See the [Typelets documentation](https://typelets.readthedocs.io/) for
usage.


## License

Typelets is available under the MIT license.


## Contributing

Contributions to Typelets can be made on our
[Review Board](https://www.reviewboard.org/) server at
https://reviews.reviewboard.org/.

To post a change for review:

1. Download RBTools:

   ```console
   $ pip install rbtools
   ```

2. Create a branch in your Git clone and make your changes.

3. Post the change for review:

   ```console
   $ rbt post
   ```

   To update your change:

   ```console
   $ rbt post -u
   ```


Our Other Projects
------------------

* [Review Board](https://www.reviewboard.org) -
  Our open source, extensible code review, document review, and image review
  tool.

* [Djblets](https://github.com/djblets/djblets/) -
  Our pack of Django utilities for datagrids, API, extensions, and more. Used
  by Review Board.

* [Housekeeping](https://github.com/beanbaginc/housekeeping) -
  Deprecation management for Python modules, classes, functions, and
  attributes.

* [kgb](https://github.com/beanbaginc/kgb) -
  A powerful function spy implementation to help write Python unit tests.

* [Registries](https://github.com/beanbaginc/python-registries) -
  A flexible, typed implementation of the Registry Pattern for more
  maintainable and extensible codebases.

You can see more on [github.com/beanbaginc](https://github.com/beanbaginc) and
[github.com/reviewboard](https://github.com/reviewboard).
