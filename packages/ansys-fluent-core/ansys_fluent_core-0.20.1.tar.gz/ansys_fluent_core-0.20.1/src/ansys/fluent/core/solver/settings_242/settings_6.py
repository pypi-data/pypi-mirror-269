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

from .smooth_sensitivities import smooth_sensitivities as smooth_sensitivities_cls
from .activation_function import activation_function as activation_function_cls
from .neural_network_topology import neural_network_topology as neural_network_topology_cls
from .input_features import input_features as input_features_cls
class settings(Group):
    """
    Turbulence model variables modelization settings.
    """

    fluent_name = "settings"

    child_names = \
        ['smooth_sensitivities', 'activation_function',
         'neural_network_topology', 'input_features']

    _child_classes = dict(
        smooth_sensitivities=smooth_sensitivities_cls,
        activation_function=activation_function_cls,
        neural_network_topology=neural_network_topology_cls,
        input_features=input_features_cls,
    )

