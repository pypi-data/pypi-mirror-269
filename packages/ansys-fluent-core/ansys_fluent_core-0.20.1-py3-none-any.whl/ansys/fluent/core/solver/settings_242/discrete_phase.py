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

from .general_settings import general_settings as general_settings_cls
from .physical_models import physical_models as physical_models_cls
from .tracking import tracking as tracking_cls
from .numerics import numerics as numerics_cls
from .parallel import parallel as parallel_cls
from .user_defined_functions import user_defined_functions as user_defined_functions_cls
from .injections import injections as injections_cls
class discrete_phase(Group):
    """
    Toplevel menu of the Discrete Phase multiphase model. A discrete phase model (DPM) is used when the aim is to investigate the behavior of the particles from a Lagrangian view and a discrete perspective.
    """

    fluent_name = "discrete-phase"

    child_names = \
        ['general_settings', 'physical_models', 'tracking', 'numerics',
         'parallel', 'user_defined_functions', 'injections']

    _child_classes = dict(
        general_settings=general_settings_cls,
        physical_models=physical_models_cls,
        tracking=tracking_cls,
        numerics=numerics_cls,
        parallel=parallel_cls,
        user_defined_functions=user_defined_functions_cls,
        injections=injections_cls,
    )

    _child_aliases = dict(
        user_functions="user_defined_functions",
    )

