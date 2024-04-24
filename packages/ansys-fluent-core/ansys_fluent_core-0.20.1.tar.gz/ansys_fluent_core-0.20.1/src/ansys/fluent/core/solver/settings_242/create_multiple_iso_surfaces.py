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

from .field_1 import field as field_cls
from .name_9 import name as name_cls
from .surfaces_5 import surfaces as surfaces_cls
from .zones_6 import zones as zones_cls
from .min_5 import min as min_cls
from .max_5 import max as max_cls
from .iso_value import iso_value as iso_value_cls
from .no_of_surfaces import no_of_surfaces as no_of_surfaces_cls
from .spacing import spacing as spacing_cls
class create_multiple_iso_surfaces(Command):
    """
    Provides access to creating new and editing multiple iso-surfaces.
    
    Parameters
    ----------
        field : str
            Select the field variable.
        name : str
            Specify the Iso-surface name.
        surfaces : typing.List[str]
            Select the surface(s) that will be used to define the iso-surface.
        zones : typing.List[str]
            Select the zone(s) that will be used to define the iso-surface.
        min : real
            Set min.
        max : real
            Set max.
        iso_value : real
            Specify the iso-value.
        no_of_surfaces : int
            Specify the number of surfaces to be created.
        spacing : real
            Specify the spacing.
    
    """

    fluent_name = "create-multiple-iso-surfaces"

    argument_names = \
        ['field', 'name', 'surfaces', 'zones', 'min', 'max', 'iso_value',
         'no_of_surfaces', 'spacing']

    _child_classes = dict(
        field=field_cls,
        name=name_cls,
        surfaces=surfaces_cls,
        zones=zones_cls,
        min=min_cls,
        max=max_cls,
        iso_value=iso_value_cls,
        no_of_surfaces=no_of_surfaces_cls,
        spacing=spacing_cls,
    )

