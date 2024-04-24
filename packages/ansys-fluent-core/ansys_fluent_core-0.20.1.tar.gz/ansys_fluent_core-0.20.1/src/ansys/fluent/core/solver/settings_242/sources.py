#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    _CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    _HasAllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)

from .enable_11 import enable as enable_cls
from .terms import terms as terms_cls
class sources(Group):
    """
    Source terms for this cell zone.
    """

    fluent_name = "sources"

    child_names = \
        ['enable', 'terms']

    _child_classes = dict(
        enable=enable_cls,
        terms=terms_cls,
    )

    _child_aliases = dict(
        source_terms="terms",
        sources="enable",
    )

