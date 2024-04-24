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

from .thermal_condition import thermal_condition as thermal_condition_cls
from .material_4 import material as material_cls
from .heat_flux_1 import heat_flux as heat_flux_cls
from .temperature_1 import temperature as temperature_cls
from .heat_transfer_coeff_1 import heat_transfer_coeff as heat_transfer_coeff_cls
from .free_stream_temp_1 import free_stream_temp as free_stream_temp_cls
from .external_emissivity import external_emissivity as external_emissivity_cls
from .ext_rad_temperature import ext_rad_temperature as ext_rad_temperature_cls
from .wall_thickness_old import wall_thickness_old as wall_thickness_old_cls
from .wall_thickness import wall_thickness as wall_thickness_cls
from .heat_generation_rate import heat_generation_rate as heat_generation_rate_cls
from .enable_shell_conduction import enable_shell_conduction as enable_shell_conduction_cls
from .conduction_layers import conduction_layers as conduction_layers_cls
from .thin_wall import thin_wall as thin_wall_cls
from .radiating_to_fixed_temp import radiating_to_fixed_temp as radiating_to_fixed_temp_cls
from .internal_radiation_temp import internal_radiation_temp as internal_radiation_temp_cls
from .area_enhancement_factor import area_enhancement_factor as area_enhancement_factor_cls
from .contact_resistance_1 import contact_resistance as contact_resistance_cls
from .therm_accom_coef import therm_accom_coef as therm_accom_coef_cls
from .eve_accom_coef import eve_accom_coef as eve_accom_coef_cls
from .caf import caf as caf_cls
from .thermal_stabilization import thermal_stabilization as thermal_stabilization_cls
from .scale_factor_1 import scale_factor as scale_factor_cls
from .stab_method import stab_method as stab_method_cls
from .boundary_advection import boundary_advection as boundary_advection_cls
class thermal(Group):
    """
    Thermal settings for this boundary-condition.
    """

    fluent_name = "thermal"

    child_names = \
        ['thermal_condition', 'material', 'heat_flux', 'temperature',
         'heat_transfer_coeff', 'free_stream_temp', 'external_emissivity',
         'ext_rad_temperature', 'wall_thickness_old', 'wall_thickness',
         'heat_generation_rate', 'enable_shell_conduction',
         'conduction_layers', 'thin_wall', 'radiating_to_fixed_temp',
         'internal_radiation_temp', 'area_enhancement_factor',
         'contact_resistance', 'therm_accom_coef', 'eve_accom_coef', 'caf',
         'thermal_stabilization', 'scale_factor', 'stab_method',
         'boundary_advection']

    _child_classes = dict(
        thermal_condition=thermal_condition_cls,
        material=material_cls,
        heat_flux=heat_flux_cls,
        temperature=temperature_cls,
        heat_transfer_coeff=heat_transfer_coeff_cls,
        free_stream_temp=free_stream_temp_cls,
        external_emissivity=external_emissivity_cls,
        ext_rad_temperature=ext_rad_temperature_cls,
        wall_thickness_old=wall_thickness_old_cls,
        wall_thickness=wall_thickness_cls,
        heat_generation_rate=heat_generation_rate_cls,
        enable_shell_conduction=enable_shell_conduction_cls,
        conduction_layers=conduction_layers_cls,
        thin_wall=thin_wall_cls,
        radiating_to_fixed_temp=radiating_to_fixed_temp_cls,
        internal_radiation_temp=internal_radiation_temp_cls,
        area_enhancement_factor=area_enhancement_factor_cls,
        contact_resistance=contact_resistance_cls,
        therm_accom_coef=therm_accom_coef_cls,
        eve_accom_coef=eve_accom_coef_cls,
        caf=caf_cls,
        thermal_stabilization=thermal_stabilization_cls,
        scale_factor=scale_factor_cls,
        stab_method=stab_method_cls,
        boundary_advection=boundary_advection_cls,
    )

    _child_aliases = dict(
        boundary_advection="boundary_advection",
        d="wall_thickness",
        d_constant="wall_thickness_old",
        ex_emiss="external_emissivity",
        h="heat_transfer_coeff",
        int_rad="radiating_to_fixed_temp",
        planar_conduction="enable_shell_conduction",
        q="heat_flux",
        q_dot="heat_generation_rate",
        shell_conduction="conduction_layers",
        t="temperature",
        thermal_bc="thermal_condition",
        tinf="free_stream_temp",
        trad="ext_rad_temperature",
        trad_internal="internal_radiation_temp",
    )

