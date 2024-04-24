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

from .diffusion_rate_constant import diffusion_rate_constant as diffusion_rate_constant_cls
from .pre_exponential_factor_1 import pre_exponential_factor as pre_exponential_factor_cls
from .activation_energy_2 import activation_energy as activation_energy_cls
class kinetics_diffusion_limited(Group):
    """
    Kinetics diffusion limited settings.
    """

    fluent_name = "kinetics-diffusion-limited"

    child_names = \
        ['diffusion_rate_constant', 'pre_exponential_factor',
         'activation_energy']

    _child_classes = dict(
        diffusion_rate_constant=diffusion_rate_constant_cls,
        pre_exponential_factor=pre_exponential_factor_cls,
        activation_energy=activation_energy_cls,
    )

