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

from .residual import residual as residual_cls
from .report_files import report_files as report_files_cls
from .report_plots import report_plots as report_plots_cls
from .convergence_conditions import convergence_conditions as convergence_conditions_cls
class monitor(Group):
    """
    Provides access to common settings to monitor the convergence dynamically during the solution process by checking residuals, statistics, force values, surface integrals, and volume integrals. You can print reports of or display plots of lift, drag and moment coefficients, surface integrations and residuals for the solution variables. For unsteady flows you can also monitor elapsed time.
    """

    fluent_name = "monitor"

    child_names = \
        ['residual', 'report_files', 'report_plots', 'convergence_conditions']

    _child_classes = dict(
        residual=residual_cls,
        report_files=report_files_cls,
        report_plots=report_plots_cls,
        convergence_conditions=convergence_conditions_cls,
    )

