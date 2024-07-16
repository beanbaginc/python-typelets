"""Typing useful for Django forms.

Version Added:
    1.0
"""

from __future__ import annotations

from typing import Any, Mapping
from typing_extensions import TypeAlias

from django.core.files.uploadedfile import UploadedFile
from django.utils.datastructures import MultiValueDict


#: Data posted to a Django form.
#:
#: Version Added:
#:     1.0
FormData: TypeAlias = Mapping[str, Any]


#: Files posted to a Django form.
#:
#: Version Added:
#:     1.0
FormFiles: TypeAlias = MultiValueDict[str, UploadedFile]
