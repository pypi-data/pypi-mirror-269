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

from .enable_turbulence_source_term import enable_turbulence_source_term as enable_turbulence_source_term_cls
class options(Group):
    """
    Turbulence model design variables options.
    """

    fluent_name = "options"

    child_names = \
        ['enable_turbulence_source_term']

    _child_classes = dict(
        enable_turbulence_source_term=enable_turbulence_source_term_cls,
    )

