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

from .discrete_boundary_condition import discrete_boundary_condition as discrete_boundary_condition_cls
from .discrete_boundary_value import discrete_boundary_value as discrete_boundary_value_cls
from .quadrature_moment_boundary_condition import quadrature_moment_boundary_condition as quadrature_moment_boundary_condition_cls
from .quadrature_moment_boundary_value import quadrature_moment_boundary_value as quadrature_moment_boundary_value_cls
from .qbmm_boundary_condition import qbmm_boundary_condition as qbmm_boundary_condition_cls
from .qbmm_boundary_value import qbmm_boundary_value as qbmm_boundary_value_cls
from .std_moment_boundary_condition import std_moment_boundary_condition as std_moment_boundary_condition_cls
from .std_moment_boundary_value import std_moment_boundary_value as std_moment_boundary_value_cls
from .dqmom_boundary_condition import dqmom_boundary_condition as dqmom_boundary_condition_cls
from .dqmom_boundary_value import dqmom_boundary_value as dqmom_boundary_value_cls
class population_balance(Group):
    """
    Population balance settings.
    """

    fluent_name = "population-balance"

    child_names = \
        ['discrete_boundary_condition', 'discrete_boundary_value',
         'quadrature_moment_boundary_condition',
         'quadrature_moment_boundary_value', 'qbmm_boundary_condition',
         'qbmm_boundary_value', 'std_moment_boundary_condition',
         'std_moment_boundary_value', 'dqmom_boundary_condition',
         'dqmom_boundary_value']

    _child_classes = dict(
        discrete_boundary_condition=discrete_boundary_condition_cls,
        discrete_boundary_value=discrete_boundary_value_cls,
        quadrature_moment_boundary_condition=quadrature_moment_boundary_condition_cls,
        quadrature_moment_boundary_value=quadrature_moment_boundary_value_cls,
        qbmm_boundary_condition=qbmm_boundary_condition_cls,
        qbmm_boundary_value=qbmm_boundary_value_cls,
        std_moment_boundary_condition=std_moment_boundary_condition_cls,
        std_moment_boundary_value=std_moment_boundary_value_cls,
        dqmom_boundary_condition=dqmom_boundary_condition_cls,
        dqmom_boundary_value=dqmom_boundary_value_cls,
    )

    _child_aliases = dict(
        pb_disc="discrete_boundary_value",
        pb_disc_bc="discrete_boundary_condition",
        pb_dqmom="dqmom_boundary_value",
        pb_dqmom_bc="dqmom_boundary_condition",
        pb_qbmm="qbmm_boundary_value",
        pb_qbmm_bc="qbmm_boundary_condition",
        pb_qmom="quadrature_moment_boundary_value",
        pb_qmom_bc="quadrature_moment_boundary_condition",
        pb_smm="std_moment_boundary_value",
        pb_smm_bc="std_moment_boundary_condition",
    )

