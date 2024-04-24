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

from .observables import observables as observables_cls
from .methods_2 import methods as methods_cls
from .controls_2 import controls as controls_cls
from .monitors import monitors as monitors_cls
from .calculation import calculation as calculation_cls
from .postprocess_options import postprocess_options as postprocess_options_cls
from .reporting import reporting as reporting_cls
from .design_tool import design_tool as design_tool_cls
from .optimizer import optimizer as optimizer_cls
from .enable_21 import enable as enable_cls
class gradient_based(Group):
    """
    Gradient-based design menu.
    """

    fluent_name = "gradient-based"

    child_names = \
        ['observables', 'methods', 'controls', 'monitors', 'calculation',
         'postprocess_options', 'reporting', 'design_tool', 'optimizer']

    command_names = \
        ['enable']

    _child_classes = dict(
        observables=observables_cls,
        methods=methods_cls,
        controls=controls_cls,
        monitors=monitors_cls,
        calculation=calculation_cls,
        postprocess_options=postprocess_options_cls,
        reporting=reporting_cls,
        design_tool=design_tool_cls,
        optimizer=optimizer_cls,
        enable=enable_cls,
    )

