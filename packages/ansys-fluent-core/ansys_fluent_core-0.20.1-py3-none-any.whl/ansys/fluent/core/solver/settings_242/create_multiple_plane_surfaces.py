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

from .method_11 import method as method_cls
from .name_format import name_format as name_format_cls
from .x_6 import x as x_cls
from .y_6 import y as y_cls
from .z_6 import z as z_cls
from .point_1 import point as point_cls
from .normal_computation_method import normal_computation_method as normal_computation_method_cls
from .surface_aligned_normal import surface_aligned_normal as surface_aligned_normal_cls
from .normal import normal as normal_cls
from .p0_1 import p0 as p0_cls
from .p1_1 import p1 as p1_cls
from .p2 import p2 as p2_cls
from .bounded import bounded as bounded_cls
from .sample_points import sample_points as sample_points_cls
from .edges import edges as edges_cls
from .surfaces_7 import surfaces as surfaces_cls
from .spacing import spacing as spacing_cls
class create_multiple_plane_surfaces(Command):
    """
    Specify the attributes of plane surface.
    
    Parameters
    ----------
        method : str
            Select the method you want to use to create the plane surface. The required inputs vary by method.
        name_format : str
            Specify the Name Format.
        x : real
            Specify the location on the X-axis where the YZ plane will be created.
        y : real
            Specify the location on the Y-axis where the ZX plane will be created.
        z : real
            Specify the location on the Z-axis where the XY plane will be created.
        point : typing.List[real]
            Specify the XYZ coordinates of the point.
        normal_computation_method : str
            Specify the normal computation method.
        surface_aligned_normal : str
            Select the surface you want to compute the normal components.
        normal : typing.List[real]
            Specify the XYZ components of the normal.
        p0 : typing.List[real]
            Specify the XYZ coordinates of Point 1 for the Three Points plane creation method.
        p1 : typing.List[real]
            Specify the XYZ coordinates of Point 2 for the Three Points plane creation method.
        p2 : typing.List[real]
            Specify the XYZ coordinates of Point 3 for the Three Points plane creation method.
        bounded : bool
            Choose whether or not the plane is bounded by its defining points.
        sample_points : bool
            Choose whether or not you want to specify a uniform distribution of points on the plane.
        edges : typing.List[int]
            Specify the point density for edges.
        surfaces : int
            Specify the number of surfaces to be created.
        spacing : real
            Specify the spacing.
    
    """

    fluent_name = "create-multiple-plane-surfaces"

    argument_names = \
        ['method', 'name_format', 'x', 'y', 'z', 'point',
         'normal_computation_method', 'surface_aligned_normal', 'normal',
         'p0', 'p1', 'p2', 'bounded', 'sample_points', 'edges', 'surfaces',
         'spacing']

    _child_classes = dict(
        method=method_cls,
        name_format=name_format_cls,
        x=x_cls,
        y=y_cls,
        z=z_cls,
        point=point_cls,
        normal_computation_method=normal_computation_method_cls,
        surface_aligned_normal=surface_aligned_normal_cls,
        normal=normal_cls,
        p0=p0_cls,
        p1=p1_cls,
        p2=p2_cls,
        bounded=bounded_cls,
        sample_points=sample_points_cls,
        edges=edges_cls,
        surfaces=surfaces_cls,
        spacing=spacing_cls,
    )

