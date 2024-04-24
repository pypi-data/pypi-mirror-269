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

from .domain_2 import domain as domain_cls
class element_mass_flow(Command):
    """
    Print element mass flow rate at boundaries.
    
    Parameters
    ----------
        domain : str
            Select the domain.
    
    """

    fluent_name = "element-mass-flow"

    argument_names = \
        ['domain']

    _child_classes = dict(
        domain=domain_cls,
    )

