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

from .name import name as name_cls
from .particle_type import particle_type as particle_type_cls
from .material_1 import material as material_cls
from .injection_type import injection_type as injection_type_cls
from .interaction_1 import interaction as interaction_cls
from .particle_reinjector import particle_reinjector as particle_reinjector_cls
from .initial_values import initial_values as initial_values_cls
from .physical_models_1 import physical_models as physical_models_cls
from .parcel_method import parcel_method as parcel_method_cls
class injections_child(Group):
    """
    'child_object_type' of injections.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'particle_type', 'material', 'injection_type', 'interaction',
         'particle_reinjector', 'initial_values', 'physical_models',
         'parcel_method']

    _child_classes = dict(
        name=name_cls,
        particle_type=particle_type_cls,
        material=material_cls,
        injection_type=injection_type_cls,
        interaction=interaction_cls,
        particle_reinjector=particle_reinjector_cls,
        initial_values=initial_values_cls,
        physical_models=physical_models_cls,
        parcel_method=parcel_method_cls,
    )

    _child_aliases = dict(
        number_of_streams="initial_values/location/number_of_streams",
        reference_frame="initial_values/reference_frame",
    )

