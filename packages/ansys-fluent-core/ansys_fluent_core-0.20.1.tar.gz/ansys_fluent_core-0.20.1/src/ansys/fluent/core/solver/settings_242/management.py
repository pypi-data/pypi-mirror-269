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

from .clear_model import clear_model as clear_model_cls
from .export_model import export_model as export_model_cls
from .import_model import import_model as import_model_cls
class management(Group):
    """
    Read the model setting and coefficients from a file.
    """

    fluent_name = "management"

    command_names = \
        ['clear_model', 'export_model', 'import_model']

    _child_classes = dict(
        clear_model=clear_model_cls,
        export_model=export_model_cls,
        import_model=import_model_cls,
    )

