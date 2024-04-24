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

from .plot_during_optimization import plot_during_optimization as plot_during_optimization_cls
from .observables_values import observables_values as observables_values_cls
from .expected_observables_values import expected_observables_values as expected_observables_values_cls
from .normalize_1 import normalize as normalize_cls
from .plot_all_optimization_ids import plot_all_optimization_ids as plot_all_optimization_ids_cls
from .optimization_id_to_plot import optimization_id_to_plot as optimization_id_to_plot_cls
from .plot_14 import plot as plot_cls
class monitor(Group):
    """
    Calculation activities monitor menu.
    """

    fluent_name = "monitor"

    child_names = \
        ['plot_during_optimization', 'observables_values',
         'expected_observables_values', 'normalize',
         'plot_all_optimization_ids', 'optimization_id_to_plot']

    command_names = \
        ['plot']

    _child_classes = dict(
        plot_during_optimization=plot_during_optimization_cls,
        observables_values=observables_values_cls,
        expected_observables_values=expected_observables_values_cls,
        normalize=normalize_cls,
        plot_all_optimization_ids=plot_all_optimization_ids_cls,
        optimization_id_to_plot=optimization_id_to_plot_cls,
        plot=plot_cls,
    )

