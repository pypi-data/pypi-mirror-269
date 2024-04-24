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

from .frequency_7 import frequency as frequency_cls
from .maximum_5 import maximum as maximum_cls
class save_files(Group):
    """
    File saving settings for optimization reporting.
    """

    fluent_name = "save-files"

    child_names = \
        ['frequency', 'maximum']

    _child_classes = dict(
        frequency=frequency_cls,
        maximum=maximum_cls,
    )

