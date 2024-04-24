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

from .convergence_reports import convergence_reports as convergence_reports_cls
from .frequency_2 import frequency as frequency_cls
from .condition import condition as condition_cls
from .check_for import check_for as check_for_cls
class convergence_conditions(Group):
    """
    Available options that allow you to set convergence conditions on the solution based on the values from report definitions. For example, surface, volume, lift, drag, and so on.
    """

    fluent_name = "convergence-conditions"

    child_names = \
        ['convergence_reports', 'frequency', 'condition', 'check_for']

    _child_classes = dict(
        convergence_reports=convergence_reports_cls,
        frequency=frequency_cls,
        condition=condition_cls,
        check_for=check_for_cls,
    )

