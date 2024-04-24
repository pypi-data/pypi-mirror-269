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

from .field_7 import field as field_cls
from .node_values_4 import node_values as node_values_cls
from .zones_8 import zones as zones_cls
from .surfaces_13 import surfaces as surfaces_cls
from .geometry_8 import geometry as geometry_cls
from .axes import axes as axes_cls
from .curves import curves as curves_cls
from .plot_8 import plot as plot_cls
class solution_plot(Group):
    """
    Plot the solution data.
    """

    fluent_name = "solution-plot"

    child_names = \
        ['field', 'node_values', 'zones', 'surfaces', 'geometry', 'axes',
         'curves']

    command_names = \
        ['plot']

    _child_classes = dict(
        field=field_cls,
        node_values=node_values_cls,
        zones=zones_cls,
        surfaces=surfaces_cls,
        geometry=geometry_cls,
        axes=axes_cls,
        curves=curves_cls,
        plot=plot_cls,
    )

