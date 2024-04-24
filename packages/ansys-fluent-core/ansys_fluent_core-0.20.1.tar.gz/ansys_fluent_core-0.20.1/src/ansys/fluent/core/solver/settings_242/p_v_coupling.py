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

from .flow_scheme import flow_scheme as flow_scheme_cls
from .skewness_correction_itr_count import skewness_correction_itr_count as skewness_correction_itr_count_cls
from .neighbor_correction_itr_count import neighbor_correction_itr_count as neighbor_correction_itr_count_cls
from .skewness_neighbor_coupling import skewness_neighbor_coupling as skewness_neighbor_coupling_cls
from .coupled_form import coupled_form as coupled_form_cls
from .solve_n_phase import solve_n_phase as solve_n_phase_cls
class p_v_coupling(Group):
    """
    Select the pressure velocity coupling scheme.
    """

    fluent_name = "p-v-coupling"

    child_names = \
        ['flow_scheme', 'skewness_correction_itr_count',
         'neighbor_correction_itr_count', 'skewness_neighbor_coupling',
         'coupled_form', 'solve_n_phase']

    _child_classes = dict(
        flow_scheme=flow_scheme_cls,
        skewness_correction_itr_count=skewness_correction_itr_count_cls,
        neighbor_correction_itr_count=neighbor_correction_itr_count_cls,
        skewness_neighbor_coupling=skewness_neighbor_coupling_cls,
        coupled_form=coupled_form_cls,
        solve_n_phase=solve_n_phase_cls,
    )

