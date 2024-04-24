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

from .zone_names_7 import zone_names as zone_names_cls
from .domain_2 import domain as domain_cls
from .quantities import quantities as quantities_cls
from .min_2 import min as min_cls
from .max_2 import max as max_cls
from .mean_1 import mean as mean_cls
from .rmse_1 import rmse as rmse_cls
from .moving_average_1 import moving_average as moving_average_cls
from .average_over_2 import average_over as average_over_cls
class add_datasets(Command):
    """
    Add datasets.
    
    Parameters
    ----------
        zone_names : typing.List[str]
            Select one or more zone names.
        domain : str
            Select the domain.
        quantities : typing.List[str]
            Select one or more quantities.
        min : bool
            Choose whether or not to specify the minimum value of the selected quantity(s) will be collected.
        max : bool
            Choose whether or not to specify the maximum value of the selected quantity(s) will be collected.
        mean : bool
            Choose whether or not to specify the average value of the selected quantity(s) will be computed and collected.
        rmse : bool
            Choose whether or not to specify that the root mean square error of the selected quantity(s) will be computed and collected.
        moving_average : bool
            Choose whether or not to specify an interval for averaging of the computed statistics.
        average_over : int
            Specify the number of iterations (steady simulations) or time steps (transient simulations) that will be used for computing the moving average.
    
    """

    fluent_name = "add-datasets"

    argument_names = \
        ['zone_names', 'domain', 'quantities', 'min', 'max', 'mean', 'rmse',
         'moving_average', 'average_over']

    _child_classes = dict(
        zone_names=zone_names_cls,
        domain=domain_cls,
        quantities=quantities_cls,
        min=min_cls,
        max=max_cls,
        mean=mean_cls,
        rmse=rmse_cls,
        moving_average=moving_average_cls,
        average_over=average_over_cls,
    )

