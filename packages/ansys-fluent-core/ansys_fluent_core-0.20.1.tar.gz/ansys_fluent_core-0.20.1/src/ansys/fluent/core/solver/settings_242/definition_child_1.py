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
from .type_11 import type as type_cls
from .surfaces_15 import surfaces as surfaces_cls
from .imported_surfaces import imported_surfaces as imported_surfaces_cls
from .fit_imported_surfaces import fit_imported_surfaces as fit_imported_surfaces_cls
from .bounding_offset import bounding_offset as bounding_offset_cls
from .deformation_profile import deformation_profile as deformation_profile_cls
from .displacement import displacement as displacement_cls
from .scaling_type import scaling_type as scaling_type_cls
from .scale_factor_2 import scale_factor as scale_factor_cls
from .angle_3 import angle as angle_cls
from .factor_3 import factor as factor_cls
from .axis_factor import axis_factor as axis_factor_cls
from .origin_4 import origin as origin_cls
from .normal_2 import normal as normal_cls
from .axis_5 import axis as axis_cls
from .axis_1_2 import axis_1 as axis_1_cls
from .axis_2_2 import axis_2 as axis_2_cls
from .distance_1 import distance as distance_cls
from .orientation_1 import orientation as orientation_cls
from .compound import compound as compound_cls
from .get_center import get_center as get_center_cls
from .import_surfaces import import_surfaces as import_surfaces_cls
from .delete_surfaces import delete_surfaces as delete_surfaces_cls
from .display_imported_surfaces import display_imported_surfaces as display_imported_surfaces_cls
from .display_8 import display as display_cls
class definition_child(Group):
    """
    'child_object_type' of definition.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'type', 'surfaces', 'imported_surfaces',
         'fit_imported_surfaces', 'bounding_offset', 'deformation_profile',
         'displacement', 'scaling_type', 'scale_factor', 'angle', 'factor',
         'axis_factor', 'origin', 'normal', 'axis', 'axis_1', 'axis_2',
         'distance', 'orientation', 'compound']

    command_names = \
        ['get_center', 'import_surfaces', 'delete_surfaces',
         'display_imported_surfaces', 'display']

    _child_classes = dict(
        name=name_cls,
        type=type_cls,
        surfaces=surfaces_cls,
        imported_surfaces=imported_surfaces_cls,
        fit_imported_surfaces=fit_imported_surfaces_cls,
        bounding_offset=bounding_offset_cls,
        deformation_profile=deformation_profile_cls,
        displacement=displacement_cls,
        scaling_type=scaling_type_cls,
        scale_factor=scale_factor_cls,
        angle=angle_cls,
        factor=factor_cls,
        axis_factor=axis_factor_cls,
        origin=origin_cls,
        normal=normal_cls,
        axis=axis_cls,
        axis_1=axis_1_cls,
        axis_2=axis_2_cls,
        distance=distance_cls,
        orientation=orientation_cls,
        compound=compound_cls,
        get_center=get_center_cls,
        import_surfaces=import_surfaces_cls,
        delete_surfaces=delete_surfaces_cls,
        display_imported_surfaces=display_imported_surfaces_cls,
        display=display_cls,
    )

