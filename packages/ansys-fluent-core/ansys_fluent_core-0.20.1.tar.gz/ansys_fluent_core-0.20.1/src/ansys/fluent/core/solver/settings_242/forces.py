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

from .option_30 import option as option_cls
from .domain_2 import domain as domain_cls
from .wall_zones_1 import wall_zones as wall_zones_cls
from .direction_vector_2 import direction_vector as direction_vector_cls
from .momentum_center import momentum_center as momentum_center_cls
from .momentum_axis import momentum_axis as momentum_axis_cls
from .pressure_coordinate import pressure_coordinate as pressure_coordinate_cls
from .coordinate_value import coordinate_value as coordinate_value_cls
from .write_to_file_2 import write_to_file as write_to_file_cls
from .file_name_14 import file_name as file_name_cls
from .append_data import append_data as append_data_cls
class forces(Command):
    """
    Provides access to settings for force reports.
    
    Parameters
    ----------
        option : str
            Select the type of report (Forces, Moments, or Center of Pressure).
        domain : str
            Select the domain.
        wall_zones : typing.List[str]
            Enter wall zone name list.
        direction_vector : typing.List[real]
            Specify the XYZ components of the direction vector.
        momentum_center : typing.List[real]
            Specify the XYZ coordinates of the moment center.
        momentum_axis : typing.List[real]
            Specify the XYZ components of the moment axis.
        pressure_coordinate : str
            Specify the line on which the center of pressure will be calculated.
        coordinate_value : real
            Specify the coordinate value.
        write_to_file : bool
            Choose whether or not to write to a file.
        file_name : str
            Enter the name you want the file saved with.
        append_data : bool
            Choose whether or not to append data to existing file.
    
    """

    fluent_name = "forces"

    argument_names = \
        ['option', 'domain', 'wall_zones', 'direction_vector',
         'momentum_center', 'momentum_axis', 'pressure_coordinate',
         'coordinate_value', 'write_to_file', 'file_name', 'append_data']

    _child_classes = dict(
        option=option_cls,
        domain=domain_cls,
        wall_zones=wall_zones_cls,
        direction_vector=direction_vector_cls,
        momentum_center=momentum_center_cls,
        momentum_axis=momentum_axis_cls,
        pressure_coordinate=pressure_coordinate_cls,
        coordinate_value=coordinate_value_cls,
        write_to_file=write_to_file_cls,
        file_name=file_name_cls,
        append_data=append_data_cls,
    )

