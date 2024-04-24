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

from .max_epochs import max_epochs as max_epochs_cls
from .mini_batch_size import mini_batch_size as mini_batch_size_cls
from .learning_rate import learning_rate as learning_rate_cls
from .initialize_neural_network import initialize_neural_network as initialize_neural_network_cls
from .manage_data_1 import manage_data as manage_data_cls
from .train import train as train_cls
from .apply_trained_model import apply_trained_model as apply_trained_model_cls
from .default_7 import default as default_cls
class offline_training(Group):
    """
    Set the training parameters.
    """

    fluent_name = "offline-training"

    child_names = \
        ['max_epochs', 'mini_batch_size', 'learning_rate',
         'initialize_neural_network', 'manage_data']

    command_names = \
        ['train', 'apply_trained_model', 'default']

    _child_classes = dict(
        max_epochs=max_epochs_cls,
        mini_batch_size=mini_batch_size_cls,
        learning_rate=learning_rate_cls,
        initialize_neural_network=initialize_neural_network_cls,
        manage_data=manage_data_cls,
        train=train_cls,
        apply_trained_model=apply_trained_model_cls,
        default=default_cls,
    )

