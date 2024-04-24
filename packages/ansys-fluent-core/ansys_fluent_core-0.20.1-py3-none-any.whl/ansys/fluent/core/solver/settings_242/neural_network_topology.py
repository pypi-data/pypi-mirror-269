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

from .list_properties import list_properties as list_properties_cls
from .resize import resize as resize_cls
from .neural_network_topology_child import neural_network_topology_child

class neural_network_topology(ListObject[neural_network_topology_child]):
    """
    Set the number of neural network nodes at each hidden layer.
    """

    fluent_name = "neural-network-topology"

    command_names = \
        ['list_properties', 'resize']

    _child_classes = dict(
        list_properties=list_properties_cls,
        resize=resize_cls,
    )

    child_object_type: neural_network_topology_child = neural_network_topology_child
    """
    child_object_type of neural_network_topology.
    """
