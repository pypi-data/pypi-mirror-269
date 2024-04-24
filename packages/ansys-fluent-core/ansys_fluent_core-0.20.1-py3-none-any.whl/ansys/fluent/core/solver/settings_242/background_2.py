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

from .hide_environment_keep_effects import hide_environment_keep_effects as hide_environment_keep_effects_cls
from .environment_image import environment_image as environment_image_cls
from .vertical import vertical as vertical_cls
from .horizontal import horizontal as horizontal_cls
from .spin import spin as spin_cls
from .env_color import env_color as env_color_cls
from .env_intensity import env_intensity as env_intensity_cls
from .view_zoom import view_zoom as view_zoom_cls
from .show_backplate import show_backplate as show_backplate_cls
from .backplate_color import backplate_color as backplate_color_cls
from .backplate_image import backplate_image as backplate_image_cls
from .env_light_upvec import env_light_upvec as env_light_upvec_cls
from .env_light_dirvec import env_light_dirvec as env_light_dirvec_cls
from .activate_env_ground import activate_env_ground as activate_env_ground_cls
from .activate_env_ground_shadow import activate_env_ground_shadow as activate_env_ground_shadow_cls
from .model_scale import model_scale as model_scale_cls
from .env_light_ground_height import env_light_ground_height as env_light_ground_height_cls
from .is_ground_shadow_at_fix_axis import is_ground_shadow_at_fix_axis as is_ground_shadow_at_fix_axis_cls
from .ground_shadow_axis import ground_shadow_axis as ground_shadow_axis_cls
class background(Group):
    """
    Ability to adjust various settings and effects for the realistic raytracing environment background.
    """

    fluent_name = "background"

    child_names = \
        ['hide_environment_keep_effects', 'environment_image', 'vertical',
         'horizontal', 'spin', 'env_color', 'env_intensity', 'view_zoom',
         'show_backplate', 'backplate_color', 'backplate_image',
         'env_light_upvec', 'env_light_dirvec', 'activate_env_ground',
         'activate_env_ground_shadow', 'model_scale',
         'env_light_ground_height', 'is_ground_shadow_at_fix_axis',
         'ground_shadow_axis']

    _child_classes = dict(
        hide_environment_keep_effects=hide_environment_keep_effects_cls,
        environment_image=environment_image_cls,
        vertical=vertical_cls,
        horizontal=horizontal_cls,
        spin=spin_cls,
        env_color=env_color_cls,
        env_intensity=env_intensity_cls,
        view_zoom=view_zoom_cls,
        show_backplate=show_backplate_cls,
        backplate_color=backplate_color_cls,
        backplate_image=backplate_image_cls,
        env_light_upvec=env_light_upvec_cls,
        env_light_dirvec=env_light_dirvec_cls,
        activate_env_ground=activate_env_ground_cls,
        activate_env_ground_shadow=activate_env_ground_shadow_cls,
        model_scale=model_scale_cls,
        env_light_ground_height=env_light_ground_height_cls,
        is_ground_shadow_at_fix_axis=is_ground_shadow_at_fix_axis_cls,
        ground_shadow_axis=ground_shadow_axis_cls,
    )

