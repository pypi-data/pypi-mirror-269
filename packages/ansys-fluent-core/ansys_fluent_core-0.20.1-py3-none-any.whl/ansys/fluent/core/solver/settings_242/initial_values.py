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

from .reference_frame_1 import reference_frame as reference_frame_cls
from .times import times as times_cls
from .location_1 import location as location_cls
from .mass_flow_rate import mass_flow_rate as mass_flow_rate_cls
from .matrix import matrix as matrix_cls
from .cone_settings import cone_settings as cone_settings_cls
from .velocity import velocity as velocity_cls
from .angular_velocity import angular_velocity as angular_velocity_cls
from .particle_size import particle_size as particle_size_cls
from .temperature import temperature as temperature_cls
from .temperature_2 import temperature_2 as temperature_2_cls
class initial_values(Group):
    """
    'initial_values' child.
    """

    fluent_name = "initial-values"

    child_names = \
        ['reference_frame', 'times', 'location', 'mass_flow_rate', 'matrix',
         'cone_settings', 'velocity', 'angular_velocity', 'particle_size',
         'temperature', 'temperature_2']

    _child_classes = dict(
        reference_frame=reference_frame_cls,
        times=times_cls,
        location=location_cls,
        mass_flow_rate=mass_flow_rate_cls,
        matrix=matrix_cls,
        cone_settings=cone_settings_cls,
        velocity=velocity_cls,
        angular_velocity=angular_velocity_cls,
        particle_size=particle_size_cls,
        temperature=temperature_cls,
        temperature_2=temperature_2_cls,
    )

