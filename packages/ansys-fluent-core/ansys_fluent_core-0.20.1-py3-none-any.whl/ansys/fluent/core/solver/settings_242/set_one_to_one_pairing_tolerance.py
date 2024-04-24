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

from .adjustable_tolerance import adjustable_tolerance as adjustable_tolerance_cls
from .length_factor import length_factor as length_factor_cls
class set_one_to_one_pairing_tolerance(Command):
    """
    Set one-to-one adjustable tolerance.
    
    Parameters
    ----------
        adjustable_tolerance : bool
            Enable/disable one-to-one adjustable tolerance.
        length_factor : real
            Enter a valid number for length factor.
    
    """

    fluent_name = "set-one-to-one-pairing-tolerance"

    argument_names = \
        ['adjustable_tolerance', 'length_factor']

    _child_classes = dict(
        adjustable_tolerance=adjustable_tolerance_cls,
        length_factor=length_factor_cls,
    )

