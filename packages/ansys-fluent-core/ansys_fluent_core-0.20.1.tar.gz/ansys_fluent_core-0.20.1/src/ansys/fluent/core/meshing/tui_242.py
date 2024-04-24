"""Fluent meshing TUI commands"""
#
# This is an auto-generated file.  DO NOT EDIT!
#
# pylint: disable=line-too-long

from ansys.fluent.core.services.datamodel_tui import PyMenu, TUIMenu, TUIMethod



class main_menu(TUIMenu):
    """
    Fluent meshing main menu.
    """
    def __init__(self, service, version, mode, path):
        self.material_point = self.__class__.material_point(service, version, mode, path + ["material_point"])
        self.objects = self.__class__.objects(service, version, mode, path + ["objects"])
        self.diagnostics = self.__class__.diagnostics(service, version, mode, path + ["diagnostics"])
        self.file = self.__class__.file(service, version, mode, path + ["file"])
        self.size_functions = self.__class__.size_functions(service, version, mode, path + ["size_functions"])
        self.boundary = self.__class__.boundary(service, version, mode, path + ["boundary"])
        self.parallel = self.__class__.parallel(service, version, mode, path + ["parallel"])
        self.reference_frames = self.__class__.reference_frames(service, version, mode, path + ["reference_frames"])
        self.cad_assemblies = self.__class__.cad_assemblies(service, version, mode, path + ["cad_assemblies"])
        self.display = self.__class__.display(service, version, mode, path + ["display"])
        self.openmp_controls = self.__class__.openmp_controls(service, version, mode, path + ["openmp_controls"])
        self.scoped_sizing = self.__class__.scoped_sizing(service, version, mode, path + ["scoped_sizing"])
        self.preferences = self.__class__.preferences(service, version, mode, path + ["preferences"])
        self.report = self.__class__.report(service, version, mode, path + ["report"])
        self.server = self.__class__.server(service, version, mode, path + ["server"])
        self.mesh = self.__class__.mesh(service, version, mode, path + ["mesh"])
        self.exit = self.__class__.exit(service, version, mode, path + ["exit"])
        self.switch_to_solution_mode = self.__class__.switch_to_solution_mode(service, version, mode, path + ["switch_to_solution_mode"])
        self.print_license_usage = self.__class__.print_license_usage(service, version, mode, path + ["print_license_usage"])
        self.close_fluent = self.__class__.close_fluent(service, version, mode, path + ["close_fluent"])
        self.beta_feature_access = self.__class__.beta_feature_access(service, version, mode, path + ["beta_feature_access"])
        super().__init__(service, version, mode, path)
    class exit(TUIMethod):
        """
        Exits the program.
        """
    class switch_to_solution_mode(TUIMethod):
        """
        Enables you to transfer the mesh data from meshing mode to solution mode in ANSYS Fluent. When you use the switch-to-solution-mode command, you will be asked to confirm that you want to switch to solution mode.
        """
    class print_license_usage(TUIMethod):
        """
        Print license usage information.
        """
    class close_fluent(TUIMethod):
        """
        (ANSYS Fluent in Workbench only) Exits program.
        """
    class beta_feature_access(TUIMethod):
        """
        Enable access to beta features in the interface.
        """

    class material_point(TUIMenu):
        """
        Manage material points.
        """
        def __init__(self, service, version, mode, path):
            self.create_material_point = self.__class__.create_material_point(service, version, mode, path + ["create_material_point"])
            self.delete_material_point = self.__class__.delete_material_point(service, version, mode, path + ["delete_material_point"])
            self.delete_all_material_points = self.__class__.delete_all_material_points(service, version, mode, path + ["delete_all_material_points"])
            self.list_material_points = self.__class__.list_material_points(service, version, mode, path + ["list_material_points"])
            super().__init__(service, version, mode, path)
        class create_material_point(TUIMethod):
            """
            Enables the definition of a material point. Specify the fluid zone name and the location to define the material point.
            """
        class delete_material_point(TUIMethod):
            """
            Deletes the specified material point.
            """
        class delete_all_material_points(TUIMethod):
            """
            Enables the deletion of all defined material points.
            """
        class list_material_points(TUIMethod):
            """
            Lists all the defined material points.
            """

    class objects(TUIMenu):
        """
        Manage objects.
        """
        def __init__(self, service, version, mode, path):
            self.create_new_mesh_object = self.__class__.create_new_mesh_object(service, version, mode, path + ["create_new_mesh_object"])
            self.labels = self.__class__.labels(service, version, mode, path + ["labels"])
            self.fix_holes = self.__class__.fix_holes(service, version, mode, path + ["fix_holes"])
            self.cad_association = self.__class__.cad_association(service, version, mode, path + ["cad_association"])
            self.deprecated = self.__class__.deprecated(service, version, mode, path + ["deprecated"])
            self.join_intersect = self.__class__.join_intersect(service, version, mode, path + ["join_intersect"])
            self.set = self.__class__.set(service, version, mode, path + ["set"])
            self.remove_gaps = self.__class__.remove_gaps(service, version, mode, path + ["remove_gaps"])
            self.volumetric_regions = self.__class__.volumetric_regions(service, version, mode, path + ["volumetric_regions"])
            self.wrap = self.__class__.wrap(service, version, mode, path + ["wrap"])
            self.extract_edges = self.__class__.extract_edges(service, version, mode, path + ["extract_edges"])
            self.rename_object = self.__class__.rename_object(service, version, mode, path + ["rename_object"])
            self.translate = self.__class__.translate(service, version, mode, path + ["translate"])
            self.check_mesh = self.__class__.check_mesh(service, version, mode, path + ["check_mesh"])
            self.clear_backup = self.__class__.clear_backup(service, version, mode, path + ["clear_backup"])
            self.improve_object_quality = self.__class__.improve_object_quality(service, version, mode, path + ["improve_object_quality"])
            self.create_and_activate_domain = self.__class__.create_and_activate_domain(service, version, mode, path + ["create_and_activate_domain"])
            self.create_groups = self.__class__.create_groups(service, version, mode, path + ["create_groups"])
            self.create = self.__class__.create(service, version, mode, path + ["create"])
            self.merge_voids = self.__class__.merge_voids(service, version, mode, path + ["merge_voids"])
            self.merge_nodes = self.__class__.merge_nodes(service, version, mode, path + ["merge_nodes"])
            self.change_suffix = self.__class__.change_suffix(service, version, mode, path + ["change_suffix"])
            self.rename_object_zones = self.__class__.rename_object_zones(service, version, mode, path + ["rename_object_zones"])
            self.create_intersection_loops = self.__class__.create_intersection_loops(service, version, mode, path + ["create_intersection_loops"])
            self.sew = self.__class__.sew(service, version, mode, path + ["sew"])
            self.restore_faces = self.__class__.restore_faces(service, version, mode, path + ["restore_faces"])
            self.create_multiple = self.__class__.create_multiple(service, version, mode, path + ["create_multiple"])
            self.delete_unreferenced_faces_and_edges = self.__class__.delete_unreferenced_faces_and_edges(service, version, mode, path + ["delete_unreferenced_faces_and_edges"])
            self.change_prefix = self.__class__.change_prefix(service, version, mode, path + ["change_prefix"])
            self.rename_cell_zone_boundaries_using_labels = self.__class__.rename_cell_zone_boundaries_using_labels(service, version, mode, path + ["rename_cell_zone_boundaries_using_labels"])
            self.update = self.__class__.update(service, version, mode, path + ["update"])
            self.improve_feature_capture = self.__class__.improve_feature_capture(service, version, mode, path + ["improve_feature_capture"])
            self.separate_faces_by_seed = self.__class__.separate_faces_by_seed(service, version, mode, path + ["separate_faces_by_seed"])
            self.separate_faces_by_angle = self.__class__.separate_faces_by_angle(service, version, mode, path + ["separate_faces_by_angle"])
            self.change_object_type = self.__class__.change_object_type(service, version, mode, path + ["change_object_type"])
            self.summary = self.__class__.summary(service, version, mode, path + ["summary"])
            self.merge_edges = self.__class__.merge_edges(service, version, mode, path + ["merge_edges"])
            self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
            self.delete_all = self.__class__.delete_all(service, version, mode, path + ["delete_all"])
            self.merge = self.__class__.merge(service, version, mode, path + ["merge"])
            self.rotate = self.__class__.rotate(service, version, mode, path + ["rotate"])
            self.list = self.__class__.list(service, version, mode, path + ["list"])
            self.scale = self.__class__.scale(service, version, mode, path + ["scale"])
            self.merge_walls = self.__class__.merge_walls(service, version, mode, path + ["merge_walls"])
            self.delete_all_geom = self.__class__.delete_all_geom(service, version, mode, path + ["delete_all_geom"])
            super().__init__(service, version, mode, path)
        class extract_edges(TUIMethod):
            """
            Extracts the edge zone(s) from the face zone(s) included in the specified object(s), based on the edge-feature-angle value specified (/objects/set/set-edge-feature-angle).
            """
        class rename_object(TUIMethod):
            """
            Allows you to rename a specified geometry or mesh object with another specified name.
            """
        class translate(TUIMethod):
            """
            Translates the object(s) based on the translation offsets specified.
            """
        class check_mesh(TUIMethod):
            """
            Checks the mesh on the specified objects for connectivity and orientation of faces. The domain extents, volume statistics, and face area statistics will be reported along with the results of other checks on the mesh.
            """
        class clear_backup(TUIMethod):
            """
            Clear backup data of objects.
            """
        class improve_object_quality(TUIMethod):
            """
            Enables you to improve the surface mesh quality for mesh objects. Select the mesh objects and the method for improving the surface mesh. The smooth-and-improve method improves the mesh by a combination of smoothing, swapping, and surface mesh improvement operations. Object normals are correctly oriented and island faces are also deleted. You can optionally coarsen the surface mesh by specifying a suitable coarsening factor. Additional imprinting operations can be done to improve feature capture on the surface mesh. The surface-remesh method improves the mesh by remeshing based on the current size field. Object normals are correctly oriented and island faces are also deleted.
            """
        class create_and_activate_domain(TUIMethod):
            """
            Creates and activates the domain comprising the face zone(s) from the object(s) specified.
            """
        class create_groups(TUIMethod):
            """
            Creates a face group and an edge group comprising the face zone(s) and edge zone(s) included in the specified object(s), respectively.
            """
        class create(TUIMethod):
            """
            Creates the object based on the priority, cell zone type, face zone(s), edge zone(s), and object type specified. You can specify the object name or retain the default blank entry to have the object name generated automatically.
            """
        class merge_voids(TUIMethod):
            """
            Allows you to merge voids in the mesh object after the sewing operation.
            """
        class merge_nodes(TUIMethod):
            """
            Merges the free nodes at the object level based on the specified tolerance or using a tolerance that is a specified percentage of shortest connected edge length.
            """
        class change_suffix(TUIMethod):
            """
            Change the suffix for specified objects.
            """
        class rename_object_zones(TUIMethod):
            """
            Renames the face and edge zones comprising the object based on the object name. You can also specify the separator to be used.
            """
        class create_intersection_loops(TUIMethod):
            """
            Allows you to create intersection loops for objects.
            """
        class sew(TUIMethod):
            """
            Contains options related to the object sewing operation. This menu is no longer supported, and will be removed in a future release.
            """
        class restore_faces(TUIMethod):
            """
            Restores the mesh object surface mesh from the backup created. The current mesh object face zones and cell zones will be deleted.  If the object backup is disabled (/mesh/auto-mesh-controls/backup-object no), you will not be able to restore the surface mesh using this command.  There may be a difference in the initial volume mesh generated for an object and that generated after restoring the object surface mesh due to differences in the order of zones/entities processed during volume meshing.
            """
        class create_multiple(TUIMethod):
            """
            Creates multiple objects by creating an object per face zone specified. The objects will be named automatically based on the prefix and priority specified.
            """
        class delete_unreferenced_faces_and_edges(TUIMethod):
            """
            Deletes all the faces and edges that are not included in any defined objects.
            """
        class change_prefix(TUIMethod):
            """
            Change the prefix for specified objects.
            """
        class rename_cell_zone_boundaries_using_labels(TUIMethod):
            """
            Renames the boundaries of the cell zones based on the existing face zone labels. This allows for the cell zone boundaries in solution mode to have names corresponding to the face zone labels in meshing mode.   This command will not work if you read in a volume mesh generated in a version prior to release 16.2. In such cases, regenerate the volume mesh before using the command.
            """
        class update(TUIMethod):
            """
            Allows you to update the objects defined when the face and/or edge zone(s) comprising the object have been deleted.
            """
        class improve_feature_capture(TUIMethod):
            """
            Enables you to imprint the edges comprising the object on to the object face zones to improve feature capture for mesh objects. You can specify the number of imprinting iterations to be performed.  The geometry objects used to create the mesh objects should be available when the improve-feature-capture command is invoked. Additionally, the face zones comprising the objects should be of type other than geometry.
            """
        class separate_faces_by_seed(TUIMethod):
            """
            Separates the face zone(s) comprising the object based on the seed face specified.
            """
        class separate_faces_by_angle(TUIMethod):
            """
            Separates the face zone(s) comprising the object based on the angle specified.
            """
        class change_object_type(TUIMethod):
            """
            Allows you to change the object type (geom, or mesh).
            """
        class summary(TUIMethod):
            """
            Allows you to obtain a summary of a specified geometry or mesh object, or obtain a summary of all geometry or mesh objects.
            """
        class merge_edges(TUIMethod):
            """
            Merges all the edge zones in an object into a single edge zone.  If the object is composed of edge zones of different types (boundary and interior), the edge zones of the same type (boundary or interior) will be merged into a single edge zone.
            """
        class delete(TUIMethod):
            """
            Deletes the specified object(s).
            """
        class delete_all(TUIMethod):
            """
            Deletes all the defined objects.
            """
        class merge(TUIMethod):
            """
            Merges the specified objects into a single object.
            """
        class rotate(TUIMethod):
            """
            Rotates the object(s) based on the angle of rotation, pivot point, and axis of rotation specified.
            """
        class list(TUIMethod):
            """
            Lists details such as cell zone type, priority, object type, comprising face and edge zones, and object reference point for all the defined objects.
            """
        class scale(TUIMethod):
            """
            Scales the object(s) based on the scale factors specified.
            """
        class merge_walls(TUIMethod):
            """
            Merges all the face zones of type wall in an object into a single face zone.
            """
        class delete_all_geom(TUIMethod):
            """
            Deletes all the defined geom objects.
            """

        class create_new_mesh_object(TUIMenu):
            """
            Contains options for creating a new mesh object by wrapping or remeshing existing objects.
            """
            def __init__(self, service, version, mode, path):
                self.remesh = self.__class__.remesh(service, version, mode, path + ["remesh"])
                self.wrap = self.__class__.wrap(service, version, mode, path + ["wrap"])
                super().__init__(service, version, mode, path)
            class remesh(TUIMethod):
                """
                Creates a new mesh object by remeshing geometry objects individually or collectively.
                """
            class wrap(TUIMethod):
                """
                Creates a new mesh object by wrapping the specified objects individually or collectively.
                """

        class labels(TUIMenu):
            """
            Contains options for creating and managing face zone labels.
            """
            def __init__(self, service, version, mode, path):
                self.cavity = self.__class__.cavity(service, version, mode, path + ["cavity"])
                self.merge = self.__class__.merge(service, version, mode, path + ["merge"])
                self.rename = self.__class__.rename(service, version, mode, path + ["rename"])
                self.remove_zones = self.__class__.remove_zones(service, version, mode, path + ["remove_zones"])
                self.label_unlabeled_zones = self.__class__.label_unlabeled_zones(service, version, mode, path + ["label_unlabeled_zones"])
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                self.create_label_per_zone = self.__class__.create_label_per_zone(service, version, mode, path + ["create_label_per_zone"])
                self.remove_all_labels_on_zones = self.__class__.remove_all_labels_on_zones(service, version, mode, path + ["remove_all_labels_on_zones"])
                self.create_label_per_object = self.__class__.create_label_per_object(service, version, mode, path + ["create_label_per_object"])
                self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                self.add_zones = self.__class__.add_zones(service, version, mode, path + ["add_zones"])
                super().__init__(service, version, mode, path)
            class merge(TUIMethod):
                """
                Merges the specified face zone labels to a single label with the name specified.
                """
            class rename(TUIMethod):
                """
                Renames the specified face zone label.
                """
            class remove_zones(TUIMethod):
                """
                Removes the specified face zones from the existing face zone label for an object.
                """
            class label_unlabeled_zones(TUIMethod):
                """
                Creates labels for unlabeled face zones within the specified object. You can either use the object name as the label or provide your own label.
                """
            class create(TUIMethod):
                """
                Creates a new face zone label for the specified face zones.
                """
            class create_label_per_zone(TUIMethod):
                """
                Creates a new face zone label for each face zone in the object.
                """
            class remove_all_labels_on_zones(TUIMethod):
                """
                Removes all the face zone labels for the specified face zones. This command is applicable to geometry objects only.
                """
            class create_label_per_object(TUIMethod):
                """
                Creates a new face zone label for all the face zones in every object.
                """
            class delete(TUIMethod):
                """
                Deletes the specified face zone labels.
                """
            class add_zones(TUIMethod):
                """
                Adds the specified face zones to the existing face zone label for an object.
                """

            class cavity(TUIMenu):
                """
                Enter menu to create cavity using labels.
                """
                def __init__(self, service, version, mode, path):
                    self.replace = self.__class__.replace(service, version, mode, path + ["replace"])
                    self.remove = self.__class__.remove(service, version, mode, path + ["remove"])
                    self.add = self.__class__.add(service, version, mode, path + ["add"])
                    super().__init__(service, version, mode, path)
                class replace(TUIMethod):
                    """
                    Create cavity by replacing labels from another mesh object.
                    """
                class remove(TUIMethod):
                    """
                    Create cavity by removing labels.
                    """
                class add(TUIMethod):
                    """
                    Create cavity by adding labels from another mesh object.
                    """

        class fix_holes(TUIMenu):
            """
            Fix holes in surface mesh using octree.
            """
            def __init__(self, service, version, mode, path):
                self.advanced = self.__class__.advanced(service, version, mode, path + ["advanced"])
                self.patch_all_holes = self.__class__.patch_all_holes(service, version, mode, path + ["patch_all_holes"])
                self.shrink_wrap = self.__class__.shrink_wrap(service, version, mode, path + ["shrink_wrap"])
                self.find_holes = self.__class__.find_holes(service, version, mode, path + ["find_holes"])
                self.reset_material_point = self.__class__.reset_material_point(service, version, mode, path + ["reset_material_point"])
                self.open_holes = self.__class__.open_holes(service, version, mode, path + ["open_holes"])
                self.open_all_holes = self.__class__.open_all_holes(service, version, mode, path + ["open_all_holes"])
                self.patch_holes = self.__class__.patch_holes(service, version, mode, path + ["patch_holes"])
                super().__init__(service, version, mode, path)
            class patch_all_holes(TUIMethod):
                """
                Patch all wetted holes of the material point.
                """
            class shrink_wrap(TUIMethod):
                """
                Shrink wrap wetted region of material point.
                """
            class find_holes(TUIMethod):
                """
                Find holes in objects using octree.
                """
            class reset_material_point(TUIMethod):
                """
                Reset material point of of region of interest.
                """
            class open_holes(TUIMethod):
                """
                Open holes even not connected by material point.
                """
            class open_all_holes(TUIMethod):
                """
                Open all wetted holes of the material point.
                """
            class patch_holes(TUIMethod):
                """
                Patch holes even not connected by material point.
                """

            class advanced(TUIMenu):
                """
                Advanced fix holes options.
                """
                def __init__(self, service, version, mode, path):
                    self.open_holes_not_connected_to_material_points = self.__class__.open_holes_not_connected_to_material_points(service, version, mode, path + ["open_holes_not_connected_to_material_points"])
                    self.patch_holes_between_material_points = self.__class__.patch_holes_between_material_points(service, version, mode, path + ["patch_holes_between_material_points"])
                    self.patch_holes_not_connected_to_material_points = self.__class__.patch_holes_not_connected_to_material_points(service, version, mode, path + ["patch_holes_not_connected_to_material_points"])
                    self.open_holes_between_material_points = self.__class__.open_holes_between_material_points(service, version, mode, path + ["open_holes_between_material_points"])
                    self.open_holes_connected_to_material_points = self.__class__.open_holes_connected_to_material_points(service, version, mode, path + ["open_holes_connected_to_material_points"])
                    self.patch_holes_connected_to_material_points = self.__class__.patch_holes_connected_to_material_points(service, version, mode, path + ["patch_holes_connected_to_material_points"])
                    self.open_traced_holes_between_material_points = self.__class__.open_traced_holes_between_material_points(service, version, mode, path + ["open_traced_holes_between_material_points"])
                    super().__init__(service, version, mode, path)
                class open_holes_not_connected_to_material_points(TUIMethod):
                    """
                    Open all holes other than holes wetted by material points.
                    """
                class patch_holes_between_material_points(TUIMethod):
                    """
                    Patch holes separating the material points.
                    """
                class patch_holes_not_connected_to_material_points(TUIMethod):
                    """
                    Patch all holes other than holes wetted by material points.
                    """
                class open_holes_between_material_points(TUIMethod):
                    """
                    Open holes separating the material points to merge them.
                    """
                class open_holes_connected_to_material_points(TUIMethod):
                    """
                    Open all holes wetted by material points.
                    """
                class patch_holes_connected_to_material_points(TUIMethod):
                    """
                    Patch all holes wetted by material points.
                    """
                class open_traced_holes_between_material_points(TUIMethod):
                    """
                    Trace a path between material points and open holes part of the traced path.
                    """

        class cad_association(TUIMenu):
            """
            Contains options for modifying the selected objects based on the associated CAD entities and attaching/detaching the CAD entities from the objects. This menu is available when the CAD Assemblies tree is created during CAD import.
            """
            def __init__(self, service, version, mode, path):
                self.detach_objects = self.__class__.detach_objects(service, version, mode, path + ["detach_objects"])
                self.query_object_association = self.__class__.query_object_association(service, version, mode, path + ["query_object_association"])
                self.detach_all_objects = self.__class__.detach_all_objects(service, version, mode, path + ["detach_all_objects"])
                self.attach_cad = self.__class__.attach_cad(service, version, mode, path + ["attach_cad"])
                self.update_all_objects = self.__class__.update_all_objects(service, version, mode, path + ["update_all_objects"])
                self.restore_cad = self.__class__.restore_cad(service, version, mode, path + ["restore_cad"])
                self.unlock_cad = self.__class__.unlock_cad(service, version, mode, path + ["unlock_cad"])
                self.update_objects = self.__class__.update_objects(service, version, mode, path + ["update_objects"])
                super().__init__(service, version, mode, path)
            class detach_objects(TUIMethod):
                """
                Detaches the CAD objects associated with the specified geometry/mesh objects. All association will be removed and the selected geometry/mesh objects will be independent of changes to the CAD entities.
                """
            class query_object_association(TUIMethod):
                """
                Returns a list of the CAD entities associated with the objects selected.
                """
            class detach_all_objects(TUIMethod):
                """
                Detaches all the CAD objects associated with the geometry/mesh objects. Specify the type of objects (geom or mesh) to be detached. All association will be removed and the geometry/mesh objects will be independent of changes to the CAD entities.
                """
            class attach_cad(TUIMethod):
                """
                Attaches CAD entities to the selected geometry/mesh objects. Select the geometry/mesh objects and specify the path for the CAD entities to be associated with the objects. The selected geometry/mesh objects will be associated with the CAD entities which will then be locked.
                """
            class update_all_objects(TUIMethod):
                """
                Updates all geometry/mesh objects based on changes to the associated CAD objects. Specify the type of objects (geom or mesh) to be updated.
                """
            class restore_cad(TUIMethod):
                """
                Restores the geometry/mesh objects from the associated CAD objects.
                """
            class unlock_cad(TUIMethod):
                """
                Unlocks the CAD objects associated with the selected geometry/mesh objects.
                """
            class update_objects(TUIMethod):
                """
                Updates the specified geometry/mesh objects based on changes to the associated CAD objects.
                """

        class deprecated(TUIMenu):
            """
            Deprecated features.
            """
            def __init__(self, service, version, mode, path):
                self.create_mesh_object_from_wrap = self.__class__.create_mesh_object_from_wrap(service, version, mode, path + ["create_mesh_object_from_wrap"])
                super().__init__(service, version, mode, path)
            class create_mesh_object_from_wrap(TUIMethod):
                """
                Create mesh object from a wrap object.
                """

        class join_intersect(TUIMenu):
            """
            Contains options for connecting overlapping and intersecting face zones.
            """
            def __init__(self, service, version, mode, path):
                self.controls = self.__class__.controls(service, version, mode, path + ["controls"])
                self.delete_region = self.__class__.delete_region(service, version, mode, path + ["delete_region"])
                self.change_region_type = self.__class__.change_region_type(service, version, mode, path + ["change_region_type"])
                self.intersect = self.__class__.intersect(service, version, mode, path + ["intersect"])
                self.add_objects_to_mesh_object = self.__class__.add_objects_to_mesh_object(service, version, mode, path + ["add_objects_to_mesh_object"])
                self.join = self.__class__.join(service, version, mode, path + ["join"])
                self.rename_region = self.__class__.rename_region(service, version, mode, path + ["rename_region"])
                self.create_mesh_object = self.__class__.create_mesh_object(service, version, mode, path + ["create_mesh_object"])
                self.merge_regions = self.__class__.merge_regions(service, version, mode, path + ["merge_regions"])
                self.list_regions = self.__class__.list_regions(service, version, mode, path + ["list_regions"])
                self.compute_regions = self.__class__.compute_regions(service, version, mode, path + ["compute_regions"])
                super().__init__(service, version, mode, path)
            class delete_region(TUIMethod):
                """
                Removes a closed cell zone region and all of its face zones, except those which are shared by other regions, from the specified mesh object.
                """
            class change_region_type(TUIMethod):
                """
                Allows you to select a cell zone type (solid, fluid or dead) for a specific region.
                """
            class intersect(TUIMethod):
                """
                Connects two intersecting face zones within specified angle and tolerance.
                """
            class add_objects_to_mesh_object(TUIMethod):
                """
                Allows you to specify one or more mesh objects to be added to an existing mesh object.
                """
            class join(TUIMethod):
                """
                Connects two overlapping face zones within specified angle and tolerance.
                """
            class rename_region(TUIMethod):
                """
                Enables you to specify a new name for a specified region.
                """
            class create_mesh_object(TUIMethod):
                """
                Allows you to specify one or more mesh objects to be connected in one mesh object.
                """
            class merge_regions(TUIMethod):
                """
                Specified regions are joined into a single region.
                """
            class list_regions(TUIMethod):
                """
                Lists details of region type, volume, material point, and comprising face zones for the topological regions computed for the specified mesh object.
                """
            class compute_regions(TUIMethod):
                """
                Closed cell zone regions are computed from the specified mesh object. You may include a material point, if desired.
                """

            class controls(TUIMenu):
                """
                Build topology controls.
                """
                def __init__(self, service, version, mode, path):
                    self.remesh_post_intersection = self.__class__.remesh_post_intersection(service, version, mode, path + ["remesh_post_intersection"])
                    super().__init__(service, version, mode, path)
                class remesh_post_intersection(TUIMethod):
                    """
                    Used to enable or disable automatic post-remesh operation after join or intersect.
                    """

        class set(TUIMenu):
            """
            Contains options for setting additional object-related settings.
            """
            def __init__(self, service, version, mode, path):
                self.show_face_zones = self.__class__.show_face_zones(service, version, mode, path + ["show_face_zones"])
                self.set_edge_feature_angle = self.__class__.set_edge_feature_angle(service, version, mode, path + ["set_edge_feature_angle"])
                self.show_edge_zones = self.__class__.show_edge_zones(service, version, mode, path + ["show_edge_zones"])
                super().__init__(service, version, mode, path)
            class show_face_zones(TUIMethod):
                """
                Displays the face zone(s) comprising the object(s) drawn in the graphics window.
                """
            class set_edge_feature_angle(TUIMethod):
                """
                Sets the edge feature angle to be used for extracting edge zone(s) from the face zone(s) included in the object(s).
                """
            class show_edge_zones(TUIMethod):
                """
                Displays the edge zone(s) comprising the object(s) drawn in the graphics window.
                """

        class remove_gaps(TUIMenu):
            """
            Contains options for removing gaps between the mesh objects specified or removing the thickness in the mesh objects specified.
            """
            def __init__(self, service, version, mode, path):
                self.remove_gaps = self.__class__.remove_gaps(service, version, mode, path + ["remove_gaps"])
                self.show_gaps = self.__class__.show_gaps(service, version, mode, path + ["show_gaps"])
                self.ignore_orientation = self.__class__.ignore_orientation(service, version, mode, path + ["ignore_orientation"])
                super().__init__(service, version, mode, path)
            class remove_gaps(TUIMethod):
                """
                Allows you to remove gaps between the mesh objects specified or remove the thickness in the mesh objects specified. Select the appropriate repair option and specify the other parameters required.
                """
            class show_gaps(TUIMethod):
                """
                Marks the faces at the gap between mesh objects based on the gap distance and percentage margin specified.
                """
            class ignore_orientation(TUIMethod):
                """
                Allows you to set whether the orientation of the normals should be taken into account while identifying the gap to be removed.
                """

        class volumetric_regions(TUIMenu):
            """
            Manage volumetric regions of an object.
            """
            def __init__(self, service, version, mode, path):
                self.scoped_prism = self.__class__.scoped_prism(service, version, mode, path + ["scoped_prism"])
                self.tet = self.__class__.tet(service, version, mode, path + ["tet"])
                self.hexcore = self.__class__.hexcore(service, version, mode, path + ["hexcore"])
                self.compute = self.__class__.compute(service, version, mode, path + ["compute"])
                self.change_type = self.__class__.change_type(service, version, mode, path + ["change_type"])
                self.merge_cells = self.__class__.merge_cells(service, version, mode, path + ["merge_cells"])
                self.merge = self.__class__.merge(service, version, mode, path + ["merge"])
                self.fill_empty_volume = self.__class__.fill_empty_volume(service, version, mode, path + ["fill_empty_volume"])
                self.rename = self.__class__.rename(service, version, mode, path + ["rename"])
                self.update = self.__class__.update(service, version, mode, path + ["update"])
                self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                self.delete_cells = self.__class__.delete_cells(service, version, mode, path + ["delete_cells"])
                self.auto_fill_volume = self.__class__.auto_fill_volume(service, version, mode, path + ["auto_fill_volume"])
                self.list = self.__class__.list(service, version, mode, path + ["list"])
                super().__init__(service, version, mode, path)
            class compute(TUIMethod):
                """
                Computes the volumetric regions based on the face zone labels. You can choose to use existing material points for computing the regions.  When regions are computed, region names and types will be based on the face zone labels of the mesh object selected. If regions are recomputed, all previous region names and types will be over written.
                """
            class change_type(TUIMethod):
                """
                Enables you to change the region type.
                """
            class merge_cells(TUIMethod):
                """
                Merge all cell zones assocaited to a region.
                """
            class merge(TUIMethod):
                """
                Merges specified regions in to a single region.  If there are shared face zones, merging regions will delete the shared face zones. However, if there are cell zones associated with the regions, then merging the regions will not delete the shared face zones. In this case, the shared face zones will be deleted when the cell zones are deleted.
                """
            class fill_empty_volume(TUIMethod):
                """
                Fill empty volume of selected regions.
                """
            class rename(TUIMethod):
                """
                Renames the region.
                """
            class update(TUIMethod):
                """
                Recomputes the selected volumetric region(s) while preserving the region name(s) and type(s).
                """
            class delete(TUIMethod):
                """
                Deletes the specified volumetric regions.
                """
            class delete_cells(TUIMethod):
                """
                Deletes the cell zones of the specified regions.
                """
            class auto_fill_volume(TUIMethod):
                """
                Creates the volume mesh for the selected volumetric regions based on the meshing parameters set.
                """
            class list(TUIMethod):
                """
                Prints region information to the console, including type, volume, material point and face zones.
                """

            class scoped_prism(TUIMenu):
                """
                Contains options for setting scoped prism controls.
                """
                def __init__(self, service, version, mode, path):
                    self.set = self.__class__.set(service, version, mode, path + ["set"])
                    self.generate = self.__class__.generate(service, version, mode, path + ["generate"])
                    super().__init__(service, version, mode, path)
                class generate(TUIMethod):
                    """
                    Grow prism into selected region using scoped prism controls.
                    """

                class set(TUIMenu):
                    """
                    Enter scoped prism settings.
                    """
                    def __init__(self, service, version, mode, path):
                        self.modify = self.__class__.modify(service, version, mode, path + ["modify"])
                        self.read = self.__class__.read(service, version, mode, path + ["read"])
                        self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                        self.set_advanced_controls = self.__class__.set_advanced_controls(service, version, mode, path + ["set_advanced_controls"])
                        self.list = self.__class__.list(service, version, mode, path + ["list"])
                        self.write = self.__class__.write(service, version, mode, path + ["write"])
                        self.set_overset_prism_controls = self.__class__.set_overset_prism_controls(service, version, mode, path + ["set_overset_prism_controls"])
                        self.growth_options = self.__class__.growth_options(service, version, mode, path + ["growth_options"])
                        self.create = self.__class__.create(service, version, mode, path + ["create"])
                        self.set_no_imprint_zones = self.__class__.set_no_imprint_zones(service, version, mode, path + ["set_no_imprint_zones"])
                        self.poly_keep_nlayer_prism_characteristics = self.__class__.poly_keep_nlayer_prism_characteristics(service, version, mode, path + ["poly_keep_nlayer_prism_characteristics"])
                        self.tet_prism_stairstep_exposed_quads = self.__class__.tet_prism_stairstep_exposed_quads(service, version, mode, path + ["tet_prism_stairstep_exposed_quads"])
                        super().__init__(service, version, mode, path)
                    class modify(TUIMethod):
                        """
                        Modify scoped prisms.
                        """
                    class read(TUIMethod):
                        """
                        Read scoped prisms from a file.
                        """
                    class delete(TUIMethod):
                        """
                        Delete scoped prisms.
                        """
                    class set_advanced_controls(TUIMethod):
                        """
                        Set scoped boundary layer controls.
                        """
                    class list(TUIMethod):
                        """
                        List all scoped prisms parameters.
                        """
                    class write(TUIMethod):
                        """
                        Write scoped prisms to a file.
                        """
                    class set_overset_prism_controls(TUIMethod):
                        """
                        Set boundary layer controls for overset mesh generation.
                        """
                    class growth_options(TUIMethod):
                        """
                        Set scoped prisms growth options.
                        """
                    class create(TUIMethod):
                        """
                        Create new scoped prism.
                        """
                    class set_no_imprint_zones(TUIMethod):
                        """
                        Set zones which should not be imprinted during prism generation.
                        """
                    class poly_keep_nlayer_prism_characteristics(TUIMethod):
                        """
                        Number of layers to maintain poly-prism characteristics.
                        """
                    class tet_prism_stairstep_exposed_quads(TUIMethod):
                        """
                        Tet-Prism Stairstep exposed quad.
                        """

            class tet(TUIMenu):
                """
                Contains options for setting tetrahedral mesh controls. See mesh/.
                """
                def __init__(self, service, version, mode, path):
                    self.set = self.__class__.set(service, version, mode, path + ["set"])
                    self.generate = self.__class__.generate(service, version, mode, path + ["generate"])
                    super().__init__(service, version, mode, path)
                class generate(TUIMethod):
                    """
                    Fill empty volume of selected regions with tets.
                    """

                class set(TUIMenu):
                    """
                    Enter tet settings.
                    """
                    def __init__(self, service, version, mode, path):
                        self.remove_slivers = self.__class__.remove_slivers(service, version, mode, path + ["remove_slivers"])
                        self.advanced = self.__class__.advanced(service, version, mode, path + ["advanced"])
                        self.improve_mesh = self.__class__.improve_mesh(service, version, mode, path + ["improve_mesh"])
                        self.tet_improve = self.__class__.tet_improve(service, version, mode, path + ["tet_improve"])
                        self.adv_front_method = self.__class__.adv_front_method(service, version, mode, path + ["adv_front_method"])
                        self.merge_free_nodes = self.__class__.merge_free_nodes(service, version, mode, path + ["merge_free_nodes"])
                        self.clear_zone_growth_rate = self.__class__.clear_zone_growth_rate(service, version, mode, path + ["clear_zone_growth_rate"])
                        self.delete_unused_nodes = self.__class__.delete_unused_nodes(service, version, mode, path + ["delete_unused_nodes"])
                        self.non_fluid_type = self.__class__.non_fluid_type(service, version, mode, path + ["non_fluid_type"])
                        self.max_cell_length = self.__class__.max_cell_length(service, version, mode, path + ["max_cell_length"])
                        self.use_max_cell_size = self.__class__.use_max_cell_size(service, version, mode, path + ["use_max_cell_size"])
                        self.skewness_method = self.__class__.skewness_method(service, version, mode, path + ["skewness_method"])
                        self.improve_surface_mesh = self.__class__.improve_surface_mesh(service, version, mode, path + ["improve_surface_mesh"])
                        self.delete_dead_zones = self.__class__.delete_dead_zones(service, version, mode, path + ["delete_dead_zones"])
                        self.set_region_based_sizing = self.__class__.set_region_based_sizing(service, version, mode, path + ["set_region_based_sizing"])
                        self.refine_method = self.__class__.refine_method(service, version, mode, path + ["refine_method"])
                        self.max_cell_volume = self.__class__.max_cell_volume(service, version, mode, path + ["max_cell_volume"])
                        self.set_zone_growth_rate = self.__class__.set_zone_growth_rate(service, version, mode, path + ["set_zone_growth_rate"])
                        self.compute_max_cell_volume = self.__class__.compute_max_cell_volume(service, version, mode, path + ["compute_max_cell_volume"])
                        self.print_region_based_sizing = self.__class__.print_region_based_sizing(service, version, mode, path + ["print_region_based_sizing"])
                        self.cell_sizing = self.__class__.cell_sizing(service, version, mode, path + ["cell_sizing"])
                        super().__init__(service, version, mode, path)
                    class merge_free_nodes(TUIMethod):
                        """
                        Automatically merge duplicate nodes?.
                        """
                    class clear_zone_growth_rate(TUIMethod):
                        """
                        Clear zone specific geometric growth rates.
                        """
                    class delete_unused_nodes(TUIMethod):
                        """
                        Automatically delete unused nodes?.
                        """
                    class non_fluid_type(TUIMethod):
                        """
                        Select the default non-fluid cell zone type.
                        """
                    class max_cell_length(TUIMethod):
                        """
                        Set max-cell-length.
                        """
                    class use_max_cell_size(TUIMethod):
                        """
                        Use max cell size for objects in auto-mesh and do not recompute it based on the object being meshed.
                        """
                    class skewness_method(TUIMethod):
                        """
                        Skewness refinement controls.
                        """
                    class improve_surface_mesh(TUIMethod):
                        """
                        Automatically improve surface mesh?.
                        """
                    class delete_dead_zones(TUIMethod):
                        """
                        Automatically delete dead face and cell zones?.
                        """
                    class set_region_based_sizing(TUIMethod):
                        """
                        Set region based sizings.
                        """
                    class refine_method(TUIMethod):
                        """
                        Define refinement method.
                        """
                    class max_cell_volume(TUIMethod):
                        """
                        Set max-cell-volume.
                        """
                    class set_zone_growth_rate(TUIMethod):
                        """
                        Set zone specific geometric growth rates.
                        """
                    class compute_max_cell_volume(TUIMethod):
                        """
                        Computes max cell size.
                        """
                    class print_region_based_sizing(TUIMethod):
                        """
                        Print region based sizings.
                        """
                    class cell_sizing(TUIMethod):
                        """
                        Allow cell volume distribution to be determined based on boundary.
                        """

                    class remove_slivers(TUIMenu):
                        """
                        Sliver remove controls.
                        """
                        def __init__(self, service, version, mode, path):
                            self.low_skew = self.__class__.low_skew(service, version, mode, path + ["low_skew"])
                            self.remove = self.__class__.remove(service, version, mode, path + ["remove"])
                            self.skew = self.__class__.skew(service, version, mode, path + ["skew"])
                            self.angle = self.__class__.angle(service, version, mode, path + ["angle"])
                            self.iterations = self.__class__.iterations(service, version, mode, path + ["iterations"])
                            self.method = self.__class__.method(service, version, mode, path + ["method"])
                            self.attempts = self.__class__.attempts(service, version, mode, path + ["attempts"])
                            super().__init__(service, version, mode, path)
                        class low_skew(TUIMethod):
                            """
                            Remove sliver low skew.
                            """
                        class remove(TUIMethod):
                            """
                            Automatically remove slivers.
                            """
                        class skew(TUIMethod):
                            """
                            Remove sliver skew.
                            """
                        class angle(TUIMethod):
                            """
                            Max dihedral angle defining a valid boundary sliver.
                            """
                        class iterations(TUIMethod):
                            """
                            Sliver remove iterations.
                            """
                        class method(TUIMethod):
                            """
                            Sliver remove method.
                            """
                        class attempts(TUIMethod):
                            """
                            Sliver remove attempts.
                            """

                    class advanced(TUIMenu):
                        """
                        Tet advanced controls.
                        """
                        def __init__(self, service, version, mode, path):
                            self.max_nodes = self.__class__.max_nodes(service, version, mode, path + ["max_nodes"])
                            self.defaults = self.__class__.defaults(service, version, mode, path + ["defaults"])
                            self.progress_reports = self.__class__.progress_reports(service, version, mode, path + ["progress_reports"])
                            self.node_tolerance = self.__class__.node_tolerance(service, version, mode, path + ["node_tolerance"])
                            self.freeze_boundary_cells = self.__class__.freeze_boundary_cells(service, version, mode, path + ["freeze_boundary_cells"])
                            self.report_max_unmeshed = self.__class__.report_max_unmeshed(service, version, mode, path + ["report_max_unmeshed"])
                            self.max_cells = self.__class__.max_cells(service, version, mode, path + ["max_cells"])
                            self.sliver_size = self.__class__.sliver_size(service, version, mode, path + ["sliver_size"])
                            self.keep_virtual_entities = self.__class__.keep_virtual_entities(service, version, mode, path + ["keep_virtual_entities"])
                            self.report_unmeshed_nodes = self.__class__.report_unmeshed_nodes(service, version, mode, path + ["report_unmeshed_nodes"])
                            self.report_unmeshed_faces = self.__class__.report_unmeshed_faces(service, version, mode, path + ["report_unmeshed_faces"])
                            super().__init__(service, version, mode, path)
                        class max_nodes(TUIMethod):
                            """
                            Set maximum number of nodes in mesh.
                            """
                        class defaults(TUIMethod):
                            """
                            Calculate defaults.
                            """
                        class progress_reports(TUIMethod):
                            """
                            Set time between progress reports in seconds.
                            """
                        class node_tolerance(TUIMethod):
                            """
                            Set node-tolerance.
                            """
                        class freeze_boundary_cells(TUIMethod):
                            """
                            Freeze boundary cells .
                            """
                        class report_max_unmeshed(TUIMethod):
                            """
                            Max number of unmeshed entities reported.
                            """
                        class max_cells(TUIMethod):
                            """
                            Set maximum number of cells in mesh.
                            """
                        class sliver_size(TUIMethod):
                            """
                            Set sliver-size.
                            """
                        class keep_virtual_entities(TUIMethod):
                            """
                            Toggle deletion of virtual entities after intialization.
                            """
                        class report_unmeshed_nodes(TUIMethod):
                            """
                            Report unmeshed nodes.
                            """
                        class report_unmeshed_faces(TUIMethod):
                            """
                            Report unmeshed faces.
                            """

                    class improve_mesh(TUIMenu):
                        """
                        Improve mesh controls.
                        """
                        def __init__(self, service, version, mode, path):
                            self.improve = self.__class__.improve(service, version, mode, path + ["improve"])
                            self.swap = self.__class__.swap(service, version, mode, path + ["swap"])
                            self.skewness_smooth = self.__class__.skewness_smooth(service, version, mode, path + ["skewness_smooth"])
                            self.laplace_smooth = self.__class__.laplace_smooth(service, version, mode, path + ["laplace_smooth"])
                            super().__init__(service, version, mode, path)
                        class improve(TUIMethod):
                            """
                            Automatically improve mesh.
                            """
                        class swap(TUIMethod):
                            """
                            Face swap parameters.
                            """
                        class skewness_smooth(TUIMethod):
                            """
                            Skewness smooth parametersx.
                            """
                        class laplace_smooth(TUIMethod):
                            """
                            Laplace smooth parameters.
                            """

                    class tet_improve(TUIMenu):
                        """
                        Improve cells controls.
                        """
                        def __init__(self, service, version, mode, path):
                            self.attempts = self.__class__.attempts(service, version, mode, path + ["attempts"])
                            self.angle = self.__class__.angle(service, version, mode, path + ["angle"])
                            self.iterations = self.__class__.iterations(service, version, mode, path + ["iterations"])
                            self.skew = self.__class__.skew(service, version, mode, path + ["skew"])
                            super().__init__(service, version, mode, path)
                        class attempts(TUIMethod):
                            """
                            Improve attempts.
                            """
                        class angle(TUIMethod):
                            """
                            Max dihedral angle defining a valid boundary cell.
                            """
                        class iterations(TUIMethod):
                            """
                            Improve iterations.
                            """
                        class skew(TUIMethod):
                            """
                            Remove skew.
                            """

                    class adv_front_method(TUIMenu):
                        """
                        Advancing front refinement controls.
                        """
                        def __init__(self, service, version, mode, path):
                            self.skew_improve = self.__class__.skew_improve(service, version, mode, path + ["skew_improve"])
                            self.second_improve_params = self.__class__.second_improve_params(service, version, mode, path + ["second_improve_params"])
                            self.first_improve_params = self.__class__.first_improve_params(service, version, mode, path + ["first_improve_params"])
                            self.refine_parameters = self.__class__.refine_parameters(service, version, mode, path + ["refine_parameters"])
                            super().__init__(service, version, mode, path)
                        class second_improve_params(TUIMethod):
                            """
                            Define cell zone improve parameters.
                            """
                        class first_improve_params(TUIMethod):
                            """
                            Define refine front improve parameters.
                            """
                        class refine_parameters(TUIMethod):
                            """
                            Define refine parameters.
                            """

                        class skew_improve(TUIMenu):
                            """
                            Refine improve controls.
                            """
                            def __init__(self, service, version, mode, path):
                                self.sliver_skew = self.__class__.sliver_skew(service, version, mode, path + ["sliver_skew"])
                                self.iterations = self.__class__.iterations(service, version, mode, path + ["iterations"])
                                self.target = self.__class__.target(service, version, mode, path + ["target"])
                                self.target_low_skew = self.__class__.target_low_skew(service, version, mode, path + ["target_low_skew"])
                                self.target_skew = self.__class__.target_skew(service, version, mode, path + ["target_skew"])
                                self.boundary_sliver_skew = self.__class__.boundary_sliver_skew(service, version, mode, path + ["boundary_sliver_skew"])
                                self.attempts = self.__class__.attempts(service, version, mode, path + ["attempts"])
                                super().__init__(service, version, mode, path)
                            class sliver_skew(TUIMethod):
                                """
                                Refine improve sliver skew.
                                """
                            class iterations(TUIMethod):
                                """
                                Refine improve iterations.
                                """
                            class target(TUIMethod):
                                """
                                Activate target skew refinement.
                                """
                            class target_low_skew(TUIMethod):
                                """
                                Refine improve target low skew.
                                """
                            class target_skew(TUIMethod):
                                """
                                Refine improve target skew.
                                """
                            class boundary_sliver_skew(TUIMethod):
                                """
                                Refine improve boundary sliver skew.
                                """
                            class attempts(TUIMethod):
                                """
                                Refine improve attempts.
                                """

            class hexcore(TUIMenu):
                """
                Contains options for setting hexcore mesh controls. See mesh/.
                """
                def __init__(self, service, version, mode, path):
                    self.set = self.__class__.set(service, version, mode, path + ["set"])
                    self.generate = self.__class__.generate(service, version, mode, path + ["generate"])
                    super().__init__(service, version, mode, path)
                class generate(TUIMethod):
                    """
                    Fill empty volume of selected regions with hexcore.
                    """

                class set(TUIMenu):
                    """
                    Enter hexcore settings.
                    """
                    def __init__(self, service, version, mode, path):
                        self.outer_domain_params = self.__class__.outer_domain_params(service, version, mode, path + ["outer_domain_params"])
                        self.smooth_relaxation = self.__class__.smooth_relaxation(service, version, mode, path + ["smooth_relaxation"])
                        self.maximum_cell_length = self.__class__.maximum_cell_length(service, version, mode, path + ["maximum_cell_length"])
                        self.smooth_interface = self.__class__.smooth_interface(service, version, mode, path + ["smooth_interface"])
                        self.avoid_1_by_8_cell_jump_in_hexcore = self.__class__.avoid_1_by_8_cell_jump_in_hexcore(service, version, mode, path + ["avoid_1_by_8_cell_jump_in_hexcore"])
                        self.skip_tet_refinement = self.__class__.skip_tet_refinement(service, version, mode, path + ["skip_tet_refinement"])
                        self.non_fluid_type = self.__class__.non_fluid_type(service, version, mode, path + ["non_fluid_type"])
                        self.maximum_initial_cells = self.__class__.maximum_initial_cells(service, version, mode, path + ["maximum_initial_cells"])
                        self.print_region_based_sizing = self.__class__.print_region_based_sizing(service, version, mode, path + ["print_region_based_sizing"])
                        self.set_region_based_sizing = self.__class__.set_region_based_sizing(service, version, mode, path + ["set_region_based_sizing"])
                        self.merge_tets_to_pyramids = self.__class__.merge_tets_to_pyramids(service, version, mode, path + ["merge_tets_to_pyramids"])
                        self.buffer_layers = self.__class__.buffer_layers(service, version, mode, path + ["buffer_layers"])
                        self.keep_hex_tet_separate = self.__class__.keep_hex_tet_separate(service, version, mode, path + ["keep_hex_tet_separate"])
                        self.island_thresholds = self.__class__.island_thresholds(service, version, mode, path + ["island_thresholds"])
                        self.maximum_subdivisions = self.__class__.maximum_subdivisions(service, version, mode, path + ["maximum_subdivisions"])
                        self.peel_layers = self.__class__.peel_layers(service, version, mode, path + ["peel_layers"])
                        self.only_hexcore = self.__class__.only_hexcore(service, version, mode, path + ["only_hexcore"])
                        self.define_hexcore_extents = self.__class__.define_hexcore_extents(service, version, mode, path + ["define_hexcore_extents"])
                        self.smooth_iterations = self.__class__.smooth_iterations(service, version, mode, path + ["smooth_iterations"])
                        self.compute_max_cell_length = self.__class__.compute_max_cell_length(service, version, mode, path + ["compute_max_cell_length"])
                        self.delete_dead_zones = self.__class__.delete_dead_zones(service, version, mode, path + ["delete_dead_zones"])
                        self.octree_hexcore = self.__class__.octree_hexcore(service, version, mode, path + ["octree_hexcore"])
                        super().__init__(service, version, mode, path)
                    class smooth_relaxation(TUIMethod):
                        """
                        Smoothing under relaxation on hexcore interface.
                        """
                    class maximum_cell_length(TUIMethod):
                        """
                        Maximum cell length.
                        """
                    class smooth_interface(TUIMethod):
                        """
                        Enable smoothing of hexcore interface.
                        """
                    class avoid_1_by_8_cell_jump_in_hexcore(TUIMethod):
                        """
                        Avoid-1:8-cell-jump-in-hexcore.
                        """
                    class skip_tet_refinement(TUIMethod):
                        """
                        Skip tethedral refinement in transition cell generation.
                        """
                    class non_fluid_type(TUIMethod):
                        """
                        Set non fluid type for cell zones.
                        """
                    class maximum_initial_cells(TUIMethod):
                        """
                        Maximum number of initial Cartesian cells.
                        """
                    class print_region_based_sizing(TUIMethod):
                        """
                        Print region based sizings.
                        """
                    class set_region_based_sizing(TUIMethod):
                        """
                        Set region based sizings.
                        """
                    class merge_tets_to_pyramids(TUIMethod):
                        """
                        Merge tets into pyramids.
                        """
                    class buffer_layers(TUIMethod):
                        """
                        Number of addition cells to mark for subdivision.
                        """
                    class keep_hex_tet_separate(TUIMethod):
                        """
                        Separate Hex and Tet cells.
                        """
                    class island_thresholds(TUIMethod):
                        """
                        Maximum number of cells and volume fraction in islands, deleted while separating the cells by region.
                        """
                    class maximum_subdivisions(TUIMethod):
                        """
                        Maximum number of subdivision sweeps.
                        """
                    class peel_layers(TUIMethod):
                        """
                        Number of hexcore cells to peel back from boundary.
                        """
                    class only_hexcore(TUIMethod):
                        """
                        Create hexcore and activate tet domain.
                        """
                    class define_hexcore_extents(TUIMethod):
                        """
                        Enables sspecificaton of hexcore outer domain parameters.
                        """
                    class smooth_iterations(TUIMethod):
                        """
                        Number of smoothing iterations on hexcore interface.
                        """
                    class compute_max_cell_length(TUIMethod):
                        """
                        Compute maximum cell length.
                        """
                    class delete_dead_zones(TUIMethod):
                        """
                        Delete dead zones after hexcore creation.
                        """
                    class octree_hexcore(TUIMethod):
                        """
                        Create hexcore using size-function driven octree.
                        """

                    class outer_domain_params(TUIMenu):
                        """
                        Define outer domain parameters.
                        """
                        def __init__(self, service, version, mode, path):
                            self.auto_align_tolerance = self.__class__.auto_align_tolerance(service, version, mode, path + ["auto_align_tolerance"])
                            self.auto_align = self.__class__.auto_align(service, version, mode, path + ["auto_align"])
                            self.list = self.__class__.list(service, version, mode, path + ["list"])
                            self.delete_old_face_zones = self.__class__.delete_old_face_zones(service, version, mode, path + ["delete_old_face_zones"])
                            self.boundaries = self.__class__.boundaries(service, version, mode, path + ["boundaries"])
                            self.specify_coordinates = self.__class__.specify_coordinates(service, version, mode, path + ["specify_coordinates"])
                            self.auto_align_boundaries = self.__class__.auto_align_boundaries(service, version, mode, path + ["auto_align_boundaries"])
                            self.coordinates = self.__class__.coordinates(service, version, mode, path + ["coordinates"])
                            self.specify_boundaries = self.__class__.specify_boundaries(service, version, mode, path + ["specify_boundaries"])
                            super().__init__(service, version, mode, path)
                        class auto_align_tolerance(TUIMethod):
                            """
                            Set auto-align-tolerance.
                            """
                        class auto_align(TUIMethod):
                            """
                            Enable auto-align?.
                            """
                        class list(TUIMethod):
                            """
                            List the face zones selected for hexcore up to boundaries.
                            """
                        class delete_old_face_zones(TUIMethod):
                            """
                            Delete replaced old tri face zones.
                            """
                        class boundaries(TUIMethod):
                            """
                            Set box-aligned zones which  have to be removed from hexcore meshing.
                            """
                        class specify_coordinates(TUIMethod):
                            """
                            Enables specification of coordinates of hexcore outer box.
                            """
                        class auto_align_boundaries(TUIMethod):
                            """
                            Auto-align selected boundaries.
                            """
                        class coordinates(TUIMethod):
                            """
                            Secifiy coordinates of outer box.
                            """
                        class specify_boundaries(TUIMethod):
                            """
                            Set parameters to get hex mesh to boundary(s).
                            """

        class wrap(TUIMenu):
            """
            Contains options related to the object wrapping operation.
            """
            def __init__(self, service, version, mode, path):
                self.set = self.__class__.set(service, version, mode, path + ["set"])
                self.debug = self.__class__.debug(service, version, mode, path + ["debug"])
                self.wrap = self.__class__.wrap(service, version, mode, path + ["wrap"])
                self.object_zone_separate = self.__class__.object_zone_separate(service, version, mode, path + ["object_zone_separate"])
                self.check_holes = self.__class__.check_holes(service, version, mode, path + ["check_holes"])
                super().__init__(service, version, mode, path)
            class debug(TUIMethod):
                """
                Debug from intermediate objects.
                """
            class wrap(TUIMethod):
                """
                Creates the mesh objects based on the geometry objects selected and other object wrapping parameters specified.
                """
            class object_zone_separate(TUIMethod):
                """
                Separate Object Face Zones.
                """
            class check_holes(TUIMethod):
                """
                Allows you to check for holes in the objects. The number of hole faces marked will be reported.
                """

            class set(TUIMenu):
                """
                Contains additional options related to the object wrapping operation.
                """
                def __init__(self, service, version, mode, path):
                    self.use_smooth_folded_faces = self.__class__.use_smooth_folded_faces(service, version, mode, path + ["use_smooth_folded_faces"])
                    self.add_geometry_recovery_level_to_zones = self.__class__.add_geometry_recovery_level_to_zones(service, version, mode, path + ["add_geometry_recovery_level_to_zones"])
                    self.resolution_factor = self.__class__.resolution_factor(service, version, mode, path + ["resolution_factor"])
                    self.include_thin_cut_edges_and_faces = self.__class__.include_thin_cut_edges_and_faces(service, version, mode, path + ["include_thin_cut_edges_and_faces"])
                    self.list_zones_geometry_recovery_levels = self.__class__.list_zones_geometry_recovery_levels(service, version, mode, path + ["list_zones_geometry_recovery_levels"])
                    self.relative_feature_tolerance = self.__class__.relative_feature_tolerance(service, version, mode, path + ["relative_feature_tolerance"])
                    self.delete_far_edges = self.__class__.delete_far_edges(service, version, mode, path + ["delete_far_edges"])
                    self.minimum_relative_topo_area = self.__class__.minimum_relative_topo_area(service, version, mode, path + ["minimum_relative_topo_area"])
                    self.minimum_topo_count = self.__class__.minimum_topo_count(service, version, mode, path + ["minimum_topo_count"])
                    self.shrink_wrap_rezone_parameters = self.__class__.shrink_wrap_rezone_parameters(service, version, mode, path + ["shrink_wrap_rezone_parameters"])
                    self.minimum_topo_area = self.__class__.minimum_topo_area(service, version, mode, path + ["minimum_topo_area"])
                    self.zone_name_prefix = self.__class__.zone_name_prefix(service, version, mode, path + ["zone_name_prefix"])
                    self.max_free_edges_for_hole_patching = self.__class__.max_free_edges_for_hole_patching(service, version, mode, path + ["max_free_edges_for_hole_patching"])
                    self.report_holes = self.__class__.report_holes(service, version, mode, path + ["report_holes"])
                    self.use_ray_tracing = self.__class__.use_ray_tracing(service, version, mode, path + ["use_ray_tracing"])
                    self.minimum_relative_topo_count = self.__class__.minimum_relative_topo_count(service, version, mode, path + ["minimum_relative_topo_count"])
                    super().__init__(service, version, mode, path)
                class use_smooth_folded_faces(TUIMethod):
                    """
                    Use smooth folded faces.
                    """
                class add_geometry_recovery_level_to_zones(TUIMethod):
                    """
                    Enables you to set the geometry recovery level (high or low) for the specified face zones.
                    """
                class resolution_factor(TUIMethod):
                    """
                    Sets the resolution factor for shrink wrapping. This option can be used to set sampling coarser or finer than the final surface mesh.
                    """
                class include_thin_cut_edges_and_faces(TUIMethod):
                    """
                    Allows better recovery of thin region configurations during the object wrapping operation.
                    """
                class list_zones_geometry_recovery_levels(TUIMethod):
                    """
                    Lists the zones based on geometry recovery level specified.
                    """
                class relative_feature_tolerance(TUIMethod):
                    """
                    Specifies the relative feature tolerance for shrink wrapping.
                    """
                class delete_far_edges(TUIMethod):
                    """
                    Delete-far-edges-after-wrap.
                    """
                class minimum_relative_topo_area(TUIMethod):
                    """
                    Specifies the minimum relative topological area for shrink wrapping.
                    """
                class minimum_topo_count(TUIMethod):
                    """
                    Specifies the minimum topological count for shrink wrapping.
                    """
                class shrink_wrap_rezone_parameters(TUIMethod):
                    """
                    Allows you to set the parameters for improving the mesh object surface quality using rezoning. The geometry object zones will be separated based on the separation angle specified to improve the feature imprinting on the mesh object.
                    """
                class minimum_topo_area(TUIMethod):
                    """
                    Specifies the minimum topological area for shrink wrapping.
                    """
                class zone_name_prefix(TUIMethod):
                    """
                    Allows you to specify a prefix for the zones included in the mesh object created using the object wrapping operation.
                    """
                class max_free_edges_for_hole_patching(TUIMethod):
                    """
                    Allows you to set the maximum number of free edges in a loop to fill the holes.
                    """
                class report_holes(TUIMethod):
                    """
                    Allows you to check for holes in the mesh object created. Holes, if any will be reported at the end of the object wrapping operation.
                    """
                class use_ray_tracing(TUIMethod):
                    """
                    Use ray tracing.
                    """
                class minimum_relative_topo_count(TUIMethod):
                    """
                    Specifies the minimum relative topological count for shrink wrapping.
                    """

    class diagnostics(TUIMenu):
        """
        Diagnostic tools.
        """
        def __init__(self, service, version, mode, path):
            self.face_connectivity = self.__class__.face_connectivity(service, version, mode, path + ["face_connectivity"])
            self.quality = self.__class__.quality(service, version, mode, path + ["quality"])
            self.manage_summary = self.__class__.manage_summary(service, version, mode, path + ["manage_summary"])
            self.set_scope = self.__class__.set_scope(service, version, mode, path + ["set_scope"])
            self.perform_summary = self.__class__.perform_summary(service, version, mode, path + ["perform_summary"])
            self.modify_defaults = self.__class__.modify_defaults(service, version, mode, path + ["modify_defaults"])
            super().__init__(service, version, mode, path)
        class manage_summary(TUIMethod):
            """
            Manage diagnostics summary checks.
            """
        class set_scope(TUIMethod):
            """
            Set Diagnostics scope.
            """
        class perform_summary(TUIMethod):
            """
            Performs diagnostics check and report in console.
            """
        class modify_defaults(TUIMethod):
            """
            Modify diagnostics defaults.
            """

        class face_connectivity(TUIMenu):
            """
            Contains options for fixing problems with face connectivity on the specified object face zones or boundary face zones.
            """
            def __init__(self, service, version, mode, path):
                self.fix_invalid_normals = self.__class__.fix_invalid_normals(service, version, mode, path + ["fix_invalid_normals"])
                self.fix_multi_faces = self.__class__.fix_multi_faces(service, version, mode, path + ["fix_multi_faces"])
                self.fix_deviations = self.__class__.fix_deviations(service, version, mode, path + ["fix_deviations"])
                self.fix_self_intersections = self.__class__.fix_self_intersections(service, version, mode, path + ["fix_self_intersections"])
                self.fix_spikes = self.__class__.fix_spikes(service, version, mode, path + ["fix_spikes"])
                self.add_label_to_small_neighbors = self.__class__.add_label_to_small_neighbors(service, version, mode, path + ["add_label_to_small_neighbors"])
                self.fix_steps = self.__class__.fix_steps(service, version, mode, path + ["fix_steps"])
                self.fix_point_contacts = self.__class__.fix_point_contacts(service, version, mode, path + ["fix_point_contacts"])
                self.fix_slivers = self.__class__.fix_slivers(service, version, mode, path + ["fix_slivers"])
                self.fix_free_faces = self.__class__.fix_free_faces(service, version, mode, path + ["fix_free_faces"])
                self.fix_duplicate_faces = self.__class__.fix_duplicate_faces(service, version, mode, path + ["fix_duplicate_faces"])
                self.remove_label_from_small_islands = self.__class__.remove_label_from_small_islands(service, version, mode, path + ["remove_label_from_small_islands"])
                self.fix_islands = self.__class__.fix_islands(service, version, mode, path + ["fix_islands"])
                super().__init__(service, version, mode, path)
            class fix_invalid_normals(TUIMethod):
                """
                Fixes invalid normals by smoothing.  Zone-specific or scoped prism settings should be applied prior to using this command.
                """
            class fix_multi_faces(TUIMethod):
                """
                Fixes multiply connected faces by a combination of deleting face fringes, overlapping faces, and disconnected faces. Specify the maximum number of fringe faces, overlapping faces, and multiply connected edges, respectively.
                """
            class fix_deviations(TUIMethod):
                """
                Fixes deviations in the wrapped surface mesh by imprinting edges on the wrapped face zones. Specify the number of imprint iterations and aggressive imprint iterations to be performed.
                """
            class fix_self_intersections(TUIMethod):
                """
                Fixes self intersecting or folded faces. For fixing folded faces by smoothing, specify whether features should be imprinted.
                """
            class fix_spikes(TUIMethod):
                """
                Fixes spiked faces based on the spike angle specified.
                """
            class add_label_to_small_neighbors(TUIMethod):
                """
                Separates island object face zones from all connected neighbors and merges them to the connected neighboring face zone label based on minimum face count specified.
                """
            class fix_steps(TUIMethod):
                """
                Fixes step configurations by smoothing or collapsing faces based on the angle and step width specified.
                """
            class fix_point_contacts(TUIMethod):
                """
                Fixes non-manifold configurations by removing point contacts.
                """
            class fix_slivers(TUIMethod):
                """
                Fixes faces based on skewness and height criteria. Height is the perpendicular distance between the longest edge of the triangle and the opposite node.
                """
            class fix_free_faces(TUIMethod):
                """
                Removes free faces by the method selected. The methods available are:.
                """
            class fix_duplicate_faces(TUIMethod):
                """
                Removes duplicate faces.
                """
            class remove_label_from_small_islands(TUIMethod):
                """
                Change small disconnected island labels to their connected neighbors.
                """
            class fix_islands(TUIMethod):
                """
                Deletes groups of island faces based on the absolute face count specified.
                """

        class quality(TUIMenu):
            """
            Contains options for fixing problems related to surface mesh quality on the specified object face zones or boundary face zones.
            """
            def __init__(self, service, version, mode, path):
                self.general_improve = self.__class__.general_improve(service, version, mode, path + ["general_improve"])
                self.collapse = self.__class__.collapse(service, version, mode, path + ["collapse"])
                self.delaunay_swap = self.__class__.delaunay_swap(service, version, mode, path + ["delaunay_swap"])
                self.smooth = self.__class__.smooth(service, version, mode, path + ["smooth"])
                super().__init__(service, version, mode, path)
            class general_improve(TUIMethod):
                """
                Improves the surface mesh based on aspect ratio, size change, or skewness. Specify the minimum quality value, feature angle, number of iterations, and whether the boundary should be preserved.
                """
            class collapse(TUIMethod):
                """
                Collapses bad quality faces based on area or skewness. For collapsing based on face area, specify the maximum face area and relative maximum area. For collapsing based on face skewness, specify the minimum skewness and feature angle. Additionally, specify the number of iterations and whether the boundary should be preserved.
                """
            class delaunay_swap(TUIMethod):
                """
                Improves the surface mesh by swapping based on the minimum skewness value and feature angle specified. Additionally, specify the number of iterations and whether the boundary should be preserved.
                """
            class smooth(TUIMethod):
                """
                Improves the surface mesh by smoothing. Specify the number of smoothing iterations and whether the boundary should be preserved.
                """

    class file(TUIMenu):
        """
        Enter the file menu.
        """
        def __init__(self, service, version, mode, path):
            self.project_beta = self.__class__.project_beta(service, version, mode, path + ["project_beta"])
            self.export = self.__class__.export(service, version, mode, path + ["export"])
            self.checkpoint = self.__class__.checkpoint(service, version, mode, path + ["checkpoint"])
            self.import_ = self.__class__.import_(service, version, mode, path + ["import_"])
            self.append_mesh = self.__class__.append_mesh(service, version, mode, path + ["append_mesh"])
            self.read_multiple_mesh = self.__class__.read_multiple_mesh(service, version, mode, path + ["read_multiple_mesh"])
            self.hdf_files = self.__class__.hdf_files(service, version, mode, path + ["hdf_files"])
            self.write_case = self.__class__.write_case(service, version, mode, path + ["write_case"])
            self.read_case = self.__class__.read_case(service, version, mode, path + ["read_case"])
            self.load_act_tool = self.__class__.load_act_tool(service, version, mode, path + ["load_act_tool"])
            self.read_mesh_vars = self.__class__.read_mesh_vars(service, version, mode, path + ["read_mesh_vars"])
            self.stop_journal = self.__class__.stop_journal(service, version, mode, path + ["stop_journal"])
            self.file_format = self.__class__.file_format(service, version, mode, path + ["file_format"])
            self.cff_files = self.__class__.cff_files(service, version, mode, path + ["cff_files"])
            self.write_mesh = self.__class__.write_mesh(service, version, mode, path + ["write_mesh"])
            self.write_domains = self.__class__.write_domains(service, version, mode, path + ["write_domains"])
            self.read_boundary_mesh = self.__class__.read_boundary_mesh(service, version, mode, path + ["read_boundary_mesh"])
            self.write_size_field = self.__class__.write_size_field(service, version, mode, path + ["write_size_field"])
            self.set_tui_version = self.__class__.set_tui_version(service, version, mode, path + ["set_tui_version"])
            self.show_configuration = self.__class__.show_configuration(service, version, mode, path + ["show_configuration"])
            self.write_options = self.__class__.write_options(service, version, mode, path + ["write_options"])
            self.read_journal = self.__class__.read_journal(service, version, mode, path + ["read_journal"])
            self.confirm_overwrite = self.__class__.confirm_overwrite(service, version, mode, path + ["confirm_overwrite"])
            self.read_mesh = self.__class__.read_mesh(service, version, mode, path + ["read_mesh"])
            self.write_boundaries = self.__class__.write_boundaries(service, version, mode, path + ["write_boundaries"])
            self.append_meshes_by_tmerge = self.__class__.append_meshes_by_tmerge(service, version, mode, path + ["append_meshes_by_tmerge"])
            self.read_options = self.__class__.read_options(service, version, mode, path + ["read_options"])
            self.read_size_field = self.__class__.read_size_field(service, version, mode, path + ["read_size_field"])
            self.filter_list = self.__class__.filter_list(service, version, mode, path + ["filter_list"])
            self.read_domains = self.__class__.read_domains(service, version, mode, path + ["read_domains"])
            self.write_mesh_vars = self.__class__.write_mesh_vars(service, version, mode, path + ["write_mesh_vars"])
            self.stop_transcript = self.__class__.stop_transcript(service, version, mode, path + ["stop_transcript"])
            self.start_transcript = self.__class__.start_transcript(service, version, mode, path + ["start_transcript"])
            self.read_multi_bound_mesh = self.__class__.read_multi_bound_mesh(service, version, mode, path + ["read_multi_bound_mesh"])
            self.set_idle_timeout = self.__class__.set_idle_timeout(service, version, mode, path + ["set_idle_timeout"])
            self.read_meshes_by_tmerge = self.__class__.read_meshes_by_tmerge(service, version, mode, path + ["read_meshes_by_tmerge"])
            self.filter_options = self.__class__.filter_options(service, version, mode, path + ["filter_options"])
            self.start_journal = self.__class__.start_journal(service, version, mode, path + ["start_journal"])
            super().__init__(service, version, mode, path)
        class append_mesh(TUIMethod):
            """
            Enables you to append the mesh files. This command is available only after a mesh file has been read in.
            """
        class read_multiple_mesh(TUIMethod):
            """
            Enables you to read in two or more files together and have the complete mesh assembled for you, if the mesh files are contained in two or more separate files.   For example, if you are going to create a hybrid mesh by reading in a triangular boundary mesh and a volume mesh consisting of hexahedral cells, you can read both files at the same time using this command.
            """
        class hdf_files(TUIMethod):
            """
            Indicate whether to write Ansys common fluids format (CFF) files or legacy case files.
            """
        class write_case(TUIMethod):
            """
            Enables you to write a case file that can be read by Fluent.   You should delete dead zones in the mesh before writing the mesh or case file for Fluent.
            """
        class read_case(TUIMethod):
            """
            Enables you to read the mesh contained in a case file.   Cell hierarchy in case files adapted in the solution mode will be lost when they are read in the meshing mode.  Case files containing polyhedral cells can also be read in the meshing mode of Fluent. You can display the polyhedral mesh, perform certain mesh manipulation operations, check the mesh quality, and so on.
            """
        class load_act_tool(TUIMethod):
            """
            Loads the Ansys ACT tool.
            """
        class read_mesh_vars(TUIMethod):
            """
            Reads mesh varaibles from a mesh file.
            """
        class stop_journal(TUIMethod):
            """
            Stops recording input and closes the journal file.
            """
        class file_format(TUIMethod):
            """
            Enables/disables the writing of binary files.
            """
        class cff_files(TUIMethod):
            """
            Answering yes will set the Common Fluids Format (CFF) as the default file format for reading and writing case/data files.
            """
        class write_mesh(TUIMethod):
            """
            Enables you to write a mesh file.   You should delete dead zones in the mesh before writing the mesh or case file for Fluent.
            """
        class write_domains(TUIMethod):
            """
            Enables you to write all the mesh domains (except global) into a file that can be read.
            """
        class read_boundary_mesh(TUIMethod):
            """
            Enables you to read a boundary mesh. If the boundary mesh is contained in two or more separate files, you can read them in together and assemble the complete boundary mesh.   This option is also convenient if you want to reuse the boundary mesh from a file containing a large volume mesh.   The naming of face zones can be controlled by Named Selections defined in Ansys Workbench. For details on exporting faceted geometry from Ansys Workbench, refer to the Ansys Workbench Help.
            """
        class write_size_field(TUIMethod):
            """
            Enables you to write a size field file.
            """
        class set_tui_version(TUIMethod):
            """
            Allows you to improve backwards compatibility for journal files. This command hides any new TUI prompts that are added at a future release of ANSYS Fluent and reverts to the arguments of the release that you specify using the command (within two full releases of the current release). The command is automatically added to a journal file as soon as you start the recording. See  for details.
            """
        class show_configuration(TUIMethod):
            """
            Displays the current release and version information.
            """
        class write_options(TUIMethod):
            """
            Allows you to enable or disable the enforce mesh topology option for writing mesh/case files.   This option is enabled by default; where it will orient the face zones consistently when the mesh file is written. If necessary, the zones will be separated, such that each boundary face zone has at most two cell zones as neighbors, one on either side. Also, internal face zones will be inserted between neighboring cell zones that are connected by interior faces.
            """
        class read_journal(TUIMethod):
            """
            Enables you to read a journal file into the program.   The read-journal command always loads the file in the main (that is, top-level) menu, regardless of where you are in the menu hierarchy when you invoke it.
            """
        class confirm_overwrite(TUIMethod):
            """
            Controls whether attempts to overwrite existing files require confirmation.  If you do not want ANSYS Fluent to ask you for confirmation before it overwrites existing files, you can enter the file/confirm-overwrite? text command and answer no.
            """
        class read_mesh(TUIMethod):
            """
            Enables you to read a mesh file. You can also use this command to read a Fluent mesh file created with GAMBIT, or to read the mesh available in a Fluent case file.   Reading a case file as a mesh file will result in loss of boundary condition data as the mesh file does not contain any information on boundary conditions.  Case files containing polyhedral cells can also be read in the meshing mode of Fluent. You can display the polyhedral mesh, perform certain mesh manipulation operations, check the mesh quality, and so on. Important:  You cannot read meshes from solvers that have been adapted using hanging nodes. To read one of these meshes in the meshing mode in Fluent, coarsen the mesh within the solver until you have recovered the original unadapted grid.   The naming of face zones can be controlled by Named Selections defined in Ansys Workbench. For details on exporting faceted geometry from Ansys Workbench, refer to the Ansys Workbench Help.
            """
        class write_boundaries(TUIMethod):
            """
            Enables you to write the specified boundaries into a mesh file.   This is useful for large cases where you may want to mesh different parts of the mesh separately and then merge them together. This enables you to avoid frequent switching between domains for such cases. You can write out selected boundaries to a mesh file and then create the volume mesh for the part in a separate session. You can then read the saved mesh into the previous session and merge the part with the rest of the mesh.
            """
        class append_meshes_by_tmerge(TUIMethod):
            """
            Enables you to append the mesh files using the tmerge utility. This command is available only after a mesh file has been read in.
            """
        class read_options(TUIMethod):
            """
            Enables you to set the following options for reading mesh files:.
            """
        class read_size_field(TUIMethod):
            """
            Enables you to read in a size field file.  If you read a size-field file after scaling the model, ensure that the size-field file is appropriate for the scaled model (size-field vertices should match the scaled model).
            """
        class filter_list(TUIMethod):
            """
            Lists the names of the converters that are used to change foreign mesh (while importing mesh files from third-party packages) files.
            """
        class read_domains(TUIMethod):
            """
            Enables you to read domain files.   Each mesh file written by Fluent has a domain section. A domain file is the domain section of the mesh file and is written as a separate file. It contains a list of node, face, and cell zone IDs that make up each domain in the mesh.   If a domain that is being read already exists in the mesh, a warning message is displayed. Fluent verifies if the zones defining the domains exist in the mesh. If not, it will display a warning message.
            """
        class write_mesh_vars(TUIMethod):
            """
            Writes mesh varaibles to a file.
            """
        class stop_transcript(TUIMethod):
            """
            Stops recording input and output, and closes the transcript file.
            """
        class start_transcript(TUIMethod):
            """
            Starts recording input and output in a file. A transcript file contains a complete record of all standard input to and output from Fluent (usually all keyboard and user interface input and all screen output).Start the transcription process with the file/start-transcript command, and end it with the file/stop-transcript command (or by exiting the program).
            """
        class read_multi_bound_mesh(TUIMethod):
            """
            Enables you to read multiple boundary mesh files into the meshing mode.
            """
        class set_idle_timeout(TUIMethod):
            """
            Allows you to set an idle timeout so that an idle ANSYS Fluent session will automatically save and close after the specified time.
            """
        class read_meshes_by_tmerge(TUIMethod):
            """
            Uses the tmerge utility to read the mesh contained in two or more separate files. It enables you to read the mesh files together and helps assemble the complete mesh.
            """
        class filter_options(TUIMethod):
            """
            Enables you to change the extension (such as .cas, .msh, .neu) and arguments used with a specified filter.   For example, if you saved the PATRAN files with a .NEU extension instead of .neu, you can substitute or add .NEU to the extension list. For some filters, one of the arguments will be the dimensionality of the grid.   When you use the filter-options command for such a filter, you will see a default dimensionality argument of -d a. The dimension will automatically be determined, so you need not substitute 2 or 3 for a.
            """
        class start_journal(TUIMethod):
            """
            Starts recording all input and writes it to a file. The current Fluent version is automatically recorded in the journal file. Note that commands entered using paths from older versions of Fluent will be upgraded to their current path in the journal file. See .
            """

        class project_beta(TUIMenu):
            """
            Enter to create new project, open project, save and archive project.
            """
            def __init__(self, service, version, mode, path):
                self.save_as = self.__class__.save_as(service, version, mode, path + ["save_as"])
                self.archive = self.__class__.archive(service, version, mode, path + ["archive"])
                self.open = self.__class__.open(service, version, mode, path + ["open"])
                self.new = self.__class__.new(service, version, mode, path + ["new"])
                self.save = self.__class__.save(service, version, mode, path + ["save"])
                self.save_as_copy = self.__class__.save_as_copy(service, version, mode, path + ["save_as_copy"])
                super().__init__(service, version, mode, path)
            class save_as(TUIMethod):
                """
                Save As Project.
                """
            class archive(TUIMethod):
                """
                Archive Project.
                """
            class open(TUIMethod):
                """
                Open project.
                """
            class new(TUIMethod):
                """
                Create New Project.
                """
            class save(TUIMethod):
                """
                Save Project.
                """
            class save_as_copy(TUIMethod):
                """
                Save As Copy.
                """

        class export(TUIMenu):
            """
            Exports case and data information.
            """
            def __init__(self, service, version, mode, path):
                self.stl = self.__class__.stl(service, version, mode, path + ["stl"])
                self.hypermesh = self.__class__.hypermesh(service, version, mode, path + ["hypermesh"])
                self.nastran = self.__class__.nastran(service, version, mode, path + ["nastran"])
                self.ansys = self.__class__.ansys(service, version, mode, path + ["ansys"])
                self.patran = self.__class__.patran(service, version, mode, path + ["patran"])
                super().__init__(service, version, mode, path)
            class stl(TUIMethod):
                """
                Write a STL boundary mesh file.
                """
            class hypermesh(TUIMethod):
                """
                Write a HYPERMESH ascii file.
                """
            class nastran(TUIMethod):
                """
                Writes a NASTRAN file.
                """
            class ansys(TUIMethod):
                """
                Write a Ansys mesh file.
                """
            class patran(TUIMethod):
                """
                Write a PATRAN mesh file.
                """

        class checkpoint(TUIMenu):
            """
            Checkpoint stores the mesh in the memory instead of writing it to a file.
            """
            def __init__(self, service, version, mode, path):
                self.restore_checkpoint = self.__class__.restore_checkpoint(service, version, mode, path + ["restore_checkpoint"])
                self.delete_checkpoint = self.__class__.delete_checkpoint(service, version, mode, path + ["delete_checkpoint"])
                self.list_checkpoint_names = self.__class__.list_checkpoint_names(service, version, mode, path + ["list_checkpoint_names"])
                self.write_checkpoint = self.__class__.write_checkpoint(service, version, mode, path + ["write_checkpoint"])
                super().__init__(service, version, mode, path)
            class restore_checkpoint(TUIMethod):
                """
                Restore to checkpoint.
                """
            class delete_checkpoint(TUIMethod):
                """
                Delete checkpoint.
                """
            class list_checkpoint_names(TUIMethod):
                """
                Get all checkpoint names.
                """
            class write_checkpoint(TUIMethod):
                """
                Write checkpoint.
                """

        class import_(TUIMenu):
            """
            Import surface and volume meshes from non-native formats.
            """
            def __init__(self, service, version, mode, path):
                self.cad_options = self.__class__.cad_options(service, version, mode, path + ["cad_options"])
                self.cad = self.__class__.cad(service, version, mode, path + ["cad"])
                self.cgns_vol_mesh = self.__class__.cgns_vol_mesh(service, version, mode, path + ["cgns_vol_mesh"])
                self.ideas_surf_mesh = self.__class__.ideas_surf_mesh(service, version, mode, path + ["ideas_surf_mesh"])
                self.cad_geometry = self.__class__.cad_geometry(service, version, mode, path + ["cad_geometry"])
                self.patran_vol_mesh = self.__class__.patran_vol_mesh(service, version, mode, path + ["patran_vol_mesh"])
                self.hypermesh_vol_mesh = self.__class__.hypermesh_vol_mesh(service, version, mode, path + ["hypermesh_vol_mesh"])
                self.reimport_last_with_cfd_surface_mesh = self.__class__.reimport_last_with_cfd_surface_mesh(service, version, mode, path + ["reimport_last_with_cfd_surface_mesh"])
                self.fluent_2d_mesh = self.__class__.fluent_2d_mesh(service, version, mode, path + ["fluent_2d_mesh"])
                self.gambit_vol_mesh = self.__class__.gambit_vol_mesh(service, version, mode, path + ["gambit_vol_mesh"])
                self.gambit_surf_mesh = self.__class__.gambit_surf_mesh(service, version, mode, path + ["gambit_surf_mesh"])
                self.fidap_vol_mesh = self.__class__.fidap_vol_mesh(service, version, mode, path + ["fidap_vol_mesh"])
                self.fl_uns2_mesh = self.__class__.fl_uns2_mesh(service, version, mode, path + ["fl_uns2_mesh"])
                self.stl = self.__class__.stl(service, version, mode, path + ["stl"])
                self.nastran_vol_mesh = self.__class__.nastran_vol_mesh(service, version, mode, path + ["nastran_vol_mesh"])
                self.fluent_3d_mesh = self.__class__.fluent_3d_mesh(service, version, mode, path + ["fluent_3d_mesh"])
                self.ansys_vol_mesh = self.__class__.ansys_vol_mesh(service, version, mode, path + ["ansys_vol_mesh"])
                self.nastran_surf_mesh = self.__class__.nastran_surf_mesh(service, version, mode, path + ["nastran_surf_mesh"])
                self.cgns_surf_mesh = self.__class__.cgns_surf_mesh(service, version, mode, path + ["cgns_surf_mesh"])
                self.patran_surf_mesh = self.__class__.patran_surf_mesh(service, version, mode, path + ["patran_surf_mesh"])
                self.fidap_surf_mesh = self.__class__.fidap_surf_mesh(service, version, mode, path + ["fidap_surf_mesh"])
                self.ansys_surf_mesh = self.__class__.ansys_surf_mesh(service, version, mode, path + ["ansys_surf_mesh"])
                self.ideas_vol_mesh = self.__class__.ideas_vol_mesh(service, version, mode, path + ["ideas_vol_mesh"])
                self.hypermesh_surf_mesh = self.__class__.hypermesh_surf_mesh(service, version, mode, path + ["hypermesh_surf_mesh"])
                super().__init__(service, version, mode, path)
            class cad(TUIMethod):
                """
                Reads the following CAD formats:
                ACIS  \\*.sat, \\*.sab
                Ansys DesignModeler  \\*.agdb
                Ansys ICEM CFD  \\*.tin
                Ansys Workbench  \\*.meshdat, \\*.mechdat
                Autodesk Inventor  \\*.ipt, \\*.iam
                CATIA V4  \\*.model, \\*.exp, \\*.session, \\*.dlv
                CATIA V5  \\*.CATPart, \\*.CATProduct
                Creo Parametric  \\*.prt, \\*.asm
                GAMBIT  \\*.dbs
                IGES  \\*.igs, \\*.iges
                JTOpen  \\*.jt
                NX  \\*.prt
                Parasolid  \\*.x_t, \\*.xmt_txt, \\*.x_b, \\*.xmt_bin
                SolidWorks  \\*.sldprt, \\*.sldasm
                STEP  \\*.stp, \\*.step
                STL  \\*.stl.
                """
            class cgns_vol_mesh(TUIMethod):
                """
                Read a volume mesh from an CGNS format file.
                """
            class ideas_surf_mesh(TUIMethod):
                """
                Read a surface mesh from an IDEAS universal file.
                """
            class cad_geometry(TUIMethod):
                """
                Reads the following CAD formats:
                ACIS  \\*.sat, \\*.sab
                Ansys DesignModeler  \\*.agdb
                Ansys ICEM CFD  \\*.tin
                Ansys Workbench  \\*.meshdat, \\*.mechdat
                Autodesk Inventor  \\*.ipt, \\*.iam
                CATIA V4  \\*.model, \\*.exp, \\*.session, \\*.dlv
                CATIA V5  \\*.CATPart, \\*.CATProduct
                Creo Parametric  \\*.prt, \\*.asm
                GAMBIT  \\*.dbs
                IGES  \\*.igs, \\*.iges
                JTOpen  \\*.jt
                NX  \\*.prt
                Parasolid  \\*.x_t, \\*.xmt_txt, \\*.x_b, \\*.xmt_bin
                SolidWorks  \\*.sldprt, \\*.sldasm
                STEP  \\*.stp, \\*.step
                STL  \\*.stl.
                """
            class patran_vol_mesh(TUIMethod):
                """
                Read a volume mesh from a PATRAN neutral file.
                """
            class hypermesh_vol_mesh(TUIMethod):
                """
                Read a volume mesh from a HYPERMESH ascii file.
                """
            class reimport_last_with_cfd_surface_mesh(TUIMethod):
                """
                Reimport CAD using the size field.
                """
            class fluent_2d_mesh(TUIMethod):
                """
                Read a 2D mesh.
                """
            class gambit_vol_mesh(TUIMethod):
                """
                Read a volume mesh from a GAMBIT neutral file.
                """
            class gambit_surf_mesh(TUIMethod):
                """
                Read a surface mesh from a GAMBIT neutral file.
                """
            class fidap_vol_mesh(TUIMethod):
                """
                Read a volume mesh from a FIDAP neutral file.
                """
            class fl_uns2_mesh(TUIMethod):
                """
                Read a mesh from a Fluent UNS V2 case file.
                """
            class stl(TUIMethod):
                """
                Read a surface mesh from a stereolithography (STL) file.
                """
            class nastran_vol_mesh(TUIMethod):
                """
                Read a volume mesh from a NASTRAN file.
                """
            class fluent_3d_mesh(TUIMethod):
                """
                Read a 3D mesh.
                """
            class ansys_vol_mesh(TUIMethod):
                """
                Read a volume mesh from an Ansys prep7 or cdb file.
                """
            class nastran_surf_mesh(TUIMethod):
                """
                Read a surface mesh from a NASTRAN file.
                """
            class cgns_surf_mesh(TUIMethod):
                """
                Read a surface mesh from a CGNS format file.
                """
            class patran_surf_mesh(TUIMethod):
                """
                Read a surface mesh from a PATRAN neutral file.
                """
            class fidap_surf_mesh(TUIMethod):
                """
                Read a surface mesh from a FIDAP neutral file.
                """
            class ansys_surf_mesh(TUIMethod):
                """
                Read a surface mesh from an Ansys prep7 or cdb file.
                """
            class ideas_vol_mesh(TUIMethod):
                """
                Read a volume mesh from an IDEAS universal file.
                """
            class hypermesh_surf_mesh(TUIMethod):
                """
                Read a surface mesh from a HYPERMESH ascii file.
                """

            class cad_options(TUIMenu):
                """
                Make settings for cad import.
                """
                def __init__(self, service, version, mode, path):
                    self.strip_file_name_extension_from_naming = self.__class__.strip_file_name_extension_from_naming(service, version, mode, path + ["strip_file_name_extension_from_naming"])
                    self.double_connected_face_label = self.__class__.double_connected_face_label(service, version, mode, path + ["double_connected_face_label"])
                    self.derive_zone_name_from_object_scope = self.__class__.derive_zone_name_from_object_scope(service, version, mode, path + ["derive_zone_name_from_object_scope"])
                    self.use_component_names = self.__class__.use_component_names(service, version, mode, path + ["use_component_names"])
                    self.continue_on_error = self.__class__.continue_on_error(service, version, mode, path + ["continue_on_error"])
                    self.save_PMDB = self.__class__.save_PMDB(service, version, mode, path + ["save_PMDB"])
                    self.reconstruct_topology = self.__class__.reconstruct_topology(service, version, mode, path + ["reconstruct_topology"])
                    self.replacement_character = self.__class__.replacement_character(service, version, mode, path + ["replacement_character"])
                    self.create_cad_assemblies = self.__class__.create_cad_assemblies(service, version, mode, path + ["create_cad_assemblies"])
                    self.use_collection_names = self.__class__.use_collection_names(service, version, mode, path + ["use_collection_names"])
                    self.modify_all_duplicate_names = self.__class__.modify_all_duplicate_names(service, version, mode, path + ["modify_all_duplicate_names"])
                    self.separate_features_by_type = self.__class__.separate_features_by_type(service, version, mode, path + ["separate_features_by_type"])
                    self.merge_objects_per_body_named_selection = self.__class__.merge_objects_per_body_named_selection(service, version, mode, path + ["merge_objects_per_body_named_selection"])
                    self.create_label_per_body_during_cad_faceting = self.__class__.create_label_per_body_during_cad_faceting(service, version, mode, path + ["create_label_per_body_during_cad_faceting"])
                    self.named_selections = self.__class__.named_selections(service, version, mode, path + ["named_selections"])
                    self.one_face_zone_per = self.__class__.one_face_zone_per(service, version, mode, path + ["one_face_zone_per"])
                    self.name_separator_character = self.__class__.name_separator_character(service, version, mode, path + ["name_separator_character"])
                    self.strip_path_prefix_from_names = self.__class__.strip_path_prefix_from_names(service, version, mode, path + ["strip_path_prefix_from_names"])
                    self.import_label_for_body_named_selection = self.__class__.import_label_for_body_named_selection(service, version, mode, path + ["import_label_for_body_named_selection"])
                    self.import_part_names = self.__class__.import_part_names(service, version, mode, path + ["import_part_names"])
                    self.tessellation = self.__class__.tessellation(service, version, mode, path + ["tessellation"])
                    self.import_body_names = self.__class__.import_body_names(service, version, mode, path + ["import_body_names"])
                    self.named_selection_tessellation_failure = self.__class__.named_selection_tessellation_failure(service, version, mode, path + ["named_selection_tessellation_failure"])
                    self.single_connected_edge_label = self.__class__.single_connected_edge_label(service, version, mode, path + ["single_connected_edge_label"])
                    self.enclosure_symm_processing = self.__class__.enclosure_symm_processing(service, version, mode, path + ["enclosure_symm_processing"])
                    self.read_all_cad_in_subdirectories = self.__class__.read_all_cad_in_subdirectories(service, version, mode, path + ["read_all_cad_in_subdirectories"])
                    self.use_body_names = self.__class__.use_body_names(service, version, mode, path + ["use_body_names"])
                    self.merge_nodes = self.__class__.merge_nodes(service, version, mode, path + ["merge_nodes"])
                    self.object_type = self.__class__.object_type(service, version, mode, path + ["object_type"])
                    self.use_part_names = self.__class__.use_part_names(service, version, mode, path + ["use_part_names"])
                    self.import_curvature_data_from_CAD = self.__class__.import_curvature_data_from_CAD(service, version, mode, path + ["import_curvature_data_from_CAD"])
                    self.one_object_per = self.__class__.one_object_per(service, version, mode, path + ["one_object_per"])
                    self.use_part_or_body_names_as_suffix_to_named_selections = self.__class__.use_part_or_body_names_as_suffix_to_named_selections(service, version, mode, path + ["use_part_or_body_names_as_suffix_to_named_selections"])
                    self.extract_features = self.__class__.extract_features(service, version, mode, path + ["extract_features"])
                    super().__init__(service, version, mode, path)
                class strip_file_name_extension_from_naming(TUIMethod):
                    """
                    Strip file name extension from naming.
                    """
                class double_connected_face_label(TUIMethod):
                    """
                    Double connected face label for CAD files.
                    """
                class derive_zone_name_from_object_scope(TUIMethod):
                    """
                    Derive zone names from object scope.
                    """
                class use_component_names(TUIMethod):
                    """
                    Use component names for CAD files.
                    """
                class continue_on_error(TUIMethod):
                    """
                    Continue on error during cad import.
                    """
                class save_PMDB(TUIMethod):
                    """
                    Saves PMDB file in the directory containing the CAD files imported.
                    """
                class reconstruct_topology(TUIMethod):
                    """
                    Reconstruct topology for STL files.
                    """
                class replacement_character(TUIMethod):
                    """
                    Name replacement character.
                    """
                class create_cad_assemblies(TUIMethod):
                    """
                    Import CAD Assemblies.
                    """
                class use_collection_names(TUIMethod):
                    """
                    Use collection names for CAD files.
                    """
                class modify_all_duplicate_names(TUIMethod):
                    """
                    Modify all duplicate names by suffixing it with incremental integers.
                    """
                class separate_features_by_type(TUIMethod):
                    """
                    Separate features by type.
                    """
                class merge_objects_per_body_named_selection(TUIMethod):
                    """
                    Merge Objects per body named selection.
                    """
                class create_label_per_body_during_cad_faceting(TUIMethod):
                    """
                    Create label Per Body during cad faceting.
                    """
                class named_selections(TUIMethod):
                    """
                    Allows to import Named Selections from the CAD file.
                    """
                class one_face_zone_per(TUIMethod):
                    """
                    Set one object per body, face or object.
                    """
                class name_separator_character(TUIMethod):
                    """
                    Character to be used as a separator in all names.
                    """
                class strip_path_prefix_from_names(TUIMethod):
                    """
                    Strip path prefixes from naming.
                    """
                class import_label_for_body_named_selection(TUIMethod):
                    """
                    Import face zone labels for body named selections.
                    """
                class import_part_names(TUIMethod):
                    """
                    Import Part names from the CAD files.
                    """
                class tessellation(TUIMethod):
                    """
                    Set tessellation controls for cad import.
                    """
                class import_body_names(TUIMethod):
                    """
                    Import Body names from the CAD files.
                    """
                class named_selection_tessellation_failure(TUIMethod):
                    """
                    Set named selection for CFD surface mesh failures.
                    """
                class single_connected_edge_label(TUIMethod):
                    """
                    Single connected edge label for CAD files.
                    """
                class enclosure_symm_processing(TUIMethod):
                    """
                    Processing of enclosure and symmetry named selections during import.
                    """
                class read_all_cad_in_subdirectories(TUIMethod):
                    """
                    Recursive search for CAD files in sub-directories.
                    """
                class use_body_names(TUIMethod):
                    """
                    Use body names for CAD files.
                    """
                class merge_nodes(TUIMethod):
                    """
                    Merge Nodes for CAD import.
                    """
                class object_type(TUIMethod):
                    """
                    Object type for CAD files.
                    """
                class use_part_names(TUIMethod):
                    """
                    Use part names for CAD files.
                    """
                class import_curvature_data_from_CAD(TUIMethod):
                    """
                    Import Curvature Data from CAD.
                    """
                class one_object_per(TUIMethod):
                    """
                    Set one object per body, part or file.
                    """
                class use_part_or_body_names_as_suffix_to_named_selections(TUIMethod):
                    """
                    Part or Body names are used as suffix for named selections spanning over multiple parts or bodies.
                    """
                class extract_features(TUIMethod):
                    """
                    Set the feature angle.
                    """

    class size_functions(TUIMenu):
        """
        Manage advanced size functions.
        """
        def __init__(self, service, version, mode, path):
            self.controls = self.__class__.controls(service, version, mode, path + ["controls"])
            self.contours = self.__class__.contours(service, version, mode, path + ["contours"])
            self.create_defaults = self.__class__.create_defaults(service, version, mode, path + ["create_defaults"])
            self.disable_periodicity_filter = self.__class__.disable_periodicity_filter(service, version, mode, path + ["disable_periodicity_filter"])
            self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
            self.list = self.__class__.list(service, version, mode, path + ["list"])
            self.set_prox_gap_tolerance = self.__class__.set_prox_gap_tolerance(service, version, mode, path + ["set_prox_gap_tolerance"])
            self.use_cad_imported_curvature = self.__class__.use_cad_imported_curvature(service, version, mode, path + ["use_cad_imported_curvature"])
            self.reset_global_controls = self.__class__.reset_global_controls(service, version, mode, path + ["reset_global_controls"])
            self.create = self.__class__.create(service, version, mode, path + ["create"])
            self.set_scaling_filter = self.__class__.set_scaling_filter(service, version, mode, path + ["set_scaling_filter"])
            self.enable_periodicity_filter = self.__class__.enable_periodicity_filter(service, version, mode, path + ["enable_periodicity_filter"])
            self.triangulate_quad_faces = self.__class__.triangulate_quad_faces(service, version, mode, path + ["triangulate_quad_faces"])
            self.delete_all = self.__class__.delete_all(service, version, mode, path + ["delete_all"])
            self.list_periodicity_filter = self.__class__.list_periodicity_filter(service, version, mode, path + ["list_periodicity_filter"])
            self.set_global_controls = self.__class__.set_global_controls(service, version, mode, path + ["set_global_controls"])
            self.compute = self.__class__.compute(service, version, mode, path + ["compute"])
            super().__init__(service, version, mode, path)
        class create_defaults(TUIMethod):
            """
            Creates default size functions based on face and edge curvature and proximity.
            """
        class disable_periodicity_filter(TUIMethod):
            """
            Removes periodicity from the size field.
            """
        class delete(TUIMethod):
            """
            Deletes the specified size function or the current size field.
            """
        class list(TUIMethod):
            """
            Lists all the defined size functions and the corresponding parameter values defined.
            """
        class set_prox_gap_tolerance(TUIMethod):
            """
            Sets the tolerance relative to minimum size to take gaps into account. Gaps whose thickness is less than the global minimum size multiplied by this factor will not be regarded as a proximity gap.
            """
        class use_cad_imported_curvature(TUIMethod):
            """
            Allows you to disable curvature data from the nodes of the CAD facets.
            """
        class reset_global_controls(TUIMethod):
            """
            Resets the global controls to their default values.
            """
        class create(TUIMethod):
            """
            Defines the size function based on the specified parameters.
            """
        class set_scaling_filter(TUIMethod):
            """
            Allows you specify the scale factor, and minimum and maximum size values to filter the size output from the size field.
            """
        class enable_periodicity_filter(TUIMethod):
            """
            Applies periodicity to the size field.  Specify the angle, pivot, and axis of rotation to set up periodicity.  If periodicity has been previously defined, the existing settings will be applied.  Only rotational periodicity is supported, translational periodicity is not supported currently.
            """
        class triangulate_quad_faces(TUIMethod):
            """
            Identifies the zones comprising non-triangular elements and uses a triangulated copy of these zones for computing the size functions.
            """
        class delete_all(TUIMethod):
            """
            Deletes all the defined size functions.
            """
        class list_periodicity_filter(TUIMethod):
            """
            List periodic in size field.
            """
        class set_global_controls(TUIMethod):
            """
            Sets the values for the global minimum and maximum size, and the growth rate.   If you set the global minimum size to a value greater than the local minimum size defined for existing proximity, curvature, or hard size functions, a warning will appear, indicating that the global minimum size cannot be greater than the specified local minimum size.
            """
        class compute(TUIMethod):
            """
            Computes the size function based on the defined parameters.
            """

        class controls(TUIMenu):
            """
            Menu to control different behavior of sf.
            """
            def __init__(self, service, version, mode, path):
                self.meshed_sf_behavior = self.__class__.meshed_sf_behavior(service, version, mode, path + ["meshed_sf_behavior"])
                self.curvature_method = self.__class__.curvature_method(service, version, mode, path + ["curvature_method"])
                super().__init__(service, version, mode, path)
            class meshed_sf_behavior(TUIMethod):
                """
                Set meshed size function processing to hard.
                """
            class curvature_method(TUIMethod):
                """
                Option to get facet curvature.
                """

        class contours(TUIMenu):
            """
            Contains options for managing contours.
            """
            def __init__(self, service, version, mode, path):
                self.set = self.__class__.set(service, version, mode, path + ["set"])
                self.draw = self.__class__.draw(service, version, mode, path + ["draw"])
                super().__init__(service, version, mode, path)
            class draw(TUIMethod):
                """
                Displays contours in the graphics window. Run compute prior to contours/draw.
                """

            class set(TUIMenu):
                """
                Contains options to manage the contour size.
                """
                def __init__(self, service, version, mode, path):
                    self.refine_facets = self.__class__.refine_facets(service, version, mode, path + ["refine_facets"])
                    super().__init__(service, version, mode, path)
                class refine_facets(TUIMethod):
                    """
                    Allows you to specify smaller facets if the original are too large. Default is no.
                    """

    class boundary(TUIMenu):
        """
        Enter the boundary menu.
        """
        def __init__(self, service, version, mode, path):
            self.separate = self.__class__.separate(service, version, mode, path + ["separate"])
            self.refine = self.__class__.refine(service, version, mode, path + ["refine"])
            self.improve = self.__class__.improve(service, version, mode, path + ["improve"])
            self.manage = self.__class__.manage(service, version, mode, path + ["manage"])
            self.boundary_conditions = self.__class__.boundary_conditions(service, version, mode, path + ["boundary_conditions"])
            self.shell_boundary_layer = self.__class__.shell_boundary_layer(service, version, mode, path + ["shell_boundary_layer"])
            self.remesh = self.__class__.remesh(service, version, mode, path + ["remesh"])
            self.modify = self.__class__.modify(service, version, mode, path + ["modify"])
            self.feature = self.__class__.feature(service, version, mode, path + ["feature"])
            self.expand_marked_faces_by_rings = self.__class__.expand_marked_faces_by_rings(service, version, mode, path + ["expand_marked_faces_by_rings"])
            self.count_free_nodes = self.__class__.count_free_nodes(service, version, mode, path + ["count_free_nodes"])
            self.wrapper = self.__class__.wrapper(service, version, mode, path + ["wrapper"])
            self.count_unused_faces = self.__class__.count_unused_faces(service, version, mode, path + ["count_unused_faces"])
            self.create_plane_surface = self.__class__.create_plane_surface(service, version, mode, path + ["create_plane_surface"])
            self.delete_free_edge_faces = self.__class__.delete_free_edge_faces(service, version, mode, path + ["delete_free_edge_faces"])
            self.resolve_face_intersection = self.__class__.resolve_face_intersection(service, version, mode, path + ["resolve_face_intersection"])
            self.unmark_faces_in_zones = self.__class__.unmark_faces_in_zones(service, version, mode, path + ["unmark_faces_in_zones"])
            self.delete_island_faces = self.__class__.delete_island_faces(service, version, mode, path + ["delete_island_faces"])
            self.face_skewness = self.__class__.face_skewness(service, version, mode, path + ["face_skewness"])
            self.merge_nodes = self.__class__.merge_nodes(service, version, mode, path + ["merge_nodes"])
            self.compute_bounding_box = self.__class__.compute_bounding_box(service, version, mode, path + ["compute_bounding_box"])
            self.mark_faces_in_region = self.__class__.mark_faces_in_region(service, version, mode, path + ["mark_faces_in_region"])
            self.check_boundary_mesh = self.__class__.check_boundary_mesh(service, version, mode, path + ["check_boundary_mesh"])
            self.orient_faces_by_point = self.__class__.orient_faces_by_point(service, version, mode, path + ["orient_faces_by_point"])
            self.mark_face_proximity = self.__class__.mark_face_proximity(service, version, mode, path + ["mark_face_proximity"])
            self.project_face_zone = self.__class__.project_face_zone(service, version, mode, path + ["project_face_zone"])
            self.reset_element_type = self.__class__.reset_element_type(service, version, mode, path + ["reset_element_type"])
            self.mark_bad_quality_faces = self.__class__.mark_bad_quality_faces(service, version, mode, path + ["mark_bad_quality_faces"])
            self.delete_duplicate_faces = self.__class__.delete_duplicate_faces(service, version, mode, path + ["delete_duplicate_faces"])
            self.jiggle_boundary_nodes = self.__class__.jiggle_boundary_nodes(service, version, mode, path + ["jiggle_boundary_nodes"])
            self.smooth_marked_faces = self.__class__.smooth_marked_faces(service, version, mode, path + ["smooth_marked_faces"])
            self.make_periodic = self.__class__.make_periodic(service, version, mode, path + ["make_periodic"])
            self.delete_unused_nodes = self.__class__.delete_unused_nodes(service, version, mode, path + ["delete_unused_nodes"])
            self.unmark_selected_faces = self.__class__.unmark_selected_faces(service, version, mode, path + ["unmark_selected_faces"])
            self.delete_unconnected_faces = self.__class__.delete_unconnected_faces(service, version, mode, path + ["delete_unconnected_faces"])
            self.clear_marked_faces = self.__class__.clear_marked_faces(service, version, mode, path + ["clear_marked_faces"])
            self.slit_boundary_face = self.__class__.slit_boundary_face(service, version, mode, path + ["slit_boundary_face"])
            self.clear_marked_nodes = self.__class__.clear_marked_nodes(service, version, mode, path + ["clear_marked_nodes"])
            self.count_unused_nodes = self.__class__.count_unused_nodes(service, version, mode, path + ["count_unused_nodes"])
            self.mark_duplicate_nodes = self.__class__.mark_duplicate_nodes(service, version, mode, path + ["mark_duplicate_nodes"])
            self.fix_mconnected_edges = self.__class__.fix_mconnected_edges(service, version, mode, path + ["fix_mconnected_edges"])
            self.print_info = self.__class__.print_info(service, version, mode, path + ["print_info"])
            self.count_unused_bound_node = self.__class__.count_unused_bound_node(service, version, mode, path + ["count_unused_bound_node"])
            self.recover_periodic_surfaces = self.__class__.recover_periodic_surfaces(service, version, mode, path + ["recover_periodic_surfaces"])
            self.mark_face_intersection = self.__class__.mark_face_intersection(service, version, mode, path + ["mark_face_intersection"])
            self.delete_all_dup_faces = self.__class__.delete_all_dup_faces(service, version, mode, path + ["delete_all_dup_faces"])
            self.edge_limits = self.__class__.edge_limits(service, version, mode, path + ["edge_limits"])
            self.auto_slit_faces = self.__class__.auto_slit_faces(service, version, mode, path + ["auto_slit_faces"])
            self.improve_surface_mesh = self.__class__.improve_surface_mesh(service, version, mode, path + ["improve_surface_mesh"])
            self.merge_small_face_zones = self.__class__.merge_small_face_zones(service, version, mode, path + ["merge_small_face_zones"])
            self.create_revolved_surface = self.__class__.create_revolved_surface(service, version, mode, path + ["create_revolved_surface"])
            self.create_swept_surface = self.__class__.create_swept_surface(service, version, mode, path + ["create_swept_surface"])
            self.scale_nodes = self.__class__.scale_nodes(service, version, mode, path + ["scale_nodes"])
            self.delete_unused_faces = self.__class__.delete_unused_faces(service, version, mode, path + ["delete_unused_faces"])
            self.check_duplicate_geom = self.__class__.check_duplicate_geom(service, version, mode, path + ["check_duplicate_geom"])
            self.face_distribution = self.__class__.face_distribution(service, version, mode, path + ["face_distribution"])
            self.set_periodicity = self.__class__.set_periodicity(service, version, mode, path + ["set_periodicity"])
            self.create_cylinder = self.__class__.create_cylinder(service, version, mode, path + ["create_cylinder"])
            self.coarsen_boundary_faces = self.__class__.coarsen_boundary_faces(service, version, mode, path + ["coarsen_boundary_faces"])
            self.create_bounding_box = self.__class__.create_bounding_box(service, version, mode, path + ["create_bounding_box"])
            self.count_marked_faces = self.__class__.count_marked_faces(service, version, mode, path + ["count_marked_faces"])
            super().__init__(service, version, mode, path)
        class expand_marked_faces_by_rings(TUIMethod):
            """
            Mark rings of faces around marked faces.
            """
        class count_free_nodes(TUIMethod):
            """
            Reports the number of boundary nodes associated with edges having only one attached face.
            """
        class wrapper(TUIMethod):
            """
            Enters the surface wrapper menu.  This menu is no longer supported, and will be removed in a future release.
            """
        class count_unused_faces(TUIMethod):
            """
            Lists the number of boundary faces that are not used by any cell.
            """
        class create_plane_surface(TUIMethod):
            """
            Creates a plane surface by specifying either the axis direction, axial location, and the extents of the surface or three points defining the plane. You can also optionally create a geometry object from the plane surface created.
            """
        class delete_free_edge_faces(TUIMethod):
            """
            Enables you to remove faces with the specified number of free edges from the specified boundary zones.
            """
        class resolve_face_intersection(TUIMethod):
            """
            Resolves self intersection on manifold surface meshes.
            """
        class unmark_faces_in_zones(TUIMethod):
            """
            Unmark faces in zones.
            """
        class delete_island_faces(TUIMethod):
            """
            Enables you to delete faces in a non-contiguous region of a face zone.
            """
        class face_skewness(TUIMethod):
            """
            Lists the worst face skewness.
            """
        class merge_nodes(TUIMethod):
            """
            Merges duplicate nodes.
            """
        class compute_bounding_box(TUIMethod):
            """
            Computes the bounding box for the zones specified.
            """
        class mark_faces_in_region(TUIMethod):
            """
            Marks the faces that are contained in a specified local refinement region.
            """
        class check_boundary_mesh(TUIMethod):
            """
            Reports the number of Delaunay violations on the triangular surface mesh and the number of isolated nodes.
            """
        class orient_faces_by_point(TUIMethod):
            """
            Orients the normals based on the specified material point.
            """
        class mark_face_proximity(TUIMethod):
            """
            Marks faces that are in proximity to each other.   Face A is considered to be in proximity to face B if any of the nodes on face A are within the calculated proximity distance from face B. The proximity distance is calculated based on the specified relative distance and the sphere radius. The sphere radius is determined by the maximum distance from the centroid of the face to its nodes. The marked faces will appear in the grid display when faces are displayed.   For a list of faces in proximity to each other, set the /report/verbosity level to 2 before using the mark-face-proximity command.
            """
        class project_face_zone(TUIMethod):
            """
            Projects nodes on a selected face zone onto a target face zone. Projection can be performed based on normal direction, closest point, or specified direction.
            """
        class reset_element_type(TUIMethod):
            """
            Resets the element type (mixed, tri, or quad) of a boundary zone. If you have separated a mixed (tri and quad) face zone into one tri face zone and one quad face zone, for example, each of these will be identified as a “mixed" zone. Resetting the element type for each of these new zones will identify them as, respectively, a triangular zone and a quadrilateral zone.
            """
        class mark_bad_quality_faces(TUIMethod):
            """
            Mark Bad Quality Faces.
            """
        class delete_duplicate_faces(TUIMethod):
            """
            Searches for faces on a specified zone that have the same nodes and deletes the duplicates.   Duplicate faces may be present if you generated the boundary mesh using a third-party grid generator, or if you have used the slit-boundary-face command to modify the boundary mesh and then merged the nodes.
            """
        class jiggle_boundary_nodes(TUIMethod):
            """
            Randomly perturbs all boundary nodes based on an input tolerance. Some nodes will be perturbed less than the tolerance value, while others will be perturbed by half of the tolerance value in all three coordinate directions.
            """
        class smooth_marked_faces(TUIMethod):
            """
            Smooths the marked faces.
            """
        class make_periodic(TUIMethod):
            """
            Enables you to make the specified boundaries periodic. You can specify the type of periodicity (rotational or translational), the angle, pivot, and axis of rotation, for rotational periodicity or the translational shift for translational periodicity.   For each of the zones specified, a corresponding periodic shadow boundary zone will be created.
            """
        class delete_unused_nodes(TUIMethod):
            """
            Deletes the boundary nodes that are not used by any boundary faces.
            """
        class unmark_selected_faces(TUIMethod):
            """
            Unmarks the marked selected faces.
            """
        class delete_unconnected_faces(TUIMethod):
            """
            Enables you to delete the unconnected face-zones.
            """
        class clear_marked_faces(TUIMethod):
            """
            Clears marked faces.
            """
        class slit_boundary_face(TUIMethod):
            """
            Slits a boundary face zone by duplicating all faces and nodes, except those nodes that are located at the edges of the boundary zone. A displacement can be specified to provide thickness to the boundary. The slit command only works when it is possible to move from face to face using the connectivity provided by the cells.   You should slit the boundary face after you generate the volume mesh so that cells will not be placed inside the gap. There may be some inaccuracies when you graphically display solution data for a mesh with a slit boundary in ANSYS Fluent.
            """
        class clear_marked_nodes(TUIMethod):
            """
            Clears nodes that were marked using the mark-duplicate-nodes command.
            """
        class count_unused_nodes(TUIMethod):
            """
            Lists the number of boundary nodes that are not used by any cell.
            """
        class mark_duplicate_nodes(TUIMethod):
            """
            Marks duplicate nodes. The marked nodes will appear in the grid display when nodes are displayed. For a list of duplicate nodes, set the /report/verbosity level to 2 before using the mark-duplicate-nodes command.
            """
        class fix_mconnected_edges(TUIMethod):
            """
            Resolves multi-connected edges/non-manifold configurations in the boundary mesh by deleting fringes and overlaps based on threshold values specified.
            """
        class print_info(TUIMethod):
            """
            Prints information about the grid in the text window.
            """
        class count_unused_bound_node(TUIMethod):
            """
            Counts the unused boundary nodes in the domain.
            """
        class recover_periodic_surfaces(TUIMethod):
            """
            Restores the periodic relationship between face zones. You will be prompted for the type (rotational or translational), method (semi-automatic, automatic, or manual, depending on the periodicity type) and for face zones. Periodicity information (angle, pivot point, axis of rotation, or translational shift) are read in with the mesh file.
            """
        class mark_face_intersection(TUIMethod):
            """
            Marks intersecting faces. Intersection is detected if the line defined by any two consecutive nodes on a face intersects any face in the current domain. The marked faces will appear in the grid display when faces are displayed. For a list of intersecting faces, set the /report/verbosity level to 2 before using the mark-face-intersection command.
            """
        class delete_all_dup_faces(TUIMethod):
            """
            Searches for faces on all boundary zones that have the same nodes and deletes the duplicates.
            """
        class edge_limits(TUIMethod):
            """
            Prints the length of the shortest and longest edges on the boundary. This information is useful for setting initial mesh parameters and refinement controls.
            """
        class auto_slit_faces(TUIMethod):
            """
            Slits all boundary faces with cells on both sides (these cells must be in the same cell zone). A displacement can be specified to provide thickness to the boundary.
            """
        class improve_surface_mesh(TUIMethod):
            """
            Improve surface mesh by swapping face edges
            where Delaunay violations occur.
            """
        class merge_small_face_zones(TUIMethod):
            """
            Merges the face zones having area less than the minimum area.
            """
        class create_revolved_surface(TUIMethod):
            """
            Creates a revolved surface by rotating the specified edge through the angle specified. Specify the number of segments, scale factor, and the pivot point and axis of rotation. You can also optionally create a geometry object from the revolved surface created.
            """
        class create_swept_surface(TUIMethod):
            """
            Creates a surface by sweeping the specified edge in the direction specified. You need to specify the distance to sweep through and the number of offsets, as required. You can also optionally create a geometry object from the swept surface created.
            """
        class scale_nodes(TUIMethod):
            """
            Applies a scaling factor to all node coordinates. You can use this command to change the units of the grid.
            """
        class delete_unused_faces(TUIMethod):
            """
            Deletes all the boundary faces that are not used by any cell.
            """
        class check_duplicate_geom(TUIMethod):
            """
            Displays the names of the duplicate surfaces and prints maximum and average distance between them.
            """
        class face_distribution(TUIMethod):
            """
            Reports the distribution of face quality in the text window.
            """
        class set_periodicity(TUIMethod):
            """
            Defines the periodicity parameters. You will be prompted for the type of periodicity (rotational or translational). For rotational periodicity, you will be prompted for the angle and axis of rotation parameters. For translational periodicity, you will be prompted for the shift vector components.
            """
        class create_cylinder(TUIMethod):
            """
            Creates a cylinder by specifying the axis, radius, and edge length or three arc nodes, the axial delta, the radial gap, and the edge length. You can also specify the prefix for the zone being created, as required. You can also optionally create a geometry object from the cylinder created.
            """
        class coarsen_boundary_faces(TUIMethod):
            """
            Coarsen boundary face zones.
            """
        class create_bounding_box(TUIMethod):
            """
            Creates the bounding box for the specified zones. You can specify the zone type, name, edge length, and the extents of the box, as required. You can also optionally create a geometry object from the bounding box created.
            """
        class count_marked_faces(TUIMethod):
            """
            Reports the number of marked faces.
            """

        class separate(TUIMenu):
            """
            Contains options for separating face zones.
            """
            def __init__(self, service, version, mode, path):
                self.local_regions = self.__class__.local_regions(service, version, mode, path + ["local_regions"])
                self.sep_face_zone_by_cnbor = self.__class__.sep_face_zone_by_cnbor(service, version, mode, path + ["sep_face_zone_by_cnbor"])
                self.mark_faces_in_region = self.__class__.mark_faces_in_region(service, version, mode, path + ["mark_faces_in_region"])
                self.sep_face_zone_by_region = self.__class__.sep_face_zone_by_region(service, version, mode, path + ["sep_face_zone_by_region"])
                self.sep_face_zone_by_shape = self.__class__.sep_face_zone_by_shape(service, version, mode, path + ["sep_face_zone_by_shape"])
                self.sep_face_zone_by_seed_angle = self.__class__.sep_face_zone_by_seed_angle(service, version, mode, path + ["sep_face_zone_by_seed_angle"])
                self.sep_face_zone_by_mark = self.__class__.sep_face_zone_by_mark(service, version, mode, path + ["sep_face_zone_by_mark"])
                self.sep_face_zone_by_seed = self.__class__.sep_face_zone_by_seed(service, version, mode, path + ["sep_face_zone_by_seed"])
                self.sep_face_zone_by_angle = self.__class__.sep_face_zone_by_angle(service, version, mode, path + ["sep_face_zone_by_angle"])
                super().__init__(service, version, mode, path)
            class sep_face_zone_by_cnbor(TUIMethod):
                """
                Separates a boundary/interior face zone based on its cell neighbors.
                """
            class mark_faces_in_region(TUIMethod):
                """
                Marks the faces that are contained in a specified local refinement region.
                """
            class sep_face_zone_by_region(TUIMethod):
                """
                Separates a boundary face zone based on contiguous regions.
                """
            class sep_face_zone_by_shape(TUIMethod):
                """
                Separates a boundary face zone based on the shape of the faces (triangular or quadrilateral).
                """
            class sep_face_zone_by_seed_angle(TUIMethod):
                """
                Separates faces connected to the seed face, whose normal fall within the specified cone.
                """
            class sep_face_zone_by_mark(TUIMethod):
                """
                Separates a boundary face zone by moving marked faces to a new zone.
                """
            class sep_face_zone_by_seed(TUIMethod):
                """
                Separates a boundary face zone by defining a seed face on the surface.
                """
            class sep_face_zone_by_angle(TUIMethod):
                """
                Separates a boundary face zone based on significant angle.
                """

            class local_regions(TUIMenu):
                """
                Enters the local refinement menu.
                """
                def __init__(self, service, version, mode, path):
                    self.init = self.__class__.init(service, version, mode, path + ["init"])
                    self.define = self.__class__.define(service, version, mode, path + ["define"])
                    self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                    self.list_all_regions = self.__class__.list_all_regions(service, version, mode, path + ["list_all_regions"])
                    super().__init__(service, version, mode, path)
                class init(TUIMethod):
                    """
                    Creates a region encompassing the entire geometry.
                    """
                class define(TUIMethod):
                    """
                    Enables you to define the local region.
                    """
                class delete(TUIMethod):
                    """
                    Deletes the specified local region.
                    """
                class list_all_regions(TUIMethod):
                    """
                    Lists all the local regions defined.
                    """

        class refine(TUIMenu):
            """
            Discusses the commands used to refine the boundary mesh.
            """
            def __init__(self, service, version, mode, path):
                self.local_regions = self.__class__.local_regions(service, version, mode, path + ["local_regions"])
                self.limits = self.__class__.limits(service, version, mode, path + ["limits"])
                self.refine = self.__class__.refine(service, version, mode, path + ["refine"])
                self.mark = self.__class__.mark(service, version, mode, path + ["mark"])
                self.auto_refine = self.__class__.auto_refine(service, version, mode, path + ["auto_refine"])
                self.clear = self.__class__.clear(service, version, mode, path + ["clear"])
                self.count = self.__class__.count(service, version, mode, path + ["count"])
                super().__init__(service, version, mode, path)
            class limits(TUIMethod):
                """
                Prints a report of the minimum and maximum size of each specified zone. This report will also tell you how many faces on each zone have been marked for refinement.
                """
            class refine(TUIMethod):
                """
                Refines the marked faces.
                """
            class mark(TUIMethod):
                """
                Marks the faces for refinement.
                """
            class auto_refine(TUIMethod):
                """
                Automatically refines a face zone based on proximity. The original face zone is treated as a background mesh. Faces are refined by multiple face splitting passes, so that no face is in close proximity to any face in the current domain.
                """
            class clear(TUIMethod):
                """
                Clears all refinement marks from all boundary faces.
                """
            class count(TUIMethod):
                """
                Counts the number of faces marked on each boundary zone.
                """

            class local_regions(TUIMenu):
                """
                Enters the local refinement menu.
                """
                def __init__(self, service, version, mode, path):
                    self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                    self.list_all_regions = self.__class__.list_all_regions(service, version, mode, path + ["list_all_regions"])
                    self.define = self.__class__.define(service, version, mode, path + ["define"])
                    self.init = self.__class__.init(service, version, mode, path + ["init"])
                    super().__init__(service, version, mode, path)
                class delete(TUIMethod):
                    """
                    Deletes the specified region.
                    """
                class list_all_regions(TUIMethod):
                    """
                    Lists all the refinement regions in the console.
                    """
                class define(TUIMethod):
                    """
                    Defines the refinement region according to the specified parameters.
                    """
                class init(TUIMethod):
                    """
                    Creates a region encompassing the entire geometry.
                    """

        class improve(TUIMenu):
            """
            Enables you to improve boundary surfaces.
            """
            def __init__(self, service, version, mode, path):
                self.swap = self.__class__.swap(service, version, mode, path + ["swap"])
                self.improve = self.__class__.improve(service, version, mode, path + ["improve"])
                self.collapse_bad_faces = self.__class__.collapse_bad_faces(service, version, mode, path + ["collapse_bad_faces"])
                self.degree_swap = self.__class__.degree_swap(service, version, mode, path + ["degree_swap"])
                self.smooth = self.__class__.smooth(service, version, mode, path + ["smooth"])
                super().__init__(service, version, mode, path)
            class swap(TUIMethod):
                """
                Enables you to improve the boundary surface using edge swapping.
                """
            class improve(TUIMethod):
                """
                Enables you to improve the boundary surface quality using skewness, size change, aspect ratio, or area as the quality measure.
                """
            class collapse_bad_faces(TUIMethod):
                """
                Enables you to collapse the short edge of faces having a high aspect ratio or skewness in the specified face zone(s).
                """
            class degree_swap(TUIMethod):
                """
                Enables you to improve the boundary mesh by swapping edges based on a node degree value other than 6. The node degree is defined as the number of edges connected to the node.
                """
            class smooth(TUIMethod):
                """
                Enables you to improve the boundary surface using smoothing.
                """

        class manage(TUIMenu):
            """
            Contains options for manipulating the boundary zones.
            """
            def __init__(self, service, version, mode, path):
                self.user_defined_groups = self.__class__.user_defined_groups(service, version, mode, path + ["user_defined_groups"])
                self.translate = self.__class__.translate(service, version, mode, path + ["translate"])
                self.translate_model = self.__class__.translate_model(service, version, mode, path + ["translate_model"])
                self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                self.id = self.__class__.id(service, version, mode, path + ["id"])
                self.orient = self.__class__.orient(service, version, mode, path + ["orient"])
                self.change_prefix = self.__class__.change_prefix(service, version, mode, path + ["change_prefix"])
                self.merge = self.__class__.merge(service, version, mode, path + ["merge"])
                self.scale = self.__class__.scale(service, version, mode, path + ["scale"])
                self.change_suffix = self.__class__.change_suffix(service, version, mode, path + ["change_suffix"])
                self.copy = self.__class__.copy(service, version, mode, path + ["copy"])
                self.flip = self.__class__.flip(service, version, mode, path + ["flip"])
                self.name = self.__class__.name(service, version, mode, path + ["name"])
                self.rotate_model = self.__class__.rotate_model(service, version, mode, path + ["rotate_model"])
                self.type = self.__class__.type(service, version, mode, path + ["type"])
                self.origin = self.__class__.origin(service, version, mode, path + ["origin"])
                self.remove_suffix = self.__class__.remove_suffix(service, version, mode, path + ["remove_suffix"])
                self.list = self.__class__.list(service, version, mode, path + ["list"])
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                self.rotate = self.__class__.rotate(service, version, mode, path + ["rotate"])
                self.auto_delete_nodes = self.__class__.auto_delete_nodes(service, version, mode, path + ["auto_delete_nodes"])
                self.scale_model = self.__class__.scale_model(service, version, mode, path + ["scale_model"])
                super().__init__(service, version, mode, path)
            class translate(TUIMethod):
                """
                Translates all nodes of the specified face zone(s).
                """
            class translate_model(TUIMethod):
                """
                Translates all nodes of the model by the specified translation offsets (x, y, z).   The translation offsets are interpreted as absolute numbers in meshing mode. In solution mode, however, the translation offsets are assumed to be distances in the length unit set. This may lead to differences in domain extents reported after translating the mesh in the respective modes.
                """
            class delete(TUIMethod):
                """
                Deletes the face zone.
                """
            class id(TUIMethod):
                """
                Specifies a new boundary zone ID. If there is a conflict, the change will be ignored.
                """
            class orient(TUIMethod):
                """
                Consistently orients the faces in the specified zones.
                """
            class change_prefix(TUIMethod):
                """
                Enables you to change the prefix for the specified face zones.
                """
            class merge(TUIMethod):
                """
                Merges face zones.
                """
            class scale(TUIMethod):
                """
                Scales all nodes of the specified face zone(s).
                """
            class change_suffix(TUIMethod):
                """
                Change the suffix for specified face zones.
                """
            class copy(TUIMethod):
                """
                Copies all nodes and faces of the specified face zone(s).
                """
            class flip(TUIMethod):
                """
                Reverses the normal direction of the specified boundary zone(s).
                """
            class name(TUIMethod):
                """
                Gives a face zone a new name.
                """
            class rotate_model(TUIMethod):
                """
                Rotates all nodes of the model through the specified angle, based on the specified point and axis of rotation.
                """
            class type(TUIMethod):
                """
                Changes the boundary type of the face zone.   When changing the boundary type of any zone to type interior, ensure that there is a single cell zone across the interior boundary. Retaining multiple cell zones across an interior boundary can cause undesirable results with further tet meshing or smoothing operations.  Also, face zones having no/one neighboring cell zone should not be changed to type interior.  The mesh check will issue a warning if multiple cell zones are maintained across an interior boundary. The boundary type in such cases should be set to internal instead.
                """
            class origin(TUIMethod):
                """
                Specifies a new origin for the mesh, to be used for face zone rotation and for periodic zone creation. The default origin is (0,0,0).
                """
            class remove_suffix(TUIMethod):
                """
                Removes the suffix (characters including and after the leftmost ":") in the face zone names.
                """
            class list(TUIMethod):
                """
                Prints information about all boundary zones.
                """
            class create(TUIMethod):
                """
                Creates a new face zone.
                """
            class rotate(TUIMethod):
                """
                Rotates all nodes of the specified face zone(s).
                """
            class auto_delete_nodes(TUIMethod):
                """
                Specifies whether or not unused nodes should be deleted when their face zone is deleted.
                """
            class scale_model(TUIMethod):
                """
                Scales all nodes of the model by multiplying the node coordinates by the specified scale factors (x, y, z).
                """

            class user_defined_groups(TUIMenu):
                """
                Enables you to manipulate user-defined groups.
                """
                def __init__(self, service, version, mode, path):
                    self.create = self.__class__.create(service, version, mode, path + ["create"])
                    self.update = self.__class__.update(service, version, mode, path + ["update"])
                    self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                    self.list = self.__class__.list(service, version, mode, path + ["list"])
                    self.activate = self.__class__.activate(service, version, mode, path + ["activate"])
                    super().__init__(service, version, mode, path)
                class create(TUIMethod):
                    """
                    Creates the user-defined group comprising the specified zones.
                    """
                class update(TUIMethod):
                    """
                    Enables you to modify an existing group.
                    """
                class delete(TUIMethod):
                    """
                    Deletes the specified user-defined group.
                    """
                class list(TUIMethod):
                    """
                    Lists the groups in the console.
                    """
                class activate(TUIMethod):
                    """
                    Activates the specified user-defined groups.
                    """

        class boundary_conditions(TUIMenu):
            """
            Contains options for copying or clearing boundary conditions when a case file is read.
            """
            def __init__(self, service, version, mode, path):
                self.clear_all = self.__class__.clear_all(service, version, mode, path + ["clear_all"])
                self.copy = self.__class__.copy(service, version, mode, path + ["copy"])
                self.clear = self.__class__.clear(service, version, mode, path + ["clear"])
                super().__init__(service, version, mode, path)
            class clear_all(TUIMethod):
                """
                Clears the boundary conditions assigned to all the face zones.
                """
            class copy(TUIMethod):
                """
                Enables you to copy the boundary conditions from the face zone selected to the face zones specified.
                """
            class clear(TUIMethod):
                """
                Clears the boundary conditions assigned to the specified face zones.
                """

        class shell_boundary_layer(TUIMenu):
            """
            Enter the shell boundary layer menu.
            """
            def __init__(self, service, version, mode, path):
                self.controls = self.__class__.controls(service, version, mode, path + ["controls"])
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                super().__init__(service, version, mode, path)
            class create(TUIMethod):
                """
                Create shell boundary layers from one or more face zones.
                """

            class controls(TUIMenu):
                """
                Shell Boundary Layer Controls.
                """
                def __init__(self, service, version, mode, path):
                    self.zone_specific_growth = self.__class__.zone_specific_growth(service, version, mode, path + ["zone_specific_growth"])
                    super().__init__(service, version, mode, path)

                class zone_specific_growth(TUIMenu):
                    """
                    Shell boundary Layer Growth Controls.
                    """
                    def __init__(self, service, version, mode, path):
                        self.apply_growth = self.__class__.apply_growth(service, version, mode, path + ["apply_growth"])
                        self.clear_growth = self.__class__.clear_growth(service, version, mode, path + ["clear_growth"])
                        super().__init__(service, version, mode, path)
                    class apply_growth(TUIMethod):
                        """
                        Apply  shell boundary la growth on individual edge zones.
                        """
                    class clear_growth(TUIMethod):
                        """
                        Clear shell boundary layer specific growth on individual edge zones.
                        """

        class remesh(TUIMenu):
            """
            Has a set of commands for remeshing the face zones.
            """
            def __init__(self, service, version, mode, path):
                self.size_functions = self.__class__.size_functions(service, version, mode, path + ["size_functions"])
                self.controls = self.__class__.controls(service, version, mode, path + ["controls"])
                self.intersect_all_face_zones = self.__class__.intersect_all_face_zones(service, version, mode, path + ["intersect_all_face_zones"])
                self.mark_join_faces = self.__class__.mark_join_faces(service, version, mode, path + ["mark_join_faces"])
                self.remesh_face_zones_conformally = self.__class__.remesh_face_zones_conformally(service, version, mode, path + ["remesh_face_zones_conformally"])
                self.triangulate = self.__class__.triangulate(service, version, mode, path + ["triangulate"])
                self.coarsen_and_refine = self.__class__.coarsen_and_refine(service, version, mode, path + ["coarsen_and_refine"])
                self.insert_edge_zone = self.__class__.insert_edge_zone(service, version, mode, path + ["insert_edge_zone"])
                self.mark_intersecting_faces = self.__class__.mark_intersecting_faces(service, version, mode, path + ["mark_intersecting_faces"])
                self.clear_marked_faces = self.__class__.clear_marked_faces(service, version, mode, path + ["clear_marked_faces"])
                self.create_all_intrst_loops = self.__class__.create_all_intrst_loops(service, version, mode, path + ["create_all_intrst_loops"])
                self.remesh_marked_faces = self.__class__.remesh_marked_faces(service, version, mode, path + ["remesh_marked_faces"])
                self.join_all_face_zones = self.__class__.join_all_face_zones(service, version, mode, path + ["join_all_face_zones"])
                self.create_edge_loops = self.__class__.create_edge_loops(service, version, mode, path + ["create_edge_loops"])
                self.intersect_face_zones = self.__class__.intersect_face_zones(service, version, mode, path + ["intersect_face_zones"])
                self.stitch_all_face_zones = self.__class__.stitch_all_face_zones(service, version, mode, path + ["stitch_all_face_zones"])
                self.remesh_face_zone = self.__class__.remesh_face_zone(service, version, mode, path + ["remesh_face_zone"])
                self.create_stitch_loop = self.__class__.create_stitch_loop(service, version, mode, path + ["create_stitch_loop"])
                self.stitch_with_preserve_boundary = self.__class__.stitch_with_preserve_boundary(service, version, mode, path + ["stitch_with_preserve_boundary"])
                self.remesh_overlapping_zones = self.__class__.remesh_overlapping_zones(service, version, mode, path + ["remesh_overlapping_zones"])
                self.join_face_zones = self.__class__.join_face_zones(service, version, mode, path + ["join_face_zones"])
                self.create_intersect_loop = self.__class__.create_intersect_loop(service, version, mode, path + ["create_intersect_loop"])
                self.create_join_loop = self.__class__.create_join_loop(service, version, mode, path + ["create_join_loop"])
                self.stitch_face_zones = self.__class__.stitch_face_zones(service, version, mode, path + ["stitch_face_zones"])
                self.remesh_constant_size = self.__class__.remesh_constant_size(service, version, mode, path + ["remesh_constant_size"])
                self.mark_stitch_faces = self.__class__.mark_stitch_faces(service, version, mode, path + ["mark_stitch_faces"])
                self.faceted_stitch_zones = self.__class__.faceted_stitch_zones(service, version, mode, path + ["faceted_stitch_zones"])
                self.delete_overlapped_edges = self.__class__.delete_overlapped_edges(service, version, mode, path + ["delete_overlapped_edges"])
                super().__init__(service, version, mode, path)
            class intersect_all_face_zones(TUIMethod):
                """
                Remeshes all the intersecting face zones.   After the intersect operation, remesh is called automatically. To disable the post-remesh operation, use the text command:  /boundary/remesh/controls/intersect/remesh-post-intersection?
                no.
                """
            class mark_join_faces(TUIMethod):
                """
                Highlights the triangles in the neighborhood of the join edge loop.
                """
            class remesh_face_zones_conformally(TUIMethod):
                """
                Remeshes face zones using the current size function and keeping a conformal interface between them. If no size function is defined, an error message will be generated.  This command will prompt for:
                Boundary Face Zones
                Boundary Edge Zones
                feature angle – used to determine the minimum angle between features that will be preserved during remeshing
                corner angle – used to specify the minimum angle between feature edges that will be preserved
                Replace Face Zone? – (default is Yes) the remeshed face zone(s) will take the name and -id of the original zones, and the original face zone(s) will have “orig” appended to their name. If No, the remeshed face zone(s) will have “retri” added postfix.
                Periodic face zones cannot be remeshed using this command.
                """
            class triangulate(TUIMethod):
                """
                Triangulates quad zones.
                """
            class coarsen_and_refine(TUIMethod):
                """
                Remeshes (coarsens/refines) the boundary face zones based on the computed size field. Specify the boundary face zones to be remeshed, the boundary edge zones, feature angle, and corner angle. Additionally, specify whether the current boundary face zones should be replaced by the remeshed face zones after the operation is complete.
                """
            class insert_edge_zone(TUIMethod):
                """
                Inserts an edge zone into a triangulated boundary face zone.
                """
            class mark_intersecting_faces(TUIMethod):
                """
                Highlights the triangles in the neighborhood of the line of intersection.
                """
            class clear_marked_faces(TUIMethod):
                """
                Clears the highlighting of the triangles that are marked.
                """
            class create_all_intrst_loops(TUIMethod):
                """
                Creates edge loop of intersection for all boundary zones in current domain.
                """
            class remesh_marked_faces(TUIMethod):
                """
                Locally remesh marked faces.
                """
            class join_all_face_zones(TUIMethod):
                """
                Connects all overlapping face zones using the join operation.   After the join operation, remesh is called automatically. To disable the post-remesh operation, use the text command:  /boundary/remesh/controls/intersect/remesh-post-intersection?
                no.
                """
            class create_edge_loops(TUIMethod):
                """
                Creates edge loops for a specified face zone, based on feature angle.
                """
            class intersect_face_zones(TUIMethod):
                """
                Remeshes two intersecting face zones so that they become conformal.   After the intersect operation, remesh is called automatically. To disable the post-remesh operation, use the text command:  /boundary/remesh/controls/intersect/remesh-post-intersection?
                no.
                """
            class stitch_all_face_zones(TUIMethod):
                """
                Connects (stitches) all the face zones along the free edges.   After the stitch operation, remesh is called automatically. To disable the post-remesh operation, use the text command:  /boundary/remesh/controls/intersect/remesh-post-intersection?
                no.
                """
            class remesh_face_zone(TUIMethod):
                """
                Remeshes a specified face zone by automatically extracting edge loops. If edge loops are present in the current domain (for example, if they were created using the create-edge-loops command), they are used to remesh the specified face zone.
                """
            class create_stitch_loop(TUIMethod):
                """
                Creates edge loops for connecting two surfaces along their free edges.
                """
            class stitch_with_preserve_boundary(TUIMethod):
                """
                Connects (stitches) a zone to another which is connected to an existing volume mesh, while preserving the boundary of the zones connected to the volume mesh. Specify a list of boundary zones to be preserved, a list of the boundary zones to be connected to each of these zones, and the tolerance value.   After the stitch operation, remesh is called automatically. To disable the post-remesh operation, use the text command:  /boundary/remesh/controls/intersect/remesh-post-intersection?
                no  This command will not work for overlapping or partially overlapping face zones.
                """
            class remesh_overlapping_zones(TUIMethod):
                """
                Remeshes overlapping face zones. The non-overlapping region is remeshed using the edge loops created from the overlapping face zones.
                """
            class join_face_zones(TUIMethod):
                """
                Connects two overlapping faces.   After the join operation, remesh is called automatically. To disable the post-remesh operation, use the text command:  /boundary/remesh/controls/intersect/remesh-post-intersection?
                no.
                """
            class create_intersect_loop(TUIMethod):
                """
                Creates an interior edge loop at the intersection between two adjacent face zones. Edges created in this way will not be remeshed by default.
                """
            class create_join_loop(TUIMethod):
                """
                Creates edge loop on boundary of the region of overlap of two surfaces.
                """
            class stitch_face_zones(TUIMethod):
                """
                Connects two surfaces along their free edges.   After the stitch operation, remesh is called automatically. To disable the post-remesh operation, use the text command:  /boundary/remesh/controls/intersect/remesh-post-intersection?
                no.
                """
            class remesh_constant_size(TUIMethod):
                """
                Remeshes the specified face zones to a constant triangle size while maintaining conformity with adjacent zones. Specify the boundary face zones to be remeshed, the boundary edge zones, feature angle, corner angle, and the constant size. Additionally, specify whether the current boundary face zones should be replaced by the remeshed face zones after the operation is complete.
                """
            class mark_stitch_faces(TUIMethod):
                """
                Highlights the triangles in the neighborhood of the stitch edge loop.
                """
            class faceted_stitch_zones(TUIMethod):
                """
                Performs the faceted stitching of zones.
                """
            class delete_overlapped_edges(TUIMethod):
                """
                Deletes edges that overlap selected edge loops.
                """

            class size_functions(TUIMenu):
                """
                Enters the size functions menu where you can define size functions for controlling mesh size distribution.
                """
                def __init__(self, service, version, mode, path):
                    self.contours = self.__class__.contours(service, version, mode, path + ["contours"])
                    self.controls = self.__class__.controls(service, version, mode, path + ["controls"])
                    self.list_periodicity_filter = self.__class__.list_periodicity_filter(service, version, mode, path + ["list_periodicity_filter"])
                    self.create_defaults = self.__class__.create_defaults(service, version, mode, path + ["create_defaults"])
                    self.use_cad_imported_curvature = self.__class__.use_cad_imported_curvature(service, version, mode, path + ["use_cad_imported_curvature"])
                    self.list = self.__class__.list(service, version, mode, path + ["list"])
                    self.triangulate_quad_faces = self.__class__.triangulate_quad_faces(service, version, mode, path + ["triangulate_quad_faces"])
                    self.set_global_controls = self.__class__.set_global_controls(service, version, mode, path + ["set_global_controls"])
                    self.enable_periodicity_filter = self.__class__.enable_periodicity_filter(service, version, mode, path + ["enable_periodicity_filter"])
                    self.set_scaling_filter = self.__class__.set_scaling_filter(service, version, mode, path + ["set_scaling_filter"])
                    self.compute = self.__class__.compute(service, version, mode, path + ["compute"])
                    self.create = self.__class__.create(service, version, mode, path + ["create"])
                    self.disable_periodicity_filter = self.__class__.disable_periodicity_filter(service, version, mode, path + ["disable_periodicity_filter"])
                    self.delete_all = self.__class__.delete_all(service, version, mode, path + ["delete_all"])
                    self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                    self.reset_global_controls = self.__class__.reset_global_controls(service, version, mode, path + ["reset_global_controls"])
                    self.set_prox_gap_tolerance = self.__class__.set_prox_gap_tolerance(service, version, mode, path + ["set_prox_gap_tolerance"])
                    super().__init__(service, version, mode, path)
                class list_periodicity_filter(TUIMethod):
                    """
                    List periodic in size field.
                    """
                class create_defaults(TUIMethod):
                    """
                    Creates default size functions based on face and edge curvature and proximity.
                    """
                class use_cad_imported_curvature(TUIMethod):
                    """
                    Enables/disables curvature data from the nodes of the CAD facets.
                    """
                class list(TUIMethod):
                    """
                    Lists all the defined size functions and the parameter values defined.
                    """
                class triangulate_quad_faces(TUIMethod):
                    """
                    Identifies the zones comprising non-triangular elements and uses a triangulated copy of these zones for computing the size functions.
                    """
                class set_global_controls(TUIMethod):
                    """
                    Sets the values for the global minimum and maximum size, and the growth rate.
                    """
                class enable_periodicity_filter(TUIMethod):
                    """
                    Enable size field periodicity.
                    """
                class set_scaling_filter(TUIMethod):
                    """
                    Specifies the scale factor, and minimum and maximum size values to filter the size output from the size field.
                    """
                class compute(TUIMethod):
                    """
                    Computes the size field based on the defined parameters.
                    """
                class create(TUIMethod):
                    """
                    Defines the size function based on the specified parameters.
                    """
                class disable_periodicity_filter(TUIMethod):
                    """
                    Removes periodicity from the size field.
                    """
                class delete_all(TUIMethod):
                    """
                    Deletes all the defined size functions.
                    """
                class delete(TUIMethod):
                    """
                    Deletes the specified size function or the current size field.
                    """
                class reset_global_controls(TUIMethod):
                    """
                    Resets the global controls to their default values.
                    """
                class set_prox_gap_tolerance(TUIMethod):
                    """
                    Sets the tolerance relative to minimum size to take gaps into account. Gaps whose thickness is less than the global minimum size multiplied by this factor will not be regarded as a proximity gap.
                    """

                class contours(TUIMenu):
                    """
                    Contains options for displaying contours of size functions.
                    """
                    def __init__(self, service, version, mode, path):
                        self.set = self.__class__.set(service, version, mode, path + ["set"])
                        self.draw = self.__class__.draw(service, version, mode, path + ["draw"])
                        super().__init__(service, version, mode, path)
                    class draw(TUIMethod):
                        """
                        Displays contours in the graphics window. Compute the size field using /size-functions/compute or read in a size field file prior to displaying the contours of size.
                        """

                    class set(TUIMenu):
                        """
                        Set contour options.
                        """
                        def __init__(self, service, version, mode, path):
                            self.refine_facets = self.__class__.refine_facets(service, version, mode, path + ["refine_facets"])
                            super().__init__(service, version, mode, path)
                        class refine_facets(TUIMethod):
                            """
                            Enables you to specify smaller facets if the original are too large. Default is no.
                            """

                class controls(TUIMenu):
                    """
                    Menu to control different behavior of sf.
                    """
                    def __init__(self, service, version, mode, path):
                        self.meshed_sf_behavior = self.__class__.meshed_sf_behavior(service, version, mode, path + ["meshed_sf_behavior"])
                        self.curvature_method = self.__class__.curvature_method(service, version, mode, path + ["curvature_method"])
                        super().__init__(service, version, mode, path)
                    class meshed_sf_behavior(TUIMethod):
                        """
                        Set meshed size function processing to hard.
                        """
                    class curvature_method(TUIMethod):
                        """
                        Option to get facet curvature.
                        """

            class controls(TUIMenu):
                """
                Enters the edge loop tools text menu.
                """
                def __init__(self, service, version, mode, path):
                    self.intersect = self.__class__.intersect(service, version, mode, path + ["intersect"])
                    self.direction = self.__class__.direction(service, version, mode, path + ["direction"])
                    self.proximity_local_search = self.__class__.proximity_local_search(service, version, mode, path + ["proximity_local_search"])
                    self.remesh_method = self.__class__.remesh_method(service, version, mode, path + ["remesh_method"])
                    self.project_method = self.__class__.project_method(service, version, mode, path + ["project_method"])
                    self.quadratic_recon = self.__class__.quadratic_recon(service, version, mode, path + ["quadratic_recon"])
                    self.spacing = self.__class__.spacing(service, version, mode, path + ["spacing"])
                    self.tolerance = self.__class__.tolerance(service, version, mode, path + ["tolerance"])
                    self.delete_overlapped = self.__class__.delete_overlapped(service, version, mode, path + ["delete_overlapped"])
                    super().__init__(service, version, mode, path)
                class direction(TUIMethod):
                    """
                    Specifies the direction of the edge loop projection.
                    """
                class proximity_local_search(TUIMethod):
                    """
                    Includes the selected face for proximity calculation.
                    """
                class remesh_method(TUIMethod):
                    """
                    Specifies the method to be used for the node distribution on the edge loop.
                    """
                class project_method(TUIMethod):
                    """
                    Specifies the method for projecting edge loops.
                    """
                class quadratic_recon(TUIMethod):
                    """
                    Enables/disables quadratic reconstruction of edge loops.
                    """
                class spacing(TUIMethod):
                    """
                    Sets the node spacing for the edge loop.
                    """
                class tolerance(TUIMethod):
                    """
                    Sets the tolerance for determining if two edges intersect.
                    """
                class delete_overlapped(TUIMethod):
                    """
                    Toggles the deletion of region of overlap of the two surfaces.
                    """

                class intersect(TUIMenu):
                    """
                    Enters the intersect control menu.
                    """
                    def __init__(self, service, version, mode, path):
                        self.feature_angle = self.__class__.feature_angle(service, version, mode, path + ["feature_angle"])
                        self.join_project_angle = self.__class__.join_project_angle(service, version, mode, path + ["join_project_angle"])
                        self.stitch_preserve = self.__class__.stitch_preserve(service, version, mode, path + ["stitch_preserve"])
                        self.ignore_parallel_faces = self.__class__.ignore_parallel_faces(service, version, mode, path + ["ignore_parallel_faces"])
                        self.retri_improve = self.__class__.retri_improve(service, version, mode, path + ["retri_improve"])
                        self.remesh_post_intersection = self.__class__.remesh_post_intersection(service, version, mode, path + ["remesh_post_intersection"])
                        self.join_match_angle = self.__class__.join_match_angle(service, version, mode, path + ["join_match_angle"])
                        self.refine_region = self.__class__.refine_region(service, version, mode, path + ["refine_region"])
                        self.absolute_tolerance = self.__class__.absolute_tolerance(service, version, mode, path + ["absolute_tolerance"])
                        self.within_tolerance = self.__class__.within_tolerance(service, version, mode, path + ["within_tolerance"])
                        self.separate = self.__class__.separate(service, version, mode, path + ["separate"])
                        self.tolerance = self.__class__.tolerance(service, version, mode, path + ["tolerance"])
                        self.delete_overlap = self.__class__.delete_overlap(service, version, mode, path + ["delete_overlap"])
                        super().__init__(service, version, mode, path)
                    class feature_angle(TUIMethod):
                        """
                        Specifies the minimum feature angle that should be considered while retriangulating the boundary zones. All the edges in the zone having feature angle greater than the specified feature angle are retained. This option is useful for preserving the shape of the intersecting boundary zones. The default value of feature angle is 40, however, a value in the range of 10–50 degrees is recommended. A large value may distort the shape of the intersecting boundary zones.
                        """
                    class join_project_angle(TUIMethod):
                        """
                        Specifies the allowed maximum angle between the face normal and the project direction for the overlapping surfaces to be joined. This parameter is used to control the size of the join region.
                        """
                    class stitch_preserve(TUIMethod):
                        """
                        Indicates that shape of the first zone specified is to be preserved. This option is enabled by default.
                        """
                    class ignore_parallel_faces(TUIMethod):
                        """
                        Default is yes. If there are close-to-parallel faces, set to no to separate the zones and avoid creating an intersection loop.
                        """
                    class retri_improve(TUIMethod):
                        """
                        Enables you to improve the mesh. After performing any intersection operation, the slivers are removed along the curve of intersection, Laplace smoothing is performed, and followed by the edge swapping. Laplace smoothing is also performed for insert-edge-zone, remesh-overlapped-zones, and prism-retriangulation options. Smoothing is performed again. The smooth-swap operations can be controlled by changing the various defaults such as swapping iterations, smoothing iterations, etc.
                        """
                    class remesh_post_intersection(TUIMethod):
                        """
                        Used to enable or disable automatic post-remesh operation after any connect operation (join, intersect, or stitch).
                        """
                    class join_match_angle(TUIMethod):
                        """
                        Specifies the allowed maximum angle between the normals of the two overlapping surfaces to be joined. This parameter is used to control the size of the join region.
                        """
                    class refine_region(TUIMethod):
                        """
                        Enables you to refine the regions that are modified during the intersect operations. It toggles the refinement of the intersecting regions after performing any of the intersection operation.   This operation improves the quality of the resulting mesh, however, this option is disabled by default.
                        """
                    class absolute_tolerance(TUIMethod):
                        """
                        Enables you to switch between the use of absolute and relative tolerance. By default, the relative tolerance value is used.
                        """
                    class within_tolerance(TUIMethod):
                        """
                        Performs the intersection operation only within the specified tolerance value. It is useful only for the Intersect option.
                        """
                    class separate(TUIMethod):
                        """
                        Enables the automatic separation of intersected zones.
                        """
                    class tolerance(TUIMethod):
                        """
                        Specifies the tolerance value for the intersect operations.
                        """
                    class delete_overlap(TUIMethod):
                        """
                        Enables/disables the deletion of overlapped edges. It toggles the automatic deletion of region of overlap of the two surfaces. This option is used by while remeshing overlapping zones and retriangulating prisms. By default, this option is enabled.
                        """

        class modify(TUIMenu):
            """
            Contains commands used to modify the boundary mesh.
            """
            def __init__(self, service, version, mode, path):
                self.skew_report_zone = self.__class__.skew_report_zone(service, version, mode, path + ["skew_report_zone"])
                self.analyze_bnd_connectvty = self.__class__.analyze_bnd_connectvty(service, version, mode, path + ["analyze_bnd_connectvty"])
                self.deselect_last = self.__class__.deselect_last(service, version, mode, path + ["deselect_last"])
                self.select_position = self.__class__.select_position(service, version, mode, path + ["select_position"])
                self.next_skew = self.__class__.next_skew(service, version, mode, path + ["next_skew"])
                self.select_entity = self.__class__.select_entity(service, version, mode, path + ["select_entity"])
                self.move = self.__class__.move(service, version, mode, path + ["move"])
                self.show_filter = self.__class__.show_filter(service, version, mode, path + ["show_filter"])
                self.rezone = self.__class__.rezone(service, version, mode, path + ["rezone"])
                self.auto_patch_holes = self.__class__.auto_patch_holes(service, version, mode, path + ["auto_patch_holes"])
                self.hole_feature_angle = self.__class__.hole_feature_angle(service, version, mode, path + ["hole_feature_angle"])
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                self.mark_skew_face = self.__class__.mark_skew_face(service, version, mode, path + ["mark_skew_face"])
                self.merge = self.__class__.merge(service, version, mode, path + ["merge"])
                self.skew = self.__class__.skew(service, version, mode, path + ["skew"])
                self.smooth = self.__class__.smooth(service, version, mode, path + ["smooth"])
                self.select_probe = self.__class__.select_probe(service, version, mode, path + ["select_probe"])
                self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                self.local_remesh = self.__class__.local_remesh(service, version, mode, path + ["local_remesh"])
                self.clear_skew_faces = self.__class__.clear_skew_faces(service, version, mode, path + ["clear_skew_faces"])
                self.select_visible_entities = self.__class__.select_visible_entities(service, version, mode, path + ["select_visible_entities"])
                self.swap = self.__class__.swap(service, version, mode, path + ["swap"])
                self.undo = self.__class__.undo(service, version, mode, path + ["undo"])
                self.list_selections = self.__class__.list_selections(service, version, mode, path + ["list_selections"])
                self.delta_move = self.__class__.delta_move(service, version, mode, path + ["delta_move"])
                self.show_probe = self.__class__.show_probe(service, version, mode, path + ["show_probe"])
                self.split_face = self.__class__.split_face(service, version, mode, path + ["split_face"])
                self.select_zone = self.__class__.select_zone(service, version, mode, path + ["select_zone"])
                self.select_filter = self.__class__.select_filter(service, version, mode, path + ["select_filter"])
                self.clear_selections = self.__class__.clear_selections(service, version, mode, path + ["clear_selections"])
                self.collapse = self.__class__.collapse(service, version, mode, path + ["collapse"])
                self.patch_options = self.__class__.patch_options(service, version, mode, path + ["patch_options"])
                self.create_mid_node = self.__class__.create_mid_node(service, version, mode, path + ["create_mid_node"])
                super().__init__(service, version, mode, path)
            class skew_report_zone(TUIMethod):
                """
                Enables you to select the zone for which you want to report the skewness. You can either specify zone name or zone ID.
                """
            class analyze_bnd_connectvty(TUIMethod):
                """
                Finds and marks free edges and nodes and multiply-connected edges and nodes. This process is necessary if the boundary mesh has been changed with Scheme functions.
                """
            class deselect_last(TUIMethod):
                """
                Removes the last selection from the selection list.
                """
            class select_position(TUIMethod):
                """
                Adds a position to the selection list by entering the coordinates of the position.
                """
            class next_skew(TUIMethod):
                """
                Finds the triangular face of nearest lower skewness value than that of the worst skewed face. The face ID, its skewness, the longest edge ID, and the node ID opposite to the longest edge are displayed in the console.
                """
            class select_entity(TUIMethod):
                """
                Adds a cell, face, or node to the selection list by entering the name of the entity.
                """
            class move(TUIMethod):
                """
                Moves the selected node to the selected position if the selection list contains a node and a position.
                """
            class show_filter(TUIMethod):
                """
                Shows the current filter.
                """
            class rezone(TUIMethod):
                """
                Moves the selected faces from their current zone into the selected zone, if the selection list contains a zone and one or more faces.
                """
            class auto_patch_holes(TUIMethod):
                """
                Patch zone(s) by filling holes.
                """
            class hole_feature_angle(TUIMethod):
                """
                Specifies the feature angle for consideration of holes in the geometry.
                """
            class create(TUIMethod):
                """
                Creates a boundary face if the selection list contains 3 nodes and an optional zone. If the selection list contains positions, then nodes are created.
                """
            class mark_skew_face(TUIMethod):
                """
                Marks faces that should be skipped when the worst skewed face is reported using the Modify Boundary dialog box. This enables you to search for the next skewed face.
                """
            class merge(TUIMethod):
                """
                Merges pairs of nodes. The first node selected is retained, and the second is the duplicate that is merged.
                """
            class skew(TUIMethod):
                """
                Finds the face with the highest (worst) skewness, selects it in the graphics window, and reports its skewness and zone ID in the console window.
                """
            class smooth(TUIMethod):
                """
                Uses Laplace smoothing to modify the position of the nodes in the selection list. It moves the selected node to a position computed from an average of its node neighbors. The new position is an average of the neighboring node coordinates and is not reprojected to the discrete surface.
                """
            class select_probe(TUIMethod):
                """
                Selects the probe function. The possible functions are:.
                """
            class delete(TUIMethod):
                """
                Deletes all selected faces and nodes.
                """
            class local_remesh(TUIMethod):
                """
                Remeshes marked faces or faces based on selections in the graphics window. Select the faces to be remeshed and specify the sizing source (constant-size, geometry, or size-field), the number of radial layers of faces to be remeshed (rings), the feature angle to be preserved while remeshing the selected faces, and the size for constant size remeshing (if applicable).
                """
            class clear_skew_faces(TUIMethod):
                """
                Clears faces that were marked using the mark-skew-face command.
                """
            class select_visible_entities(TUIMethod):
                """
                Enables you to select only visible entities (nodes, edges, faces, zones, objects) when the box select or polygon select options are used. Ensure that the model is zoomed to an appropriate level for correct selection.
                """
            class swap(TUIMethod):
                """
                Swaps boundary edges (of triangular faces) if the selection list contains edges.
                """
            class undo(TUIMethod):
                """
                Undoes the previous operation. When an operation is performed, the reverse operation is stored on the undo stack. For example, a create operation places a delete on the stack, and a delete adds a create operation.   The undo operation requires that the name of the object exist when the action is undone. If the name does not exist, then the undo will fail. You can undo the last few operations, but if many operations are being performed it is recommended that you also save the mesh periodically.
                """
            class list_selections(TUIMethod):
                """
                Lists all of the selected objects.
                """
            class delta_move(TUIMethod):
                """
                Moves the selected node by specified magnitude.
                """
            class show_probe(TUIMethod):
                """
                Shows the current probe function.
                """
            class split_face(TUIMethod):
                """
                Splits two selected faces into four faces.
                """
            class select_zone(TUIMethod):
                """
                Adds a zone to the selection list by entering the zone name or ID.
                """
            class select_filter(TUIMethod):
                """
                Selects a filter. The possible filters are off, cell, face, edge, node, zone, position, object, and size. If off is chosen, then when a selection is made, it is first checked to see if it is a cell, then a face, an edge, and so on. When the node filter is used, and if a cell or face is selected, the node closest to the selection point is picked. Thus, the nodes do not have to be displayed, to be picked.
                """
            class clear_selections(TUIMethod):
                """
                Clears all selections.
                """
            class collapse(TUIMethod):
                """
                Collapses pairs of nodes, edge(s), or face(s). If a pair of nodes is selected, both the nodes are deleted and a new node is created at the midpoint of the two nodes. If a triangular face is selected, the complete face is collapsed into a single node at the centroid of the face.
                """
            class patch_options(TUIMethod):
                """
                Settings for Patching zone(s) by filling holes.
                """
            class create_mid_node(TUIMethod):
                """
                Creates a node at the midpoint between two selected nodes.
                """

        class feature(TUIMenu):
            """
            Enables you to create and modify features.
            """
            def __init__(self, service, version, mode, path):
                self.orient_edge_direction = self.__class__.orient_edge_direction(service, version, mode, path + ["orient_edge_direction"])
                self.remesh_edge_zones = self.__class__.remesh_edge_zones(service, version, mode, path + ["remesh_edge_zones"])
                self.merge_edge_zones = self.__class__.merge_edge_zones(service, version, mode, path + ["merge_edge_zones"])
                self.create_edge_zones = self.__class__.create_edge_zones(service, version, mode, path + ["create_edge_zones"])
                self.intersect_edge_zones = self.__class__.intersect_edge_zones(service, version, mode, path + ["intersect_edge_zones"])
                self.separate_delete_small_edges = self.__class__.separate_delete_small_edges(service, version, mode, path + ["separate_delete_small_edges"])
                self.project_edge_zones = self.__class__.project_edge_zones(service, version, mode, path + ["project_edge_zones"])
                self.reverse_edge_direction = self.__class__.reverse_edge_direction(service, version, mode, path + ["reverse_edge_direction"])
                self.ungroup = self.__class__.ungroup(service, version, mode, path + ["ungroup"])
                self.toggle_edge_type = self.__class__.toggle_edge_type(service, version, mode, path + ["toggle_edge_type"])
                self.separate_edge_zones_by_seed = self.__class__.separate_edge_zones_by_seed(service, version, mode, path + ["separate_edge_zones_by_seed"])
                self.list_edge_zones = self.__class__.list_edge_zones(service, version, mode, path + ["list_edge_zones"])
                self.edge_size_limits = self.__class__.edge_size_limits(service, version, mode, path + ["edge_size_limits"])
                self.separate_edge_zones = self.__class__.separate_edge_zones(service, version, mode, path + ["separate_edge_zones"])
                self.delete_degenerated_edges = self.__class__.delete_degenerated_edges(service, version, mode, path + ["delete_degenerated_edges"])
                self.delete_edge_zones = self.__class__.delete_edge_zones(service, version, mode, path + ["delete_edge_zones"])
                self.group = self.__class__.group(service, version, mode, path + ["group"])
                self.copy_edge_zones = self.__class__.copy_edge_zones(service, version, mode, path + ["copy_edge_zones"])
                super().__init__(service, version, mode, path)
            class orient_edge_direction(TUIMethod):
                """
                Orients the edges on the loop to point in the same direction.
                """
            class remesh_edge_zones(TUIMethod):
                """
                Remeshes the specified edge loop(s), modifying the node distribution according to the specified remeshing method, spacing values, and feature angle. You can also enable quadratic reconstruction, if required.
                """
            class merge_edge_zones(TUIMethod):
                """
                Merges multiple edge loops of the same type into a single loop.
                """
            class create_edge_zones(TUIMethod):
                """
                Extracts edge loops for the specified face zone(s) based on the feature method specified. You also need to specify an appropriate value for feature angle when using the fixed-angle method.   The Face Seed approach cannot be used when creating edge loops using text commands.
                """
            class intersect_edge_zones(TUIMethod):
                """
                Intersects the specified edge loops to create a new edge loop comprising the common edges. You can enable automatic deleting of overlapped edges and specify an appropriate intersection tolerance.
                """
            class separate_delete_small_edges(TUIMethod):
                """
                Separates the edge zones based on the feature angle specified, and then deletes the edges having a count smaller than the minimum count specified.
                """
            class project_edge_zones(TUIMethod):
                """
                Projects the edges of the specified loop onto the specified face zone using the specified projection method.
                """
            class reverse_edge_direction(TUIMethod):
                """
                Reverses the direction of the edge loop.
                """
            class ungroup(TUIMethod):
                """
                Ungroups previously grouped edge zones.
                """
            class toggle_edge_type(TUIMethod):
                """
                Toggles the edge type between boundary and interior.
                """
            class separate_edge_zones_by_seed(TUIMethod):
                """
                Separates the edge loop based on the seed edge specified. The edge zone separation angle is used to separate the edge zone (default 40).
                """
            class list_edge_zones(TUIMethod):
                """
                Lists the name, ID, type, and count for the specified edge zone(s).
                """
            class edge_size_limits(TUIMethod):
                """
                Reports the minimum, maximum, and average edge length for the specified edge zone(s) in the console.
                """
            class separate_edge_zones(TUIMethod):
                """
                Separates the specified edge loop based on connectivity and the specified feature angle.
                """
            class delete_degenerated_edges(TUIMethod):
                """
                Deletes degenerated edges (edges where the two end nodes are the same) for the edge zone(s) specified.
                """
            class delete_edge_zones(TUIMethod):
                """
                Deletes the specified edge zone(s).
                """
            class group(TUIMethod):
                """
                Associates the specified edge zone(s) with the specified face zone.
                """
            class copy_edge_zones(TUIMethod):
                """
                Copies the specified edge zone(s) to new edge zone(s).
                """

    class parallel(TUIMenu):
        """
        Enter the parallel menu.
        """
        def __init__(self, service, version, mode, path):
            self.agglomerate = self.__class__.agglomerate(service, version, mode, path + ["agglomerate"])
            self.auto_partition = self.__class__.auto_partition(service, version, mode, path + ["auto_partition"])
            self.spawn_solver_processes = self.__class__.spawn_solver_processes(service, version, mode, path + ["spawn_solver_processes"])
            self.thread_number_control = self.__class__.thread_number_control(service, version, mode, path + ["thread_number_control"])
            self.print_partition_info = self.__class__.print_partition_info(service, version, mode, path + ["print_partition_info"])
            super().__init__(service, version, mode, path)
        class agglomerate(TUIMethod):
            """
            Recombines distributed mesh data into a single partition on compute node 0.
            """
        class auto_partition(TUIMethod):
            """
            Automatically partitions face-zones for parallel meshing.
            """
        class spawn_solver_processes(TUIMethod):
            """
            Specifies the number of solver processes. Additional processes will be spawned as necessary when switching to solution mode in Linux with the default MPI. You will also be prompted for (Linux and mixed Windows/Linux) interconnect type, machine list or host file, and (Linux and mixed Windows/Linux) option to be used.
            """
        class thread_number_control(TUIMethod):
            """
            Controls the maximum number of threads on each machine.
            """
        class print_partition_info(TUIMethod):
            """
            Displays computed partition data to the console.
            """

    class reference_frames(TUIMenu):
        """
        Manage reference frames.
        """
        def __init__(self, service, version, mode, path):
            self.edit = self.__class__.edit(service, version, mode, path + ["edit"])
            self.list = self.__class__.list(service, version, mode, path + ["list"])
            self.display = self.__class__.display(service, version, mode, path + ["display"])
            self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
            self.hide = self.__class__.hide(service, version, mode, path + ["hide"])
            self.display_edit = self.__class__.display_edit(service, version, mode, path + ["display_edit"])
            self.add = self.__class__.add(service, version, mode, path + ["add"])
            self.list_properties = self.__class__.list_properties(service, version, mode, path + ["list_properties"])
            super().__init__(service, version, mode, path)
        class edit(TUIMethod):
            """
            Edit an object.
            """
        class list(TUIMethod):
            """
            List objects.
            """
        class display(TUIMethod):
            """
            Display Reference Frame.
            """
        class delete(TUIMethod):
            """
            Delete an object.
            """
        class hide(TUIMethod):
            """
            Hide Reference Frame.
            """
        class display_edit(TUIMethod):
            """
            Display and edit reference frame from graphics.
            """
        class add(TUIMethod):
            """
            Add a new object.
            """
        class list_properties(TUIMethod):
            """
            List properties of an object.
            """

    class cad_assemblies(TUIMenu):
        """
        Menu for cad assemblies.
        """
        def __init__(self, service, version, mode, path):
            self.manage_state = self.__class__.manage_state(service, version, mode, path + ["manage_state"])
            self.labels = self.__class__.labels(service, version, mode, path + ["labels"])
            self.update_options = self.__class__.update_options(service, version, mode, path + ["update_options"])
            self.draw_options = self.__class__.draw_options(service, version, mode, path + ["draw_options"])
            self.delete_cad_assemblies = self.__class__.delete_cad_assemblies(service, version, mode, path + ["delete_cad_assemblies"])
            self.update_cad_assemblies = self.__class__.update_cad_assemblies(service, version, mode, path + ["update_cad_assemblies"])
            self.replace_object = self.__class__.replace_object(service, version, mode, path + ["replace_object"])
            self.extract_edges_zones = self.__class__.extract_edges_zones(service, version, mode, path + ["extract_edges_zones"])
            self.add_prefix = self.__class__.add_prefix(service, version, mode, path + ["add_prefix"])
            self.rename = self.__class__.rename(service, version, mode, path + ["rename"])
            self.add_to_object = self.__class__.add_to_object(service, version, mode, path + ["add_to_object"])
            self.create_objects = self.__class__.create_objects(service, version, mode, path + ["create_objects"])
            self.draw = self.__class__.draw(service, version, mode, path + ["draw"])
            super().__init__(service, version, mode, path)
        class delete_cad_assemblies(TUIMethod):
            """
            Deletes all the CAD assemblies data.
            """
        class update_cad_assemblies(TUIMethod):
            """
            Reimports the selected CAD entities using new parameters specified in the update-options/ menu.
            """
        class replace_object(TUIMethod):
            """
            Enables you to replace an object with the selected CAD entities. Specify the path for the entities to be added and select the object to be modified.
            """
        class extract_edges_zones(TUIMethod):
            """
            Extract feature edges for CAD assemblies.
            """
        class add_prefix(TUIMethod):
            """
            Enables you to add a prefix to the selected entities. Specify the path for the entities and the prefix to be added.
            """
        class rename(TUIMethod):
            """
            Enables you to rename the selected entities. Specify the path for the entities and the new name. For multiple entities, the specified name will be used, with a suitable index as suffix. For example, specifying a new name wall will result in entities wall.1, wall.2, etc.
            """
        class add_to_object(TUIMethod):
            """
            Enables you to add the selected CAD entities to an existing object. Specify the path for the entities to be added and select the object to be modified.
            """
        class create_objects(TUIMethod):
            """
            Enables you to create new geometry/mesh objects for the selected entities. Specify the path for the entities and if required, choose to create one object per CAD entity selected and/or retain the CAD zone granularity for object creation. By default, a single object will be created for all entities selected and the CAD zone granularity will not be retained. Specify the object name (if applicable), object type (geom or mesh), and cell zone type (dead, fluid, or solid).
            """
        class draw(TUIMethod):
            """
            Displays the selected CAD entities.
            """

        class manage_state(TUIMenu):
            """
            Contains options for setting the CAD entity state.
            """
            def __init__(self, service, version, mode, path):
                self.unsuppress = self.__class__.unsuppress(service, version, mode, path + ["unsuppress"])
                self.unlock = self.__class__.unlock(service, version, mode, path + ["unlock"])
                self.suppress = self.__class__.suppress(service, version, mode, path + ["suppress"])
                super().__init__(service, version, mode, path)
            class unsuppress(TUIMethod):
                """
                Unsuppresses the selected CAD entities.
                """
            class unlock(TUIMethod):
                """
                Unlocks the selected CAD entities.
                """
            class suppress(TUIMethod):
                """
                Suppresses the selected CAD entities.
                """

        class labels(TUIMenu):
            """
            Contains options for displaying and managing labels.
            """
            def __init__(self, service, version, mode, path):
                self.remove_from_graphics = self.__class__.remove_from_graphics(service, version, mode, path + ["remove_from_graphics"])
                self.add_to_graphics = self.__class__.add_to_graphics(service, version, mode, path + ["add_to_graphics"])
                self.rename = self.__class__.rename(service, version, mode, path + ["rename"])
                self.draw = self.__class__.draw(service, version, mode, path + ["draw"])
                self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                super().__init__(service, version, mode, path)
            class remove_from_graphics(TUIMethod):
                """
                Removes the selected labels from the display in the graphics window.
                """
            class add_to_graphics(TUIMethod):
                """
                Adds the selected labels to the display in the graphics window.
                """
            class rename(TUIMethod):
                """
                Enables you to rename the selected labels. Specify the path for the labels and the new name. For multiple selections, the specified name will be used, with a suitable index as suffix. For example, specifying a new label name wall will result in entities wall.1, wall.2, etc.
                """
            class draw(TUIMethod):
                """
                Displays the selected labels.
                """
            class delete(TUIMethod):
                """
                Deletes the selected labels.
                """

        class update_options(TUIMenu):
            """
            Contains options for updating the CAD entities on reimport.
            """
            def __init__(self, service, version, mode, path):
                self.one_object_per = self.__class__.one_object_per(service, version, mode, path + ["one_object_per"])
                self.tessellation = self.__class__.tessellation(service, version, mode, path + ["tessellation"])
                self.one_zone_per = self.__class__.one_zone_per(service, version, mode, path + ["one_zone_per"])
                self.import_edge_zones = self.__class__.import_edge_zones(service, version, mode, path + ["import_edge_zones"])
                super().__init__(service, version, mode, path)
            class one_object_per(TUIMethod):
                """
                Enables you to change the CAD object granularity on reimport.
                """
            class tessellation(TUIMethod):
                """
                Enables you to control the tessellation (faceting) during reimport. You can select either cad-faceting or cfd-surface-mesh.   CAD faceting enables you to control the tessellation based on the CAD faceting tolerance and maximum facet size specified.   CFD Surface Mesh enables you to use a size field file during reimport. If you enter yes, specify the size field file to be read. If you do not want to use a size field file, you can obtain conformal faceting based on the underlying curve and surface curvature (using the minimum and maximum facet sizes, and the facet curvature normal angle specified) and edge proximity (using the cells per gap specified). You can also save the size field in a file (size field is computed based on the specified parameters; that is, Min Size, Max Size, Curvature Normal Angle, Cells Per Gap).
                """
            class one_zone_per(TUIMethod):
                """
                Enables you to change the CAD zone granularity on reimport.
                """
            class import_edge_zones(TUIMethod):
                """
                Enables you to import edge zones from the CAD entities on reimport. Specify an appropriate value for feature angle.
                """

        class draw_options(TUIMenu):
            """
            Contains additional options for displaying CAD entities.
            """
            def __init__(self, service, version, mode, path):
                self.draw_unlabelled_zones = self.__class__.draw_unlabelled_zones(service, version, mode, path + ["draw_unlabelled_zones"])
                self.add_to_graphics = self.__class__.add_to_graphics(service, version, mode, path + ["add_to_graphics"])
                self.remove_from_graphics = self.__class__.remove_from_graphics(service, version, mode, path + ["remove_from_graphics"])
                super().__init__(service, version, mode, path)
            class draw_unlabelled_zones(TUIMethod):
                """
                Displays the unlabeled zones for the selected entities in the graphics window.
                """
            class add_to_graphics(TUIMethod):
                """
                Adds the selected entities to the display in the graphics window.
                """
            class remove_from_graphics(TUIMethod):
                """
                Removes the selected entities from the display in the graphics window.
                """

    class display(TUIMenu):
        """
        Enter the display menu.
        """
        def __init__(self, service, version, mode, path):
            self.update_scene = self.__class__.update_scene(service, version, mode, path + ["update_scene"])
            self.set_grid = self.__class__.set_grid(service, version, mode, path + ["set_grid"])
            self.set = self.__class__.set(service, version, mode, path + ["set"])
            self.zones = self.__class__.zones(service, version, mode, path + ["zones"])
            self.objects = self.__class__.objects(service, version, mode, path + ["objects"])
            self.advanced_rendering = self.__class__.advanced_rendering(service, version, mode, path + ["advanced_rendering"])
            self.display_states = self.__class__.display_states(service, version, mode, path + ["display_states"])
            self.xy_plot = self.__class__.xy_plot(service, version, mode, path + ["xy_plot"])
            self.annotate = self.__class__.annotate(service, version, mode, path + ["annotate"])
            self.views = self.__class__.views(service, version, mode, path + ["views"])
            self.set_list_tree_separator = self.__class__.set_list_tree_separator(service, version, mode, path + ["set_list_tree_separator"])
            self.draw_zones = self.__class__.draw_zones(service, version, mode, path + ["draw_zones"])
            self.update_layout = self.__class__.update_layout(service, version, mode, path + ["update_layout"])
            self.all_grid = self.__class__.all_grid(service, version, mode, path + ["all_grid"])
            self.boundary_grid = self.__class__.boundary_grid(service, version, mode, path + ["boundary_grid"])
            self.clear = self.__class__.clear(service, version, mode, path + ["clear"])
            self.draw_face_zones_using_entities = self.__class__.draw_face_zones_using_entities(service, version, mode, path + ["draw_face_zones_using_entities"])
            self.center_view_on = self.__class__.center_view_on(service, version, mode, path + ["center_view_on"])
            self.boundary_cells = self.__class__.boundary_cells(service, version, mode, path + ["boundary_cells"])
            self.draw_cells_using_faces = self.__class__.draw_cells_using_faces(service, version, mode, path + ["draw_cells_using_faces"])
            self.redisplay = self.__class__.redisplay(service, version, mode, path + ["redisplay"])
            self.show_hide_clipping_plane_triad = self.__class__.show_hide_clipping_plane_triad(service, version, mode, path + ["show_hide_clipping_plane_triad"])
            self.clear_annotation = self.__class__.clear_annotation(service, version, mode, path + ["clear_annotation"])
            self.save_picture = self.__class__.save_picture(service, version, mode, path + ["save_picture"])
            self.draw_cells_using_nodes = self.__class__.draw_cells_using_nodes(service, version, mode, path + ["draw_cells_using_nodes"])
            super().__init__(service, version, mode, path)
        class annotate(TUIMethod):
            """
            Adds annotation text to a graphics window. It will prompt you for a string to use as the annotation text, and then a dialog box will prompt you to select a screen location using the mouse-probe button on your mouse.
            """
        class views(TUIMethod):
            """
            Enters the view window options menu.
            """
        class set_list_tree_separator(TUIMethod):
            """
            Sets the separator character to be used to determine the common prefix for items listed in the selection lists, when the tree view is used.
            """
        class draw_zones(TUIMethod):
            """
            Draws the boundary/cell zones using the zone ID specified as input.
            """
        class update_layout(TUIMethod):
            """
            Update the fluent layout.
            """
        class all_grid(TUIMethod):
            """
            Displays the grid according to the currently set parameters.
            """
        class boundary_grid(TUIMethod):
            """
            Displays only boundary zones according to the currently set parameters.
            """
        class clear(TUIMethod):
            """
            Clears the active graphics window. This option is useful when you redo an overlay.
            """
        class draw_face_zones_using_entities(TUIMethod):
            """
            Draws cells that are connected to the selected entities.
            """
        class center_view_on(TUIMethod):
            """
            Sets the camera target to be the center (centroid) of an entity.
            """
        class boundary_cells(TUIMethod):
            """
            Displays boundary cells attached to the specified face zones.
            """
        class draw_cells_using_faces(TUIMethod):
            """
            Draws cells that are neighbors for the selected faces.
            """
        class redisplay(TUIMethod):
            """
            Redraws the grid in the graphics window.
            """
        class show_hide_clipping_plane_triad(TUIMethod):
            """
            S.
            """
        class clear_annotation(TUIMethod):
            """
            Removes all annotations and attachment lines from the active graphics window.
            """
        class save_picture(TUIMethod):
            """
            Saves a picture file of the active graphics window.
            """
        class draw_cells_using_nodes(TUIMethod):
            """
            Draws cells that are connected to the selected nodes.
            """

        class update_scene(TUIMenu):
            """
            Contains commands that enable you to update the scene description.
            """
            def __init__(self, service, version, mode, path):
                self.set_frame = self.__class__.set_frame(service, version, mode, path + ["set_frame"])
                self.time = self.__class__.time(service, version, mode, path + ["time"])
                self.select_geometry = self.__class__.select_geometry(service, version, mode, path + ["select_geometry"])
                self.draw_frame = self.__class__.draw_frame(service, version, mode, path + ["draw_frame"])
                self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                self.iso_sweep = self.__class__.iso_sweep(service, version, mode, path + ["iso_sweep"])
                self.overlays = self.__class__.overlays(service, version, mode, path + ["overlays"])
                self.display = self.__class__.display(service, version, mode, path + ["display"])
                self.transform = self.__class__.transform(service, version, mode, path + ["transform"])
                self.pathline = self.__class__.pathline(service, version, mode, path + ["pathline"])
                super().__init__(service, version, mode, path)
            class set_frame(TUIMethod):
                """
                Enables you to change the frame options.
                """
            class time(TUIMethod):
                """
                Changes time-step value.
                """
            class select_geometry(TUIMethod):
                """
                Enables you to select the geometry to be updated.
                """
            class draw_frame(TUIMethod):
                """
                Enables/disables the drawing of the bounding frame.
                """
            class delete(TUIMethod):
                """
                Deletes the geometry selected using the select-geometry command.
                """
            class iso_sweep(TUIMethod):
                """
                Changes iso-sweep values.
                """
            class overlays(TUIMethod):
                """
                Enables/disables the overlays option.
                """
            class display(TUIMethod):
                """
                Displays the geometry selected using the select-geometry command.
                """
            class transform(TUIMethod):
                """
                Enables you to apply the transformation matrix to the geometry selected using the select-geometry command.
                """
            class pathline(TUIMethod):
                """
                Changes pathline attributes.
                """

        class set_grid(TUIMenu):
            """
            Contains options controlling the display of the grid.
            """
            def __init__(self, service, version, mode, path):
                self.unused = self.__class__.unused(service, version, mode, path + ["unused"])
                self.all_cells = self.__class__.all_cells(service, version, mode, path + ["all_cells"])
                self.refine = self.__class__.refine(service, version, mode, path + ["refine"])
                self.normals = self.__class__.normals(service, version, mode, path + ["normals"])
                self.node_size = self.__class__.node_size(service, version, mode, path + ["node_size"])
                self.normal_scale = self.__class__.normal_scale(service, version, mode, path + ["normal_scale"])
                self.marked = self.__class__.marked(service, version, mode, path + ["marked"])
                self.z_range = self.__class__.z_range(service, version, mode, path + ["z_range"])
                self.neighborhood = self.__class__.neighborhood(service, version, mode, path + ["neighborhood"])
                self.left_handed = self.__class__.left_handed(service, version, mode, path + ["left_handed"])
                self.face_quality = self.__class__.face_quality(service, version, mode, path + ["face_quality"])
                self.x_range = self.__class__.x_range(service, version, mode, path + ["x_range"])
                self.default = self.__class__.default(service, version, mode, path + ["default"])
                self.list = self.__class__.list(service, version, mode, path + ["list"])
                self.y_range = self.__class__.y_range(service, version, mode, path + ["y_range"])
                self.all_nodes = self.__class__.all_nodes(service, version, mode, path + ["all_nodes"])
                self.label_font = self.__class__.label_font(service, version, mode, path + ["label_font"])
                self.label_alignment = self.__class__.label_alignment(service, version, mode, path + ["label_alignment"])
                self.free = self.__class__.free(service, version, mode, path + ["free"])
                self.label_scale = self.__class__.label_scale(service, version, mode, path + ["label_scale"])
                self.all_faces = self.__class__.all_faces(service, version, mode, path + ["all_faces"])
                self.node_symbol = self.__class__.node_symbol(service, version, mode, path + ["node_symbol"])
                self.labels = self.__class__.labels(service, version, mode, path + ["labels"])
                self.unmeshed = self.__class__.unmeshed(service, version, mode, path + ["unmeshed"])
                self.cell_quality = self.__class__.cell_quality(service, version, mode, path + ["cell_quality"])
                self.multi = self.__class__.multi(service, version, mode, path + ["multi"])
                self.tagged = self.__class__.tagged(service, version, mode, path + ["tagged"])
                super().__init__(service, version, mode, path)
            class unused(TUIMethod):
                """
                Enables/disables the display of unused nodes.
                """
            class all_cells(TUIMethod):
                """
                Enables/disables the display of all cells.
                """
            class refine(TUIMethod):
                """
                Enables/disables the display of those faces that have been marked for refinement.
                """
            class normals(TUIMethod):
                """
                Enables/disables the display of face normals.
                """
            class node_size(TUIMethod):
                """
                Sets the node symbol scaling factor.
                """
            class normal_scale(TUIMethod):
                """
                Sets the scale factor for face normals.
                """
            class marked(TUIMethod):
                """
                Enables/disables the display of marked nodes.
                """
            class z_range(TUIMethod):
                """
                Limits the display of grid objects to the specified z-range.
                """
            class neighborhood(TUIMethod):
                """
                Sets the x, y, and z range to be within a specified neighborhood of a specified grid object.
                """
            class left_handed(TUIMethod):
                """
                Enables/disables the display of left-handed faces.
                """
            class face_quality(TUIMethod):
                """
                Sets the lower and upper bounds of quality for faces to be displayed. Only faces with a quality measure value (for example, skewness) within the specified range will be displayed.
                """
            class x_range(TUIMethod):
                """
                Limits the display of grid objects to the specified x-range.
                """
            class default(TUIMethod):
                """
                Resets the grid display parameters to their default values.
                """
            class list(TUIMethod):
                """
                Lists all the grid display settings.
                """
            class y_range(TUIMethod):
                """
                Limits the display of grid objects to the specified y-range.
                """
            class all_nodes(TUIMethod):
                """
                Enables/disables the display of all nodes.
                """
            class label_font(TUIMethod):
                """
                Sets the label font. By default, all labels appear in “sans serif" font. Some other choices are roman, typewriter, and stroked.
                """
            class label_alignment(TUIMethod):
                """
                Sets the alignment of labels that appear in the graphics window. By default, the label is centered on the node, cell, and so on, to which the label refers. You can specify \\*,ˆ, v, <, > for center, top, bottom, left, or right. You can also combine symbols—for example, "\\*v" for bottom center.
                """
            class free(TUIMethod):
                """
                Enables/disables the drawing of faces/nodes that have no neighboring face on at least one edge.
                """
            class label_scale(TUIMethod):
                """
                Scales the size of the label.
                """
            class all_faces(TUIMethod):
                """
                Enables/disables the display of all faces.
                """
            class node_symbol(TUIMethod):
                """
                Specifies the node symbol.
                """
            class labels(TUIMethod):
                """
                Enables/disables the display of labels.
                """
            class unmeshed(TUIMethod):
                """
                Enables/disables the display of nodes and faces that have not been meshed.
                """
            class cell_quality(TUIMethod):
                """
                Sets the lower and upper bounds of quality for cells to be displayed. Only cells with a quality measure value (for example, skewness) within the specified range will be displayed.
                """
            class multi(TUIMethod):
                """
                Enables/disables the display of those faces/nodes that have more than one neighboring face on an edge.
                """
            class tagged(TUIMethod):
                """
                Enables/disables the display of tagged nodes.
                """

        class set(TUIMenu):
            """
            Enables you to enter the set menu to set the display parameters.
            """
            def __init__(self, service, version, mode, path):
                self.styles = self.__class__.styles(service, version, mode, path + ["styles"])
                self.colors = self.__class__.colors(service, version, mode, path + ["colors"])
                self.rendering_options = self.__class__.rendering_options(service, version, mode, path + ["rendering_options"])
                self.lights = self.__class__.lights(service, version, mode, path + ["lights"])
                self.picture = self.__class__.picture(service, version, mode, path + ["picture"])
                self.overlays = self.__class__.overlays(service, version, mode, path + ["overlays"])
                self.reset_graphics = self.__class__.reset_graphics(service, version, mode, path + ["reset_graphics"])
                self.re_render = self.__class__.re_render(service, version, mode, path + ["re_render"])
                self.quick_moves_algorithm = self.__class__.quick_moves_algorithm(service, version, mode, path + ["quick_moves_algorithm"])
                self.line_weight = self.__class__.line_weight(service, version, mode, path + ["line_weight"])
                self.remote_display_defaults = self.__class__.remote_display_defaults(service, version, mode, path + ["remote_display_defaults"])
                self.highlight_tree_selection = self.__class__.highlight_tree_selection(service, version, mode, path + ["highlight_tree_selection"])
                self.windows = self.__class__.windows(service, version, mode, path + ["windows"])
                self.filled_grid = self.__class__.filled_grid(service, version, mode, path + ["filled_grid"])
                self.edges = self.__class__.edges(service, version, mode, path + ["edges"])
                self.shrink_factor = self.__class__.shrink_factor(service, version, mode, path + ["shrink_factor"])
                self.native_display_defaults = self.__class__.native_display_defaults(service, version, mode, path + ["native_display_defaults"])
                self.title = self.__class__.title(service, version, mode, path + ["title"])
                super().__init__(service, version, mode, path)
            class overlays(TUIMethod):
                """
                Turns overlays on and off.
                """
            class reset_graphics(TUIMethod):
                """
                Resets the graphics system.
                """
            class re_render(TUIMethod):
                """
                Re-renders the current window after modifying the variables in the set menu.
                """
            class quick_moves_algorithm(TUIMethod):
                """
                Select quick moves algorithm for icons and helptext overlay.
                """
            class line_weight(TUIMethod):
                """
                Sets the line width factor for the window.
                """
            class remote_display_defaults(TUIMethod):
                """
                Adjusts graphics window parameters to optimal settings for a remote display.   Restore parameters for local display using native-display-defaults.
                """
            class highlight_tree_selection(TUIMethod):
                """
                Turn on/off outline display of tree selection in graphics window.
                """
            class windows(TUIMethod):
                """
                Enters the windows options menu, which contains commands that enable you to customize the relative positions of sub-windows inside the active graphics window.
                """
            class filled_grid(TUIMethod):
                """
                Enables/disables the filled grid option. When a grid is not filled, only its outline is drawn.
                """
            class edges(TUIMethod):
                """
                Enables/disables the display of face/cell edges.
                """
            class shrink_factor(TUIMethod):
                """
                Sets shrinkage of both faces and cells. A value of zero indicates no shrinkage, while a value of one would shrink the face or cell to a point.
                """
            class native_display_defaults(TUIMethod):
                """
                Resets graphics window parameters to optimal settings for a local display.   Used after setting parameters for a remote display with remote-display-defaults.
                """
            class title(TUIMethod):
                """
                Sets the problem title.
                """

            class styles(TUIMenu):
                """
                Contains commands for setting the display style for the different types of nodes and faces that can be displayed.
                """
                def __init__(self, service, version, mode, path):
                    self.dummy = self.__class__.dummy(service, version, mode, path + ["dummy"])
                    super().__init__(service, version, mode, path)
                class dummy(TUIMethod):
                    """
                    .
                    """

            class colors(TUIMenu):
                """
                Enables you to enter the colors options menu.
                """
                def __init__(self, service, version, mode, path):
                    self.by_type = self.__class__.by_type(service, version, mode, path + ["by_type"])
                    self.by_surface = self.__class__.by_surface(service, version, mode, path + ["by_surface"])
                    self.periodic_faces = self.__class__.periodic_faces(service, version, mode, path + ["periodic_faces"])
                    self.wall_faces = self.__class__.wall_faces(service, version, mode, path + ["wall_faces"])
                    self.grid_interior = self.__class__.grid_interior(service, version, mode, path + ["grid_interior"])
                    self.color_by_type = self.__class__.color_by_type(service, version, mode, path + ["color_by_type"])
                    self.axis_faces = self.__class__.axis_faces(service, version, mode, path + ["axis_faces"])
                    self.grid_inlet = self.__class__.grid_inlet(service, version, mode, path + ["grid_inlet"])
                    self.interior_faces = self.__class__.interior_faces(service, version, mode, path + ["interior_faces"])
                    self.outlet_faces = self.__class__.outlet_faces(service, version, mode, path + ["outlet_faces"])
                    self.show_user_colors = self.__class__.show_user_colors(service, version, mode, path + ["show_user_colors"])
                    self.background = self.__class__.background(service, version, mode, path + ["background"])
                    self.highlight_color = self.__class__.highlight_color(service, version, mode, path + ["highlight_color"])
                    self.surface = self.__class__.surface(service, version, mode, path + ["surface"])
                    self.foreground = self.__class__.foreground(service, version, mode, path + ["foreground"])
                    self.automatic_skip = self.__class__.automatic_skip(service, version, mode, path + ["automatic_skip"])
                    self.user_color = self.__class__.user_color(service, version, mode, path + ["user_color"])
                    self.free_surface_faces = self.__class__.free_surface_faces(service, version, mode, path + ["free_surface_faces"])
                    self.interface_faces = self.__class__.interface_faces(service, version, mode, path + ["interface_faces"])
                    self.graphics_color_theme = self.__class__.graphics_color_theme(service, version, mode, path + ["graphics_color_theme"])
                    self.internal_faces = self.__class__.internal_faces(service, version, mode, path + ["internal_faces"])
                    self.list = self.__class__.list(service, version, mode, path + ["list"])
                    self.traction_faces = self.__class__.traction_faces(service, version, mode, path + ["traction_faces"])
                    self.overset_faces = self.__class__.overset_faces(service, version, mode, path + ["overset_faces"])
                    self.reset_colors = self.__class__.reset_colors(service, version, mode, path + ["reset_colors"])
                    self.far_field_faces = self.__class__.far_field_faces(service, version, mode, path + ["far_field_faces"])
                    self.reset_user_colors = self.__class__.reset_user_colors(service, version, mode, path + ["reset_user_colors"])
                    self.inlet_faces = self.__class__.inlet_faces(service, version, mode, path + ["inlet_faces"])
                    self.skip_label = self.__class__.skip_label(service, version, mode, path + ["skip_label"])
                    self.symmetry_faces = self.__class__.symmetry_faces(service, version, mode, path + ["symmetry_faces"])
                    self.rans_les_interface_faces = self.__class__.rans_les_interface_faces(service, version, mode, path + ["rans_les_interface_faces"])
                    super().__init__(service, version, mode, path)
                class periodic_faces(TUIMethod):
                    """
                    Sets the color of periodic faces.
                    """
                class wall_faces(TUIMethod):
                    """
                    Sets color for wall faces.
                    """
                class grid_interior(TUIMethod):
                    """
                    Set the color of interior faces.
                    """
                class color_by_type(TUIMethod):
                    """
                    Enables you to specify that the entities should be colored by their type or ID.
                    """
                class axis_faces(TUIMethod):
                    """
                    Sets the color of axisymmetric faces.
                    """
                class grid_inlet(TUIMethod):
                    """
                    Set the color of inlet faces.
                    """
                class interior_faces(TUIMethod):
                    """
                    Sets the color of the interior faces.
                    """
                class outlet_faces(TUIMethod):
                    """
                    Sets the color of the outlet faces.
                    """
                class show_user_colors(TUIMethod):
                    """
                    Lists the current defined user colors.
                    """
                class background(TUIMethod):
                    """
                    Sets the background (window) color.
                    """
                class highlight_color(TUIMethod):
                    """
                    Sets the highlight color.
                    """
                class surface(TUIMethod):
                    """
                    Sets the color of surfaces.
                    """
                class foreground(TUIMethod):
                    """
                    Sets the foreground (text and window frame) color.
                    """
                class automatic_skip(TUIMethod):
                    """
                    Specify whether the number of colormap labels is determined automatically. The default is yes.
                    """
                class user_color(TUIMethod):
                    """
                    Enables you to change the color for the specified zone.
                    """
                class free_surface_faces(TUIMethod):
                    """
                    Sets the color of free surface faces.
                    """
                class interface_faces(TUIMethod):
                    """
                    Sets the color of grid interface faces.
                    """
                class graphics_color_theme(TUIMethod):
                    """
                    Sets the color theme for the graphics window. The color options (black, white, gray-gradient, or workbench) are for the background display, but changing the theme also changes the default colors for items that display in the graphics windows, like faces and edges.
                    """
                class internal_faces(TUIMethod):
                    """
                    Sets the color of the internal interface faces.
                    """
                class list(TUIMethod):
                    """
                    Lists the colors available for the selected zone type.
                    """
                class traction_faces(TUIMethod):
                    """
                    Sets the color for traction faces.
                    """
                class overset_faces(TUIMethod):
                    """
                    Sets the color of the overset faces.
                    """
                class reset_colors(TUIMethod):
                    """
                    Resets the individual grid surface colors to the defaults.
                    """
                class far_field_faces(TUIMethod):
                    """
                    Sets the color of far field faces.
                    """
                class reset_user_colors(TUIMethod):
                    """
                    Resets individual grid surface colors to the defaults.
                    """
                class inlet_faces(TUIMethod):
                    """
                    Sets the color of the inlet faces.
                    """
                class skip_label(TUIMethod):
                    """
                    Sets the number of labels to be skipped in the colormap scale.
                    """
                class symmetry_faces(TUIMethod):
                    """
                    Sets the color of symmetric faces.
                    """
                class rans_les_interface_faces(TUIMethod):
                    """
                    Sets the color of RANS/LES interface faces.
                    """

                class by_type(TUIMenu):
                    """
                    Enter the zone type color and material assignment menu.
                    """
                    def __init__(self, service, version, mode, path):
                        self.type_name = self.__class__.type_name(service, version, mode, path + ["type_name"])
                        self.use_inherent_material_color = self.__class__.use_inherent_material_color(service, version, mode, path + ["use_inherent_material_color"])
                        self.reset = self.__class__.reset(service, version, mode, path + ["reset"])
                        self.only_list_case_boundaries = self.__class__.only_list_case_boundaries(service, version, mode, path + ["only_list_case_boundaries"])
                        super().__init__(service, version, mode, path)
                    class use_inherent_material_color(TUIMethod):
                        """
                        Use inherent material color for boundary zones.
                        """
                    class reset(TUIMethod):
                        """
                        To reset colors and/or materials to the defaults.
                        """
                    class only_list_case_boundaries(TUIMethod):
                        """
                        Only list the boundary types that are assigned in this case.
                        """

                    class type_name(TUIMenu):
                        """
                        Select the boundary type to specify colors and/or materials.
                        """
                        def __init__(self, service, version, mode, path):
                            self.free_surface = self.__class__.free_surface(service, version, mode, path + ["free_surface"])
                            self.far_field = self.__class__.far_field(service, version, mode, path + ["far_field"])
                            self.interface = self.__class__.interface(service, version, mode, path + ["interface"])
                            self.overset = self.__class__.overset(service, version, mode, path + ["overset"])
                            self.wall = self.__class__.wall(service, version, mode, path + ["wall"])
                            self.interior = self.__class__.interior(service, version, mode, path + ["interior"])
                            self.traction = self.__class__.traction(service, version, mode, path + ["traction"])
                            self.rans_les_interface = self.__class__.rans_les_interface(service, version, mode, path + ["rans_les_interface"])
                            self.surface = self.__class__.surface(service, version, mode, path + ["surface"])
                            self.periodic = self.__class__.periodic(service, version, mode, path + ["periodic"])
                            self.outlet = self.__class__.outlet(service, version, mode, path + ["outlet"])
                            self.inlet = self.__class__.inlet(service, version, mode, path + ["inlet"])
                            self.internal = self.__class__.internal(service, version, mode, path + ["internal"])
                            self.axis = self.__class__.axis(service, version, mode, path + ["axis"])
                            self.symmetry = self.__class__.symmetry(service, version, mode, path + ["symmetry"])
                            super().__init__(service, version, mode, path)

                        class free_surface(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                super().__init__(service, version, mode, path)
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """

                        class far_field(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                super().__init__(service, version, mode, path)
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """

                        class interface(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                super().__init__(service, version, mode, path)
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """

                        class overset(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                super().__init__(service, version, mode, path)
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """

                        class wall(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                super().__init__(service, version, mode, path)
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """

                        class interior(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                super().__init__(service, version, mode, path)
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """

                        class traction(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                super().__init__(service, version, mode, path)
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """

                        class rans_les_interface(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                super().__init__(service, version, mode, path)
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """

                        class surface(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                super().__init__(service, version, mode, path)
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """

                        class periodic(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                super().__init__(service, version, mode, path)
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """

                        class outlet(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                super().__init__(service, version, mode, path)
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """

                        class inlet(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                super().__init__(service, version, mode, path)
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """

                        class internal(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                super().__init__(service, version, mode, path)
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """

                        class axis(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                super().__init__(service, version, mode, path)
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """

                        class symmetry(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                super().__init__(service, version, mode, path)
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """

                class by_surface(TUIMenu):
                    """
                    Enter the surface(s) color and material assignment menu.
                    """
                    def __init__(self, service, version, mode, path):
                        self.use_inherent_material_color = self.__class__.use_inherent_material_color(service, version, mode, path + ["use_inherent_material_color"])
                        self.list_surfaces_by_material = self.__class__.list_surfaces_by_material(service, version, mode, path + ["list_surfaces_by_material"])
                        self.surfaces = self.__class__.surfaces(service, version, mode, path + ["surfaces"])
                        self.list_surfaces_by_color = self.__class__.list_surfaces_by_color(service, version, mode, path + ["list_surfaces_by_color"])
                        self.reset = self.__class__.reset(service, version, mode, path + ["reset"])
                        super().__init__(service, version, mode, path)
                    class use_inherent_material_color(TUIMethod):
                        """
                        Use inherent material color for surfaces.
                        """
                    class list_surfaces_by_material(TUIMethod):
                        """
                        To list the surfaces by its material.
                        """
                    class surfaces(TUIMethod):
                        """
                        Select the surface(s) to specify colors and/or materials.
                        """
                    class list_surfaces_by_color(TUIMethod):
                        """
                        To list the surfaces by its color.
                        """
                    class reset(TUIMethod):
                        """
                        To reset colors and/or materials to the defaults.
                        """

            class rendering_options(TUIMenu):
                """
                Contains the commands that enable you to set options that determine how the scene is rendered.
                """
                def __init__(self, service, version, mode, path):
                    self.help_text_color = self.__class__.help_text_color(service, version, mode, path + ["help_text_color"])
                    self.hidden_surfaces = self.__class__.hidden_surfaces(service, version, mode, path + ["hidden_surfaces"])
                    self.device_info = self.__class__.device_info(service, version, mode, path + ["device_info"])
                    self.surface_edge_visibility = self.__class__.surface_edge_visibility(service, version, mode, path + ["surface_edge_visibility"])
                    self.hidden_surface_method = self.__class__.hidden_surface_method(service, version, mode, path + ["hidden_surface_method"])
                    self.hidden_line_method = self.__class__.hidden_line_method(service, version, mode, path + ["hidden_line_method"])
                    self.driver = self.__class__.driver(service, version, mode, path + ["driver"])
                    self.auto_spin = self.__class__.auto_spin(service, version, mode, path + ["auto_spin"])
                    self.color_map_alignment = self.__class__.color_map_alignment(service, version, mode, path + ["color_map_alignment"])
                    self.hidden_lines = self.__class__.hidden_lines(service, version, mode, path + ["hidden_lines"])
                    self.double_buffering = self.__class__.double_buffering(service, version, mode, path + ["double_buffering"])
                    self.front_faces_transparent = self.__class__.front_faces_transparent(service, version, mode, path + ["front_faces_transparent"])
                    self.show_colormap = self.__class__.show_colormap(service, version, mode, path + ["show_colormap"])
                    self.set_rendering_options = self.__class__.set_rendering_options(service, version, mode, path + ["set_rendering_options"])
                    self.face_displacement = self.__class__.face_displacement(service, version, mode, path + ["face_displacement"])
                    self.animation_option = self.__class__.animation_option(service, version, mode, path + ["animation_option"])
                    super().__init__(service, version, mode, path)
                class help_text_color(TUIMethod):
                    """
                    Sets the color of the help text on the screen. You can select black, default, or white.
                    """
                class hidden_surfaces(TUIMethod):
                    """
                    Enables/disables the display of hidden surfaces.
                    """
                class device_info(TUIMethod):
                    """
                    Prints out information about your graphics driver.
                    """
                class surface_edge_visibility(TUIMethod):
                    """
                    Controls whether or not the mesh edges are drawn.
                    """
                class hidden_surface_method(TUIMethod):
                    """
                    Enables you to choose from among the hidden surface removal methods that are supported. These options (listed below) are display hardware dependent.
                    """
                class hidden_line_method(TUIMethod):
                    """
                    Specifies the method to perform hidden line rendering. This command will appear only when hidden-lines? is true.
                    """
                class driver(TUIMethod):
                    """
                    Changes the current graphics driver. When enabling graphics display, you have various options: for Linux, the available drivers include opengl and x11; for Windows, the available drivers include opengl, dx11 (for DirectX 11), and msw (for Microsoft Windows). You can also disable the graphics display window by entering null. For a comprehensive list of the drivers available to you, press the Enter key at the driver> prompt.  For any session that displays graphics in a graphics window and/or saves picture files, having the driver set to x11, msw, or null will cause the rendering / saving speed to be significantly slower.
                    """
                class auto_spin(TUIMethod):
                    """
                    Enables mouse view rotations to continue to spin the display after the button is released.
                    """
                class color_map_alignment(TUIMethod):
                    """
                    Sets the color bar alignment.
                    """
                class hidden_lines(TUIMethod):
                    """
                    Turns hidden line removal on or off. This command is available only when the color scheme is set to classic.  This command (only available when Graphics Color Theme is set to Black) is deprecated and will be removed at a future release.
                    """
                class double_buffering(TUIMethod):
                    """
                    Enables or disables double buffering. Double buffering dramatically reduces screen flicker during graphics updates. If your display hardware does not support double buffering and you turn this option on, double buffering will be done in software. Software double buffering uses extra memory.
                    """
                class front_faces_transparent(TUIMethod):
                    """
                    Make the front faces transparent.
                    """
                class show_colormap(TUIMethod):
                    """
                    Enable/Disable colormap.
                    """
                class set_rendering_options(TUIMethod):
                    """
                    Sets the rendering options.
                    """
                class face_displacement(TUIMethod):
                    """
                    Sets the face displacement (in Z-buffer units along the camera Z-axis) for the displayed geometry when both faces and edges are displayed simultaneously.
                    """
                class animation_option(TUIMethod):
                    """
                    Enables you to specify the animation option as appropriate.
                    """

            class lights(TUIMenu):
                """
                Enters the lights menu.
                """
                def __init__(self, service, version, mode, path):
                    self.headlight_on = self.__class__.headlight_on(service, version, mode, path + ["headlight_on"])
                    self.lights_on = self.__class__.lights_on(service, version, mode, path + ["lights_on"])
                    self.lighting_interpolation = self.__class__.lighting_interpolation(service, version, mode, path + ["lighting_interpolation"])
                    self.set_ambient_color = self.__class__.set_ambient_color(service, version, mode, path + ["set_ambient_color"])
                    self.set_light = self.__class__.set_light(service, version, mode, path + ["set_light"])
                    super().__init__(service, version, mode, path)
                class headlight_on(TUIMethod):
                    """
                    Turns the light that moves with the camera on or off. This is controlled automatically by default.
                    """
                class lights_on(TUIMethod):
                    """
                    Enables/disables the display of all lights.
                    """
                class lighting_interpolation(TUIMethod):
                    """
                    Sets the lighting interpolation method to be used. You can choose automatic, flat, gouraud, or phong. "Automatic" automatically picks the best lighting method for the display in the graphics window. Flat is the most basic method, and the others are more sophisticated and provide smoother gradations of color.
                    """
                class set_ambient_color(TUIMethod):
                    """
                    Sets the ambient color for the scene. The ambient color is the background light color in scene.
                    """
                class set_light(TUIMethod):
                    """
                    Adds or modifies a directional, colored light.
                    """

            class picture(TUIMenu):
                """
                Saves a hardcopy file of the active graphics window.
                """
                def __init__(self, service, version, mode, path):
                    self.driver = self.__class__.driver(service, version, mode, path + ["driver"])
                    self.color_mode = self.__class__.color_mode(service, version, mode, path + ["color_mode"])
                    self.dpi = self.__class__.dpi(service, version, mode, path + ["dpi"])
                    self.raytracer_image = self.__class__.raytracer_image(service, version, mode, path + ["raytracer_image"])
                    self.x_resolution = self.__class__.x_resolution(service, version, mode, path + ["x_resolution"])
                    self.preview = self.__class__.preview(service, version, mode, path + ["preview"])
                    self.set_standard_resolution = self.__class__.set_standard_resolution(service, version, mode, path + ["set_standard_resolution"])
                    self.jpeg_hardcopy_quality = self.__class__.jpeg_hardcopy_quality(service, version, mode, path + ["jpeg_hardcopy_quality"])
                    self.y_resolution = self.__class__.y_resolution(service, version, mode, path + ["y_resolution"])
                    self.invert_background = self.__class__.invert_background(service, version, mode, path + ["invert_background"])
                    self.landscape = self.__class__.landscape(service, version, mode, path + ["landscape"])
                    self.use_window_resolution = self.__class__.use_window_resolution(service, version, mode, path + ["use_window_resolution"])
                    super().__init__(service, version, mode, path)
                class dpi(TUIMethod):
                    """
                    Specifies the resolution in dots per inch for EPS and PostScript files.
                    """
                class raytracer_image(TUIMethod):
                    """
                    Enable raytracering rendering.
                    """
                class x_resolution(TUIMethod):
                    """
                    Sets the width of the raster format images in pixels (0 implies that the hardcopy should use the same resolution as the active graphics window).
                    """
                class preview(TUIMethod):
                    """
                    Applies the settings of the color-mode, invert-background, and landscape options to the currently active graphics window to preview the appearance of printed hardcopies.
                    """
                class set_standard_resolution(TUIMethod):
                    """
                    Select from pre-defined resolution list.
                    """
                class jpeg_hardcopy_quality(TUIMethod):
                    """
                    Controls the size and quality of how JPEG files are saved based on a scale of 0-100, with zero being low quality small files and 100 being high quality larger files.
                    """
                class y_resolution(TUIMethod):
                    """
                    Sets the height of the raster format images in pixels (0 implies that the hardcopy should use the same resolution as the active graphics window).
                    """
                class invert_background(TUIMethod):
                    """
                    Enables/disables the exchange of foreground/background colors for hardcopy files.
                    """
                class landscape(TUIMethod):
                    """
                    Toggles between landscape or portrait orientation.
                    """
                class use_window_resolution(TUIMethod):
                    """
                    Disables/enables the use of the current graphics window resolution when saving an image of the graphics window. If disabled, the resolution will be as specified for x-resolution and y-resolution.
                    """

                class driver(TUIMenu):
                    """
                    Contains the available hardcopy formats.
                    """
                    def __init__(self, service, version, mode, path):
                        self.post_format = self.__class__.post_format(service, version, mode, path + ["post_format"])
                        self.ppm = self.__class__.ppm(service, version, mode, path + ["ppm"])
                        self.dump_window = self.__class__.dump_window(service, version, mode, path + ["dump_window"])
                        self.hsf = self.__class__.hsf(service, version, mode, path + ["hsf"])
                        self.eps = self.__class__.eps(service, version, mode, path + ["eps"])
                        self.tiff = self.__class__.tiff(service, version, mode, path + ["tiff"])
                        self.vrml = self.__class__.vrml(service, version, mode, path + ["vrml"])
                        self.post_script = self.__class__.post_script(service, version, mode, path + ["post_script"])
                        self.jpeg = self.__class__.jpeg(service, version, mode, path + ["jpeg"])
                        self.glb = self.__class__.glb(service, version, mode, path + ["glb"])
                        self.avz = self.__class__.avz(service, version, mode, path + ["avz"])
                        self.list = self.__class__.list(service, version, mode, path + ["list"])
                        self.options = self.__class__.options(service, version, mode, path + ["options"])
                        self.png = self.__class__.png(service, version, mode, path + ["png"])
                        super().__init__(service, version, mode, path)
                    class ppm(TUIMethod):
                        """
                        Sets the PPM format.
                        """
                    class dump_window(TUIMethod):
                        """
                        Sets the command to dump a graphics window to a file.
                        """
                    class hsf(TUIMethod):
                        """
                        Produces HOOPS Visualize Stream Format (HSF) output for  hardcopies.
                        """
                    class eps(TUIMethod):
                        """
                        Sets the Encapsulated PostScript format.
                        """
                    class tiff(TUIMethod):
                        """
                        Sets the TIFF format.
                        """
                    class vrml(TUIMethod):
                        """
                        Sets the VRML format.
                        """
                    class post_script(TUIMethod):
                        """
                        Sets the PostScript format.
                        """
                    class jpeg(TUIMethod):
                        """
                        Sets the JPEG image format.
                        """
                    class glb(TUIMethod):
                        """
                        Produces GLB output for hardcopies.
                        """
                    class avz(TUIMethod):
                        """
                        Use AVZ output for hardcopies.
                        """
                    class list(TUIMethod):
                        """
                        Displays the current hardcopy format.
                        """
                    class options(TUIMethod):
                        """
                        Enables you to set hardcopy options, such as landscape orientation, pen speed, and physical size. The options may be entered on one line if you separate them with commas.
                        """
                    class png(TUIMethod):
                        """
                        Sets the PNG image format.
                        """

                    class post_format(TUIMenu):
                        """
                        Contains commands for setting the PostScript driver format and save files in PS files that can be printed quickly.
                        """
                        def __init__(self, service, version, mode, path):
                            self.fast_raster = self.__class__.fast_raster(service, version, mode, path + ["fast_raster"])
                            self.raster = self.__class__.raster(service, version, mode, path + ["raster"])
                            self.rle_raster = self.__class__.rle_raster(service, version, mode, path + ["rle_raster"])
                            self.vector = self.__class__.vector(service, version, mode, path + ["vector"])
                            super().__init__(service, version, mode, path)
                        class fast_raster(TUIMethod):
                            """
                            Enables a raster file that may be larger than the standard raster file, but will print much more quickly.
                            """
                        class raster(TUIMethod):
                            """
                            Enables the standard raster file.
                            """
                        class rle_raster(TUIMethod):
                            """
                            Enables a run-length encoded raster file that will be about the same size as the standard raster file, but will print slightly more quickly. This is the default file type.
                            """
                        class vector(TUIMethod):
                            """
                            Enables the standard vector file.
                            """

                class color_mode(TUIMenu):
                    """
                    Contains the available color modes.
                    """
                    def __init__(self, service, version, mode, path):
                        self.color = self.__class__.color(service, version, mode, path + ["color"])
                        self.gray_scale = self.__class__.gray_scale(service, version, mode, path + ["gray_scale"])
                        self.list = self.__class__.list(service, version, mode, path + ["list"])
                        self.mono_chrome = self.__class__.mono_chrome(service, version, mode, path + ["mono_chrome"])
                        super().__init__(service, version, mode, path)
                    class color(TUIMethod):
                        """
                        Selects full color and plots the hardcopy in color.
                        """
                    class gray_scale(TUIMethod):
                        """
                        Selects gray scale (that is, various shades of gray) and converts color to gray-scale for hardcopy.
                        """
                    class list(TUIMethod):
                        """
                        Displays the current hardcopy color mode.
                        """
                    class mono_chrome(TUIMethod):
                        """
                        Selects color to monochrome (black and white) for hardcopy.
                        """

        class zones(TUIMenu):
            """
            Contains commands for displaying zones.
            """
            def __init__(self, service, version, mode, path):
                self.show_all = self.__class__.show_all(service, version, mode, path + ["show_all"])
                self.display_neighborhood = self.__class__.display_neighborhood(service, version, mode, path + ["display_neighborhood"])
                self.display_similar_area = self.__class__.display_similar_area(service, version, mode, path + ["display_similar_area"])
                self.select_all_visible = self.__class__.select_all_visible(service, version, mode, path + ["select_all_visible"])
                self.toggle_color_palette = self.__class__.toggle_color_palette(service, version, mode, path + ["toggle_color_palette"])
                self.hide_zones = self.__class__.hide_zones(service, version, mode, path + ["hide_zones"])
                self.isolate_zones = self.__class__.isolate_zones(service, version, mode, path + ["isolate_zones"])
                self.toggle_color_mode = self.__class__.toggle_color_mode(service, version, mode, path + ["toggle_color_mode"])
                self.make_transparent = self.__class__.make_transparent(service, version, mode, path + ["make_transparent"])
                super().__init__(service, version, mode, path)
            class show_all(TUIMethod):
                """
                Unhides all the zones in the geometry and displays them.
                """
            class display_neighborhood(TUIMethod):
                """
                Displays the zones that are in the neighborhood of the selected zones. The neighboring zones have to be in contact, or intersecting the selected zone.
                """
            class display_similar_area(TUIMethod):
                """
                Displays the zones with similar area to the selected zone area.
                """
            class select_all_visible(TUIMethod):
                """
                Selects all the visible zones in the graphics window.
                """
            class toggle_color_palette(TUIMethod):
                """
                Toggles the color palette of the geometry.
                """
            class hide_zones(TUIMethod):
                """
                Hides the selected zones in the display.
                """
            class isolate_zones(TUIMethod):
                """
                Displays only the selected zones.
                """
            class toggle_color_mode(TUIMethod):
                """
                Toggles the colors of the geometry. In one mode geometry is colored object-wise while in the other mode it is colored zone-wise.
                """
            class make_transparent(TUIMethod):
                """
                Makes the geometry transparent so that internal zones are visible. This command works as a toggle undoing the transparency of the previously selected zones.
                """

        class objects(TUIMenu):
            """
            Contains commands for displaying objects.
            """
            def __init__(self, service, version, mode, path):
                self.show_all = self.__class__.show_all(service, version, mode, path + ["show_all"])
                self.select_all_visible = self.__class__.select_all_visible(service, version, mode, path + ["select_all_visible"])
                self.display_similar_area = self.__class__.display_similar_area(service, version, mode, path + ["display_similar_area"])
                self.make_transparent = self.__class__.make_transparent(service, version, mode, path + ["make_transparent"])
                self.explode = self.__class__.explode(service, version, mode, path + ["explode"])
                self.toggle_color_palette = self.__class__.toggle_color_palette(service, version, mode, path + ["toggle_color_palette"])
                self.display_neighborhood = self.__class__.display_neighborhood(service, version, mode, path + ["display_neighborhood"])
                self.isolate_objects = self.__class__.isolate_objects(service, version, mode, path + ["isolate_objects"])
                self.hide_objects = self.__class__.hide_objects(service, version, mode, path + ["hide_objects"])
                self.toggle_color_mode = self.__class__.toggle_color_mode(service, version, mode, path + ["toggle_color_mode"])
                self.implode = self.__class__.implode(service, version, mode, path + ["implode"])
                super().__init__(service, version, mode, path)
            class show_all(TUIMethod):
                """
                Unhides all the objects in the geometry and displays them.
                """
            class select_all_visible(TUIMethod):
                """
                Selects all the visible objects in the graphics window.
                """
            class display_similar_area(TUIMethod):
                """
                Displays the objects with similar area to the selected object area.
                """
            class make_transparent(TUIMethod):
                """
                Makes the geometry transparent so that internal objects are visible. This command works as a toggle undoing the transparency of the previously selected objects.
                """
            class explode(TUIMethod):
                """
                Explodes the objects in the geometry. (This command is valid only when the geometry is an assembled mode.).
                """
            class toggle_color_palette(TUIMethod):
                """
                Toggles the color palette of the geometry.
                """
            class display_neighborhood(TUIMethod):
                """
                Displays the objects that are in the neighborhood of the selected object. The neighboring objects have to be in contact, or intersecting the selected object.
                """
            class isolate_objects(TUIMethod):
                """
                Displays only the selected objects.
                """
            class hide_objects(TUIMethod):
                """
                Hides the selected objects in the display.
                """
            class toggle_color_mode(TUIMethod):
                """
                Toggles the colors of the geometry. In one mode geometry is colored object-wise while in the other mode it is colored zone-wise.
                """
            class implode(TUIMethod):
                """
                Implodes or assembles the objects in the geometry. (This command is available only when the geometry is an exploded mode.).
                """

        class advanced_rendering(TUIMenu):
            """
            Enter the advanced rendering menu.
            """
            def __init__(self, service, version, mode, path):
                self.edge_color = self.__class__.edge_color(service, version, mode, path + ["edge_color"])
                self.fast_silhouette_edges = self.__class__.fast_silhouette_edges(service, version, mode, path + ["fast_silhouette_edges"])
                self.max_extent_culling = self.__class__.max_extent_culling(service, version, mode, path + ["max_extent_culling"])
                self.static_model = self.__class__.static_model(service, version, mode, path + ["static_model"])
                self.simple_shadow = self.__class__.simple_shadow(service, version, mode, path + ["simple_shadow"])
                super().__init__(service, version, mode, path)
            class edge_color(TUIMethod):
                """
                Choose between black and body colored edges.
                """
            class fast_silhouette_edges(TUIMethod):
                """
                Enhances viewability by adding fast silhouette edges.
                """
            class max_extent_culling(TUIMethod):
                """
                Truncates zones smaller that the maximum extent culling pixel value.
                """
            class static_model(TUIMethod):
                """
                Static model driver setting.
                """
            class simple_shadow(TUIMethod):
                """
                Enhances viewability by adding a simple shadow.
                """

        class display_states(TUIMenu):
            """
            Enter the display states menu.
            """
            def __init__(self, service, version, mode, path):
                self.use_active = self.__class__.use_active(service, version, mode, path + ["use_active"])
                self.edit = self.__class__.edit(service, version, mode, path + ["edit"])
                self.list = self.__class__.list(service, version, mode, path + ["list"])
                self.apply = self.__class__.apply(service, version, mode, path + ["apply"])
                self.read = self.__class__.read(service, version, mode, path + ["read"])
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                self.copy = self.__class__.copy(service, version, mode, path + ["copy"])
                self.write = self.__class__.write(service, version, mode, path + ["write"])
                super().__init__(service, version, mode, path)
            class use_active(TUIMethod):
                """
                Save the display state settings of the active graphics window to an existing display state. This command is not available when the active window is displaying a 2D plot.
                """
            class edit(TUIMethod):
                """
                Edit a display state. Enter quit (or a substring, such as q or qui) to exit the editing loop.
                """
            class list(TUIMethod):
                """
                Print the names of the existing display states to the console.
                """
            class apply(TUIMethod):
                """
                Apply a display state to the active graphics window.
                """
            class read(TUIMethod):
                """
                Read in display states from a file.
                """
            class create(TUIMethod):
                """
                Create a new display state.
                """
            class delete(TUIMethod):
                """
                Delete a display state.
                """
            class copy(TUIMethod):
                """
                Copy the settings of an existing display state to another existing display state.
                """
            class write(TUIMethod):
                """
                Write one or more of the saved display states to a file.
                """

        class xy_plot(TUIMenu):
            """
            Enters the XY plot menu.
            """
            def __init__(self, service, version, mode, path):
                self.file = self.__class__.file(service, version, mode, path + ["file"])
                self.set = self.__class__.set(service, version, mode, path + ["set"])
                self.face_distribution = self.__class__.face_distribution(service, version, mode, path + ["face_distribution"])
                self.cell_distribution = self.__class__.cell_distribution(service, version, mode, path + ["cell_distribution"])
                super().__init__(service, version, mode, path)
            class file(TUIMethod):
                """
                Enables you to choose a file from which to create an xy plot.
                """
            class set(TUIMethod):
                """
                Enters the set window options menu.
                """
            class face_distribution(TUIMethod):
                """
                Plots a histogram of face quality.
                """
            class cell_distribution(TUIMethod):
                """
                Plots a histogram of cell quality.
                """

    class openmp_controls(TUIMenu):
        """
        Enter the openmp menu.
        """
        def __init__(self, service, version, mode, path):
            self.set_num_cores = self.__class__.set_num_cores(service, version, mode, path + ["set_num_cores"])
            self.get_max_cores = self.__class__.get_max_cores(service, version, mode, path + ["get_max_cores"])
            self.get_active_cores = self.__class__.get_active_cores(service, version, mode, path + ["get_active_cores"])
            super().__init__(service, version, mode, path)
        class set_num_cores(TUIMethod):
            """
            Enter Number of Cores.
            """
        class get_max_cores(TUIMethod):
            """
            Max Number of Cores.
            """
        class get_active_cores(TUIMethod):
            """
            Number of Active Cores.
            """

    class scoped_sizing(TUIMenu):
        """
        Manage scoped sizing.
        """
        def __init__(self, service, version, mode, path):
            self.read = self.__class__.read(service, version, mode, path + ["read"])
            self.write = self.__class__.write(service, version, mode, path + ["write"])
            self.create = self.__class__.create(service, version, mode, path + ["create"])
            self.modify = self.__class__.modify(service, version, mode, path + ["modify"])
            self.list = self.__class__.list(service, version, mode, path + ["list"])
            self.delete_size_field = self.__class__.delete_size_field(service, version, mode, path + ["delete_size_field"])
            self.list_zones_uncovered_by_controls = self.__class__.list_zones_uncovered_by_controls(service, version, mode, path + ["list_zones_uncovered_by_controls"])
            self.validate = self.__class__.validate(service, version, mode, path + ["validate"])
            self.delete_all = self.__class__.delete_all(service, version, mode, path + ["delete_all"])
            self.compute = self.__class__.compute(service, version, mode, path + ["compute"])
            self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
            super().__init__(service, version, mode, path)
        class read(TUIMethod):
            """
            Enables you to read in a scoped sizing file (\\*.szcontrol).
            """
        class write(TUIMethod):
            """
            Enables you to write a scoped sizing file (\\*.szcontrol).
            """
        class create(TUIMethod):
            """
            Defines the scoped size based on the specified parameters.
            """
        class modify(TUIMethod):
            """
            Modifies the scoped size control definition.
            """
        class list(TUIMethod):
            """
            Lists all the defined scoped size controls and the corresponding parameter values defined.
            """
        class delete_size_field(TUIMethod):
            """
            Deletes the current size field.
            """
        class list_zones_uncovered_by_controls(TUIMethod):
            """
            Lists the zones for which no scoped sizing controls have been defined.
            """
        class validate(TUIMethod):
            """
            Validates the scoped sizing controls defined. An error will be reported if the scoped sizing controls do not exist or the scope for one (or more) controls is invalid.
            """
        class delete_all(TUIMethod):
            """
            Deletes all the defined scoped size controls.
            """
        class compute(TUIMethod):
            """
            Computes the size field based on the defined size functions and/or scoped size controls.
            """
        class delete(TUIMethod):
            """
            Deletes the specified scoped size controls.
            """

    class preferences(TUIMenu):
        """
        Set preferences.
        """
        def __init__(self, service, version, mode, path):
            self.navigation = self.__class__.navigation(service, version, mode, path + ["navigation"])
            self.meshing_workflow = self.__class__.meshing_workflow(service, version, mode, path + ["meshing_workflow"])
            self.general = self.__class__.general(service, version, mode, path + ["general"])
            self.turbo_workflow = self.__class__.turbo_workflow(service, version, mode, path + ["turbo_workflow"])
            self.mat_pro_app = self.__class__.mat_pro_app(service, version, mode, path + ["mat_pro_app"])
            self.parametric_study = self.__class__.parametric_study(service, version, mode, path + ["parametric_study"])
            self.appearance = self.__class__.appearance(service, version, mode, path + ["appearance"])
            self.prj_app = self.__class__.prj_app(service, version, mode, path + ["prj_app"])
            self.gpuapp = self.__class__.gpuapp(service, version, mode, path + ["gpuapp"])
            self.graphics = self.__class__.graphics(service, version, mode, path + ["graphics"])
            self.simulation = self.__class__.simulation(service, version, mode, path + ["simulation"])
            super().__init__(service, version, mode, path)

        class navigation(TUIMenu):
            """
            Enter the menu for controlling navigation in ANSYS Fluent.
            """
            def __init__(self, service, version, mode, path):
                self.mouse_mapping = self.__class__.mouse_mapping(service, version, mode, path + ["mouse_mapping"])
                super().__init__(service, version, mode, path)

            class mouse_mapping(TUIMenu):
                """
                Enable/disable the printing of additional information and messages in the Console.
                """
                def __init__(self, service, version, mode, path):
                    self.basic = self.__class__.basic(service, version, mode, path + ["basic"])
                    self.additional = self.__class__.additional(service, version, mode, path + ["additional"])
                    self.mousemaptheme = self.__class__.mousemaptheme(service, version, mode, path + ["mousemaptheme"])
                    super().__init__(service, version, mode, path)
                class mousemaptheme(TUIMethod):
                    """
                    .
                    """

                class basic(TUIMenu):
                    """
                    .
                    """
                    def __init__(self, service, version, mode, path):
                        self.mmb = self.__class__.mmb(service, version, mode, path + ["mmb"])
                        self.rmbclick = self.__class__.rmbclick(service, version, mode, path + ["rmbclick"])
                        self.mmbclick = self.__class__.mmbclick(service, version, mode, path + ["mmbclick"])
                        self.lmbclick = self.__class__.lmbclick(service, version, mode, path + ["lmbclick"])
                        self.rmb = self.__class__.rmb(service, version, mode, path + ["rmb"])
                        self.lmb = self.__class__.lmb(service, version, mode, path + ["lmb"])
                        super().__init__(service, version, mode, path)
                    class mmb(TUIMethod):
                        """
                        .
                        """
                    class rmbclick(TUIMethod):
                        """
                        .
                        """
                    class mmbclick(TUIMethod):
                        """
                        .
                        """
                    class lmbclick(TUIMethod):
                        """
                        .
                        """
                    class rmb(TUIMethod):
                        """
                        .
                        """
                    class lmb(TUIMethod):
                        """
                        .
                        """

                class additional(TUIMenu):
                    """
                    Enter the menu for controlling mouse mappings that include a modifier button such as Ctrl and Shift.
                    """
                    def __init__(self, service, version, mode, path):
                        self.reversewheeldirection = self.__class__.reversewheeldirection(service, version, mode, path + ["reversewheeldirection"])
                        self.shiftlmbclick = self.__class__.shiftlmbclick(service, version, mode, path + ["shiftlmbclick"])
                        self.ctrlrmbdrag = self.__class__.ctrlrmbdrag(service, version, mode, path + ["ctrlrmbdrag"])
                        self.mousewheel = self.__class__.mousewheel(service, version, mode, path + ["mousewheel"])
                        self.ctrlrmbclick = self.__class__.ctrlrmbclick(service, version, mode, path + ["ctrlrmbclick"])
                        self.ctrlmmbdrag = self.__class__.ctrlmmbdrag(service, version, mode, path + ["ctrlmmbdrag"])
                        self.shiftlmbdrag = self.__class__.shiftlmbdrag(service, version, mode, path + ["shiftlmbdrag"])
                        self.mouseprobe = self.__class__.mouseprobe(service, version, mode, path + ["mouseprobe"])
                        self.shiftrmbclick = self.__class__.shiftrmbclick(service, version, mode, path + ["shiftrmbclick"])
                        self.shiftmmbclick = self.__class__.shiftmmbclick(service, version, mode, path + ["shiftmmbclick"])
                        self.shiftrmbdrag = self.__class__.shiftrmbdrag(service, version, mode, path + ["shiftrmbdrag"])
                        self.ctrlmmbclick = self.__class__.ctrlmmbclick(service, version, mode, path + ["ctrlmmbclick"])
                        self.ctrllmbdrag = self.__class__.ctrllmbdrag(service, version, mode, path + ["ctrllmbdrag"])
                        self.mousewheelsensitivity = self.__class__.mousewheelsensitivity(service, version, mode, path + ["mousewheelsensitivity"])
                        self.shiftmmbdrag = self.__class__.shiftmmbdrag(service, version, mode, path + ["shiftmmbdrag"])
                        self.ctrllmbclick = self.__class__.ctrllmbclick(service, version, mode, path + ["ctrllmbclick"])
                        super().__init__(service, version, mode, path)
                    class reversewheeldirection(TUIMethod):
                        """
                        Reverse the behavior of the mouse-wheel.
                        """
                    class shiftlmbclick(TUIMethod):
                        """
                        Specify the action/behavior for Shift + left-mouse-button + click.
                        """
                    class ctrlrmbdrag(TUIMethod):
                        """
                        Specify the action/behavior for Ctrl + right-mouse-button + drag.
                        """
                    class mousewheel(TUIMethod):
                        """
                        Specify the action/behavior of the mouse-wheel.
                        """
                    class ctrlrmbclick(TUIMethod):
                        """
                        Specify the action/behavior for Ctrl + right-mouse-button + click.
                        """
                    class ctrlmmbdrag(TUIMethod):
                        """
                        Specify the action/behavior for Ctrl + middle-mouse-button + drag.
                        """
                    class shiftlmbdrag(TUIMethod):
                        """
                        Specify the action/behavior for Shift + left-mouse-button + drag.
                        """
                    class mouseprobe(TUIMethod):
                        """
                        Specify whether the probe action provides a long description or a short description.
                        """
                    class shiftrmbclick(TUIMethod):
                        """
                        Specify the action/behavior for Shift + right-mouse-button + click.
                        """
                    class shiftmmbclick(TUIMethod):
                        """
                        Specify the action/behavior for Shift + middle-mouse-button + click.
                        """
                    class shiftrmbdrag(TUIMethod):
                        """
                        Specify the action/behavior for Shift + right-mouse-button + drag.
                        """
                    class ctrlmmbclick(TUIMethod):
                        """
                        Specify the action/behavior for Ctrl + middle-mouse-button + click.
                        """
                    class ctrllmbdrag(TUIMethod):
                        """
                        Specify the action/behavior for Ctrl + left-mouse-button + drag.
                        """
                    class mousewheelsensitivity(TUIMethod):
                        """
                        Specify the sensitivity of the mouse-wheel (0 is least sensitive, 1 is most sensitive).
                        """
                    class shiftmmbdrag(TUIMethod):
                        """
                        Specify the action/behavior for Shift + middle-mouse-button + drag.
                        """
                    class ctrllmbclick(TUIMethod):
                        """
                        Specify the action/behavoir for Ctrl + left-mouse-button + click.
                        """

        class meshing_workflow(TUIMenu):
            """
            Enter the menu for preferences covering the Fluent Meshing workflows.
            """
            def __init__(self, service, version, mode, path):
                self.draw_settings = self.__class__.draw_settings(service, version, mode, path + ["draw_settings"])
                self.cadoptions = self.__class__.cadoptions(service, version, mode, path + ["cadoptions"])
                self.temp_folder = self.__class__.temp_folder(service, version, mode, path + ["temp_folder"])
                self.save_wft_file_with_mesh = self.__class__.save_wft_file_with_mesh(service, version, mode, path + ["save_wft_file_with_mesh"])
                self.verbosity = self.__class__.verbosity(service, version, mode, path + ["verbosity"])
                self.save_checkpoint_files = self.__class__.save_checkpoint_files(service, version, mode, path + ["save_checkpoint_files"])
                self.checkpointing_option = self.__class__.checkpointing_option(service, version, mode, path + ["checkpointing_option"])
                self.templates_folder = self.__class__.templates_folder(service, version, mode, path + ["templates_folder"])
                super().__init__(service, version, mode, path)
            class temp_folder(TUIMethod):
                """
                Specify a temporary location to hold generated mesh files. If nothing is specified, Fluent Meshing will write to percentageTEMPpercentage on Windows and to  /tmp on Linux.
                """
            class save_wft_file_with_mesh(TUIMethod):
                """
                .
                """
            class verbosity(TUIMethod):
                """
                Enable/disable the printing of additional information and messages in the Console.
                """
            class save_checkpoint_files(TUIMethod):
                """
                Enable/disable the saving of task editing data when writing a mesh file.
                """
            class checkpointing_option(TUIMethod):
                """
                Specify how Fluent Meshing will save data when you edit a task.
                """
            class templates_folder(TUIMethod):
                """
                .
                """

            class draw_settings(TUIMenu):
                """
                Enter the menu for specifying drawing settings.
                """
                def __init__(self, service, version, mode, path):
                    self.facet_limit = self.__class__.facet_limit(service, version, mode, path + ["facet_limit"])
                    self.auto_draw = self.__class__.auto_draw(service, version, mode, path + ["auto_draw"])
                    self.face_zone_limit = self.__class__.face_zone_limit(service, version, mode, path + ["face_zone_limit"])
                    super().__init__(service, version, mode, path)
                class facet_limit(TUIMethod):
                    """
                    Specify the cutoff number facets, beyond which, Fluent Meshing will not automatically display changes.
                    """
                class auto_draw(TUIMethod):
                    """
                    Enable/disable the automatic display of changes in the graphics window based on the current task.
                    """
                class face_zone_limit(TUIMethod):
                    """
                    Specify the cutoff number of face zones, beyond which, Fluent Meshing will not automatically display changes.
                    """

            class cadoptions(TUIMenu):
                """
                .
                """
                def __init__(self, service, version, mode, path):
                    self.refaceter = self.__class__.refaceter(service, version, mode, path + ["refaceter"])
                    super().__init__(service, version, mode, path)
                class refaceter(TUIMethod):
                    """
                    .
                    """

        class general(TUIMenu):
            """
            Enter the menu for general preferences.
            """
            def __init__(self, service, version, mode, path):
                self.startup_messages = self.__class__.startup_messages(service, version, mode, path + ["startup_messages"])
                self.automatic_transcript = self.__class__.automatic_transcript(service, version, mode, path + ["automatic_transcript"])
                self.skip_creation_of_groups_pointing_to_single_entity = self.__class__.skip_creation_of_groups_pointing_to_single_entity(service, version, mode, path + ["skip_creation_of_groups_pointing_to_single_entity"])
                self.dock_editor = self.__class__.dock_editor(service, version, mode, path + ["dock_editor"])
                self.flow_model = self.__class__.flow_model(service, version, mode, path + ["flow_model"])
                self.idle_timeout = self.__class__.idle_timeout(service, version, mode, path + ["idle_timeout"])
                self.utlcreate_physics_on_mode_change = self.__class__.utlcreate_physics_on_mode_change(service, version, mode, path + ["utlcreate_physics_on_mode_change"])
                self.advanced_partition = self.__class__.advanced_partition(service, version, mode, path + ["advanced_partition"])
                self.utlmode = self.__class__.utlmode(service, version, mode, path + ["utlmode"])
                self.default_ioformat = self.__class__.default_ioformat(service, version, mode, path + ["default_ioformat"])
                self.initial_physics_volume_definitions = self.__class__.initial_physics_volume_definitions(service, version, mode, path + ["initial_physics_volume_definitions"])
                self.import_physics_volume_definitions = self.__class__.import_physics_volume_definitions(service, version, mode, path + ["import_physics_volume_definitions"])
                super().__init__(service, version, mode, path)
            class automatic_transcript(TUIMethod):
                """
                Enable/disable the automatic creation of a transcript file for each ANSYS Fluent session.
                """
            class skip_creation_of_groups_pointing_to_single_entity(TUIMethod):
                """
                .
                """
            class dock_editor(TUIMethod):
                """
                .
                """
            class flow_model(TUIMethod):
                """
                .
                """
            class idle_timeout(TUIMethod):
                """
                Specify the default file format for saving case and data files.
                """
            class utlcreate_physics_on_mode_change(TUIMethod):
                """
                .
                """
            class advanced_partition(TUIMethod):
                """
                .
                """
            class utlmode(TUIMethod):
                """
                .
                """
            class default_ioformat(TUIMethod):
                """
                .
                """
            class initial_physics_volume_definitions(TUIMethod):
                """
                .
                """
            class import_physics_volume_definitions(TUIMethod):
                """
                .
                """

            class startup_messages(TUIMenu):
                """
                .
                """
                def __init__(self, service, version, mode, path):
                    self.color_theme_change_message = self.__class__.color_theme_change_message(service, version, mode, path + ["color_theme_change_message"])
                    self.key_behavioral_changes_message = self.__class__.key_behavioral_changes_message(service, version, mode, path + ["key_behavioral_changes_message"])
                    self.qaservice_message = self.__class__.qaservice_message(service, version, mode, path + ["qaservice_message"])
                    super().__init__(service, version, mode, path)
                class color_theme_change_message(TUIMethod):
                    """
                    .
                    """
                class key_behavioral_changes_message(TUIMethod):
                    """
                    .
                    """
                class qaservice_message(TUIMethod):
                    """
                    .
                    """

        class turbo_workflow(TUIMenu):
            """
            .
            """
            def __init__(self, service, version, mode, path):
                self.graphics_settings = self.__class__.graphics_settings(service, version, mode, path + ["graphics_settings"])
                self.face_zone_settings = self.__class__.face_zone_settings(service, version, mode, path + ["face_zone_settings"])
                self.checkpointing_option = self.__class__.checkpointing_option(service, version, mode, path + ["checkpointing_option"])
                self.save_checkpoint_files = self.__class__.save_checkpoint_files(service, version, mode, path + ["save_checkpoint_files"])
                super().__init__(service, version, mode, path)
            class checkpointing_option(TUIMethod):
                """
                .
                """
            class save_checkpoint_files(TUIMethod):
                """
                .
                """

            class graphics_settings(TUIMenu):
                """
                .
                """
                def __init__(self, service, version, mode, path):
                    self.auto_draw = self.__class__.auto_draw(service, version, mode, path + ["auto_draw"])
                    super().__init__(service, version, mode, path)
                class auto_draw(TUIMethod):
                    """
                    .
                    """

            class face_zone_settings(TUIMenu):
                """
                .
                """
                def __init__(self, service, version, mode, path):
                    self.fzsearch_order = self.__class__.fzsearch_order(service, version, mode, path + ["fzsearch_order"])
                    self.outlet_region = self.__class__.outlet_region(service, version, mode, path + ["outlet_region"])
                    self.periodic2_region = self.__class__.periodic2_region(service, version, mode, path + ["periodic2_region"])
                    self.tip2_region = self.__class__.tip2_region(service, version, mode, path + ["tip2_region"])
                    self.blade_region = self.__class__.blade_region(service, version, mode, path + ["blade_region"])
                    self.hub_region = self.__class__.hub_region(service, version, mode, path + ["hub_region"])
                    self.symmetry_region = self.__class__.symmetry_region(service, version, mode, path + ["symmetry_region"])
                    self.shroud_region = self.__class__.shroud_region(service, version, mode, path + ["shroud_region"])
                    self.interior_region = self.__class__.interior_region(service, version, mode, path + ["interior_region"])
                    self.tip1_region = self.__class__.tip1_region(service, version, mode, path + ["tip1_region"])
                    self.periodic1_region = self.__class__.periodic1_region(service, version, mode, path + ["periodic1_region"])
                    self.inlet_region = self.__class__.inlet_region(service, version, mode, path + ["inlet_region"])
                    super().__init__(service, version, mode, path)
                class fzsearch_order(TUIMethod):
                    """
                    .
                    """
                class outlet_region(TUIMethod):
                    """
                    .
                    """
                class periodic2_region(TUIMethod):
                    """
                    .
                    """
                class tip2_region(TUIMethod):
                    """
                    .
                    """
                class blade_region(TUIMethod):
                    """
                    .
                    """
                class hub_region(TUIMethod):
                    """
                    .
                    """
                class symmetry_region(TUIMethod):
                    """
                    .
                    """
                class shroud_region(TUIMethod):
                    """
                    .
                    """
                class interior_region(TUIMethod):
                    """
                    .
                    """
                class tip1_region(TUIMethod):
                    """
                    .
                    """
                class periodic1_region(TUIMethod):
                    """
                    .
                    """
                class inlet_region(TUIMethod):
                    """
                    .
                    """

        class mat_pro_app(TUIMenu):
            """
            .
            """
            def __init__(self, service, version, mode, path):
                self.statistics = self.__class__.statistics(service, version, mode, path + ["statistics"])
                self.check_expression = self.__class__.check_expression(service, version, mode, path + ["check_expression"])
                self.debug = self.__class__.debug(service, version, mode, path + ["debug"])
                self.warning = self.__class__.warning(service, version, mode, path + ["warning"])
                self.mesh_naming = self.__class__.mesh_naming(service, version, mode, path + ["mesh_naming"])
                self.tracking = self.__class__.tracking(service, version, mode, path + ["tracking"])
                self.beta_features = self.__class__.beta_features(service, version, mode, path + ["beta_features"])
                self.focus = self.__class__.focus(service, version, mode, path + ["focus"])
                super().__init__(service, version, mode, path)
            class debug(TUIMethod):
                """
                .
                """
            class warning(TUIMethod):
                """
                .
                """
            class mesh_naming(TUIMethod):
                """
                .
                """
            class tracking(TUIMethod):
                """
                .
                """
            class beta_features(TUIMethod):
                """
                .
                """
            class focus(TUIMethod):
                """
                .
                """

            class statistics(TUIMenu):
                """
                .
                """
                def __init__(self, service, version, mode, path):
                    self.quick_slicing = self.__class__.quick_slicing(service, version, mode, path + ["quick_slicing"])
                    self.max_positions = self.__class__.max_positions(service, version, mode, path + ["max_positions"])
                    super().__init__(service, version, mode, path)
                class quick_slicing(TUIMethod):
                    """
                    .
                    """
                class max_positions(TUIMethod):
                    """
                    .
                    """

            class check_expression(TUIMenu):
                """
                .
                """
                def __init__(self, service, version, mode, path):
                    self.edot = self.__class__.edot(service, version, mode, path + ["edot"])
                    self.velocities = self.__class__.velocities(service, version, mode, path + ["velocities"])
                    self.gdot = self.__class__.gdot(service, version, mode, path + ["gdot"])
                    self.temperature = self.__class__.temperature(service, version, mode, path + ["temperature"])
                    self.species = self.__class__.species(service, version, mode, path + ["species"])
                    self.coordinates = self.__class__.coordinates(service, version, mode, path + ["coordinates"])
                    self.vorticity = self.__class__.vorticity(service, version, mode, path + ["vorticity"])
                    self.dvv = self.__class__.dvv(service, version, mode, path + ["dvv"])
                    self.time = self.__class__.time(service, version, mode, path + ["time"])
                    self.cdot = self.__class__.cdot(service, version, mode, path + ["cdot"])
                    self.pressure = self.__class__.pressure(service, version, mode, path + ["pressure"])
                    self.giesekus = self.__class__.giesekus(service, version, mode, path + ["giesekus"])
                    super().__init__(service, version, mode, path)
                class edot(TUIMethod):
                    """
                    .
                    """
                class velocities(TUIMethod):
                    """
                    .
                    """
                class gdot(TUIMethod):
                    """
                    .
                    """
                class temperature(TUIMethod):
                    """
                    .
                    """
                class species(TUIMethod):
                    """
                    .
                    """
                class coordinates(TUIMethod):
                    """
                    .
                    """
                class vorticity(TUIMethod):
                    """
                    .
                    """
                class dvv(TUIMethod):
                    """
                    .
                    """
                class time(TUIMethod):
                    """
                    .
                    """
                class cdot(TUIMethod):
                    """
                    .
                    """
                class pressure(TUIMethod):
                    """
                    .
                    """
                class giesekus(TUIMethod):
                    """
                    .
                    """

        class parametric_study(TUIMenu):
            """
            .
            """
            def __init__(self, service, version, mode, path):
                self.update_options = self.__class__.update_options(service, version, mode, path + ["update_options"])
                self.layout_options = self.__class__.layout_options(service, version, mode, path + ["layout_options"])
                super().__init__(service, version, mode, path)

            class update_options(TUIMenu):
                """
                .
                """
                def __init__(self, service, version, mode, path):
                    self.capture_sim_report_data = self.__class__.capture_sim_report_data(service, version, mode, path + ["capture_sim_report_data"])
                    self.auto_refresh_time = self.__class__.auto_refresh_time(service, version, mode, path + ["auto_refresh_time"])
                    self.save_project_after_dpupdate = self.__class__.save_project_after_dpupdate(service, version, mode, path + ["save_project_after_dpupdate"])
                    self.enable_auto_refresh = self.__class__.enable_auto_refresh(service, version, mode, path + ["enable_auto_refresh"])
                    self.write_data = self.__class__.write_data(service, version, mode, path + ["write_data"])
                    super().__init__(service, version, mode, path)
                class capture_sim_report_data(TUIMethod):
                    """
                    .
                    """
                class auto_refresh_time(TUIMethod):
                    """
                    .
                    """
                class save_project_after_dpupdate(TUIMethod):
                    """
                    .
                    """
                class enable_auto_refresh(TUIMethod):
                    """
                    .
                    """
                class write_data(TUIMethod):
                    """
                    .
                    """

            class layout_options(TUIMenu):
                """
                .
                """
                def __init__(self, service, version, mode, path):
                    self.current_case_parameters = self.__class__.current_case_parameters(service, version, mode, path + ["current_case_parameters"])
                    self.parametric_study_tree = self.__class__.parametric_study_tree(service, version, mode, path + ["parametric_study_tree"])
                    super().__init__(service, version, mode, path)
                class current_case_parameters(TUIMethod):
                    """
                    .
                    """
                class parametric_study_tree(TUIMethod):
                    """
                    .
                    """

        class appearance(TUIMenu):
            """
            Enter the menu for preferences covering appearance.
            """
            def __init__(self, service, version, mode, path):
                self.ansys_logo = self.__class__.ansys_logo(service, version, mode, path + ["ansys_logo"])
                self.charts = self.__class__.charts(service, version, mode, path + ["charts"])
                self.selections = self.__class__.selections(service, version, mode, path + ["selections"])
                self.completer = self.__class__.completer(service, version, mode, path + ["completer"])
                self.graphics_title_window_framecolor = self.__class__.graphics_title_window_framecolor(service, version, mode, path + ["graphics_title_window_framecolor"])
                self.number_of_pastel_colors = self.__class__.number_of_pastel_colors(service, version, mode, path + ["number_of_pastel_colors"])
                self.axis_triad = self.__class__.axis_triad(service, version, mode, path + ["axis_triad"])
                self.quick_property_view = self.__class__.quick_property_view(service, version, mode, path + ["quick_property_view"])
                self.pastel_color_value = self.__class__.pastel_color_value(service, version, mode, path + ["pastel_color_value"])
                self.graphics_default_manual_node_color = self.__class__.graphics_default_manual_node_color(service, version, mode, path + ["graphics_default_manual_node_color"])
                self.graphics_default_manual_face_color = self.__class__.graphics_default_manual_face_color(service, version, mode, path + ["graphics_default_manual_face_color"])
                self.number_of_files_recently_used = self.__class__.number_of_files_recently_used(service, version, mode, path + ["number_of_files_recently_used"])
                self.titles_border_offset = self.__class__.titles_border_offset(service, version, mode, path + ["titles_border_offset"])
                self.show_enabled_models = self.__class__.show_enabled_models(service, version, mode, path + ["show_enabled_models"])
                self.color_theme = self.__class__.color_theme(service, version, mode, path + ["color_theme"])
                self.ruler = self.__class__.ruler(service, version, mode, path + ["ruler"])
                self.pastel_color_saturation = self.__class__.pastel_color_saturation(service, version, mode, path + ["pastel_color_saturation"])
                self.surface_specularity_for_contours = self.__class__.surface_specularity_for_contours(service, version, mode, path + ["surface_specularity_for_contours"])
                self.graphics_foreground_color = self.__class__.graphics_foreground_color(service, version, mode, path + ["graphics_foreground_color"])
                self.default_view = self.__class__.default_view(service, version, mode, path + ["default_view"])
                self.graphics_wall_face_color = self.__class__.graphics_wall_face_color(service, version, mode, path + ["graphics_wall_face_color"])
                self.surface_emissivity = self.__class__.surface_emissivity(service, version, mode, path + ["surface_emissivity"])
                self.surface_specularity = self.__class__.surface_specularity(service, version, mode, path + ["surface_specularity"])
                self.group_physics_by_tree_view = self.__class__.group_physics_by_tree_view(service, version, mode, path + ["group_physics_by_tree_view"])
                self.graphics_background_color1 = self.__class__.graphics_background_color1(service, version, mode, path + ["graphics_background_color1"])
                self.show_model_edges = self.__class__.show_model_edges(service, version, mode, path + ["show_model_edges"])
                self.titles = self.__class__.titles(service, version, mode, path + ["titles"])
                self.custom_title_bar = self.__class__.custom_title_bar(service, version, mode, path + ["custom_title_bar"])
                self.group_by_tree_view = self.__class__.group_by_tree_view(service, version, mode, path + ["group_by_tree_view"])
                self.graphics_background_style = self.__class__.graphics_background_style(service, version, mode, path + ["graphics_background_style"])
                self.application_font_size = self.__class__.application_font_size(service, version, mode, path + ["application_font_size"])
                self.graphics_surface_color = self.__class__.graphics_surface_color(service, version, mode, path + ["graphics_surface_color"])
                self.solution_mode_edge_color_in_meshing_mode = self.__class__.solution_mode_edge_color_in_meshing_mode(service, version, mode, path + ["solution_mode_edge_color_in_meshing_mode"])
                self.model_color_scheme = self.__class__.model_color_scheme(service, version, mode, path + ["model_color_scheme"])
                self.graphics_background_color2 = self.__class__.graphics_background_color2(service, version, mode, path + ["graphics_background_color2"])
                self.graphics_partition_boundary_color = self.__class__.graphics_partition_boundary_color(service, version, mode, path + ["graphics_partition_boundary_color"])
                self.graphics_view = self.__class__.graphics_view(service, version, mode, path + ["graphics_view"])
                self.transient_post_processing = self.__class__.transient_post_processing(service, version, mode, path + ["transient_post_processing"])
                self.graphics_color_theme = self.__class__.graphics_color_theme(service, version, mode, path + ["graphics_color_theme"])
                self.graphics_edge_color = self.__class__.graphics_edge_color(service, version, mode, path + ["graphics_edge_color"])
                self.show_interface_children_zone = self.__class__.show_interface_children_zone(service, version, mode, path + ["show_interface_children_zone"])
                super().__init__(service, version, mode, path)
            class completer(TUIMethod):
                """
                Enable/disable the console automatic-completer, which suggests available commands as you type in the console.
                """
            class graphics_title_window_framecolor(TUIMethod):
                """
                .
                """
            class number_of_pastel_colors(TUIMethod):
                """
                .
                """
            class axis_triad(TUIMethod):
                """
                Enable or disable the visibility of the axis triad in the graphics window.
                """
            class quick_property_view(TUIMethod):
                """
                Enables/Disables the "quick-edit" properties panels that appear when you select a boundary in the graphics windows.
                """
            class pastel_color_value(TUIMethod):
                """
                .
                """
            class graphics_default_manual_node_color(TUIMethod):
                """
                .
                """
            class graphics_default_manual_face_color(TUIMethod):
                """
                .
                """
            class number_of_files_recently_used(TUIMethod):
                """
                Controls how many recently-used files are listed in the File ribbon tab and the Fluent Launcher.
                """
            class titles_border_offset(TUIMethod):
                """
                .
                """
            class show_enabled_models(TUIMethod):
                """
                .
                """
            class color_theme(TUIMethod):
                """
                Specify a color theme for the appearance of ANSYS Fluent.
                """
            class ruler(TUIMethod):
                """
                Adds or removes the ruler from the graphics window. Note that you must be in orthographic view for the ruler to be visible in the graphics  window.
                """
            class pastel_color_saturation(TUIMethod):
                """
                .
                """
            class surface_specularity_for_contours(TUIMethod):
                """
                .
                """
            class graphics_foreground_color(TUIMethod):
                """
                Specify the color of graphics window text.
                """
            class default_view(TUIMethod):
                """
                .
                """
            class graphics_wall_face_color(TUIMethod):
                """
                Set the default face color for when the mesh is displayed.
                """
            class surface_emissivity(TUIMethod):
                """
                .
                """
            class surface_specularity(TUIMethod):
                """
                Specify the specularity of all surfaces except those included in contour plots. Sepecularity is the reflectiveness of a surface; higher values (closer to 1) equate to a more reflective surface.
                """
            class group_physics_by_tree_view(TUIMethod):
                """
                .
                """
            class graphics_background_color1(TUIMethod):
                """
                Controls the primary background color of the graphics window.
                """
            class show_model_edges(TUIMethod):
                """
                Enable/disable whether mesh edges are shown in a mesh display.
                """
            class titles(TUIMethod):
                """
                Enable/disable the display of solver information in the graphics window.
                """
            class custom_title_bar(TUIMethod):
                """
                .
                """
            class group_by_tree_view(TUIMethod):
                """
                Specify how boundary conditions are grouped in the tree.
                """
            class graphics_background_style(TUIMethod):
                """
                Specify whether the background color is uniform or if there is a gradient.
                """
            class application_font_size(TUIMethod):
                """
                .
                """
            class graphics_surface_color(TUIMethod):
                """
                .
                """
            class solution_mode_edge_color_in_meshing_mode(TUIMethod):
                """
                .
                """
            class model_color_scheme(TUIMethod):
                """
                .
                """
            class graphics_background_color2(TUIMethod):
                """
                Controls the secondary background color when the style is set as a gradient.
                """
            class graphics_partition_boundary_color(TUIMethod):
                """
                .
                """
            class graphics_view(TUIMethod):
                """
                Specify whether the default view is orthographic or perspective.
                """
            class transient_post_processing(TUIMethod):
                """
                .
                """
            class graphics_color_theme(TUIMethod):
                """
                .
                """
            class graphics_edge_color(TUIMethod):
                """
                .
                """
            class show_interface_children_zone(TUIMethod):
                """
                Enable/disable the showing of the non-overlapping zones and interior zones associated with one-to-one mesh interfaces under Setup / Boundary Conditions (under their zone types) in the outline view tree.
                """

            class ansys_logo(TUIMenu):
                """
                Enter the menu for controlling Ansys logo visibility.
                """
                def __init__(self, service, version, mode, path):
                    self.color = self.__class__.color(service, version, mode, path + ["color"])
                    self.visible = self.__class__.visible(service, version, mode, path + ["visible"])
                    super().__init__(service, version, mode, path)
                class color(TUIMethod):
                    """
                    Specify whether the Ansys logo is white or black.
                    """
                class visible(TUIMethod):
                    """
                    Enable or disable the visibility of the Ansys logo in the graphics window.
                    """

            class charts(TUIMenu):
                """
                Enter the menu for controlling the display of 2D charts/plots.
                """
                def __init__(self, service, version, mode, path):
                    self.text_color = self.__class__.text_color(service, version, mode, path + ["text_color"])
                    self.font = self.__class__.font(service, version, mode, path + ["font"])
                    self.enable_open_glfor_modern_plots = self.__class__.enable_open_glfor_modern_plots(service, version, mode, path + ["enable_open_glfor_modern_plots"])
                    self.modern_plots_points_threshold = self.__class__.modern_plots_points_threshold(service, version, mode, path + ["modern_plots_points_threshold"])
                    self.legend_alignment = self.__class__.legend_alignment(service, version, mode, path + ["legend_alignment"])
                    self.curve_colors = self.__class__.curve_colors(service, version, mode, path + ["curve_colors"])
                    self.print_residuals_data = self.__class__.print_residuals_data(service, version, mode, path + ["print_residuals_data"])
                    self.print_plot_data = self.__class__.print_plot_data(service, version, mode, path + ["print_plot_data"])
                    self.modern_plots_enabled = self.__class__.modern_plots_enabled(service, version, mode, path + ["modern_plots_enabled"])
                    self.plots_behavior = self.__class__.plots_behavior(service, version, mode, path + ["plots_behavior"])
                    self.legend_visibility = self.__class__.legend_visibility(service, version, mode, path + ["legend_visibility"])
                    self.tooltip_interpolation = self.__class__.tooltip_interpolation(service, version, mode, path + ["tooltip_interpolation"])
                    self.threshold = self.__class__.threshold(service, version, mode, path + ["threshold"])
                    super().__init__(service, version, mode, path)
                class enable_open_glfor_modern_plots(TUIMethod):
                    """
                    .
                    """
                class modern_plots_points_threshold(TUIMethod):
                    """
                    .
                    """
                class legend_alignment(TUIMethod):
                    """
                    .
                    """
                class curve_colors(TUIMethod):
                    """
                    Specify the initial set of default colors for the rendering of curves. Note that changing this setting requires any plots to be replotted before you see the effect of the new setting.
                    """
                class print_residuals_data(TUIMethod):
                    """
                    .
                    """
                class print_plot_data(TUIMethod):
                    """
                    .
                    """
                class modern_plots_enabled(TUIMethod):
                    """
                    Enables enhanced plots, which is a beta feature. Enabling this feature exposes new fields (all beta functionality).
                    """
                class plots_behavior(TUIMethod):
                    """
                    .
                    """
                class legend_visibility(TUIMethod):
                    """
                    .
                    """
                class tooltip_interpolation(TUIMethod):
                    """
                    .
                    """
                class threshold(TUIMethod):
                    """
                    .
                    """

                class text_color(TUIMenu):
                    """
                    .
                    """
                    def __init__(self, service, version, mode, path):
                        self.title = self.__class__.title(service, version, mode, path + ["title"])
                        self.legend = self.__class__.legend(service, version, mode, path + ["legend"])
                        self.axes = self.__class__.axes(service, version, mode, path + ["axes"])
                        self.axes_titles = self.__class__.axes_titles(service, version, mode, path + ["axes_titles"])
                        super().__init__(service, version, mode, path)
                    class title(TUIMethod):
                        """
                        .
                        """
                    class legend(TUIMethod):
                        """
                        .
                        """
                    class axes(TUIMethod):
                        """
                        .
                        """
                    class axes_titles(TUIMethod):
                        """
                        .
                        """

                class font(TUIMenu):
                    """
                    .
                    """
                    def __init__(self, service, version, mode, path):
                        self.axes_titles = self.__class__.axes_titles(service, version, mode, path + ["axes_titles"])
                        self.axes = self.__class__.axes(service, version, mode, path + ["axes"])
                        self.legend = self.__class__.legend(service, version, mode, path + ["legend"])
                        self.title = self.__class__.title(service, version, mode, path + ["title"])
                        super().__init__(service, version, mode, path)
                    class axes_titles(TUIMethod):
                        """
                        .
                        """
                    class axes(TUIMethod):
                        """
                        .
                        """
                    class legend(TUIMethod):
                        """
                        .
                        """
                    class title(TUIMethod):
                        """
                        .
                        """

            class selections(TUIMenu):
                """
                Enters the menu for controlling selections in the graphics window.
                """
                def __init__(self, service, version, mode, path):
                    self.probe_tooltip_show_delay_timer = self.__class__.probe_tooltip_show_delay_timer(service, version, mode, path + ["probe_tooltip_show_delay_timer"])
                    self.probe_tooltip_hide_delay_timer = self.__class__.probe_tooltip_hide_delay_timer(service, version, mode, path + ["probe_tooltip_hide_delay_timer"])
                    self.highlight_face_color = self.__class__.highlight_face_color(service, version, mode, path + ["highlight_face_color"])
                    self.highlight_gloss = self.__class__.highlight_gloss(service, version, mode, path + ["highlight_gloss"])
                    self.enable_highlight_edge_transparency = self.__class__.enable_highlight_edge_transparency(service, version, mode, path + ["enable_highlight_edge_transparency"])
                    self.general_displacement = self.__class__.general_displacement(service, version, mode, path + ["general_displacement"])
                    self.highlight_edge_weight = self.__class__.highlight_edge_weight(service, version, mode, path + ["highlight_edge_weight"])
                    self.mouse_hover_probe_values_enabled = self.__class__.mouse_hover_probe_values_enabled(service, version, mode, path + ["mouse_hover_probe_values_enabled"])
                    self.mouse_over_highlight_enabled = self.__class__.mouse_over_highlight_enabled(service, version, mode, path + ["mouse_over_highlight_enabled"])
                    self.highlight_edge_color = self.__class__.highlight_edge_color(service, version, mode, path + ["highlight_edge_color"])
                    self.highlight_transparency = self.__class__.highlight_transparency(service, version, mode, path + ["highlight_transparency"])
                    self.highlight_specular_component = self.__class__.highlight_specular_component(service, version, mode, path + ["highlight_specular_component"])
                    super().__init__(service, version, mode, path)
                class probe_tooltip_show_delay_timer(TUIMethod):
                    """
                    .
                    """
                class probe_tooltip_hide_delay_timer(TUIMethod):
                    """
                    .
                    """
                class highlight_face_color(TUIMethod):
                    """
                    Specify which color indicates that a face is selected.
                    """
                class highlight_gloss(TUIMethod):
                    """
                    .
                    """
                class enable_highlight_edge_transparency(TUIMethod):
                    """
                    .
                    """
                class general_displacement(TUIMethod):
                    """
                    .
                    """
                class highlight_edge_weight(TUIMethod):
                    """
                    Specifies the thickness of the edge highlights when the Hover-Over Highlight feature is enabled (mouse-over-highlight-enabled).
                    """
                class mouse_hover_probe_values_enabled(TUIMethod):
                    """
                    .
                    """
                class mouse_over_highlight_enabled(TUIMethod):
                    """
                    Enable/disable the highlighted outline of a surface when hovered-over. Note that objects must be redisplayed after changing this setting before the new setting is visible.
                    """
                class highlight_edge_color(TUIMethod):
                    """
                    Specifies the color used to highlight edges when the Hover-Over Highlight feature is enabled (mouse-over-highlight-enabled).
                    """
                class highlight_transparency(TUIMethod):
                    """
                    Specify the transparency of the coloring on a selected surface. 0.1 is fully opaque and 1 is fully transparent.
                    """
                class highlight_specular_component(TUIMethod):
                    """
                    .
                    """

        class prj_app(TUIMenu):
            """
            .
            """
            def __init__(self, service, version, mode, path):
                self.beta_flag = self.__class__.beta_flag(service, version, mode, path + ["beta_flag"])
                self.advanced_flag = self.__class__.advanced_flag(service, version, mode, path + ["advanced_flag"])
                self.unit_system = self.__class__.unit_system(service, version, mode, path + ["unit_system"])
                super().__init__(service, version, mode, path)
            class beta_flag(TUIMethod):
                """
                .
                """
            class advanced_flag(TUIMethod):
                """
                .
                """
            class unit_system(TUIMethod):
                """
                .
                """

        class gpuapp(TUIMenu):
            """
            .
            """
            def __init__(self, service, version, mode, path):
                self.alpha_features = self.__class__.alpha_features(service, version, mode, path + ["alpha_features"])
                super().__init__(service, version, mode, path)
            class alpha_features(TUIMethod):
                """
                .
                """

        class graphics(TUIMenu):
            """
            Enter the menu for preferences covering appearance.
            """
            def __init__(self, service, version, mode, path):
                self.performance = self.__class__.performance(service, version, mode, path + ["performance"])
                self.colormap_settings = self.__class__.colormap_settings(service, version, mode, path + ["colormap_settings"])
                self.hardcopy_settings = self.__class__.hardcopy_settings(service, version, mode, path + ["hardcopy_settings"])
                self.material_effects = self.__class__.material_effects(service, version, mode, path + ["material_effects"])
                self.export_video_settings = self.__class__.export_video_settings(service, version, mode, path + ["export_video_settings"])
                self.manage_hoops_memory = self.__class__.manage_hoops_memory(service, version, mode, path + ["manage_hoops_memory"])
                self.vector_settings = self.__class__.vector_settings(service, version, mode, path + ["vector_settings"])
                self.ray_tracing_options = self.__class__.ray_tracing_options(service, version, mode, path + ["ray_tracing_options"])
                self.lighting = self.__class__.lighting(service, version, mode, path + ["lighting"])
                self.boundary_markers = self.__class__.boundary_markers(service, version, mode, path + ["boundary_markers"])
                self.graphics_effects = self.__class__.graphics_effects(service, version, mode, path + ["graphics_effects"])
                self.transparency = self.__class__.transparency(service, version, mode, path + ["transparency"])
                self.embedded_windows = self.__class__.embedded_windows(service, version, mode, path + ["embedded_windows"])
                self.meshing_mode = self.__class__.meshing_mode(service, version, mode, path + ["meshing_mode"])
                self.show_hidden_surfaces = self.__class__.show_hidden_surfaces(service, version, mode, path + ["show_hidden_surfaces"])
                self.point_tool_size = self.__class__.point_tool_size(service, version, mode, path + ["point_tool_size"])
                self.set_camera_normal_to_surface_increments = self.__class__.set_camera_normal_to_surface_increments(service, version, mode, path + ["set_camera_normal_to_surface_increments"])
                self.show_hidden_lines = self.__class__.show_hidden_lines(service, version, mode, path + ["show_hidden_lines"])
                self.double_buffering = self.__class__.double_buffering(service, version, mode, path + ["double_buffering"])
                self.marker_drawing_mode = self.__class__.marker_drawing_mode(service, version, mode, path + ["marker_drawing_mode"])
                self.graphics_window_line_width = self.__class__.graphics_window_line_width(service, version, mode, path + ["graphics_window_line_width"])
                self.hidden_surface_removal_method = self.__class__.hidden_surface_removal_method(service, version, mode, path + ["hidden_surface_removal_method"])
                self.event_poll_interval = self.__class__.event_poll_interval(service, version, mode, path + ["event_poll_interval"])
                self.animation_option = self.__class__.animation_option(service, version, mode, path + ["animation_option"])
                self.event_poll_timeout = self.__class__.event_poll_timeout(service, version, mode, path + ["event_poll_timeout"])
                self.rotation_centerpoint_visible = self.__class__.rotation_centerpoint_visible(service, version, mode, path + ["rotation_centerpoint_visible"])
                self.remove_partition_lines = self.__class__.remove_partition_lines(service, version, mode, path + ["remove_partition_lines"])
                self.test_use_external_function = self.__class__.test_use_external_function(service, version, mode, path + ["test_use_external_function"])
                self.max_graphics_text_size = self.__class__.max_graphics_text_size(service, version, mode, path + ["max_graphics_text_size"])
                self.min_graphics_text_size = self.__class__.min_graphics_text_size(service, version, mode, path + ["min_graphics_text_size"])
                self.force_key_frame_animation_markers_to_off = self.__class__.force_key_frame_animation_markers_to_off(service, version, mode, path + ["force_key_frame_animation_markers_to_off"])
                self.higher_resolution_graphics_window_line_width = self.__class__.higher_resolution_graphics_window_line_width(service, version, mode, path + ["higher_resolution_graphics_window_line_width"])
                self.text_window_line_width = self.__class__.text_window_line_width(service, version, mode, path + ["text_window_line_width"])
                self.scroll_wheel_event_end_timer = self.__class__.scroll_wheel_event_end_timer(service, version, mode, path + ["scroll_wheel_event_end_timer"])
                self.plot_legend_margin = self.__class__.plot_legend_margin(service, version, mode, path + ["plot_legend_margin"])
                self.enable_non_object_based_workflow = self.__class__.enable_non_object_based_workflow(service, version, mode, path + ["enable_non_object_based_workflow"])
                self.remove_partition_lines_tolerance = self.__class__.remove_partition_lines_tolerance(service, version, mode, path + ["remove_partition_lines_tolerance"])
                self.graphics_window_point_symbol = self.__class__.graphics_window_point_symbol(service, version, mode, path + ["graphics_window_point_symbol"])
                self.switch_to_open_glfor_remote_visualization = self.__class__.switch_to_open_glfor_remote_visualization(service, version, mode, path + ["switch_to_open_glfor_remote_visualization"])
                self.backface_cull = self.__class__.backface_cull(service, version, mode, path + ["backface_cull"])
                self.lower_resolution_graphics_window_line_width = self.__class__.lower_resolution_graphics_window_line_width(service, version, mode, path + ["lower_resolution_graphics_window_line_width"])
                self.surface_general_displacement = self.__class__.surface_general_displacement(service, version, mode, path + ["surface_general_displacement"])
                super().__init__(service, version, mode, path)
            class show_hidden_surfaces(TUIMethod):
                """
                Enable/disable the display of hidden surfaces.
                """
            class point_tool_size(TUIMethod):
                """
                Specify the size of the point tool (10-100).
                """
            class set_camera_normal_to_surface_increments(TUIMethod):
                """
                .
                """
            class show_hidden_lines(TUIMethod):
                """
                .
                """
            class double_buffering(TUIMethod):
                """
                Enable/disable double-buffering, which reduces screen flicker, but may use more memory on some machines.
                """
            class marker_drawing_mode(TUIMethod):
                """
                .
                """
            class graphics_window_line_width(TUIMethod):
                """
                Specify the thickness of lines that appear in the graphics window.
                """
            class hidden_surface_removal_method(TUIMethod):
                """
                Specify the method for removing hidden surfaces. These methods vary in speed and quality, depending on your machine.
                """
            class event_poll_interval(TUIMethod):
                """
                .
                """
            class animation_option(TUIMethod):
                """
                Specify whether the entire model or just a wireframe is shown during manipulations in the graphics window.
                """
            class event_poll_timeout(TUIMethod):
                """
                .
                """
            class rotation_centerpoint_visible(TUIMethod):
                """
                .
                """
            class remove_partition_lines(TUIMethod):
                """
                .
                """
            class test_use_external_function(TUIMethod):
                """
                .
                """
            class max_graphics_text_size(TUIMethod):
                """
                .
                """
            class min_graphics_text_size(TUIMethod):
                """
                .
                """
            class force_key_frame_animation_markers_to_off(TUIMethod):
                """
                .
                """
            class higher_resolution_graphics_window_line_width(TUIMethod):
                """
                .
                """
            class text_window_line_width(TUIMethod):
                """
                .
                """
            class scroll_wheel_event_end_timer(TUIMethod):
                """
                .
                """
            class plot_legend_margin(TUIMethod):
                """
                .
                """
            class enable_non_object_based_workflow(TUIMethod):
                """
                .
                """
            class remove_partition_lines_tolerance(TUIMethod):
                """
                .
                """
            class graphics_window_point_symbol(TUIMethod):
                """
                Specify the symbol used for indicating points in the graphics window (like the points in an XY plot).
                """
            class switch_to_open_glfor_remote_visualization(TUIMethod):
                """
                .
                """
            class backface_cull(TUIMethod):
                """
                .
                """
            class lower_resolution_graphics_window_line_width(TUIMethod):
                """
                .
                """
            class surface_general_displacement(TUIMethod):
                """
                .
                """

            class performance(TUIMenu):
                """
                Enter the menu for selecting the predefined graphics effects settings.
                """
                def __init__(self, service, version, mode, path):
                    self.fast_display_mode = self.__class__.fast_display_mode(service, version, mode, path + ["fast_display_mode"])
                    self.minimum_frame_rate = self.__class__.minimum_frame_rate(service, version, mode, path + ["minimum_frame_rate"])
                    self.ratio_of_target_frame_rate_to_classify_heavy_geometry = self.__class__.ratio_of_target_frame_rate_to_classify_heavy_geometry(service, version, mode, path + ["ratio_of_target_frame_rate_to_classify_heavy_geometry"])
                    self.optimize_for = self.__class__.optimize_for(service, version, mode, path + ["optimize_for"])
                    self.ratio_of_target_frame_rate_to_declassify_heavy_geometry = self.__class__.ratio_of_target_frame_rate_to_declassify_heavy_geometry(service, version, mode, path + ["ratio_of_target_frame_rate_to_declassify_heavy_geometry"])
                    super().__init__(service, version, mode, path)
                class ratio_of_target_frame_rate_to_classify_heavy_geometry(TUIMethod):
                    """
                    .
                    """
                class optimize_for(TUIMethod):
                    """
                    Choose a preset selection for how graphics are displayed.
                    """
                class ratio_of_target_frame_rate_to_declassify_heavy_geometry(TUIMethod):
                    """
                    .
                    """

                class fast_display_mode(TUIMenu):
                    """
                    .
                    """
                    def __init__(self, service, version, mode, path):
                        self.faces_shown = self.__class__.faces_shown(service, version, mode, path + ["faces_shown"])
                        self.perimeter_edges_shown = self.__class__.perimeter_edges_shown(service, version, mode, path + ["perimeter_edges_shown"])
                        self.transparency = self.__class__.transparency(service, version, mode, path + ["transparency"])
                        self.nodes_shown = self.__class__.nodes_shown(service, version, mode, path + ["nodes_shown"])
                        self.silhouette_shown = self.__class__.silhouette_shown(service, version, mode, path + ["silhouette_shown"])
                        self.status = self.__class__.status(service, version, mode, path + ["status"])
                        self.markers_decimation = self.__class__.markers_decimation(service, version, mode, path + ["markers_decimation"])
                        self.culling = self.__class__.culling(service, version, mode, path + ["culling"])
                        super().__init__(service, version, mode, path)
                    class faces_shown(TUIMethod):
                        """
                        .
                        """
                    class perimeter_edges_shown(TUIMethod):
                        """
                        .
                        """
                    class transparency(TUIMethod):
                        """
                        .
                        """
                    class nodes_shown(TUIMethod):
                        """
                        .
                        """
                    class silhouette_shown(TUIMethod):
                        """
                        .
                        """
                    class status(TUIMethod):
                        """
                        .
                        """
                    class markers_decimation(TUIMethod):
                        """
                        .
                        """
                    class culling(TUIMethod):
                        """
                        .
                        """

                class minimum_frame_rate(TUIMenu):
                    """
                    Enter the menu for minimum frame-rate settings.
                    """
                    def __init__(self, service, version, mode, path):
                        self.target_fps = self.__class__.target_fps(service, version, mode, path + ["target_fps"])
                        self.fixed_culling_value = self.__class__.fixed_culling_value(service, version, mode, path + ["fixed_culling_value"])
                        self.dynamic_adjustment = self.__class__.dynamic_adjustment(service, version, mode, path + ["dynamic_adjustment"])
                        self.minimum_culling_threshold = self.__class__.minimum_culling_threshold(service, version, mode, path + ["minimum_culling_threshold"])
                        self.enabled = self.__class__.enabled(service, version, mode, path + ["enabled"])
                        self.maximum_culling_threshold = self.__class__.maximum_culling_threshold(service, version, mode, path + ["maximum_culling_threshold"])
                        super().__init__(service, version, mode, path)
                    class target_fps(TUIMethod):
                        """
                        Specify the target frames-per-second.
                        """
                    class fixed_culling_value(TUIMethod):
                        """
                        .
                        """
                    class dynamic_adjustment(TUIMethod):
                        """
                        Enable/disable dynamic adjustment of quality loss per frame to get to the desired frame rate.
                        """
                    class minimum_culling_threshold(TUIMethod):
                        """
                        With minimum frame rate enabled, Fluent will cull at least this number of pixels.
                        """
                    class enabled(TUIMethod):
                        """
                        Enable/disable minimum frame rate.
                        """
                    class maximum_culling_threshold(TUIMethod):
                        """
                        With minimum frame rate enabled, Fluent will not cull beyond this number of pixels.
                        """

            class colormap_settings(TUIMenu):
                """
                Enter the colormap settings menu.
                """
                def __init__(self, service, version, mode, path):
                    self.number_format_precision = self.__class__.number_format_precision(service, version, mode, path + ["number_format_precision"])
                    self.preserve_aspect_ratio_for_hardcopy = self.__class__.preserve_aspect_ratio_for_hardcopy(service, version, mode, path + ["preserve_aspect_ratio_for_hardcopy"])
                    self.labels = self.__class__.labels(service, version, mode, path + ["labels"])
                    self.colormap = self.__class__.colormap(service, version, mode, path + ["colormap"])
                    self.text_behavior = self.__class__.text_behavior(service, version, mode, path + ["text_behavior"])
                    self.log_scale = self.__class__.log_scale(service, version, mode, path + ["log_scale"])
                    self.show_colormap = self.__class__.show_colormap(service, version, mode, path + ["show_colormap"])
                    self.skip_value = self.__class__.skip_value(service, version, mode, path + ["skip_value"])
                    self.number_format_type = self.__class__.number_format_type(service, version, mode, path + ["number_format_type"])
                    self.text_font_automatic_horizontal_size = self.__class__.text_font_automatic_horizontal_size(service, version, mode, path + ["text_font_automatic_horizontal_size"])
                    self.type = self.__class__.type(service, version, mode, path + ["type"])
                    self.automatic_resize = self.__class__.automatic_resize(service, version, mode, path + ["automatic_resize"])
                    self.isolines_position_offset = self.__class__.isolines_position_offset(service, version, mode, path + ["isolines_position_offset"])
                    self.levels = self.__class__.levels(service, version, mode, path + ["levels"])
                    self.text_font_fixed_units = self.__class__.text_font_fixed_units(service, version, mode, path + ["text_font_fixed_units"])
                    self.text_font_automatic_units = self.__class__.text_font_automatic_units(service, version, mode, path + ["text_font_automatic_units"])
                    self.aspect_ratio_when_horizontal = self.__class__.aspect_ratio_when_horizontal(service, version, mode, path + ["aspect_ratio_when_horizontal"])
                    self.text_truncation_limit_for_horizontal_colormaps = self.__class__.text_truncation_limit_for_horizontal_colormaps(service, version, mode, path + ["text_truncation_limit_for_horizontal_colormaps"])
                    self.use_no_sub_windows = self.__class__.use_no_sub_windows(service, version, mode, path + ["use_no_sub_windows"])
                    self.text_font_fixed_horizontal_size = self.__class__.text_font_fixed_horizontal_size(service, version, mode, path + ["text_font_fixed_horizontal_size"])
                    self.max_size_scale_factor = self.__class__.max_size_scale_factor(service, version, mode, path + ["max_size_scale_factor"])
                    self.border_style = self.__class__.border_style(service, version, mode, path + ["border_style"])
                    self.margin_from_edge_to_screen_ratio = self.__class__.margin_from_edge_to_screen_ratio(service, version, mode, path + ["margin_from_edge_to_screen_ratio"])
                    self.auto_refit_on_resize = self.__class__.auto_refit_on_resize(service, version, mode, path + ["auto_refit_on_resize"])
                    self.aspect_ratio_when_vertical = self.__class__.aspect_ratio_when_vertical(service, version, mode, path + ["aspect_ratio_when_vertical"])
                    self.text_font_fixed_vertical_size = self.__class__.text_font_fixed_vertical_size(service, version, mode, path + ["text_font_fixed_vertical_size"])
                    self.min_size_scale_factor = self.__class__.min_size_scale_factor(service, version, mode, path + ["min_size_scale_factor"])
                    self.text_truncation_limit_for_vertical_colormaps = self.__class__.text_truncation_limit_for_vertical_colormaps(service, version, mode, path + ["text_truncation_limit_for_vertical_colormaps"])
                    self.major_length_to_screen_ratio_when_horizontal = self.__class__.major_length_to_screen_ratio_when_horizontal(service, version, mode, path + ["major_length_to_screen_ratio_when_horizontal"])
                    self.text_font_fixed_size = self.__class__.text_font_fixed_size(service, version, mode, path + ["text_font_fixed_size"])
                    self.major_length_to_screen_ratio_when_vertical = self.__class__.major_length_to_screen_ratio_when_vertical(service, version, mode, path + ["major_length_to_screen_ratio_when_vertical"])
                    self.alignment = self.__class__.alignment(service, version, mode, path + ["alignment"])
                    self.text_font_automatic_size = self.__class__.text_font_automatic_size(service, version, mode, path + ["text_font_automatic_size"])
                    self.text_font_automatic_vertical_size = self.__class__.text_font_automatic_vertical_size(service, version, mode, path + ["text_font_automatic_vertical_size"])
                    self.text_font_name = self.__class__.text_font_name(service, version, mode, path + ["text_font_name"])
                    super().__init__(service, version, mode, path)
                class number_format_precision(TUIMethod):
                    """
                    Specify the colormap number label precision.
                    """
                class preserve_aspect_ratio_for_hardcopy(TUIMethod):
                    """
                    .
                    """
                class labels(TUIMethod):
                    """
                    Specify whether there is a label for every colormap value or if some are skipped.
                    """
                class colormap(TUIMethod):
                    """
                    Choose the default colormap.
                    """
                class text_behavior(TUIMethod):
                    """
                    Specify whether colormap label text automatically scales with the colormap size.
                    """
                class log_scale(TUIMethod):
                    """
                    Enable/disable the use of a logarithmic scale for the colormap.
                    """
                class show_colormap(TUIMethod):
                    """
                    Enable/disable the display of colormaps.
                    """
                class skip_value(TUIMethod):
                    """
                    Specify how many number labels are skipped in the colormap.
                    """
                class number_format_type(TUIMethod):
                    """
                    Specify how colormap numbers are displayed.
                    """
                class text_font_automatic_horizontal_size(TUIMethod):
                    """
                    .
                    """
                class type(TUIMethod):
                    """
                    Specify whether the colormap appearance is smooth or banded.
                    """
                class automatic_resize(TUIMethod):
                    """
                    .
                    """
                class isolines_position_offset(TUIMethod):
                    """
                    .
                    """
                class levels(TUIMethod):
                    """
                    Specify the default colormap size.
                    """
                class text_font_fixed_units(TUIMethod):
                    """
                    .
                    """
                class text_font_automatic_units(TUIMethod):
                    """
                    .
                    """
                class aspect_ratio_when_horizontal(TUIMethod):
                    """
                    .
                    """
                class text_truncation_limit_for_horizontal_colormaps(TUIMethod):
                    """
                    .
                    """
                class use_no_sub_windows(TUIMethod):
                    """
                    .
                    """
                class text_font_fixed_horizontal_size(TUIMethod):
                    """
                    .
                    """
                class max_size_scale_factor(TUIMethod):
                    """
                    .
                    """
                class border_style(TUIMethod):
                    """
                    Specify how/when the colormap border appears.
                    """
                class margin_from_edge_to_screen_ratio(TUIMethod):
                    """
                    .
                    """
                class auto_refit_on_resize(TUIMethod):
                    """
                    .
                    """
                class aspect_ratio_when_vertical(TUIMethod):
                    """
                    Specify the length vs. width ratio for a vertical colormap, which controls the thickness of the colormap; smaller values mean a thicker colormap.
                    """
                class text_font_fixed_vertical_size(TUIMethod):
                    """
                    .
                    """
                class min_size_scale_factor(TUIMethod):
                    """
                    .
                    """
                class text_truncation_limit_for_vertical_colormaps(TUIMethod):
                    """
                    .
                    """
                class major_length_to_screen_ratio_when_horizontal(TUIMethod):
                    """
                    .
                    """
                class text_font_fixed_size(TUIMethod):
                    """
                    Set the font size for colormap labels.
                    """
                class major_length_to_screen_ratio_when_vertical(TUIMethod):
                    """
                    Choose the length of the colormap as a fraction of graphics window height, when the colormap is vertical.
                    """
                class alignment(TUIMethod):
                    """
                    Specify the default colormap location.
                    """
                class text_font_automatic_size(TUIMethod):
                    """
                    .
                    """
                class text_font_automatic_vertical_size(TUIMethod):
                    """
                    Specify the initial font size as a ratio of the colormap overall size, for vertically aligned colormaps.
                    """
                class text_font_name(TUIMethod):
                    """
                    .
                    """

            class hardcopy_settings(TUIMenu):
                """
                Enter the menu for saving picture settings.
                """
                def __init__(self, service, version, mode, path):
                    self.retain_colormap_pos_for_avz = self.__class__.retain_colormap_pos_for_avz(service, version, mode, path + ["retain_colormap_pos_for_avz"])
                    self.hardware_image_accel = self.__class__.hardware_image_accel(service, version, mode, path + ["hardware_image_accel"])
                    self.post_script_permission_override = self.__class__.post_script_permission_override(service, version, mode, path + ["post_script_permission_override"])
                    self.hardcopy_driver = self.__class__.hardcopy_driver(service, version, mode, path + ["hardcopy_driver"])
                    self.hardcopy_line_width = self.__class__.hardcopy_line_width(service, version, mode, path + ["hardcopy_line_width"])
                    self.save_embedded_windows_in_hardcopy = self.__class__.save_embedded_windows_in_hardcopy(service, version, mode, path + ["save_embedded_windows_in_hardcopy"])
                    self.export_edges_for_avz = self.__class__.export_edges_for_avz(service, version, mode, path + ["export_edges_for_avz"])
                    self.transparent_embedded_windows = self.__class__.transparent_embedded_windows(service, version, mode, path + ["transparent_embedded_windows"])
                    self.save_embedded_hardcopies_separately = self.__class__.save_embedded_hardcopies_separately(service, version, mode, path + ["save_embedded_hardcopies_separately"])
                    super().__init__(service, version, mode, path)
                class retain_colormap_pos_for_avz(TUIMethod):
                    """
                    .
                    """
                class hardware_image_accel(TUIMethod):
                    """
                    .
                    """
                class post_script_permission_override(TUIMethod):
                    """
                    .
                    """
                class hardcopy_driver(TUIMethod):
                    """
                    Specify the default format for saving pictures.
                    """
                class hardcopy_line_width(TUIMethod):
                    """
                    Specify the thinkness of lines for saved pictures.
                    """
                class save_embedded_windows_in_hardcopy(TUIMethod):
                    """
                    .
                    """
                class export_edges_for_avz(TUIMethod):
                    """
                    .
                    """
                class transparent_embedded_windows(TUIMethod):
                    """
                    .
                    """
                class save_embedded_hardcopies_separately(TUIMethod):
                    """
                    .
                    """

            class material_effects(TUIMenu):
                """
                .
                """
                def __init__(self, service, version, mode, path):
                    self.tiling_style = self.__class__.tiling_style(service, version, mode, path + ["tiling_style"])
                    self.decimation_filter = self.__class__.decimation_filter(service, version, mode, path + ["decimation_filter"])
                    self.parameterization_source = self.__class__.parameterization_source(service, version, mode, path + ["parameterization_source"])
                    super().__init__(service, version, mode, path)
                class tiling_style(TUIMethod):
                    """
                    .
                    """
                class decimation_filter(TUIMethod):
                    """
                    .
                    """
                class parameterization_source(TUIMethod):
                    """
                    .
                    """

            class export_video_settings(TUIMenu):
                """
                .
                """
                def __init__(self, service, version, mode, path):
                    self.advanced_video_quality_options = self.__class__.advanced_video_quality_options(service, version, mode, path + ["advanced_video_quality_options"])
                    self.video_resoution_x = self.__class__.video_resoution_x(service, version, mode, path + ["video_resoution_x"])
                    self.video_use_frame_resolution = self.__class__.video_use_frame_resolution(service, version, mode, path + ["video_use_frame_resolution"])
                    self.video_scale = self.__class__.video_scale(service, version, mode, path + ["video_scale"])
                    self.video_format = self.__class__.video_format(service, version, mode, path + ["video_format"])
                    self.video_quality = self.__class__.video_quality(service, version, mode, path + ["video_quality"])
                    self.video_resoution_y = self.__class__.video_resoution_y(service, version, mode, path + ["video_resoution_y"])
                    self.video_fps = self.__class__.video_fps(service, version, mode, path + ["video_fps"])
                    self.video_smooth_scaling = self.__class__.video_smooth_scaling(service, version, mode, path + ["video_smooth_scaling"])
                    super().__init__(service, version, mode, path)
                class video_resoution_x(TUIMethod):
                    """
                    .
                    """
                class video_use_frame_resolution(TUIMethod):
                    """
                    .
                    """
                class video_scale(TUIMethod):
                    """
                    .
                    """
                class video_format(TUIMethod):
                    """
                    .
                    """
                class video_quality(TUIMethod):
                    """
                    .
                    """
                class video_resoution_y(TUIMethod):
                    """
                    .
                    """
                class video_fps(TUIMethod):
                    """
                    .
                    """
                class video_smooth_scaling(TUIMethod):
                    """
                    .
                    """

                class advanced_video_quality_options(TUIMenu):
                    """
                    .
                    """
                    def __init__(self, service, version, mode, path):
                        self.enable_h264 = self.__class__.enable_h264(service, version, mode, path + ["enable_h264"])
                        self.compression_method = self.__class__.compression_method(service, version, mode, path + ["compression_method"])
                        self.bitrate = self.__class__.bitrate(service, version, mode, path + ["bitrate"])
                        self.bit_rate_quality = self.__class__.bit_rate_quality(service, version, mode, path + ["bit_rate_quality"])
                        super().__init__(service, version, mode, path)
                    class enable_h264(TUIMethod):
                        """
                        .
                        """
                    class compression_method(TUIMethod):
                        """
                        .
                        """
                    class bitrate(TUIMethod):
                        """
                        .
                        """
                    class bit_rate_quality(TUIMethod):
                        """
                        .
                        """

            class manage_hoops_memory(TUIMenu):
                """
                .
                """
                def __init__(self, service, version, mode, path):
                    self.enabled = self.__class__.enabled(service, version, mode, path + ["enabled"])
                    self.hsfimport_limit = self.__class__.hsfimport_limit(service, version, mode, path + ["hsfimport_limit"])
                    super().__init__(service, version, mode, path)
                class enabled(TUIMethod):
                    """
                    .
                    """
                class hsfimport_limit(TUIMethod):
                    """
                    .
                    """

            class vector_settings(TUIMenu):
                """
                .
                """
                def __init__(self, service, version, mode, path):
                    self.arrowhead3_dradius1_factor = self.__class__.arrowhead3_dradius1_factor(service, version, mode, path + ["arrowhead3_dradius1_factor"])
                    self.arrow3_dradius2_factor = self.__class__.arrow3_dradius2_factor(service, version, mode, path + ["arrow3_dradius2_factor"])
                    self.arrow3_dradius1_factor = self.__class__.arrow3_dradius1_factor(service, version, mode, path + ["arrow3_dradius1_factor"])
                    self.line_arrow3_dperpendicular_radius = self.__class__.line_arrow3_dperpendicular_radius(service, version, mode, path + ["line_arrow3_dperpendicular_radius"])
                    super().__init__(service, version, mode, path)
                class arrowhead3_dradius1_factor(TUIMethod):
                    """
                    .
                    """
                class arrow3_dradius2_factor(TUIMethod):
                    """
                    .
                    """
                class arrow3_dradius1_factor(TUIMethod):
                    """
                    .
                    """
                class line_arrow3_dperpendicular_radius(TUIMethod):
                    """
                    .
                    """

            class ray_tracing_options(TUIMenu):
                """
                .
                """
                def __init__(self, service, version, mode, path):
                    self.volume_rendering_method = self.__class__.volume_rendering_method(service, version, mode, path + ["volume_rendering_method"])
                    super().__init__(service, version, mode, path)
                class volume_rendering_method(TUIMethod):
                    """
                    .
                    """

            class lighting(TUIMenu):
                """
                Enter the lighting menu.
                """
                def __init__(self, service, version, mode, path):
                    self.headlight_intensity = self.__class__.headlight_intensity(service, version, mode, path + ["headlight_intensity"])
                    self.lighting_method = self.__class__.lighting_method(service, version, mode, path + ["lighting_method"])
                    self.ambient_light_intensity = self.__class__.ambient_light_intensity(service, version, mode, path + ["ambient_light_intensity"])
                    self.headlight = self.__class__.headlight(service, version, mode, path + ["headlight"])
                    super().__init__(service, version, mode, path)
                class headlight_intensity(TUIMethod):
                    """
                    Specify the intensity of the headlight.
                    """
                class lighting_method(TUIMethod):
                    """
                    Specify the default lighting method.
                    """
                class ambient_light_intensity(TUIMethod):
                    """
                    .
                    """
                class headlight(TUIMethod):
                    """
                    Turn the headlight on or off or set it as automatic.
                    """

            class boundary_markers(TUIMenu):
                """
                Enter the boundary markers menu.
                """
                def __init__(self, service, version, mode, path):
                    self.inlet_color = self.__class__.inlet_color(service, version, mode, path + ["inlet_color"])
                    self.outlet_color = self.__class__.outlet_color(service, version, mode, path + ["outlet_color"])
                    self.marker_size_limiting_scale_multiplier = self.__class__.marker_size_limiting_scale_multiplier(service, version, mode, path + ["marker_size_limiting_scale_multiplier"])
                    self.color_option = self.__class__.color_option(service, version, mode, path + ["color_option"])
                    self.markers_limit = self.__class__.markers_limit(service, version, mode, path + ["markers_limit"])
                    self.scale_marker = self.__class__.scale_marker(service, version, mode, path + ["scale_marker"])
                    self.show_inlet_markers = self.__class__.show_inlet_markers(service, version, mode, path + ["show_inlet_markers"])
                    self.enabled = self.__class__.enabled(service, version, mode, path + ["enabled"])
                    self.automatic_marker_scaling = self.__class__.automatic_marker_scaling(service, version, mode, path + ["automatic_marker_scaling"])
                    self.marker_fraction = self.__class__.marker_fraction(service, version, mode, path + ["marker_fraction"])
                    self.exclude_from_bounding = self.__class__.exclude_from_bounding(service, version, mode, path + ["exclude_from_bounding"])
                    self.show_outlet_markers = self.__class__.show_outlet_markers(service, version, mode, path + ["show_outlet_markers"])
                    super().__init__(service, version, mode, path)
                class inlet_color(TUIMethod):
                    """
                    Specify the color of the inlet boundary markers.
                    """
                class outlet_color(TUIMethod):
                    """
                    Specify the color of the outlet boundary markers.
                    """
                class marker_size_limiting_scale_multiplier(TUIMethod):
                    """
                    .
                    """
                class color_option(TUIMethod):
                    """
                    Specify whether boundary markers are a fixed color or if they match the color of the surface they are identifying.
                    """
                class markers_limit(TUIMethod):
                    """
                    .
                    """
                class scale_marker(TUIMethod):
                    """
                    Specify the scale factor for the boundary markers (0.1-10), which controls the overall size of the markers.
                    """
                class show_inlet_markers(TUIMethod):
                    """
                    Enable/disable the display of boundary markers for inlets.
                    """
                class enabled(TUIMethod):
                    """
                    Enable/disable boundary marker display.
                    """
                class automatic_marker_scaling(TUIMethod):
                    """
                    .
                    """
                class marker_fraction(TUIMethod):
                    """
                    Specify marker density factor (0.1-1).
                    """
                class exclude_from_bounding(TUIMethod):
                    """
                    .
                    """
                class show_outlet_markers(TUIMethod):
                    """
                    Enable/disable the display of boundary markers for outlets.
                    """

            class graphics_effects(TUIMenu):
                """
                Enter the graphics effects menu.
                """
                def __init__(self, service, version, mode, path):
                    self.grid_color = self.__class__.grid_color(service, version, mode, path + ["grid_color"])
                    self.update_after_mouse_release = self.__class__.update_after_mouse_release(service, version, mode, path + ["update_after_mouse_release"])
                    self.plane_direction = self.__class__.plane_direction(service, version, mode, path + ["plane_direction"])
                    self.grid_plane_enabled = self.__class__.grid_plane_enabled(service, version, mode, path + ["grid_plane_enabled"])
                    self.show_edge_reflections = self.__class__.show_edge_reflections(service, version, mode, path + ["show_edge_reflections"])
                    self.grid_plane_offset = self.__class__.grid_plane_offset(service, version, mode, path + ["grid_plane_offset"])
                    self.bloom_blur = self.__class__.bloom_blur(service, version, mode, path + ["bloom_blur"])
                    self.ambient_occlusion_strength = self.__class__.ambient_occlusion_strength(service, version, mode, path + ["ambient_occlusion_strength"])
                    self.grid_plane_size_factor = self.__class__.grid_plane_size_factor(service, version, mode, path + ["grid_plane_size_factor"])
                    self.ambient_occlusion_enabled = self.__class__.ambient_occlusion_enabled(service, version, mode, path + ["ambient_occlusion_enabled"])
                    self.reflections_enabled = self.__class__.reflections_enabled(service, version, mode, path + ["reflections_enabled"])
                    self.bloom_strength = self.__class__.bloom_strength(service, version, mode, path + ["bloom_strength"])
                    self.ambient_occlusion_quality = self.__class__.ambient_occlusion_quality(service, version, mode, path + ["ambient_occlusion_quality"])
                    self.anti_aliasing = self.__class__.anti_aliasing(service, version, mode, path + ["anti_aliasing"])
                    self.shadow_map_enabled = self.__class__.shadow_map_enabled(service, version, mode, path + ["shadow_map_enabled"])
                    self.bloom_enabled = self.__class__.bloom_enabled(service, version, mode, path + ["bloom_enabled"])
                    self.simple_shadows_enabled = self.__class__.simple_shadows_enabled(service, version, mode, path + ["simple_shadows_enabled"])
                    self.grid_plane_count = self.__class__.grid_plane_count(service, version, mode, path + ["grid_plane_count"])
                    self.show_marker_reflections = self.__class__.show_marker_reflections(service, version, mode, path + ["show_marker_reflections"])
                    super().__init__(service, version, mode, path)
                class grid_color(TUIMethod):
                    """
                    Specify the color of the grid lines when the ground plane grid is shown.
                    """
                class update_after_mouse_release(TUIMethod):
                    """
                    Enable/disable the updating of graphics effects as a model is being manipulated in the graphics window.
                    """
                class plane_direction(TUIMethod):
                    """
                    Specify the direction of the plane for the ground plane grid and reflections.
                    """
                class grid_plane_enabled(TUIMethod):
                    """
                    Enable/disable the display of the ground plane grid.
                    """
                class show_edge_reflections(TUIMethod):
                    """
                    Enable/disable the display of model edges in reflections. Note that this can negatively affect performance.
                    """
                class grid_plane_offset(TUIMethod):
                    """
                    Set the grid plane offset from the model as a percentage of the model size.
                    """
                class bloom_blur(TUIMethod):
                    """
                    .
                    """
                class ambient_occlusion_strength(TUIMethod):
                    """
                    .
                    """
                class grid_plane_size_factor(TUIMethod):
                    """
                    .
                    """
                class ambient_occlusion_enabled(TUIMethod):
                    """
                    .
                    """
                class reflections_enabled(TUIMethod):
                    """
                    Enable/disable model reflections (mirror-type reflections).
                    """
                class bloom_strength(TUIMethod):
                    """
                    .
                    """
                class ambient_occlusion_quality(TUIMethod):
                    """
                    .
                    """
                class anti_aliasing(TUIMethod):
                    """
                    Enable/disable the smoothing of lines and text.
                    """
                class shadow_map_enabled(TUIMethod):
                    """
                    Enable/disable dynamic shadows, which show shadows of geometric entities on other objects based on lighting and object orientation.
                    """
                class bloom_enabled(TUIMethod):
                    """
                    .
                    """
                class simple_shadows_enabled(TUIMethod):
                    """
                    Enable/disable the display of static shadows on the ground plane.
                    """
                class grid_plane_count(TUIMethod):
                    """
                    .
                    """
                class show_marker_reflections(TUIMethod):
                    """
                    .
                    """

            class transparency(TUIMenu):
                """
                .
                """
                def __init__(self, service, version, mode, path):
                    self.quick_moves = self.__class__.quick_moves(service, version, mode, path + ["quick_moves"])
                    self.depth_peeling_layers = self.__class__.depth_peeling_layers(service, version, mode, path + ["depth_peeling_layers"])
                    self.depth_peeling_preference = self.__class__.depth_peeling_preference(service, version, mode, path + ["depth_peeling_preference"])
                    self.zsort_options = self.__class__.zsort_options(service, version, mode, path + ["zsort_options"])
                    self.algorithm_for_modern_drivers = self.__class__.algorithm_for_modern_drivers(service, version, mode, path + ["algorithm_for_modern_drivers"])
                    super().__init__(service, version, mode, path)
                class quick_moves(TUIMethod):
                    """
                    .
                    """
                class depth_peeling_layers(TUIMethod):
                    """
                    .
                    """
                class depth_peeling_preference(TUIMethod):
                    """
                    .
                    """
                class zsort_options(TUIMethod):
                    """
                    .
                    """
                class algorithm_for_modern_drivers(TUIMethod):
                    """
                    .
                    """

            class embedded_windows(TUIMenu):
                """
                .
                """
                def __init__(self, service, version, mode, path):
                    self.save_embedded_window_layout = self.__class__.save_embedded_window_layout(service, version, mode, path + ["save_embedded_window_layout"])
                    self.default_embedded_mesh_windows_view = self.__class__.default_embedded_mesh_windows_view(service, version, mode, path + ["default_embedded_mesh_windows_view"])
                    self.show_border_for_embedded_window = self.__class__.show_border_for_embedded_window(service, version, mode, path + ["show_border_for_embedded_window"])
                    self.default_embedded_windows_view = self.__class__.default_embedded_windows_view(service, version, mode, path + ["default_embedded_windows_view"])
                    super().__init__(service, version, mode, path)
                class save_embedded_window_layout(TUIMethod):
                    """
                    .
                    """
                class default_embedded_mesh_windows_view(TUIMethod):
                    """
                    .
                    """
                class show_border_for_embedded_window(TUIMethod):
                    """
                    .
                    """
                class default_embedded_windows_view(TUIMethod):
                    """
                    .
                    """

            class meshing_mode(TUIMenu):
                """
                Enter the menu for meshing-specific graphics settings.
                """
                def __init__(self, service, version, mode, path):
                    self.graphics_window_display_timeout_value = self.__class__.graphics_window_display_timeout_value(service, version, mode, path + ["graphics_window_display_timeout_value"])
                    self.graphics_window_display_timeout = self.__class__.graphics_window_display_timeout(service, version, mode, path + ["graphics_window_display_timeout"])
                    super().__init__(service, version, mode, path)
                class graphics_window_display_timeout_value(TUIMethod):
                    """
                    Specify the graphics window display timeout value.
                    """
                class graphics_window_display_timeout(TUIMethod):
                    """
                    Enable/disable graphics window display timeout.
                    """

        class simulation(TUIMenu):
            """
            .
            """
            def __init__(self, service, version, mode, path):
                self.report_definitions = self.__class__.report_definitions(service, version, mode, path + ["report_definitions"])
                self.local_residual_scaling = self.__class__.local_residual_scaling(service, version, mode, path + ["local_residual_scaling"])
                self.flow_model = self.__class__.flow_model(service, version, mode, path + ["flow_model"])
                self.pdf_combustion_robust_numerics = self.__class__.pdf_combustion_robust_numerics(service, version, mode, path + ["pdf_combustion_robust_numerics"])
                super().__init__(service, version, mode, path)
            class local_residual_scaling(TUIMethod):
                """
                .
                """
            class flow_model(TUIMethod):
                """
                .
                """
            class pdf_combustion_robust_numerics(TUIMethod):
                """
                .
                """

            class report_definitions(TUIMenu):
                """
                Enter the menu for report definition preferences.
                """
                def __init__(self, service, version, mode, path):
                    self.report_plot_history_data_size = self.__class__.report_plot_history_data_size(service, version, mode, path + ["report_plot_history_data_size"])
                    self.automatic_plot_file = self.__class__.automatic_plot_file(service, version, mode, path + ["automatic_plot_file"])
                    super().__init__(service, version, mode, path)
                class report_plot_history_data_size(TUIMethod):
                    """
                    Specify how many data points are read from the associated report file and plotted in the graphics window. If the case/data files are already open, read the case and data again, after changing this setting, and re-plot to see the updated report plot.
                    """
                class automatic_plot_file(TUIMethod):
                    """
                    New report definitions will automatically create associated report files and plots.
                    """

    class report(TUIMenu):
        """
        Enter the report menu.
        """
        def __init__(self, service, version, mode, path):
            self.unrefined_cells = self.__class__.unrefined_cells(service, version, mode, path + ["unrefined_cells"])
            self.cell_size_limits = self.__class__.cell_size_limits(service, version, mode, path + ["cell_size_limits"])
            self.neighborhood_quality = self.__class__.neighborhood_quality(service, version, mode, path + ["neighborhood_quality"])
            self.boundary_cell_quality = self.__class__.boundary_cell_quality(service, version, mode, path + ["boundary_cell_quality"])
            self.edge_size_limits = self.__class__.edge_size_limits(service, version, mode, path + ["edge_size_limits"])
            self.cell_quality_limits = self.__class__.cell_quality_limits(service, version, mode, path + ["cell_quality_limits"])
            self.meshing_time = self.__class__.meshing_time(service, version, mode, path + ["meshing_time"])
            self.enhanced_orthogonal_quality = self.__class__.enhanced_orthogonal_quality(service, version, mode, path + ["enhanced_orthogonal_quality"])
            self.cell_distribution = self.__class__.cell_distribution(service, version, mode, path + ["cell_distribution"])
            self.number_meshed = self.__class__.number_meshed(service, version, mode, path + ["number_meshed"])
            self.face_zone_at_location = self.__class__.face_zone_at_location(service, version, mode, path + ["face_zone_at_location"])
            self.face_size_limits = self.__class__.face_size_limits(service, version, mode, path + ["face_size_limits"])
            self.face_node_degree_distribution = self.__class__.face_node_degree_distribution(service, version, mode, path + ["face_node_degree_distribution"])
            self.cell_zone_at_location = self.__class__.cell_zone_at_location(service, version, mode, path + ["cell_zone_at_location"])
            self.quality_method = self.__class__.quality_method(service, version, mode, path + ["quality_method"])
            self.spy_level = self.__class__.spy_level(service, version, mode, path + ["spy_level"])
            self.update_bounding_box = self.__class__.update_bounding_box(service, version, mode, path + ["update_bounding_box"])
            self.face_quality_limits = self.__class__.face_quality_limits(service, version, mode, path + ["face_quality_limits"])
            self.face_zone_area = self.__class__.face_zone_area(service, version, mode, path + ["face_zone_area"])
            self.verbosity_level = self.__class__.verbosity_level(service, version, mode, path + ["verbosity_level"])
            self.mesh_size = self.__class__.mesh_size(service, version, mode, path + ["mesh_size"])
            self.print_info = self.__class__.print_info(service, version, mode, path + ["print_info"])
            self.memory_usage = self.__class__.memory_usage(service, version, mode, path + ["memory_usage"])
            self.cell_zone_volume = self.__class__.cell_zone_volume(service, version, mode, path + ["cell_zone_volume"])
            self.mesh_statistics = self.__class__.mesh_statistics(service, version, mode, path + ["mesh_statistics"])
            self.face_distribution = self.__class__.face_distribution(service, version, mode, path + ["face_distribution"])
            self.list_cell_quality = self.__class__.list_cell_quality(service, version, mode, path + ["list_cell_quality"])
            super().__init__(service, version, mode, path)
        class unrefined_cells(TUIMethod):
            """
            Reports the number of cells that have not been refined.
            """
        class cell_size_limits(TUIMethod):
            """
            Reports the cell size limits.
            """
        class neighborhood_quality(TUIMethod):
            """
            Reports the maximum skewness, aspect ratio, or size change of all cells using a specified node.
            """
        class boundary_cell_quality(TUIMethod):
            """
            Reports the number and quality limits of boundary cells containing the specified number of boundary faces. If you specify zero for number of boundary faces, you will be prompted for number of boundary nodes.
            """
        class edge_size_limits(TUIMethod):
            """
            Reports the edge size limits.
            """
        class cell_quality_limits(TUIMethod):
            """
            Reports the cell quality limits.
            """
        class meshing_time(TUIMethod):
            """
            Report meshing time.
            """
        class enhanced_orthogonal_quality(TUIMethod):
            """
            Employs an enhanced definition of the orthogonal quality measure that combines a variety of quality measures, including: the orthogonality of a face relative to a vector between the face and cell centroids; a metric that detects poor cell shape at a local edge (such as twisting and/or concavity); and the variation of normals between the faces that can be constructed from the cell face. This definition is optimal for evaluating thin prism cells.
            """
        class cell_distribution(TUIMethod):
            """
            Reports the distribution of cell quality or size based on the bounding limits and number of partitions specified.
            """
        class number_meshed(TUIMethod):
            """
            Reports the number of elements that have been meshed.
            """
        class face_zone_at_location(TUIMethod):
            """
            Reports the face zone at the given location.
            """
        class face_size_limits(TUIMethod):
            """
            Reports the face size limits.
            """
        class face_node_degree_distribution(TUIMethod):
            """
            Reports the distribution of boundary faces based on face node degree. The node degree is the number of faces connected to the node. Specify the list of boundary face zones and the minimum and maximum face node degree to be reported. You can also consider only internal nodes, if required.
            """
        class cell_zone_at_location(TUIMethod):
            """
            Returns the cell zone at or closest to the specified location.
            """
        class quality_method(TUIMethod):
            """
            Specifies the method to be used for reporting face and cell quality.
            """
        class spy_level(TUIMethod):
            """
            Spy on meshing process.
            """
        class update_bounding_box(TUIMethod):
            """
            Updates the bounding box.
            """
        class face_quality_limits(TUIMethod):
            """
            Reports the face quality limits.
            """
        class face_zone_area(TUIMethod):
            """
            Reports the area of the specified face zone.
            """
        class verbosity_level(TUIMethod):
            """
            Specifies how much information should be displayed during mesh initialization, refinement and other operations. Changing the value to 2 from the default value of 1 will produce more messages, while changing it to 0 will disable all messages.
            """
        class mesh_size(TUIMethod):
            """
            Reports the number of nodes, faces, and cells in the mesh.
            """
        class print_info(TUIMethod):
            """
            Prints information about individual components of the mesh. This command also appears in the boundary menu. When you use this command, you will be prompted for an “entity” (that is, a node, face, or cell). An entity name consists of a prefix and an index. For a description of the displayed information see.
            """
        class memory_usage(TUIMethod):
            """
            Reports the amount of memory used for all nodes, faces, and cells, and the total memory allocated.
            """
        class cell_zone_volume(TUIMethod):
            """
            Reports the volume of the specified cell zone.
            """
        class mesh_statistics(TUIMethod):
            """
            Writes mesh statistics (such as zone information, number of cells, faces, and nodes, range of quality and size) to an external file.
            """
        class face_distribution(TUIMethod):
            """
            Reports the distribution of face quality or size based on the bounding limits and number of partitions specified.
            """
        class list_cell_quality(TUIMethod):
            """
            Reports a list of cells with the specified quality measure within a specified range. The valid prefixes are bn (boundary node), n (node), bf (boundary face), f (face), and c (cell).
            """

    class server(TUIMenu):
        """
        Enter the server menu.
        """
        def __init__(self, service, version, mode, path):
            self.print_web_server_info = self.__class__.print_web_server_info(service, version, mode, path + ["print_web_server_info"])
            self.start_web_server = self.__class__.start_web_server(service, version, mode, path + ["start_web_server"])
            self.stop_web_server = self.__class__.stop_web_server(service, version, mode, path + ["stop_web_server"])
            super().__init__(service, version, mode, path)
        class print_web_server_info(TUIMethod):
            """
            .
            """
        class start_web_server(TUIMethod):
            """
            .
            """
        class stop_web_server(TUIMethod):
            """
            .
            """

    class mesh(TUIMenu):
        """
        Enter the grid menu.
        """
        def __init__(self, service, version, mode, path):
            self.cavity = self.__class__.cavity(service, version, mode, path + ["cavity"])
            self.pyramid = self.__class__.pyramid(service, version, mode, path + ["pyramid"])
            self.poly = self.__class__.poly(service, version, mode, path + ["poly"])
            self.tet = self.__class__.tet(service, version, mode, path + ["tet"])
            self.domains = self.__class__.domains(service, version, mode, path + ["domains"])
            self.cartesian = self.__class__.cartesian(service, version, mode, path + ["cartesian"])
            self.cell_zone_conditions = self.__class__.cell_zone_conditions(service, version, mode, path + ["cell_zone_conditions"])
            self.poly_hexcore = self.__class__.poly_hexcore(service, version, mode, path + ["poly_hexcore"])
            self.auto_mesh_controls = self.__class__.auto_mesh_controls(service, version, mode, path + ["auto_mesh_controls"])
            self.scoped_prisms = self.__class__.scoped_prisms(service, version, mode, path + ["scoped_prisms"])
            self.prism = self.__class__.prism(service, version, mode, path + ["prism"])
            self.separate = self.__class__.separate(service, version, mode, path + ["separate"])
            self.non_conformals = self.__class__.non_conformals(service, version, mode, path + ["non_conformals"])
            self.modify = self.__class__.modify(service, version, mode, path + ["modify"])
            self.manage = self.__class__.manage(service, version, mode, path + ["manage"])
            self.thin_volume_mesh = self.__class__.thin_volume_mesh(service, version, mode, path + ["thin_volume_mesh"])
            self.hexcore = self.__class__.hexcore(service, version, mode, path + ["hexcore"])
            self.rapid_octree = self.__class__.rapid_octree(service, version, mode, path + ["rapid_octree"])
            self.activate_lean_datastructures = self.__class__.activate_lean_datastructures(service, version, mode, path + ["activate_lean_datastructures"])
            self.zone_names_clean_up = self.__class__.zone_names_clean_up(service, version, mode, path + ["zone_names_clean_up"])
            self.clear_mesh = self.__class__.clear_mesh(service, version, mode, path + ["clear_mesh"])
            self.create_frustrum = self.__class__.create_frustrum(service, version, mode, path + ["create_frustrum"])
            self.list_mesh_parameter = self.__class__.list_mesh_parameter(service, version, mode, path + ["list_mesh_parameter"])
            self.check_mesh = self.__class__.check_mesh(service, version, mode, path + ["check_mesh"])
            self.reset_mesh = self.__class__.reset_mesh(service, version, mode, path + ["reset_mesh"])
            self.laplace_smooth_nodes = self.__class__.laplace_smooth_nodes(service, version, mode, path + ["laplace_smooth_nodes"])
            self.reset_mesh_parameter = self.__class__.reset_mesh_parameter(service, version, mode, path + ["reset_mesh_parameter"])
            self.selective_mesh_check = self.__class__.selective_mesh_check(service, version, mode, path + ["selective_mesh_check"])
            self.create_heat_exchanger = self.__class__.create_heat_exchanger(service, version, mode, path + ["create_heat_exchanger"])
            self.deactivate_lean_datastructures = self.__class__.deactivate_lean_datastructures(service, version, mode, path + ["deactivate_lean_datastructures"])
            self.auto_prefix_cell_zones = self.__class__.auto_prefix_cell_zones(service, version, mode, path + ["auto_prefix_cell_zones"])
            self.check_quality_level = self.__class__.check_quality_level(service, version, mode, path + ["check_quality_level"])
            self.auto_mesh = self.__class__.auto_mesh(service, version, mode, path + ["auto_mesh"])
            self.auto_mesh_multiple_objects = self.__class__.auto_mesh_multiple_objects(service, version, mode, path + ["auto_mesh_multiple_objects"])
            self.prepare_for_solve = self.__class__.prepare_for_solve(service, version, mode, path + ["prepare_for_solve"])
            self.clear_undo_stack = self.__class__.clear_undo_stack(service, version, mode, path + ["clear_undo_stack"])
            self.cutcell = self.__class__.cutcell(service, version, mode, path + ["cutcell"])
            self.repair_face_handedness = self.__class__.repair_face_handedness(service, version, mode, path + ["repair_face_handedness"])
            self.check_quality = self.__class__.check_quality(service, version, mode, path + ["check_quality"])
            super().__init__(service, version, mode, path)
        class activate_lean_datastructures(TUIMethod):
            """
            Activates Lean data structures to reduce memory.
            """
        class zone_names_clean_up(TUIMethod):
            """
            S.
            """
        class clear_mesh(TUIMethod):
            """
            Enables you to generate a new mesh by deleting the internal mesh and leaving only the boundary faces and nodes.
            """
        class create_frustrum(TUIMethod):
            """
            Create a cylindrical hex mesh.
            """
        class list_mesh_parameter(TUIMethod):
            """
            Shows all mesh parameters.
            """
        class check_mesh(TUIMethod):
            """
            Checks the mesh for topological errors.
            """
        class reset_mesh(TUIMethod):
            """
            Clears the entire mesh.
            """
        class laplace_smooth_nodes(TUIMethod):
            """
            Applies a Laplacian smoothing operator to the mesh nodes. This command can be used for smoothing of all cell types, including prismatic cells.
            """
        class reset_mesh_parameter(TUIMethod):
            """
            Resets all parameters to their default value.
            """
        class selective_mesh_check(TUIMethod):
            """
            Performs a customized mesh check on specific zones rather than all zones.
            """
        class create_heat_exchanger(TUIMethod):
            """
            Creates the heat exchanger mesh. You need to specify the method for selecting the Location coordinates (by Position or Nodes), the location coordinates, the parameters for setting up mesh density (by Interval or Size), and the number of intervals (sizes) between points (nodes) 1–2, 1–3, 1–4. Also specify the object/zone name prefix and enable creating the mesh object, if required.
            """
        class deactivate_lean_datastructures(TUIMethod):
            """
            Deactivates Lean data structures.
            """
        class auto_prefix_cell_zones(TUIMethod):
            """
            Enables you to specify a prefix for cell zones created during the auto mesh procedure.   The auto-prefix-cell-zones command is not relevant for object-based meshing, where the cell zone names are generated based on the material points and the objects used to generate the mesh object.
            """
        class check_quality_level(TUIMethod):
            """
            Enables you to report additional quality metrics when set to 1.  In addition to the orthogonal quality and Fluent aspect ratio, additional metrics such as cell squish and skewness will be reported when the check-quality-level is set to 1.
            """
        class auto_mesh(TUIMethod):
            """
            Enables you to generate the volume mesh automatically. Specify a mesh object name for object-based auto mesh; if no name is given, face zone based auto mesh is performed. Specify the mesh elements to be used when prompted. Specify whether to merge the cells into a single zone or keep the cell zones separate. For face zone based meshing, specify whether automatically identify the domain to be meshed based on the topology information.
            """
        class auto_mesh_multiple_objects(TUIMethod):
            """
            Automatically executes initialization and refinement of mesh for multiple objects.
            """
        class prepare_for_solve(TUIMethod):
            """
            Prepares the mesh for solving in solution mode by performing a cleanup operation after the volume mesh has been generated. Operations such as deleting dead zones, deleting geometry objects, deleting edge zones, deleting unused faces and nodes are performed during this operation.
            """
        class clear_undo_stack(TUIMethod):
            """
            Clears undo stack.
            """
        class cutcell(TUIMethod):
            """
            Enters the cutcell menu. This menu is no longer supported, and will be removed in a future release.
            """
        class repair_face_handedness(TUIMethod):
            """
            Reverses face node orientation.
            """
        class check_quality(TUIMethod):
            """
            Enables you to ensure that the mesh quality is appropriate before transferring the mesh to the solution mode.
            """

        class cavity(TUIMenu):
            """
            Enters the cavity menu.
            """
            def __init__(self, service, version, mode, path):
                self.add_zones = self.__class__.add_zones(service, version, mode, path + ["add_zones"])
                self.remesh_hexcore_cavity = self.__class__.remesh_hexcore_cavity(service, version, mode, path + ["remesh_hexcore_cavity"])
                self.create_hexcore_cavity_by_region = self.__class__.create_hexcore_cavity_by_region(service, version, mode, path + ["create_hexcore_cavity_by_region"])
                self.create_hexcore_cavity_by_scale = self.__class__.create_hexcore_cavity_by_scale(service, version, mode, path + ["create_hexcore_cavity_by_scale"])
                self.remove_zones = self.__class__.remove_zones(service, version, mode, path + ["remove_zones"])
                self.merge_cavity = self.__class__.merge_cavity(service, version, mode, path + ["merge_cavity"])
                self.region = self.__class__.region(service, version, mode, path + ["region"])
                self.replace_zones = self.__class__.replace_zones(service, version, mode, path + ["replace_zones"])
                super().__init__(service, version, mode, path)
            class add_zones(TUIMethod):
                """
                Enables you to create a cavity for adding new zones to the existing volume mesh.
                """
            class remesh_hexcore_cavity(TUIMethod):
                """
                Remesh a cavity in hexcore mesh.
                """
            class create_hexcore_cavity_by_region(TUIMethod):
                """
                Creates the cavity in the hexcore mesh based on the zones and bounding box extents specified. The create-hexcore-cavity-by-region option is no longer supported and will be removed at a future release.
                """
            class create_hexcore_cavity_by_scale(TUIMethod):
                """
                Creates the cavity in the hexcore mesh based on the zones and scale specified. The create-hexcore-cavity-by-scale option is no longer supported and will be removed at a future release.
                """
            class remove_zones(TUIMethod):
                """
                Enables you to create a cavity for removing zones from the existing volume mesh.
                """
            class merge_cavity(TUIMethod):
                """
                Enables you to merge the specified cavity domain with the parent domain.  During the merging operation, the cavity cell zones merges with the zones in the parent domain. The wall boundaries extracted from the interior zones will be converted to  interior type and merged with the corresponding zones in the parent domain.
                """
            class region(TUIMethod):
                """
                Enables you to create a cavity to modify the existing volume mesh in the specified region.
                """
            class replace_zones(TUIMethod):
                """
                Enables you to create a cavity for removing a set of zones from an existing volume mesh and replacing them with new set of zones.
                """

        class pyramid(TUIMenu):
            """
            Enters the pyramid menu.
            """
            def __init__(self, service, version, mode, path):
                self.controls = self.__class__.controls(service, version, mode, path + ["controls"])
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                super().__init__(service, version, mode, path)
            class create(TUIMethod):
                """
                Creates a layer of pyramids on the quad face zone.
                """

            class controls(TUIMenu):
                """
                Enters the pyramid controls menu.
                """
                def __init__(self, service, version, mode, path):
                    self.vertex_method = self.__class__.vertex_method(service, version, mode, path + ["vertex_method"])
                    self.neighbor_angle = self.__class__.neighbor_angle(service, version, mode, path + ["neighbor_angle"])
                    self.offset_scaling = self.__class__.offset_scaling(service, version, mode, path + ["offset_scaling"])
                    self.offset_factor = self.__class__.offset_factor(service, version, mode, path + ["offset_factor"])
                    super().__init__(service, version, mode, path)
                class vertex_method(TUIMethod):
                    """
                    Specifies the method by which the location of the new vertex of the pyramid will be determined. The skewness method is used by default.
                    """
                class neighbor_angle(TUIMethod):
                    """
                    Sets the threshold dihedral angle used to limit the neighboring faces considered for pyramid creation. For example, if the value is set to 110° and the angle between a given quadrilateral face and a neighboring triangular face is greater than 110°, the resulting pyramid will not include the triangular face.
                    """
                class offset_scaling(TUIMethod):
                    """
                    Specifies the scaling, to be used to determine the height of the pyramid.
                    """
                class offset_factor(TUIMethod):
                    """
                    Specifies the fraction of the computed pyramid height (offset) by which the pyramid heights will be randomly adjusted. The default value is 0, indicating that all pyramids will have the exact height computed. A value of 0.1, for example, will limit each adjustment to ±10percentage of the computed height.
                    """

        class poly(TUIMenu):
            """
            Enters the polyhedral mesh generation menu.
            """
            def __init__(self, service, version, mode, path):
                self.local_regions = self.__class__.local_regions(service, version, mode, path + ["local_regions"])
                self.controls = self.__class__.controls(service, version, mode, path + ["controls"])
                self.collapse = self.__class__.collapse(service, version, mode, path + ["collapse"])
                self.improve = self.__class__.improve(service, version, mode, path + ["improve"])
                self.quality_method = self.__class__.quality_method(service, version, mode, path + ["quality_method"])
                self.remesh = self.__class__.remesh(service, version, mode, path + ["remesh"])
                super().__init__(service, version, mode, path)
            class collapse(TUIMethod):
                """
                Merge nodes to remove short edges and small faces. The decision threshold uses  edge size ratio, face size ratio, and (face)  area fraction.
                """
            class improve(TUIMethod):
                """
                Allows you to improve the polyhedral mesh quality based on the  quality-method.
                """
            class quality_method(TUIMethod):
                """
                Asks you to choose from internal-default,  orthoskew or squish quality measure for mesh improvement.
                """
            class remesh(TUIMethod):
                """
                Improves the quality in a local region based on the minimum skewness threshold.
                """

            class local_regions(TUIMenu):
                """
                Enters the local refinement menu.  Poly meshing follows tet meshing. These commands behave like the equivalent commands under /mesh/tet/local-regions/.
                """
                def __init__(self, service, version, mode, path):
                    self.deactivate = self.__class__.deactivate(service, version, mode, path + ["deactivate"])
                    self.refine = self.__class__.refine(service, version, mode, path + ["refine"])
                    self.init = self.__class__.init(service, version, mode, path + ["init"])
                    self.define = self.__class__.define(service, version, mode, path + ["define"])
                    self.ideal_area = self.__class__.ideal_area(service, version, mode, path + ["ideal_area"])
                    self.ideal_vol = self.__class__.ideal_vol(service, version, mode, path + ["ideal_vol"])
                    self.activate = self.__class__.activate(service, version, mode, path + ["activate"])
                    self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                    self.list_all_regions = self.__class__.list_all_regions(service, version, mode, path + ["list_all_regions"])
                    super().__init__(service, version, mode, path)
                class deactivate(TUIMethod):
                    """
                    Deactivates the specified regions for refinement.
                    """
                class refine(TUIMethod):
                    """
                    Refines the active cells inside the selected region based on the specified refinement parameters.
                    """
                class init(TUIMethod):
                    """
                    Defines the default refinement region encompassing the entire geometry.
                    """
                class define(TUIMethod):
                    """
                    Defines the refinement region according to the specified parameters.
                    """
                class ideal_area(TUIMethod):
                    """
                    Ideal triangle area for given edge length.
                    """
                class ideal_vol(TUIMethod):
                    """
                    Reports the volume of an ideal tetrahedron for the edge length specified.
                    """
                class activate(TUIMethod):
                    """
                    Activates the specified regions for refinement.
                    """
                class delete(TUIMethod):
                    """
                    Deletes the specified refinement region.
                    """
                class list_all_regions(TUIMethod):
                    """
                    Lists all refinement region parameters and the activated regions in the console.
                    """

            class controls(TUIMenu):
                """
                Enters the controls menu for setting poly parameters.
                """
                def __init__(self, service, version, mode, path):
                    self.smooth_controls = self.__class__.smooth_controls(service, version, mode, path + ["smooth_controls"])
                    self.prism = self.__class__.prism(service, version, mode, path + ["prism"])
                    self.face_size_ratio = self.__class__.face_size_ratio(service, version, mode, path + ["face_size_ratio"])
                    self.sliver_cell_area_fraction = self.__class__.sliver_cell_area_fraction(service, version, mode, path + ["sliver_cell_area_fraction"])
                    self.edge_size_ratio = self.__class__.edge_size_ratio(service, version, mode, path + ["edge_size_ratio"])
                    self.remesh_skew = self.__class__.remesh_skew(service, version, mode, path + ["remesh_skew"])
                    self.non_fluid_type = self.__class__.non_fluid_type(service, version, mode, path + ["non_fluid_type"])
                    self.improve = self.__class__.improve(service, version, mode, path + ["improve"])
                    self.merge_skew = self.__class__.merge_skew(service, version, mode, path + ["merge_skew"])
                    self.feature_angle = self.__class__.feature_angle(service, version, mode, path + ["feature_angle"])
                    self.cell_sizing = self.__class__.cell_sizing(service, version, mode, path + ["cell_sizing"])
                    super().__init__(service, version, mode, path)
                class face_size_ratio(TUIMethod):
                    """
                    Sets the threshold for the size ratio of two faces on one cell. Recommended range is 100 to 300.
                    """
                class sliver_cell_area_fraction(TUIMethod):
                    """
                    Sets the threshold for the area of a single face to the cell surface area. Recommended range is 0.00001 to 0.001.
                    """
                class edge_size_ratio(TUIMethod):
                    """
                    Sets the threshold for the size ratio of two connected edges. Recommended range is 20 to 200.
                    """
                class remesh_skew(TUIMethod):
                    """
                    Sets the target skewness when remeshing.
                    """
                class non_fluid_type(TUIMethod):
                    """
                    Selects the default type for non-fluid zones.
                    """
                class improve(TUIMethod):
                    """
                    Enables poly mesh improvement by smoothing based on the smooth-controls.
                    """
                class merge_skew(TUIMethod):
                    """
                    Sets the minimum skewness threshold for cell merge.
                    """
                class feature_angle(TUIMethod):
                    """
                    Sets the minimum threshold that should be preserved as a feature.
                    """
                class cell_sizing(TUIMethod):
                    """
                    Sets cell volume distribution function as geometric, linear, or size-field.
                    """

                class smooth_controls(TUIMenu):
                    """
                    Enters the menu for setting smoothing parameters for poly mesh.
                    """
                    def __init__(self, service, version, mode, path):
                        self.smooth_skew = self.__class__.smooth_skew(service, version, mode, path + ["smooth_skew"])
                        self.edge_smooth_iterations = self.__class__.edge_smooth_iterations(service, version, mode, path + ["edge_smooth_iterations"])
                        self.laplace_smooth_iterations = self.__class__.laplace_smooth_iterations(service, version, mode, path + ["laplace_smooth_iterations"])
                        self.smooth_iterations = self.__class__.smooth_iterations(service, version, mode, path + ["smooth_iterations"])
                        self.smooth_attempts = self.__class__.smooth_attempts(service, version, mode, path + ["smooth_attempts"])
                        self.centroid_smooth_iterations = self.__class__.centroid_smooth_iterations(service, version, mode, path + ["centroid_smooth_iterations"])
                        self.smooth_on_layer = self.__class__.smooth_on_layer(service, version, mode, path + ["smooth_on_layer"])
                        self.smooth_boundary = self.__class__.smooth_boundary(service, version, mode, path + ["smooth_boundary"])
                        super().__init__(service, version, mode, path)
                    class smooth_skew(TUIMethod):
                        """
                        Sets the minimum skewness threshold for poly mesh smoothing.
                        """
                    class edge_smooth_iterations(TUIMethod):
                        """
                        Sets the number of passes for tet-cell edge smoothing during the poly mesh generation phase.
                        """
                    class laplace_smooth_iterations(TUIMethod):
                        """
                        Sets the number of passes for tet-cell Laplace smoothing during the poly mesh generation phase.
                        """
                    class smooth_iterations(TUIMethod):
                        """
                        Sets the number of improvement passes over the full poly mesh.
                        """
                    class smooth_attempts(TUIMethod):
                        """
                        Sets the maximum number of movements for a single node during poly mesh smoothing.
                        """
                    class centroid_smooth_iterations(TUIMethod):
                        """
                        Sets the number of passes for tet-cell centroid smoothing during the poly mesh generation phase.
                        """
                    class smooth_on_layer(TUIMethod):
                        """
                        Constrains movement of nodes to maintain layering during poly mesh smoothing.
                        """
                    class smooth_boundary(TUIMethod):
                        """
                        Enables boundary smoothing as part of poly cell smoothing. Default is no.
                        """

                class prism(TUIMenu):
                    """
                    Poly prism transition controls.
                    """
                    def __init__(self, service, version, mode, path):
                        self.clear_growth = self.__class__.clear_growth(service, version, mode, path + ["clear_growth"])
                        self.apply_growth = self.__class__.apply_growth(service, version, mode, path + ["apply_growth"])
                        self.list_growth = self.__class__.list_growth(service, version, mode, path + ["list_growth"])
                        super().__init__(service, version, mode, path)
                    class clear_growth(TUIMethod):
                        """
                        Clear growth settings.
                        """
                    class apply_growth(TUIMethod):
                        """
                        Apply growth settings.
                        """
                    class list_growth(TUIMethod):
                        """
                        List growth settings.
                        """

        class tet(TUIMenu):
            """
            Enters the tetrahedral mesh menu.
            """
            def __init__(self, service, version, mode, path):
                self.improve = self.__class__.improve(service, version, mode, path + ["improve"])
                self.controls = self.__class__.controls(service, version, mode, path + ["controls"])
                self.local_regions = self.__class__.local_regions(service, version, mode, path + ["local_regions"])
                self.refine = self.__class__.refine(service, version, mode, path + ["refine"])
                self.un_preserve_cell_zone = self.__class__.un_preserve_cell_zone(service, version, mode, path + ["un_preserve_cell_zone"])
                self.init_refine = self.__class__.init_refine(service, version, mode, path + ["init_refine"])
                self.delete_virtual_cells = self.__class__.delete_virtual_cells(service, version, mode, path + ["delete_virtual_cells"])
                self.trace_path_between_cells = self.__class__.trace_path_between_cells(service, version, mode, path + ["trace_path_between_cells"])
                self.mesh_object = self.__class__.mesh_object(service, version, mode, path + ["mesh_object"])
                self.preserve_cell_zone = self.__class__.preserve_cell_zone(service, version, mode, path + ["preserve_cell_zone"])
                self.init = self.__class__.init(service, version, mode, path + ["init"])
                super().__init__(service, version, mode, path)
            class refine(TUIMethod):
                """
                Refines the initialized mesh.
                """
            class un_preserve_cell_zone(TUIMethod):
                """
                Un-preserve cell zone.
                """
            class init_refine(TUIMethod):
                """
                Generates the tetrahedral mesh.
                """
            class delete_virtual_cells(TUIMethod):
                """
                Deletes virtual cells created due to the use of the  keep-virtual-entities? option.
                """
            class trace_path_between_cells(TUIMethod):
                """
                Detects holes in the geometry by tracing the path between the two specified cells.
                """
            class mesh_object(TUIMethod):
                """
                Tet mesh object of type mesh.
                """
            class preserve_cell_zone(TUIMethod):
                """
                Allows you to specify the cell zones to be preserved during the meshing process.
                """
            class init(TUIMethod):
                """
                Generates the initial Delaunay mesh by meshing the boundary nodes.
                """

            class improve(TUIMenu):
                """
                Enters the tet improve menu.
                """
                def __init__(self, service, version, mode, path):
                    self.collapse_slivers = self.__class__.collapse_slivers(service, version, mode, path + ["collapse_slivers"])
                    self.sliver_boundary_swap = self.__class__.sliver_boundary_swap(service, version, mode, path + ["sliver_boundary_swap"])
                    self.refine_slivers = self.__class__.refine_slivers(service, version, mode, path + ["refine_slivers"])
                    self.improve_cells = self.__class__.improve_cells(service, version, mode, path + ["improve_cells"])
                    self.refine_boundary_slivers = self.__class__.refine_boundary_slivers(service, version, mode, path + ["refine_boundary_slivers"])
                    self.smooth_interior_sliver = self.__class__.smooth_interior_sliver(service, version, mode, path + ["smooth_interior_sliver"])
                    self.swap_faces = self.__class__.swap_faces(service, version, mode, path + ["swap_faces"])
                    self.smooth_boundary_sliver = self.__class__.smooth_boundary_sliver(service, version, mode, path + ["smooth_boundary_sliver"])
                    self.skew_smooth_nodes = self.__class__.skew_smooth_nodes(service, version, mode, path + ["skew_smooth_nodes"])
                    self.smooth_nodes = self.__class__.smooth_nodes(service, version, mode, path + ["smooth_nodes"])
                    super().__init__(service, version, mode, path)
                class collapse_slivers(TUIMethod):
                    """
                    Attempts to collapse the nodes of a skewed sliver cell on any one of its neighbors.
                    """
                class sliver_boundary_swap(TUIMethod):
                    """
                    Removes boundary slivers by moving the boundary to exclude the cells from the zone.
                    """
                class refine_slivers(TUIMethod):
                    """
                    Attempts to remove the sliver by placing a node at or near the centroid of the sliver cell. Swapping and smoothing are performed to improve the skewness. You can also specify whether boundary cells are to be refined. Refining the boundary cells may enable you to carry out further improvement options such as smoothing, swapping, and collapsing slivers.
                    """
                class improve_cells(TUIMethod):
                    """
                    Improves skewed tetrahedral cells.
                    """
                class refine_boundary_slivers(TUIMethod):
                    """
                    Attempts to increase the volume of boundary slivers to create a valid tet cell. Tetrahedra having one or two faces on the boundary are identified and then the appropriate edge split. The split node is then smoothed such that the volume of the tetrahedron increases, thereby creating a valid tet cell.
                    """
                class smooth_interior_sliver(TUIMethod):
                    """
                    Smooths non-boundary nodes on sliver cells having skewness greater than the specified threshold value. The default value for the skewness threshold is 0.985.
                    """
                class swap_faces(TUIMethod):
                    """
                    Performs interior face swapping to improve cell skewness.
                    """
                class smooth_boundary_sliver(TUIMethod):
                    """
                    Smooths nodes on sliver cells having all four nodes on the boundary until the skewness value is less than the specified value. The default values for the skewness threshold, minimum dihedral angle between boundary faces, and feature angle are 0.985, 10, and 30, respectively.
                    """
                class skew_smooth_nodes(TUIMethod):
                    """
                    Applies skewness-based smoothing to nodes on the tetrahedral cell zones to improve the mesh quality.
                    """
                class smooth_nodes(TUIMethod):
                    """
                    Enables you to apply either Laplacian or variational smoothing to nodes on the tetrahedral cell zones to improve the mesh quality.
                    """

            class controls(TUIMenu):
                """
                Enters the tet controls menu.
                """
                def __init__(self, service, version, mode, path):
                    self.remove_slivers = self.__class__.remove_slivers(service, version, mode, path + ["remove_slivers"])
                    self.advanced = self.__class__.advanced(service, version, mode, path + ["advanced"])
                    self.adv_front_method = self.__class__.adv_front_method(service, version, mode, path + ["adv_front_method"])
                    self.improve_mesh = self.__class__.improve_mesh(service, version, mode, path + ["improve_mesh"])
                    self.tet_improve = self.__class__.tet_improve(service, version, mode, path + ["tet_improve"])
                    self.merge_free_nodes = self.__class__.merge_free_nodes(service, version, mode, path + ["merge_free_nodes"])
                    self.print_region_based_sizing = self.__class__.print_region_based_sizing(service, version, mode, path + ["print_region_based_sizing"])
                    self.max_cell_volume = self.__class__.max_cell_volume(service, version, mode, path + ["max_cell_volume"])
                    self.clear_zone_growth_rate = self.__class__.clear_zone_growth_rate(service, version, mode, path + ["clear_zone_growth_rate"])
                    self.set_zone_growth_rate = self.__class__.set_zone_growth_rate(service, version, mode, path + ["set_zone_growth_rate"])
                    self.delete_unused_nodes = self.__class__.delete_unused_nodes(service, version, mode, path + ["delete_unused_nodes"])
                    self.skewness_method = self.__class__.skewness_method(service, version, mode, path + ["skewness_method"])
                    self.improve_surface_mesh = self.__class__.improve_surface_mesh(service, version, mode, path + ["improve_surface_mesh"])
                    self.max_cell_length = self.__class__.max_cell_length(service, version, mode, path + ["max_cell_length"])
                    self.compute_max_cell_volume = self.__class__.compute_max_cell_volume(service, version, mode, path + ["compute_max_cell_volume"])
                    self.use_max_cell_size = self.__class__.use_max_cell_size(service, version, mode, path + ["use_max_cell_size"])
                    self.cell_sizing = self.__class__.cell_sizing(service, version, mode, path + ["cell_sizing"])
                    self.non_fluid_type = self.__class__.non_fluid_type(service, version, mode, path + ["non_fluid_type"])
                    self.refine_method = self.__class__.refine_method(service, version, mode, path + ["refine_method"])
                    self.delete_dead_zones = self.__class__.delete_dead_zones(service, version, mode, path + ["delete_dead_zones"])
                    self.set_region_based_sizing = self.__class__.set_region_based_sizing(service, version, mode, path + ["set_region_based_sizing"])
                    super().__init__(service, version, mode, path)
                class merge_free_nodes(TUIMethod):
                    """
                    Automatically merge duplicate nodes?.
                    """
                class print_region_based_sizing(TUIMethod):
                    """
                    Displays local sizing settings (max cell length) for specified region(s).
                    """
                class max_cell_volume(TUIMethod):
                    """
                    Specifies the maximum allowable cell volume.
                    """
                class clear_zone_growth_rate(TUIMethod):
                    """
                    Clear zone specific geometric growth rates.
                    """
                class set_zone_growth_rate(TUIMethod):
                    """
                    Set zone specific geometric growth rates.
                    """
                class delete_unused_nodes(TUIMethod):
                    """
                    Toggles the deleting of unused nodes during mesh initialization.  The delete-unused-nodes? option is no longer supported and will be removed at a future release.
                    """
                class skewness_method(TUIMethod):
                    """
                    Enters the skewness refinement controls menu.
                    """
                class improve_surface_mesh(TUIMethod):
                    """
                    Enables you to improve the surface mesh by swapping face edges where Delaunay violations occur. The improve-surface-mesh? option is no longer supported and will be removed at a future release.
                    """
                class max_cell_length(TUIMethod):
                    """
                    Specifies the maximum allowable cell length.
                    """
                class compute_max_cell_volume(TUIMethod):
                    """
                    Computes the maximum cell volume for the current mesh.
                    """
                class use_max_cell_size(TUIMethod):
                    """
                    Enables you to use the maximum cell size specified instead of recomputing the value based on the objects, when the volume mesh is generated. This option is disabled by default.
                    """
                class cell_sizing(TUIMethod):
                    """
                    Specifies the cell sizing function for refinement. You can select geometric, linear, none, or size-field as appropriate.
                    """
                class non_fluid_type(TUIMethod):
                    """
                    Selects the non-fluid cell zone type. After the mesh is initialized, any non-fluid zones will be set to this type. If the mesh includes multiple regions (for example, the problem for which you are creating the mesh includes a fluid zone and one or more solid zones), and you plan to refine all of them using the same refinement parameters, modify the non-fluid type before generating the mesh.  For zone-based meshing, if any cell zone has at least one boundary zone type as inlet, it will automatically be set to fluid type. For object based meshing, volume region type is used to determine the cell zone type.
                    """
                class refine_method(TUIMethod):
                    """
                    Enables you to select the refinement method. You can select either skewness-based refinement or the advancing front method.  The skewness-based refinement option is no longer supported and will be removed at a future release.
                    """
                class delete_dead_zones(TUIMethod):
                    """
                    Specifies the maximum allowable cell volume.
                    """
                class set_region_based_sizing(TUIMethod):
                    """
                    Allows you to specify local sizing settings (max cell length) for specified region(s).
                    """

                class remove_slivers(TUIMenu):
                    """
                    Enters the sliver remove controls menu.
                    """
                    def __init__(self, service, version, mode, path):
                        self.method = self.__class__.method(service, version, mode, path + ["method"])
                        self.attempts = self.__class__.attempts(service, version, mode, path + ["attempts"])
                        self.iterations = self.__class__.iterations(service, version, mode, path + ["iterations"])
                        self.low_skew = self.__class__.low_skew(service, version, mode, path + ["low_skew"])
                        self.remove = self.__class__.remove(service, version, mode, path + ["remove"])
                        self.skew = self.__class__.skew(service, version, mode, path + ["skew"])
                        self.angle = self.__class__.angle(service, version, mode, path + ["angle"])
                        super().__init__(service, version, mode, path)
                    class method(TUIMethod):
                        """
                        Enables you to select the method for sliver removal. The default method used is the fast method. The fast and the aggressive methods use the same controls and give similar results for good quality surface meshes. In case of poor surface meshes, the aggressive method will typically succeed in improving the mesh to a greater extent, but it may be slower than the fast method.
                        """
                    class attempts(TUIMethod):
                        """
                        Specifies the number of attempts overall to remove slivers.
                        """
                    class iterations(TUIMethod):
                        """
                        Specifies the number of iterations to be performed for the specific sliver removal operation.
                        """
                    class low_skew(TUIMethod):
                        """
                        Specifies the targeted skewness threshold above which cells will be improved. The improve operation will attempt to improve cells with skewness above the low-skew value specified, but there will be no attempt to reduce the skewness below the specified value. A limited set of improve operations will be used as compared to the operations required for the skew value-based improvement.
                        """
                    class remove(TUIMethod):
                        """
                        Enables/disables the automatic removal of slivers.
                        """
                    class skew(TUIMethod):
                        """
                        Specifies the skewness threshold for sliver removal.
                        """
                    class angle(TUIMethod):
                        """
                        Specifies the maximum dihedral angle for considering the cell to be a sliver.
                        """

                class advanced(TUIMenu):
                    """
                    Tet advanced controls.
                    """
                    def __init__(self, service, version, mode, path):
                        self.defaults = self.__class__.defaults(service, version, mode, path + ["defaults"])
                        self.node_tolerance = self.__class__.node_tolerance(service, version, mode, path + ["node_tolerance"])
                        self.report_unmeshed_faces = self.__class__.report_unmeshed_faces(service, version, mode, path + ["report_unmeshed_faces"])
                        self.sliver_size = self.__class__.sliver_size(service, version, mode, path + ["sliver_size"])
                        self.max_nodes = self.__class__.max_nodes(service, version, mode, path + ["max_nodes"])
                        self.keep_virtual_entities = self.__class__.keep_virtual_entities(service, version, mode, path + ["keep_virtual_entities"])
                        self.max_cells = self.__class__.max_cells(service, version, mode, path + ["max_cells"])
                        self.report_unmeshed_nodes = self.__class__.report_unmeshed_nodes(service, version, mode, path + ["report_unmeshed_nodes"])
                        self.freeze_boundary_cells = self.__class__.freeze_boundary_cells(service, version, mode, path + ["freeze_boundary_cells"])
                        self.progress_reports = self.__class__.progress_reports(service, version, mode, path + ["progress_reports"])
                        self.report_max_unmeshed = self.__class__.report_max_unmeshed(service, version, mode, path + ["report_max_unmeshed"])
                        super().__init__(service, version, mode, path)
                    class defaults(TUIMethod):
                        """
                        Calculate defaults.
                        """
                    class node_tolerance(TUIMethod):
                        """
                        Set node-tolerance.
                        """
                    class report_unmeshed_faces(TUIMethod):
                        """
                        Report unmeshed faces.
                        """
                    class sliver_size(TUIMethod):
                        """
                        Set sliver-size.
                        """
                    class max_nodes(TUIMethod):
                        """
                        Set maximum number of nodes in mesh.
                        """
                    class keep_virtual_entities(TUIMethod):
                        """
                        Toggle deletion of virtual entities after intialization.
                        """
                    class max_cells(TUIMethod):
                        """
                        Set maximum number of cells in mesh.
                        """
                    class report_unmeshed_nodes(TUIMethod):
                        """
                        Report unmeshed nodes.
                        """
                    class freeze_boundary_cells(TUIMethod):
                        """
                        Freeze boundary cells .
                        """
                    class progress_reports(TUIMethod):
                        """
                        Set time between progress reports in seconds.
                        """
                    class report_max_unmeshed(TUIMethod):
                        """
                        Max number of unmeshed entities reported.
                        """

                class adv_front_method(TUIMenu):
                    """
                    Enters the advancing front refinement controls menu.
                    """
                    def __init__(self, service, version, mode, path):
                        self.skew_improve = self.__class__.skew_improve(service, version, mode, path + ["skew_improve"])
                        self.first_improve_params = self.__class__.first_improve_params(service, version, mode, path + ["first_improve_params"])
                        self.refine_parameters = self.__class__.refine_parameters(service, version, mode, path + ["refine_parameters"])
                        self.second_improve_params = self.__class__.second_improve_params(service, version, mode, path + ["second_improve_params"])
                        super().__init__(service, version, mode, path)
                    class first_improve_params(TUIMethod):
                        """
                        Defines the refining front improvement parameters for the advancing front method.
                        """
                    class refine_parameters(TUIMethod):
                        """
                        Defines the cell zone improvement parameters for the advancing front method.
                        """
                    class second_improve_params(TUIMethod):
                        """
                        Defines the cell zone improvement parameters for the advancing front method.
                        """

                    class skew_improve(TUIMenu):
                        """
                        Enters the refine improve controls menu.
                        """
                        def __init__(self, service, version, mode, path):
                            self.iterations = self.__class__.iterations(service, version, mode, path + ["iterations"])
                            self.boundary_sliver_skew = self.__class__.boundary_sliver_skew(service, version, mode, path + ["boundary_sliver_skew"])
                            self.target_skew = self.__class__.target_skew(service, version, mode, path + ["target_skew"])
                            self.target_low_skew = self.__class__.target_low_skew(service, version, mode, path + ["target_low_skew"])
                            self.attempts = self.__class__.attempts(service, version, mode, path + ["attempts"])
                            self.sliver_skew = self.__class__.sliver_skew(service, version, mode, path + ["sliver_skew"])
                            self.target = self.__class__.target(service, version, mode, path + ["target"])
                            super().__init__(service, version, mode, path)
                        class iterations(TUIMethod):
                            """
                            Specifies the number of improvement iterations in each attempt for the  advancing front method.
                            """
                        class boundary_sliver_skew(TUIMethod):
                            """
                            Specifies the boundary sliver skewness for the advancing front method. This  parameter is used for removing sliver cells along the boundary.
                            """
                        class target_skew(TUIMethod):
                            """
                            Specifies the targeted skewness during improvement for the advancing front  method.
                            """
                        class target_low_skew(TUIMethod):
                            """
                            Specifies the targeted skewness threshold above which cells will be improved.  The improve operation will attempt to improve cells with skewness above the target-low-skew value specified, but there will be no  attempt to reduce the skewness below the specified value. A limited set of improve  operations will be used as compared to the operations required for the target-skew value-based improvement. The value specified  could be approximately 0.1 lower than the target-skew  value.
                            """
                        class attempts(TUIMethod):
                            """
                            Specifies the number of overall improvement attempts for the advancing front  method.
                            """
                        class sliver_skew(TUIMethod):
                            """
                            Specifies the sliver skewness for the advancing front method. This parameter  is used for removing sliver cells in the interior.
                            """
                        class target(TUIMethod):
                            """
                            Enables you to enable targeted skewness-based refinement for the advancing  front method. This option enables you to improve the mesh until the targeted  skewness value is achieved.
                            """

                class improve_mesh(TUIMenu):
                    """
                    Enters the improve mesh controls menu.
                    """
                    def __init__(self, service, version, mode, path):
                        self.laplace_smooth = self.__class__.laplace_smooth(service, version, mode, path + ["laplace_smooth"])
                        self.skewness_smooth = self.__class__.skewness_smooth(service, version, mode, path + ["skewness_smooth"])
                        self.improve = self.__class__.improve(service, version, mode, path + ["improve"])
                        self.swap = self.__class__.swap(service, version, mode, path + ["swap"])
                        super().__init__(service, version, mode, path)
                    class laplace_smooth(TUIMethod):
                        """
                        Enables you to specify the Laplace smoothing parameters.
                        """
                    class skewness_smooth(TUIMethod):
                        """
                        Enables you to specify the skewness smooth parameters.
                        """
                    class improve(TUIMethod):
                        """
                        Automatically improves the mesh.
                        """
                    class swap(TUIMethod):
                        """
                        Enables you to specify the face swap parameters.
                        """

                class tet_improve(TUIMenu):
                    """
                    Improve cells controls.
                    """
                    def __init__(self, service, version, mode, path):
                        self.attempts = self.__class__.attempts(service, version, mode, path + ["attempts"])
                        self.angle = self.__class__.angle(service, version, mode, path + ["angle"])
                        self.iterations = self.__class__.iterations(service, version, mode, path + ["iterations"])
                        self.skew = self.__class__.skew(service, version, mode, path + ["skew"])
                        super().__init__(service, version, mode, path)
                    class attempts(TUIMethod):
                        """
                        Improve attempts.
                        """
                    class angle(TUIMethod):
                        """
                        Max dihedral angle defining a valid boundary cell.
                        """
                    class iterations(TUIMethod):
                        """
                        Improve iterations.
                        """
                    class skew(TUIMethod):
                        """
                        Remove skew.
                        """

            class local_regions(TUIMenu):
                """
                Enters the local refinement menu.
                """
                def __init__(self, service, version, mode, path):
                    self.list_all_regions = self.__class__.list_all_regions(service, version, mode, path + ["list_all_regions"])
                    self.define = self.__class__.define(service, version, mode, path + ["define"])
                    self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                    self.ideal_vol = self.__class__.ideal_vol(service, version, mode, path + ["ideal_vol"])
                    self.deactivate = self.__class__.deactivate(service, version, mode, path + ["deactivate"])
                    self.ideal_area = self.__class__.ideal_area(service, version, mode, path + ["ideal_area"])
                    self.activate = self.__class__.activate(service, version, mode, path + ["activate"])
                    self.refine = self.__class__.refine(service, version, mode, path + ["refine"])
                    self.init = self.__class__.init(service, version, mode, path + ["init"])
                    super().__init__(service, version, mode, path)
                class list_all_regions(TUIMethod):
                    """
                    Lists all refinement region parameters and the activated regions in the console.
                    """
                class define(TUIMethod):
                    """
                    Defines the refinement region according to the specified parameters.
                    """
                class delete(TUIMethod):
                    """
                    Deletes the specified refinement region.
                    """
                class ideal_vol(TUIMethod):
                    """
                    Reports the volume of an ideal tetrahedron for the edge length specified.
                    """
                class deactivate(TUIMethod):
                    """
                    Deactivates the specified regions for refinement.
                    """
                class ideal_area(TUIMethod):
                    """
                    Ideal triangle area for given edge length.
                    """
                class activate(TUIMethod):
                    """
                    Activates the specified regions for refinement.
                    """
                class refine(TUIMethod):
                    """
                    Refines the active cells inside the selected region based on the specified refinement parameters.
                    """
                class init(TUIMethod):
                    """
                    Defines the default refinement region encompassing the entire geometry.
                    """

        class domains(TUIMenu):
            """
            Enters the domain menu.
            """
            def __init__(self, service, version, mode, path):
                self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                self.draw = self.__class__.draw(service, version, mode, path + ["draw"])
                self.print = self.__class__.print(service, version, mode, path + ["print"])
                self.create_by_point = self.__class__.create_by_point(service, version, mode, path + ["create_by_point"])
                self.create_by_cell_zone = self.__class__.create_by_cell_zone(service, version, mode, path + ["create_by_cell_zone"])
                self.activate = self.__class__.activate(service, version, mode, path + ["activate"])
                super().__init__(service, version, mode, path)
            class delete(TUIMethod):
                """
                Deletes the specified domain.
                """
            class create(TUIMethod):
                """
                Creates a new domain based on the specified boundary face zones. Ensure valid boundary zones are specified; specifying invalid zones will generate an error.
                """
            class draw(TUIMethod):
                """
                Displays the boundary face zones of the specified domain.
                """
            class print(TUIMethod):
                """
                Prints the information for the specified domain.
                """
            class create_by_point(TUIMethod):
                """
                Creates a new domain based on the specified   The create-by-point option works only for cases with no overlapping face zones.
                """
            class create_by_cell_zone(TUIMethod):
                """
                Creates a new domain based on the specified cell zone.
                """
            class activate(TUIMethod):
                """
                Activates the specified domain for meshing or reporting operations.
                """

        class cartesian(TUIMenu):
            """
            Enter Cartesian mesh menu.
            """
            def __init__(self, service, version, mode, path):
                self.mesh = self.__class__.mesh(service, version, mode, path + ["mesh"])
                super().__init__(service, version, mode, path)
            class mesh(TUIMethod):
                """
                Generate Cartesian mesh.
                """

        class cell_zone_conditions(TUIMenu):
            """
            Contains options for copying or clearing cell zone conditions when a case file is read.
            """
            def __init__(self, service, version, mode, path):
                self.copy = self.__class__.copy(service, version, mode, path + ["copy"])
                self.clear = self.__class__.clear(service, version, mode, path + ["clear"])
                self.clear_all = self.__class__.clear_all(service, version, mode, path + ["clear_all"])
                super().__init__(service, version, mode, path)
            class copy(TUIMethod):
                """
                Enables you to copy the cell zone conditions from the zone selected to the zones specified.
                """
            class clear(TUIMethod):
                """
                Clears the cell zone conditions assigned to the specified zones.
                """
            class clear_all(TUIMethod):
                """
                Clears the cell conditions assigned to all the zones.
                """

        class poly_hexcore(TUIMenu):
            """
            Enters the menu for poly-hexcore mesh.
            """
            def __init__(self, service, version, mode, path):
                self.controls = self.__class__.controls(service, version, mode, path + ["controls"])
                super().__init__(service, version, mode, path)

            class controls(TUIMenu):
                """
                Enters the menu for setting parameters for poly-hexcore mesh.
                """
                def __init__(self, service, version, mode, path):
                    self.poly_cell_sizing_method = self.__class__.poly_cell_sizing_method(service, version, mode, path + ["poly_cell_sizing_method"])
                    self.only_polyhedra_for_selected_regions = self.__class__.only_polyhedra_for_selected_regions(service, version, mode, path + ["only_polyhedra_for_selected_regions"])
                    self.avoid_1_by_8_cell_jump_in_hexcore = self.__class__.avoid_1_by_8_cell_jump_in_hexcore(service, version, mode, path + ["avoid_1_by_8_cell_jump_in_hexcore"])
                    self.mark_core_region_cell_type_as_hex = self.__class__.mark_core_region_cell_type_as_hex(service, version, mode, path + ["mark_core_region_cell_type_as_hex"])
                    super().__init__(service, version, mode, path)
                class poly_cell_sizing_method(TUIMethod):
                    """
                    Poly-cell-sizing.
                    """
                class only_polyhedra_for_selected_regions(TUIMethod):
                    """
                    Determines if polyhedra cells are to be applied to the selected regions.
                    """
                class avoid_1_by_8_cell_jump_in_hexcore(TUIMethod):
                    """
                    Avoid-1:8-cell-jump-in-hexcore.
                    """
                class mark_core_region_cell_type_as_hex(TUIMethod):
                    """
                    Determines whether or not to apply hexahedra cells in the core region of the mesh. The default value is yes.
                    """

        class auto_mesh_controls(TUIMenu):
            """
            Enters the auto-mesh-controls submenu.
            """
            def __init__(self, service, version, mode, path):
                self.backup_object = self.__class__.backup_object(service, version, mode, path + ["backup_object"])
                super().__init__(service, version, mode, path)
            class backup_object(TUIMethod):
                """
                Enables creation of a backup of the surface mesh before volume meshing starts. This option is enabled by default.
                """

        class scoped_prisms(TUIMenu):
            """
            Contains options for creating scoped prism controls for mesh objects.
            """
            def __init__(self, service, version, mode, path):
                self.set_advanced_controls = self.__class__.set_advanced_controls(service, version, mode, path + ["set_advanced_controls"])
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                self.tet_prism_stairstep_exposed_quads = self.__class__.tet_prism_stairstep_exposed_quads(service, version, mode, path + ["tet_prism_stairstep_exposed_quads"])
                self.modify = self.__class__.modify(service, version, mode, path + ["modify"])
                self.write = self.__class__.write(service, version, mode, path + ["write"])
                self.growth_options = self.__class__.growth_options(service, version, mode, path + ["growth_options"])
                self.poly_keep_nlayer_prism_characteristics = self.__class__.poly_keep_nlayer_prism_characteristics(service, version, mode, path + ["poly_keep_nlayer_prism_characteristics"])
                self.read = self.__class__.read(service, version, mode, path + ["read"])
                self.list = self.__class__.list(service, version, mode, path + ["list"])
                self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                self.set_overset_prism_controls = self.__class__.set_overset_prism_controls(service, version, mode, path + ["set_overset_prism_controls"])
                self.set_no_imprint_zones = self.__class__.set_no_imprint_zones(service, version, mode, path + ["set_no_imprint_zones"])
                super().__init__(service, version, mode, path)
            class set_advanced_controls(TUIMethod):
                """
                Used to specify various controls for scoped prisms. Prompts include setting iterations for normal based prisms, smoothing, prism improvement, automatic node movement, and warp improvement. Prompts also include checks for stair-step interactions, as well as proximity, quality, and the exposure of quad quality. Automatic stair-stepping occurs during prism generation based on the proximity and quality limits. You can intentionally avoid stair-stepping by setting the last three prompts (proximity, quality, and the exposure of quad quality) to no, although you may also retain some poor quality cells.
                """
            class create(TUIMethod):
                """
                Creates a new scoped prism control based on the parameters and scope specified. Specify the name, offset method, first height or aspect ratio, number of layers, and rate or last percent. Select the mesh object and set the scope  (fluid-regions, named-regions, or  solid-regions). Specify the zones to grow prisms  (all-zones, only-walls,  selected-face-zones, or selected-labels, or solid-fluid-interface). When  named-regions and/or selected-face-zones or selected-labels are selected, specify the volume and/or boundary scope. If interior baffle zones are selected, retain the option to grow prisms on both sides of the baffles or disable it to grow prisms on one side.
                """
            class tet_prism_stairstep_exposed_quads(TUIMethod):
                """
                Tet-Prism Stairstep exposed quad.
                """
            class modify(TUIMethod):
                """
                Modifies the specified control based on the parameters specified.
                """
            class write(TUIMethod):
                """
                Writes the scoped prism controls to a prism control file (\\*.pzmcontrol). Specify the scoped prism file name.
                """
            class growth_options(TUIMethod):
                """
                Enables you to specify scoped prism growth options. Select Fix First  Height if required, and specify the gap factor, maximum aspect ratio, prism quality method, and the threshold quality value for stair stepping.
                """
            class poly_keep_nlayer_prism_characteristics(TUIMethod):
                """
                Number of layers to maintain poly-prism characteristics.
                """
            class read(TUIMethod):
                """
                Reads in the specified scoped prism control file (\\*.pzmcontrol).
                """
            class list(TUIMethod):
                """
                Lists all the defined scoped prism controls.
                """
            class delete(TUIMethod):
                """
                Deletes the specified scoped prism control.
                """
            class set_overset_prism_controls(TUIMethod):
                """
                Set boundary layer controls for overset mesh generation.
                """
            class set_no_imprint_zones(TUIMethod):
                """
                Used to specify face zones that should not be imprinted during prism generation.
                """

        class prism(TUIMenu):
            """
            Enters the prism menu.
            """
            def __init__(self, service, version, mode, path):
                self.improve = self.__class__.improve(service, version, mode, path + ["improve"])
                self.split = self.__class__.split(service, version, mode, path + ["split"])
                self.post_ignore = self.__class__.post_ignore(service, version, mode, path + ["post_ignore"])
                self.controls = self.__class__.controls(service, version, mode, path + ["controls"])
                self.mark_nonmanifold_nodes = self.__class__.mark_nonmanifold_nodes(service, version, mode, path + ["mark_nonmanifold_nodes"])
                self.list_parameters = self.__class__.list_parameters(service, version, mode, path + ["list_parameters"])
                self.mark_ignore_faces = self.__class__.mark_ignore_faces(service, version, mode, path + ["mark_ignore_faces"])
                self.quality_method = self.__class__.quality_method(service, version, mode, path + ["quality_method"])
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                self.reset_parameters = self.__class__.reset_parameters(service, version, mode, path + ["reset_parameters"])
                self.mark_proximity_faces = self.__class__.mark_proximity_faces(service, version, mode, path + ["mark_proximity_faces"])
                super().__init__(service, version, mode, path)
            class mark_nonmanifold_nodes(TUIMethod):
                """
                Enables you to mark the non-manifold prism base nodes. A list of the non-manifold nodes will be printed in the console. The faces connected to the non-manifold nodes will also be marked. You can use this command after specifying zone-specific prism settings, prior to generating the prisms to verify that non-manifold configurations do not exist.
                """
            class list_parameters(TUIMethod):
                """
                Shows all prism mesh parameters.
                """
            class mark_ignore_faces(TUIMethod):
                """
                Enables you to mark the faces to be ignored during prism meshing.
                """
            class quality_method(TUIMethod):
                """
                Specifies the quality method used during prism generation.
                """
            class create(TUIMethod):
                """
                Creates prism layers on one or more boundary face zones based on the offset method, growth method, number of layers, and rate specified.
                """
            class reset_parameters(TUIMethod):
                """
                Resets all prism parameters.
                """
            class mark_proximity_faces(TUIMethod):
                """
                Mark prism base faces with certain gap.
                """

            class improve(TUIMenu):
                """
                Enters the prism improve menu.
                """
                def __init__(self, service, version, mode, path):
                    self.smooth_improve_prism_cells = self.__class__.smooth_improve_prism_cells(service, version, mode, path + ["smooth_improve_prism_cells"])
                    self.smooth_brute_force = self.__class__.smooth_brute_force(service, version, mode, path + ["smooth_brute_force"])
                    self.smooth_prism_cells = self.__class__.smooth_prism_cells(service, version, mode, path + ["smooth_prism_cells"])
                    self.smooth_cell_rings = self.__class__.smooth_cell_rings(service, version, mode, path + ["smooth_cell_rings"])
                    self.smooth_sliver_skew = self.__class__.smooth_sliver_skew(service, version, mode, path + ["smooth_sliver_skew"])
                    self.improve_prism_cells = self.__class__.improve_prism_cells(service, version, mode, path + ["improve_prism_cells"])
                    super().__init__(service, version, mode, path)
                class smooth_improve_prism_cells(TUIMethod):
                    """
                    Uses a combination of node movement and optimized smoothing to improve the quality. This command is a combination of the smooth-prism-cells and improve-prism-cells commands. The cell aspect ratio will also be maintained based on the value specified for max-aspect-ratio.
                    """
                class smooth_brute_force(TUIMethod):
                    """
                    Forcibly smooths cells if cell skewness is still high after regular smoothing.
                    """
                class smooth_prism_cells(TUIMethod):
                    """
                    Enables optimization based smoothing of prism cells. The nodes of cells with quality worse than the specified threshold value will be moved to improve quality. The cell aspect ratio will also be maintained based on the value specified for max-aspect-ratio.
                    """
                class smooth_cell_rings(TUIMethod):
                    """
                    Specifies the number of cell rings around the skewed cell used by improve-prism-cells.
                    """
                class smooth_sliver_skew(TUIMethod):
                    """
                    Specifies the skewness above which prism cells will be smoothed.
                    """
                class improve_prism_cells(TUIMethod):
                    """
                    Collects and smooths cells in layers around poor quality cells. Cells with quality worse than the specified threshold value will be identified, and the nodes of the cells surrounding the poor quality cells will be moved to improve quality.
                    """

            class split(TUIMenu):
                """
                Contains options for splitting the prism layers after the initial prism layers are generated, to generate the total number of layers required.
                """
                def __init__(self, service, version, mode, path):
                    self.split = self.__class__.split(service, version, mode, path + ["split"])
                    super().__init__(service, version, mode, path)
                class split(TUIMethod):
                    """
                    Enables you to split the prism layers after the initial prism layers are generated, to generate the total number of layers required. Specify the prism cell zones to be split and the number of divisions per layer. You can also choose to use the existing growth rate (default) or specify the growth rate to be used while splitting the prism layers.
                    """

            class post_ignore(TUIMenu):
                """
                Contains the following options for ignoring prism cells:.
                """
                def __init__(self, service, version, mode, path):
                    self.mark_cavity_prism_cap = self.__class__.mark_cavity_prism_cap(service, version, mode, path + ["mark_cavity_prism_cap"])
                    self.create_cavity = self.__class__.create_cavity(service, version, mode, path + ["create_cavity"])
                    self.mark_prism_cap = self.__class__.mark_prism_cap(service, version, mode, path + ["mark_prism_cap"])
                    self.post_remove_cells = self.__class__.post_remove_cells(service, version, mode, path + ["post_remove_cells"])
                    super().__init__(service, version, mode, path)
                class mark_cavity_prism_cap(TUIMethod):
                    """
                    Marks the prism cap faces and tetrahedral cell faces bounding the cavity to be created in regions where prism quality is adequate, but the quality of adjacent tetrahedra is poor. Specify the tetrahedral cell zone, the quality measure and the corresponding threshold value to be used, and the additional number of cell rings based on which the cavity will be created.
                    """
                class create_cavity(TUIMethod):
                    """
                    Creates a cavity in regions where prism quality is adequate, but the quality of adjacent tetrahedra is poor. The cavity is created based on the tetrahedral cell zone, the quality measure and the corresponding threshold value, and the additional number of cell rings specified. You can create a cavity comprising only tetrahedral cells or optionally include prism cells in the cavity created. When prism cells are also included in the cavity, you can specify whether the non-conformal interface is to be created.
                    """
                class mark_prism_cap(TUIMethod):
                    """
                    Marks the prism cap faces for ignoring prism cells in regions of poor quality cells and sharp corners. Specify the prism cell zone and the basis for ignoring prism cells and the relevant parameters. The prism cells can be ignored based on quality, intersection, (both enabled by default), warp, and features (both disabled by default). Specify the quality measure and threshold value to be used for ignoring cells based on quality and (if applicable) the feature edges for ignoring cells based on features. Additionally, specify whether cells are to be marked in regions of high aspect ratio and based on feature angle, and the additional number of cell rings based on which prism cells will be removed.
                    """
                class post_remove_cells(TUIMethod):
                    """
                    Enables you to remove prism cells in layers around poor quality cells and sharp corners. Specify the prism cell zone, the basis for ignoring prism cells (quality, intersection, warp, features) and the relevant parameters. Specify the number of cell rings to be removed around the marked cells. Cells will be marked for removal in regions of sharp corners based on quality, intersection, warp, and features (as applicable) and then extended based on the number of cell rings specified. Additional cells will be marked for removal in regions of high aspect ratio and based on feature angle (if applicable) around the exposed prism side. The boundary will be smoothed at feature corners after the prism cells have been removed. The prism-side faces exposed by the removal of the prism cells will be collected in a zone named prism-side-#, while for a zone wall-n, the faces corresponding to the ignored prism cells will be collected in a zone named wall-n:ignore. You can also optionally smooth the prism side nodes from the base node to the cap node to create better triangles for the non-conformal interface.
                    """

            class controls(TUIMenu):
                """
                Enters the prism controls menu.
                """
                def __init__(self, service, version, mode, path):
                    self.offset = self.__class__.offset(service, version, mode, path + ["offset"])
                    self.proximity = self.__class__.proximity(service, version, mode, path + ["proximity"])
                    self.zone_specific_growth = self.__class__.zone_specific_growth(service, version, mode, path + ["zone_specific_growth"])
                    self.morph = self.__class__.morph(service, version, mode, path + ["morph"])
                    self.normal = self.__class__.normal(service, version, mode, path + ["normal"])
                    self.adjacent_zone = self.__class__.adjacent_zone(service, version, mode, path + ["adjacent_zone"])
                    self.improve = self.__class__.improve(service, version, mode, path + ["improve"])
                    self.post_ignore = self.__class__.post_ignore(service, version, mode, path + ["post_ignore"])
                    self.merge_ignored_threads = self.__class__.merge_ignored_threads(service, version, mode, path + ["merge_ignored_threads"])
                    self.remove_invalid_layer = self.__class__.remove_invalid_layer(service, version, mode, path + ["remove_invalid_layer"])
                    self.grow_individually = self.__class__.grow_individually(service, version, mode, path + ["grow_individually"])
                    self.set_overset_prism_controls = self.__class__.set_overset_prism_controls(service, version, mode, path + ["set_overset_prism_controls"])
                    self.split = self.__class__.split(service, version, mode, path + ["split"])
                    self.auto_separate_cells = self.__class__.auto_separate_cells(service, version, mode, path + ["auto_separate_cells"])
                    self.set_post_mesh_controls = self.__class__.set_post_mesh_controls(service, version, mode, path + ["set_post_mesh_controls"])
                    self.check_quality = self.__class__.check_quality(service, version, mode, path + ["check_quality"])
                    super().__init__(service, version, mode, path)
                class merge_ignored_threads(TUIMethod):
                    """
                    Enables you to automatically merge all ignored zones related to a base thread into a single thread. This option is enabled by default. When this option is disabled, more than one ignored thread will be generated per base thread. However, various zones can be created by ignoring this option. They are:.
                    """
                class remove_invalid_layer(TUIMethod):
                    """
                    Removes the last prism layer if it fails in the quality check.
                    """
                class grow_individually(TUIMethod):
                    """
                    Grow from multiple zones one-at-a-time?.
                    """
                class set_overset_prism_controls(TUIMethod):
                    """
                    Set boundary layer controls for overset mesh generation.
                    """
                class split(TUIMethod):
                    """
                    Enables you to set parameters for splitting the prism layers after the initial prism layers are generated, to generate the total number of layers required. Specify the number of divisions per layer.
                    """
                class auto_separate_cells(TUIMethod):
                    """
                    Automatically separate prism cells extruded from multiple face threads?.
                    """
                class set_post_mesh_controls(TUIMethod):
                    """
                    Sets controls specific to growing prisms post volume mesh generation.
                    """
                class check_quality(TUIMethod):
                    """
                    Enables/disables the checking of volume, skewness, and handedness of each new cell and face.
                    """

                class offset(TUIMenu):
                    """
                    Enters the prism offset controls menu.
                    """
                    def __init__(self, service, version, mode, path):
                        self.smooth_converged = self.__class__.smooth_converged(service, version, mode, path + ["smooth_converged"])
                        self.first_aspect_ratio_min = self.__class__.first_aspect_ratio_min(service, version, mode, path + ["first_aspect_ratio_min"])
                        self.smooth_iter = self.__class__.smooth_iter(service, version, mode, path + ["smooth_iter"])
                        self.min_aspect_ratio = self.__class__.min_aspect_ratio(service, version, mode, path + ["min_aspect_ratio"])
                        self.smooth = self.__class__.smooth(service, version, mode, path + ["smooth"])
                        super().__init__(service, version, mode, path)
                    class smooth_converged(TUIMethod):
                        """
                        Convergence criterion for offset smoothing.
                        """
                    class first_aspect_ratio_min(TUIMethod):
                        """
                        Specifies the minimum first aspect ratio (ratio of prism base length to prism layer height) for the prism cells.
                        """
                    class smooth_iter(TUIMethod):
                        """
                        Maximum number of smoothing iterations for offset distances.
                        """
                    class min_aspect_ratio(TUIMethod):
                        """
                        Specifies the minimum aspect ratio (ratio of prism base length to prism layer height) for the prism cells.
                        """
                    class smooth(TUIMethod):
                        """
                        Perform smoothing of offset distances?.
                        """

                class proximity(TUIMenu):
                    """
                    Enters the prism proximity controls menu.
                    """
                    def __init__(self, service, version, mode, path):
                        self.allow_ignore = self.__class__.allow_ignore(service, version, mode, path + ["allow_ignore"])
                        self.max_shrink_factor = self.__class__.max_shrink_factor(service, version, mode, path + ["max_shrink_factor"])
                        self.smoothing_rate = self.__class__.smoothing_rate(service, version, mode, path + ["smoothing_rate"])
                        self.max_aspect_ratio = self.__class__.max_aspect_ratio(service, version, mode, path + ["max_aspect_ratio"])
                        self.gap_factor = self.__class__.gap_factor(service, version, mode, path + ["gap_factor"])
                        self.allow_shrinkage = self.__class__.allow_shrinkage(service, version, mode, path + ["allow_shrinkage"])
                        self.keep_first_layer_offsets = self.__class__.keep_first_layer_offsets(service, version, mode, path + ["keep_first_layer_offsets"])
                        super().__init__(service, version, mode, path)
                    class allow_ignore(TUIMethod):
                        """
                        Enables you to ignore nodes where the specified maximum shrink factor cannot be maintained.
                        """
                    class max_shrink_factor(TUIMethod):
                        """
                        Specifies the shrink factor determining the maximum shrinkage of the prism layers. This option is available only when the allow-ignore? option is enabled.
                        """
                    class smoothing_rate(TUIMethod):
                        """
                        Rate at which shrinkage is propagated in lateral direction.
                        """
                    class max_aspect_ratio(TUIMethod):
                        """
                        Specifies the maximum allowable cell aspect ratio to determine the limit for the shrinkage of prism layers. This option is available only when the allow-ignore? option is disabled.
                        """
                    class gap_factor(TUIMethod):
                        """
                        Controls the gap between the intersecting prisms layers in the proximity region with respect to the cell size of the prisms.
                        """
                    class allow_shrinkage(TUIMethod):
                        """
                        Enables shrinkage while growing prism layers.
                        """
                    class keep_first_layer_offsets(TUIMethod):
                        """
                        Enables you to retain first layer offsets while performing proximity detection.
                        """

                class zone_specific_growth(TUIMenu):
                    """
                    Enters the prism growth controls menu.
                    """
                    def __init__(self, service, version, mode, path):
                        self.apply_growth = self.__class__.apply_growth(service, version, mode, path + ["apply_growth"])
                        self.clear_growth = self.__class__.clear_growth(service, version, mode, path + ["clear_growth"])
                        self.list_growth = self.__class__.list_growth(service, version, mode, path + ["list_growth"])
                        super().__init__(service, version, mode, path)
                    class apply_growth(TUIMethod):
                        """
                        Applies the zone-specific growth parameters specified.
                        """
                    class clear_growth(TUIMethod):
                        """
                        Clears the zone-specific growth specified.
                        """
                    class list_growth(TUIMethod):
                        """
                        Lists the zone-specific growth parameters specified for individual zones in the console.
                        """

                class morph(TUIMenu):
                    """
                    Enters the prism morphing controls menu.
                    """
                    def __init__(self, service, version, mode, path):
                        self.morphing_frequency = self.__class__.morphing_frequency(service, version, mode, path + ["morphing_frequency"])
                        self.morphing_convergence_limit = self.__class__.morphing_convergence_limit(service, version, mode, path + ["morphing_convergence_limit"])
                        self.improve_threshold = self.__class__.improve_threshold(service, version, mode, path + ["improve_threshold"])
                        super().__init__(service, version, mode, path)
                    class morphing_frequency(TUIMethod):
                        """
                        Specifies the frequency of the morphing operation. The number specified denotes the number of prism layers after which the morpher is applied to the remainder of the mesh (for example, a value of 5 indicates that the morpher is applied to the mesh after every 5 prism layers grown).
                        """
                    class morphing_convergence_limit(TUIMethod):
                        """
                        Specifies the convergence limit for the morphing operation. The morpher uses an iterative solver. It is assumed to have converged when the relative residual is less than this number.
                        """
                    class improve_threshold(TUIMethod):
                        """
                        Specifies the quality threshold used for improving the quality during the morphing operation.
                        """

                class normal(TUIMenu):
                    """
                    Enters the prism normal controls menu.
                    """
                    def __init__(self, service, version, mode, path):
                        self.max_angle_change = self.__class__.max_angle_change(service, version, mode, path + ["max_angle_change"])
                        self.direction_method = self.__class__.direction_method(service, version, mode, path + ["direction_method"])
                        self.orient_mesh_object_face_normals = self.__class__.orient_mesh_object_face_normals(service, version, mode, path + ["orient_mesh_object_face_normals"])
                        self.orthogonal_layers = self.__class__.orthogonal_layers(service, version, mode, path + ["orthogonal_layers"])
                        self.smooth = self.__class__.smooth(service, version, mode, path + ["smooth"])
                        self.smooth_relaxation_factor = self.__class__.smooth_relaxation_factor(service, version, mode, path + ["smooth_relaxation_factor"])
                        self.ignore_invalid_normals = self.__class__.ignore_invalid_normals(service, version, mode, path + ["ignore_invalid_normals"])
                        self.bisect_angle = self.__class__.bisect_angle(service, version, mode, path + ["bisect_angle"])
                        self.compute_normal = self.__class__.compute_normal(service, version, mode, path + ["compute_normal"])
                        self.normal_method = self.__class__.normal_method(service, version, mode, path + ["normal_method"])
                        self.smooth_converged = self.__class__.smooth_converged(service, version, mode, path + ["smooth_converged"])
                        self.converge_locally = self.__class__.converge_locally(service, version, mode, path + ["converge_locally"])
                        self.direction_vector = self.__class__.direction_vector(service, version, mode, path + ["direction_vector"])
                        self.smooth_iter = self.__class__.smooth_iter(service, version, mode, path + ["smooth_iter"])
                        super().__init__(service, version, mode, path)
                    class max_angle_change(TUIMethod):
                        """
                        Specifies the maximum angle by which the normal direction at a node can change during smoothing.
                        """
                    class direction_method(TUIMethod):
                        """
                        Specifies whether the prism layers should be grown normal to surfaces or along a specified direction vector.
                        """
                    class orient_mesh_object_face_normals(TUIMethod):
                        """
                        Enables you to orient the face normals for mesh object boundary zones. Specify the mesh object, region or material point as appropriate, and specify whether walls, baffles or both comprising the prism base zones are to be separated and oriented.
                        """
                    class orthogonal_layers(TUIMethod):
                        """
                        Specifies the number of layers to preserve orthogonality. All smoothing is deferred until after these layers.
                        """
                    class smooth(TUIMethod):
                        """
                        Perform smoothing of normal advancement direction vectors?.
                        """
                    class smooth_relaxation_factor(TUIMethod):
                        """
                        Normal Smooth Relaxation factor.
                        """
                    class ignore_invalid_normals(TUIMethod):
                        """
                        Enables you to ignore nodes that have poor normals.
                        """
                    class bisect_angle(TUIMethod):
                        """
                        Is required for growing prisms out of sharp interior corners. When the value of this angle is set, the normals are automatically projected onto the plane bisecting the angle between faces having an interior angle less than this angle.
                        """
                    class compute_normal(TUIMethod):
                        """
                        Computes the normal for the specified face zone.
                        """
                    class normal_method(TUIMethod):
                        """
                        Method in which normal marching direction vectors are determined.
                        """
                    class smooth_converged(TUIMethod):
                        """
                        Convergence criterion (in DEGREES) for angle changes
                        during normal smoothing.
                        """
                    class converge_locally(TUIMethod):
                        """
                        Converge normal smoothing locally by freezing each
                        individually once it has converged?.  Otherwise, all normals are continuously
                        smoothed until all have converged.
                        """
                    class direction_vector(TUIMethod):
                        """
                        Specifies the direction vector for prism extrusion when the uniform method is selected for direction-method.
                        """
                    class smooth_iter(TUIMethod):
                        """
                        Maximum number of smoothing iterations for normal vectors.
                        """

                class adjacent_zone(TUIMenu):
                    """
                    Enters the prism adjacent zone controls menu.
                    """
                    def __init__(self, service, version, mode, path):
                        self.side_feature_align_angle = self.__class__.side_feature_align_angle(service, version, mode, path + ["side_feature_align_angle"])
                        self.project_iter = self.__class__.project_iter(service, version, mode, path + ["project_iter"])
                        self.project_converged = self.__class__.project_converged(service, version, mode, path + ["project_converged"])
                        self.retriangulate_adjacent = self.__class__.retriangulate_adjacent(service, version, mode, path + ["retriangulate_adjacent"])
                        self.side_topology_align_angle = self.__class__.side_topology_align_angle(service, version, mode, path + ["side_topology_align_angle"])
                        self.side_feature_angle = self.__class__.side_feature_angle(service, version, mode, path + ["side_feature_angle"])
                        self.retri_feature_angle = self.__class__.retri_feature_angle(service, version, mode, path + ["retri_feature_angle"])
                        self.project = self.__class__.project(service, version, mode, path + ["project"])
                        self.project_adjacent_angle = self.__class__.project_adjacent_angle(service, version, mode, path + ["project_adjacent_angle"])
                        super().__init__(service, version, mode, path)
                    class side_feature_align_angle(TUIMethod):
                        """
                        This angle (degrees) is used for aligning projected normals along a feature edge.
                        """
                    class project_iter(TUIMethod):
                        """
                        Maximum number of iterations for projection to adjacent zones.
                        """
                    class project_converged(TUIMethod):
                        """
                        Convergence criterion for projection to adjacent zones.
                        """
                    class retriangulate_adjacent(TUIMethod):
                        """
                        Retriangulate planar zones along which prism layers are grown?.
                        """
                    class side_topology_align_angle(TUIMethod):
                        """
                        This angle (degrees) is used for aligning projected normals along one from many feature edges based on topology (if feature-align doesn't occur).
                        """
                    class side_feature_angle(TUIMethod):
                        """
                        Specifies the angle used for computing the feature normals.
                        """
                    class retri_feature_angle(TUIMethod):
                        """
                        This angle (degrees) is used for determining the feature edges on the face zones which are retirangulated.
                        """
                    class project(TUIMethod):
                        """
                        Project outer nodes to adjacent planar zones?.
                        """
                    class project_adjacent_angle(TUIMethod):
                        """
                        Determines whether or not to project to an adjacent zone. If a zone shares outer nodes with any of the zones from which the layers are being grown (the “base zones”), its angle with respect to the growth direction is compared with this value. If the angle is less than or equal to this value, then the zone will be projected to. The default value is 75 degrees. See  for details.
                        """

                class improve(TUIMenu):
                    """
                    Enters the prism smoothing controls menu.
                    """
                    def __init__(self, service, version, mode, path):
                        self.check_size = self.__class__.check_size(service, version, mode, path + ["check_size"])
                        self.smooth_improve_prism_cells = self.__class__.smooth_improve_prism_cells(service, version, mode, path + ["smooth_improve_prism_cells"])
                        self.corner_height_weight = self.__class__.corner_height_weight(service, version, mode, path + ["corner_height_weight"])
                        self.node_smooth_converged = self.__class__.node_smooth_converged(service, version, mode, path + ["node_smooth_converged"])
                        self.face_smooth_rings = self.__class__.face_smooth_rings(service, version, mode, path + ["face_smooth_rings"])
                        self.improve_warp = self.__class__.improve_warp(service, version, mode, path + ["improve_warp"])
                        self.edge_swap_cap_angle = self.__class__.edge_swap_cap_angle(service, version, mode, path + ["edge_swap_cap_angle"])
                        self.face_smooth = self.__class__.face_smooth(service, version, mode, path + ["face_smooth"])
                        self.left_hand_check = self.__class__.left_hand_check(service, version, mode, path + ["left_hand_check"])
                        self.post_adjust_height = self.__class__.post_adjust_height(service, version, mode, path + ["post_adjust_height"])
                        self.face_smooth_skew = self.__class__.face_smooth_skew(service, version, mode, path + ["face_smooth_skew"])
                        self.edge_smooth_angle = self.__class__.edge_smooth_angle(service, version, mode, path + ["edge_smooth_angle"])
                        self.face_smooth_converged = self.__class__.face_smooth_converged(service, version, mode, path + ["face_smooth_converged"])
                        self.swap_smooth_skew = self.__class__.swap_smooth_skew(service, version, mode, path + ["swap_smooth_skew"])
                        self.node_smooth_rings = self.__class__.node_smooth_rings(service, version, mode, path + ["node_smooth_rings"])
                        self.node_smooth_local = self.__class__.node_smooth_local(service, version, mode, path + ["node_smooth_local"])
                        self.node_smooth_angle = self.__class__.node_smooth_angle(service, version, mode, path + ["node_smooth_angle"])
                        self.max_allowable_cap_skew = self.__class__.max_allowable_cap_skew(service, version, mode, path + ["max_allowable_cap_skew"])
                        self.node_smooth_iter = self.__class__.node_smooth_iter(service, version, mode, path + ["node_smooth_iter"])
                        self.node_smooth = self.__class__.node_smooth(service, version, mode, path + ["node_smooth"])
                        self.check_allowable_skew = self.__class__.check_allowable_skew(service, version, mode, path + ["check_allowable_skew"])
                        self.identify_feature_line = self.__class__.identify_feature_line(service, version, mode, path + ["identify_feature_line"])
                        self.max_allowable_cell_skew = self.__class__.max_allowable_cell_skew(service, version, mode, path + ["max_allowable_cell_skew"])
                        self.shrink_left_handed_cap = self.__class__.shrink_left_handed_cap(service, version, mode, path + ["shrink_left_handed_cap"])
                        self.edge_swap = self.__class__.edge_swap(service, version, mode, path + ["edge_swap"])
                        self.edge_swap_base_angle = self.__class__.edge_swap_base_angle(service, version, mode, path + ["edge_swap_base_angle"])
                        self.edge_smooth = self.__class__.edge_smooth(service, version, mode, path + ["edge_smooth"])
                        self.layer_by_layer_smoothing = self.__class__.layer_by_layer_smoothing(service, version, mode, path + ["layer_by_layer_smoothing"])
                        super().__init__(service, version, mode, path)
                    class check_size(TUIMethod):
                        """
                        Check for negative cell volume?.
                        """
                    class smooth_improve_prism_cells(TUIMethod):
                        """
                        Enables you to set the parameters for improving the prism cells after the required prism layers are created. You can select optimized smoothing (smooth), node movement (improve), or a combination of both to improve the quality. Specify the quality measure to be used, the cell quality threshold, the number of improvement iterations, and the minimum improvement required.
                        """
                    class corner_height_weight(TUIMethod):
                        """
                        When enabled, the offset height at corners with large angles (for example, 270º) is reduced to give a smoother prism cap.
                        """
                    class node_smooth_converged(TUIMethod):
                        """
                        Convergence criterion for node smoothing.
                        """
                    class face_smooth_rings(TUIMethod):
                        """
                        No. of rings to propagate skewness during smoothing of cap faces.
                        """
                    class improve_warp(TUIMethod):
                        """
                        Enables or disables improving of face warp during prism generation. This option is disabled by default.
                        """
                    class edge_swap_cap_angle(TUIMethod):
                        """
                        Specifies the maximum allowable angle between the normals of the cap faces for skewness-driven edge swapping.
                        """
                    class face_smooth(TUIMethod):
                        """
                        Perform face-driven smoothing to improve skewness?.
                        """
                    class left_hand_check(TUIMethod):
                        """
                        Controls checking for left-handedness of faces. The default setting of 0 implies face handedness will not be checked. A value of 1 implies only cap faces will be checked, while 2 implies faces of all cells in current layer will be checked.
                        """
                    class post_adjust_height(TUIMethod):
                        """
                        Perform prism height adjustment based on growth rate?.
                        """
                    class face_smooth_skew(TUIMethod):
                        """
                        Min. skewness to smooth cap faces.
                        """
                    class edge_smooth_angle(TUIMethod):
                        """
                        Skewness-driven edge smoothing is only allowed between cap faces whose normals
                        are within this angle.
                        """
                    class face_smooth_converged(TUIMethod):
                        """
                        Convergence criteria for cap face smoothing.
                        """
                    class swap_smooth_skew(TUIMethod):
                        """
                        Only faces with skewness >= this value are swapped and/or smoothed.
                        """
                    class node_smooth_rings(TUIMethod):
                        """
                        Controls locality of skewness-driven node smoothing.
                        If greater than zero, nodes surrounding a node to be smoothed are smoothed
                        first.  Nodes directly connected to the target node are in ring 1.  Nodes not
                        in ring 1 which are directly connected to nodes in ring 1 are in ring 2,
                        and so on.  This value determines how many surrounding rings to smooth.
                        """
                    class node_smooth_local(TUIMethod):
                        """
                        Allow node-smoothing to converge locally (for large geometries).
                        """
                    class node_smooth_angle(TUIMethod):
                        """
                        Only manifolds having characteristic angles
                        within this many degrees of 180 will be smoothed.
                        """
                    class max_allowable_cap_skew(TUIMethod):
                        """
                        Specifies the maximum skewness allowed for a prism cap face. If the skewness of a cap face exceeds this value, the meshing process will stop and a warning indicates that the skewness for that layer is too high.
                        """
                    class node_smooth_iter(TUIMethod):
                        """
                        Maximum number of smoothing iterations for nodes on advancing layers.
                        """
                    class node_smooth(TUIMethod):
                        """
                        Perform node-driven smoothing to improve skewness?.
                        """
                    class check_allowable_skew(TUIMethod):
                        """
                        Enables you to check the skewness of the prism cap for every layer.
                        """
                    class identify_feature_line(TUIMethod):
                        """
                        Perform normal smoothing on feature lines?.
                        """
                    class max_allowable_cell_skew(TUIMethod):
                        """
                        Specifies the cell quality criteria for smoothing and quality checking.
                        """
                    class shrink_left_handed_cap(TUIMethod):
                        """
                        Shrink if required to get rid of left handed faces.
                        """
                    class edge_swap(TUIMethod):
                        """
                        Perform edge swapping to improve skewness?.
                        """
                    class edge_swap_base_angle(TUIMethod):
                        """
                        Specifies the maximum allowable angle between the normals of the base faces for skewness-driven edge swapping.
                        """
                    class edge_smooth(TUIMethod):
                        """
                        Perform local smoothing of nodes on longest edges of skewed faces?.
                        """
                    class layer_by_layer_smoothing(TUIMethod):
                        """
                        Perform normals and heights smoothing to improve cell quality/shape?.
                        """

                class post_ignore(TUIMenu):
                    """
                    Contains options for setting the parameters for removing poor quality prism cells after the required prism layers are created.
                    """
                    def __init__(self, service, version, mode, path):
                        self.post_remove_cells = self.__class__.post_remove_cells(service, version, mode, path + ["post_remove_cells"])
                        super().__init__(service, version, mode, path)
                    class post_remove_cells(TUIMethod):
                        """
                        Enables you to set the parameters for removing poor quality prism cells after the required prism layers are created. You can remove cells based on quality, intersection, interior warp, and feature edges. Specify options for removing additional cells in regions of high aspect ratio and feature angle, the number of cell rings to be removed around the marked cells, and options for smoothing the prism boundary and prism side height.
                        """

        class separate(TUIMenu):
            """
            Separates cells by various user-defined methods.
            """
            def __init__(self, service, version, mode, path):
                self.local_regions = self.__class__.local_regions(service, version, mode, path + ["local_regions"])
                self.separate_cell_by_shape = self.__class__.separate_cell_by_shape(service, version, mode, path + ["separate_cell_by_shape"])
                self.separate_wedge_prisms = self.__class__.separate_wedge_prisms(service, version, mode, path + ["separate_wedge_prisms"])
                self.separate_prisms_from_poly = self.__class__.separate_prisms_from_poly(service, version, mode, path + ["separate_prisms_from_poly"])
                self.separate_cell_by_skew = self.__class__.separate_cell_by_skew(service, version, mode, path + ["separate_cell_by_skew"])
                self.separate_cell_by_region = self.__class__.separate_cell_by_region(service, version, mode, path + ["separate_cell_by_region"])
                self.separate_cell_by_size = self.__class__.separate_cell_by_size(service, version, mode, path + ["separate_cell_by_size"])
                self.separate_cell_by_face = self.__class__.separate_cell_by_face(service, version, mode, path + ["separate_cell_by_face"])
                self.separate_prisms_from_hex = self.__class__.separate_prisms_from_hex(service, version, mode, path + ["separate_prisms_from_hex"])
                self.separate_cell_by_mark = self.__class__.separate_cell_by_mark(service, version, mode, path + ["separate_cell_by_mark"])
                super().__init__(service, version, mode, path)
            class separate_cell_by_shape(TUIMethod):
                """
                Separates cells with different shapes (pyramids, tetrahedra, etc.) into separate cell zones.
                """
            class separate_wedge_prisms(TUIMethod):
                """
                Separate wedge-prism cells from bulk.
                """
            class separate_prisms_from_poly(TUIMethod):
                """
                Separates the poly-prism cells from the poly cells within your mesh. Available only when the report/enhanced-orthogonal-quality? flag is set to  yes, and is only supported for the .h5 format.
                """
            class separate_cell_by_skew(TUIMethod):
                """
                Separates cells based on the specified cell skewness.
                """
            class separate_cell_by_region(TUIMethod):
                """
                Separates contiguous regions within a cell zone into separate cell zones.
                """
            class separate_cell_by_size(TUIMethod):
                """
                Separates cells based on the specified minimum and maximum cell sizes.
                """
            class separate_cell_by_face(TUIMethod):
                """
                Separates cells that are connected to a specified face zone into another cell zone. This separation method applies only to prism cells.
                """
            class separate_prisms_from_hex(TUIMethod):
                """
                Separate prism cells from hex.
                """
            class separate_cell_by_mark(TUIMethod):
                """
                Separates cells within a specified local region into another cell zone.
                """

            class local_regions(TUIMenu):
                """
                Enters the local refinement menu.
                """
                def __init__(self, service, version, mode, path):
                    self.init = self.__class__.init(service, version, mode, path + ["init"])
                    self.define = self.__class__.define(service, version, mode, path + ["define"])
                    self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                    self.list_all_regions = self.__class__.list_all_regions(service, version, mode, path + ["list_all_regions"])
                    super().__init__(service, version, mode, path)
                class init(TUIMethod):
                    """
                    Deletes all current regions and adds the default refinement region.
                    """
                class define(TUIMethod):
                    """
                    Enables you to define the parameters for the refinement region.
                    """
                class delete(TUIMethod):
                    """
                    Enables you to delete a refinement region.
                    """
                class list_all_regions(TUIMethod):
                    """
                    Lists all the refinement regions.
                    """

        class non_conformals(TUIMenu):
            """
            Enters the non-conformals menu.
            """
            def __init__(self, service, version, mode, path):
                self.controls = self.__class__.controls(service, version, mode, path + ["controls"])
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                self.separate = self.__class__.separate(service, version, mode, path + ["separate"])
                super().__init__(service, version, mode, path)
            class create(TUIMethod):
                """
                Creates the non-conformal interface on the specified face zones using the specified retriangulation method.
                """
            class separate(TUIMethod):
                """
                Enables you to separate the face zones comprising the non-conformal interface between the cell zones specified. Specify the cell zones where the interface is non-conformal, an appropriate gap distance, and the critical angle to be used for separating the face zones. You can also choose to orient the boundary face zones after separation and additionally write a journal file for the separation operation.   If you choose to write a journal file when using the /mesh/non-conformals/separate command to separate the mesh  interface zones, you can read the journal file to create the mesh interface automatically  in solution mode.
                """

            class controls(TUIMenu):
                """
                Enters the non-conformals controls menu.
                """
                def __init__(self, service, version, mode, path):
                    self.retri_method = self.__class__.retri_method(service, version, mode, path + ["retri_method"])
                    self.enable = self.__class__.enable(service, version, mode, path + ["enable"])
                    super().__init__(service, version, mode, path)
                class retri_method(TUIMethod):
                    """
                    Specifies the method to be used for retriangulating the quad faces on the non-conformal zones.
                    """
                class enable(TUIMethod):
                    """
                    Toggles the creation of a non-conformal interface.
                    """

        class modify(TUIMenu):
            """
            Enters the mesh modify menu.
            """
            def __init__(self, service, version, mode, path):
                self.extract_unused_nodes = self.__class__.extract_unused_nodes(service, version, mode, path + ["extract_unused_nodes"])
                self.select_entity = self.__class__.select_entity(service, version, mode, path + ["select_entity"])
                self.repair_negative_volume_cells = self.__class__.repair_negative_volume_cells(service, version, mode, path + ["repair_negative_volume_cells"])
                self.list_skewed_cells = self.__class__.list_skewed_cells(service, version, mode, path + ["list_skewed_cells"])
                self.auto_improve_warp = self.__class__.auto_improve_warp(service, version, mode, path + ["auto_improve_warp"])
                self.refine_cell = self.__class__.refine_cell(service, version, mode, path + ["refine_cell"])
                self.mesh_node = self.__class__.mesh_node(service, version, mode, path + ["mesh_node"])
                self.mesh_nodes_on_zone = self.__class__.mesh_nodes_on_zone(service, version, mode, path + ["mesh_nodes_on_zone"])
                self.clear_selections = self.__class__.clear_selections(service, version, mode, path + ["clear_selections"])
                self.delete_isolated_cells = self.__class__.delete_isolated_cells(service, version, mode, path + ["delete_isolated_cells"])
                self.auto_node_move = self.__class__.auto_node_move(service, version, mode, path + ["auto_node_move"])
                self.neighborhood_skew = self.__class__.neighborhood_skew(service, version, mode, path + ["neighborhood_skew"])
                self.smooth_node = self.__class__.smooth_node(service, version, mode, path + ["smooth_node"])
                self.list_selections = self.__class__.list_selections(service, version, mode, path + ["list_selections"])
                self.deselect_last = self.__class__.deselect_last(service, version, mode, path + ["deselect_last"])
                super().__init__(service, version, mode, path)
            class extract_unused_nodes(TUIMethod):
                """
                Places all unused nodes in a separate interior node zone.
                """
            class select_entity(TUIMethod):
                """
                Adds an entity (face, node, cell, etc.) to the selection list.
                """
            class repair_negative_volume_cells(TUIMethod):
                """
                Repairs negative volume cells by moving nodes. Specify the appropriate boundary zones, the number of iterations per node to be moved, dihedral angle, whether to restrict the movement of boundary nodes along the surface, and the number of iterations of the automatic node movement procedure (default, 1).
                """
            class list_skewed_cells(TUIMethod):
                """
                Lists cells with skewness in a specified range.
                """
            class auto_improve_warp(TUIMethod):
                """
                Enables you to improve face warp by node movement. Specify the appropriate cell zones and boundary zones, the maximum warp, the number of iterations per face to be improved, and the number of iterations of the automatic node movement procedure (default, 4).
                """
            class refine_cell(TUIMethod):
                """
                Attempts to refine the cells in the probe list by introducing a node nears its centroid. This technique is useful for removing very flat cells near the boundary when boundary sliver removal is not possible. After refining the cell, you should smooth the mesh.
                """
            class mesh_node(TUIMethod):
                """
                Attempts to introduce a new node into the existing mesh.
                """
            class mesh_nodes_on_zone(TUIMethod):
                """
                Inserts nodes associated with node or face zone into the volume mesh.
                """
            class clear_selections(TUIMethod):
                """
                Clears all items from the selection list.
                """
            class delete_isolated_cells(TUIMethod):
                """
                Delete isolated cells.
                """
            class auto_node_move(TUIMethod):
                """
                Enables you to improve the mesh quality by node movement. Specify the appropriate cell zones and boundary zones, the quality limit based on the quality measure selected, dihedral angle, the number of iterations per node to be moved and the number of iterations of the automatic node movement procedure (default, 1). You can also choose to restrict the movement of boundary nodes along the surface.
                """
            class neighborhood_skew(TUIMethod):
                """
                Reports the maximum skewness of cells using the specified node.
                """
            class smooth_node(TUIMethod):
                """
                Applies Laplace smoothing to the nodes in the selection list.
                """
            class list_selections(TUIMethod):
                """
                Lists all items in the selection list.
                """
            class deselect_last(TUIMethod):
                """
                Deselects the last item you selected using the select-entity command.
                """

        class manage(TUIMenu):
            """
            Enters the manage cell zones menu.
            """
            def __init__(self, service, version, mode, path):
                self.active_list = self.__class__.active_list(service, version, mode, path + ["active_list"])
                self.scale_model = self.__class__.scale_model(service, version, mode, path + ["scale_model"])
                self.adjacent_face_zones = self.__class__.adjacent_face_zones(service, version, mode, path + ["adjacent_face_zones"])
                self.origin = self.__class__.origin(service, version, mode, path + ["origin"])
                self.merge_dead_zones = self.__class__.merge_dead_zones(service, version, mode, path + ["merge_dead_zones"])
                self.revolve_face_zone = self.__class__.revolve_face_zone(service, version, mode, path + ["revolve_face_zone"])
                self.rotate_model = self.__class__.rotate_model(service, version, mode, path + ["rotate_model"])
                self.rotate = self.__class__.rotate(service, version, mode, path + ["rotate"])
                self.scale = self.__class__.scale(service, version, mode, path + ["scale"])
                self.auto_set_active = self.__class__.auto_set_active(service, version, mode, path + ["auto_set_active"])
                self.type = self.__class__.type(service, version, mode, path + ["type"])
                self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                self.set_active = self.__class__.set_active(service, version, mode, path + ["set_active"])
                self.id = self.__class__.id(service, version, mode, path + ["id"])
                self.list = self.__class__.list(service, version, mode, path + ["list"])
                self.change_prefix = self.__class__.change_prefix(service, version, mode, path + ["change_prefix"])
                self.merge = self.__class__.merge(service, version, mode, path + ["merge"])
                self.change_suffix = self.__class__.change_suffix(service, version, mode, path + ["change_suffix"])
                self.copy = self.__class__.copy(service, version, mode, path + ["copy"])
                self.get_material_point = self.__class__.get_material_point(service, version, mode, path + ["get_material_point"])
                self.name = self.__class__.name(service, version, mode, path + ["name"])
                self.translate = self.__class__.translate(service, version, mode, path + ["translate"])
                self.translate_model = self.__class__.translate_model(service, version, mode, path + ["translate_model"])
                super().__init__(service, version, mode, path)
            class active_list(TUIMethod):
                """
                Lists all active zones.
                """
            class scale_model(TUIMethod):
                """
                Scales all nodes of the model by a specified factor.
                """
            class adjacent_face_zones(TUIMethod):
                """
                Lists all face zones that refer to the specified cell zone.
                """
            class origin(TUIMethod):
                """
                Specifies a new origin for the mesh, to be used for cell zone rotation. The default origin is (0,0,0).
                """
            class merge_dead_zones(TUIMethod):
                """
                Enables you to merge dead zones having a cell count lower than the specified threshold value, with the adjacent cell zone. The result of the merge operation is determined by the type of the adjacent cell zone and the shared face area. The priority for merging with the adjacent cell zone based on type is fluid > solid > dead (that is, merging with an adjacent fluid zone takes priority over merging with an adjacent solid zone, which in turn takes priority over merging with a dead zone). Also, if the adjacent zones are of the same type (for example, fluid), the zone will be merged with the zone having the largest shared face area.
                """
            class revolve_face_zone(TUIMethod):
                """
                Generates cells by revolving a face thread.
                """
            class rotate_model(TUIMethod):
                """
                Rotates all nodes of the model by a specified angle.
                """
            class rotate(TUIMethod):
                """
                Rotates all nodes of specified cell zones by a specified angle.
                """
            class scale(TUIMethod):
                """
                Scales all nodes of specified cell zones by a specified factor.
                """
            class auto_set_active(TUIMethod):
                """
                Sets the active zones based on points that are defined in an external file. For each zone you want to activate, you need to specify the coordinates of a point in the zone, the zone type (for example, fluid), and (optionally) a new name. A sample file is shown below:.
                """
            class type(TUIMethod):
                """
                Changes the type and name of a cell zone.
                """
            class delete(TUIMethod):
                """
                Deletes a cell zone, along with its associated nodes and faces. When deleting cell zones that contain poly cells, you will be warned that the original mesh needs to be deleted and the original faces restored prior to remeshing the volumetric region.
                """
            class set_active(TUIMethod):
                """
                Sets the specified cell zones to be active.
                """
            class id(TUIMethod):
                """
                Specifies a new cell zone ID. If a conflict is detected, the change will be ignored.
                """
            class list(TUIMethod):
                """
                Prints information on all cell zones.
                """
            class change_prefix(TUIMethod):
                """
                Enables you to change the prefix for the cell zone.
                """
            class merge(TUIMethod):
                """
                Merges two or more cell zones.  For object-based merge, the selected zones must be in the same volumetric region. If  not, you will have to merge the volumetric regions first using /objects/volumetric-regions/merge. If the volumetric regions  cannot be merged because they are not contiguous, you will have to delete the object(s)  only before merging the cell zones.
                """
            class change_suffix(TUIMethod):
                """
                Change the suffix for specified face zones.
                """
            class copy(TUIMethod):
                """
                Copies all nodes and faces of specified cell zones.
                """
            class get_material_point(TUIMethod):
                """
                Prints the coordinates of the material point for the specified cell zone.  If the cell zone is non-contiguous, the get-material-point  command will print a list of material points, one for each contiguous region.
                """
            class name(TUIMethod):
                """
                Enables you to rename a cell zone.
                """
            class translate(TUIMethod):
                """
                Translates all nodes of specified cell zones by a specified vector.
                """
            class translate_model(TUIMethod):
                """
                Translates all nodes of the model by a specified vector.
                """

        class thin_volume_mesh(TUIMenu):
            """
            Creates a sweep-like mesh for a body occupying a thin gap. You define source and target boundary faces zones (the source face normal should point to the target). The source face mesh may be triangles or quads.
            """
            def __init__(self, service, version, mode, path):
                self.controls = self.__class__.controls(service, version, mode, path + ["controls"])
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                super().__init__(service, version, mode, path)
            class controls(TUIMethod):
                """
                Prime Auto Mesh thin volume controls.
                """
            class create(TUIMethod):
                """
                Initiates the dialog box to specify source and target faces and specify the following parameters.
                """

        class hexcore(TUIMenu):
            """
            Enters the hexcore menu.
            """
            def __init__(self, service, version, mode, path):
                self.controls = self.__class__.controls(service, version, mode, path + ["controls"])
                self.local_regions = self.__class__.local_regions(service, version, mode, path + ["local_regions"])
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                self.merge_tets_to_pyramids = self.__class__.merge_tets_to_pyramids(service, version, mode, path + ["merge_tets_to_pyramids"])
                super().__init__(service, version, mode, path)
            class create(TUIMethod):
                """
                Enables you to create the hexcore mesh according to the specified parameters.
                """
            class merge_tets_to_pyramids(TUIMethod):
                """
                Enables the merge-tets-to-pyramids command to reduce the total cell count.  If skip-tet-refinement is enabled, pairs of tets will be merged into pyramids. Hexcore count is unaffected.
                """

            class controls(TUIMenu):
                """
                Enters the hexcore controls menu.
                """
                def __init__(self, service, version, mode, path):
                    self.outer_domain_params = self.__class__.outer_domain_params(service, version, mode, path + ["outer_domain_params"])
                    self.peel_layers = self.__class__.peel_layers(service, version, mode, path + ["peel_layers"])
                    self.maximum_cell_length = self.__class__.maximum_cell_length(service, version, mode, path + ["maximum_cell_length"])
                    self.compute_max_cell_length = self.__class__.compute_max_cell_length(service, version, mode, path + ["compute_max_cell_length"])
                    self.only_hexcore = self.__class__.only_hexcore(service, version, mode, path + ["only_hexcore"])
                    self.keep_hex_tet_separate = self.__class__.keep_hex_tet_separate(service, version, mode, path + ["keep_hex_tet_separate"])
                    self.delete_dead_zones = self.__class__.delete_dead_zones(service, version, mode, path + ["delete_dead_zones"])
                    self.octree_hexcore = self.__class__.octree_hexcore(service, version, mode, path + ["octree_hexcore"])
                    self.smooth_interface = self.__class__.smooth_interface(service, version, mode, path + ["smooth_interface"])
                    self.define_hexcore_extents = self.__class__.define_hexcore_extents(service, version, mode, path + ["define_hexcore_extents"])
                    self.set_region_based_sizing = self.__class__.set_region_based_sizing(service, version, mode, path + ["set_region_based_sizing"])
                    self.skip_tet_refinement = self.__class__.skip_tet_refinement(service, version, mode, path + ["skip_tet_refinement"])
                    self.smooth_iterations = self.__class__.smooth_iterations(service, version, mode, path + ["smooth_iterations"])
                    self.buffer_layers = self.__class__.buffer_layers(service, version, mode, path + ["buffer_layers"])
                    self.merge_tets_to_pyramids = self.__class__.merge_tets_to_pyramids(service, version, mode, path + ["merge_tets_to_pyramids"])
                    self.island_thresholds = self.__class__.island_thresholds(service, version, mode, path + ["island_thresholds"])
                    self.non_fluid_type = self.__class__.non_fluid_type(service, version, mode, path + ["non_fluid_type"])
                    self.print_region_based_sizing = self.__class__.print_region_based_sizing(service, version, mode, path + ["print_region_based_sizing"])
                    self.maximum_initial_cells = self.__class__.maximum_initial_cells(service, version, mode, path + ["maximum_initial_cells"])
                    self.maximum_subdivisions = self.__class__.maximum_subdivisions(service, version, mode, path + ["maximum_subdivisions"])
                    self.avoid_1_by_8_cell_jump_in_hexcore = self.__class__.avoid_1_by_8_cell_jump_in_hexcore(service, version, mode, path + ["avoid_1_by_8_cell_jump_in_hexcore"])
                    self.smooth_relaxation = self.__class__.smooth_relaxation(service, version, mode, path + ["smooth_relaxation"])
                    super().__init__(service, version, mode, path)
                class peel_layers(TUIMethod):
                    """
                    Specifies the distance for the hexcore interface to peel-back from the boundary. The default value is 0. The higher the value of peel layer, the bigger the distance between the hexcore interface and the boundary.
                    """
                class maximum_cell_length(TUIMethod):
                    """
                    Sets the maximum cell length for the hex cells in the domain.
                    """
                class compute_max_cell_length(TUIMethod):
                    """
                    Computes the maximum cell length for the hexcore mesh.
                    """
                class only_hexcore(TUIMethod):
                    """
                    Create hexcore and activate tet domain.
                    """
                class keep_hex_tet_separate(TUIMethod):
                    """
                    Separate Hex and Tet cells.
                    """
                class delete_dead_zones(TUIMethod):
                    """
                    Toggles the automatic deleting of the dead zones.
                    """
                class octree_hexcore(TUIMethod):
                    """
                    Speeds up hexahedral core generation by enabling the octree technique for hexcore mesh generation. This option is disabled by default.   Body-of-influence sizing may be used for refinement.  This option does not support hexcore generation up to boundaries.
                    """
                class smooth_interface(TUIMethod):
                    """
                    Enable smoothing of hexcore interface.
                    """
                class define_hexcore_extents(TUIMethod):
                    """
                    Enables you to extend the hexcore mesh to specified domain extents and/or selected planar boundaries. When enabled, the outer-domain-params sub-menu will be available.
                    """
                class set_region_based_sizing(TUIMethod):
                    """
                    Allows you to specify local sizing settings (max cell length and growth rate) for specified region(s).
                    """
                class skip_tet_refinement(TUIMethod):
                    """
                    Enables you to omit the tetrahedral refinement phase for reducing total cell count (default is no). Hex cell count is unaffected.
                    """
                class smooth_iterations(TUIMethod):
                    """
                    Number of smoothing iterations on hexcore interface.
                    """
                class buffer_layers(TUIMethod):
                    """
                    Sets the number of addition cells to mark for subdivision.
                    """
                class merge_tets_to_pyramids(TUIMethod):
                    """
                    Merge tets into pyramids.
                    """
                class island_thresholds(TUIMethod):
                    """
                    Maximum number of cells and volume fraction in islands, deleted while separating the cells by region.
                    """
                class non_fluid_type(TUIMethod):
                    """
                    Selects the default non-fluid cell zone type. After the mesh is initialized, any non-fluid zones will be set to this type. If the mesh includes multiple regions (for example, the problem for which you are creating the mesh includes a fluid zone and one or more solid zones), and you plan to refine all of them using the same refinement parameters, modify the Non-Fluid Type
                    before generating the hexcore mesh.  For zone-based meshing, if any cell zone has at least one boundary zone type as inlet, it will automatically be set to fluid type. For object based meshing, volume region type is used to determine the cell zone type.
                    """
                class print_region_based_sizing(TUIMethod):
                    """
                    Displays local sizing settings (max cell length and growth rate) for specified region(s).
                    """
                class maximum_initial_cells(TUIMethod):
                    """
                    Specifies the maximum number of cells in the initial Cartesian mesh.
                    """
                class maximum_subdivisions(TUIMethod):
                    """
                    Maximum number of subdivision sweeps.
                    """
                class avoid_1_by_8_cell_jump_in_hexcore(TUIMethod):
                    """
                    Avoid-1:8-cell-jump-in-hexcore.
                    """
                class smooth_relaxation(TUIMethod):
                    """
                    Smoothing under relaxation on hexcore interface.
                    """

                class outer_domain_params(TUIMenu):
                    """
                    Contains options for defining the outer domain parameters. This sub-menu is available only when define-hexcore-extents? is enabled.
                    """
                    def __init__(self, service, version, mode, path):
                        self.list = self.__class__.list(service, version, mode, path + ["list"])
                        self.specify_coordinates = self.__class__.specify_coordinates(service, version, mode, path + ["specify_coordinates"])
                        self.delete_old_face_zones = self.__class__.delete_old_face_zones(service, version, mode, path + ["delete_old_face_zones"])
                        self.coordinates = self.__class__.coordinates(service, version, mode, path + ["coordinates"])
                        self.auto_align_tolerance = self.__class__.auto_align_tolerance(service, version, mode, path + ["auto_align_tolerance"])
                        self.auto_align = self.__class__.auto_align(service, version, mode, path + ["auto_align"])
                        self.specify_boundaries = self.__class__.specify_boundaries(service, version, mode, path + ["specify_boundaries"])
                        self.auto_align_boundaries = self.__class__.auto_align_boundaries(service, version, mode, path + ["auto_align_boundaries"])
                        self.boundaries = self.__class__.boundaries(service, version, mode, path + ["boundaries"])
                        super().__init__(service, version, mode, path)
                    class list(TUIMethod):
                        """
                        Lists the boundaries to which the hexcore mesh is to be generated. This option is available only when the specify-boundaries? option is enabled and the boundaries are specified.
                        """
                    class specify_coordinates(TUIMethod):
                        """
                        Enables you to specify the extents of the hexcore outer box using the coordinates command.
                        """
                    class delete_old_face_zones(TUIMethod):
                        """
                        Enables you to delete the original tri face zones that have been replaced during the hexcore meshing process. This option is available only when the specify-boundaries? option is enabled and the boundaries are specified.
                        """
                    class coordinates(TUIMethod):
                        """
                        Specifies the extents (min and max coordinates) of the hexcore outer box. This command is available when the specify-coordinates? option is enabled.
                        """
                    class auto_align_tolerance(TUIMethod):
                        """
                        Specifies the tolerance for aligning boundary zones when auto-align? is enabled.
                        """
                    class auto_align(TUIMethod):
                        """
                        Enables you to axis-align non-aligned planar boundaries to which hexcore mesh is to be generated. This option is available only when the specify-boundaries? option is enabled and the boundaries are specified.
                        """
                    class specify_boundaries(TUIMethod):
                        """
                        Enables you to specify selected boundaries to which the hexcore mesh is to be generated using the boundaries command.
                        """
                    class auto_align_boundaries(TUIMethod):
                        """
                        Aligns the boundary zones specified (using the boundaries command) with the tolerance specified \ (using the auto-align-tolerance command) when auto-align? is enabled.
                        """
                    class boundaries(TUIMethod):
                        """
                        Specifies the boundaries to which the hexcore mesh is to be generated when the specify-boundaries? option is enabled. After specifying the boundaries, the auto-align?, delete-old-face-zones?, and list options will also be available.
                        """

            class local_regions(TUIMenu):
                """
                Enters the hexcore local refinement region sub-menu.
                """
                def __init__(self, service, version, mode, path):
                    self.ideal_quad_area = self.__class__.ideal_quad_area(service, version, mode, path + ["ideal_quad_area"])
                    self.ideal_hex_vol = self.__class__.ideal_hex_vol(service, version, mode, path + ["ideal_hex_vol"])
                    self.define = self.__class__.define(service, version, mode, path + ["define"])
                    self.activate = self.__class__.activate(service, version, mode, path + ["activate"])
                    self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                    self.list_all_regions = self.__class__.list_all_regions(service, version, mode, path + ["list_all_regions"])
                    self.init = self.__class__.init(service, version, mode, path + ["init"])
                    self.deactivate = self.__class__.deactivate(service, version, mode, path + ["deactivate"])
                    super().__init__(service, version, mode, path)
                class ideal_quad_area(TUIMethod):
                    """
                    Ideal quad area for given edge length.
                    """
                class ideal_hex_vol(TUIMethod):
                    """
                    Reports the ideal hex volume for the given edge length.
                    """
                class define(TUIMethod):
                    """
                    Defines the local region according to the specified parameters.
                    """
                class activate(TUIMethod):
                    """
                    Enables you to activate the specified local regions for refinement.
                    """
                class delete(TUIMethod):
                    """
                    Deletes the specified refinement region.
                    """
                class list_all_regions(TUIMethod):
                    """
                    Lists the defined and active regions in the console.
                    """
                class init(TUIMethod):
                    """
                    Creates a default region encompassing the entire geometry.
                    """
                class deactivate(TUIMethod):
                    """
                    Enables you to deactivate the specified local regions for refinement.
                    """

        class rapid_octree(TUIMenu):
            """
            Enters the rapid octree menu, which provides text commands for using the Rapid Octree mesher.
            """
            def __init__(self, service, version, mode, path):
                self.advanced_meshing_options = self.__class__.advanced_meshing_options(service, version, mode, path + ["advanced_meshing_options"])
                self.mesh_sizing = self.__class__.mesh_sizing(service, version, mode, path + ["mesh_sizing"])
                self.boundary_layer_mesh_configuration = self.__class__.boundary_layer_mesh_configuration(service, version, mode, path + ["boundary_layer_mesh_configuration"])
                self.refinement_regions = self.__class__.refinement_regions(service, version, mode, path + ["refinement_regions"])
                self.boundary_mesh_optimization = self.__class__.boundary_mesh_optimization(service, version, mode, path + ["boundary_mesh_optimization"])
                self.bounding_box = self.__class__.bounding_box(service, version, mode, path + ["bounding_box"])
                self.dry_run = self.__class__.dry_run(service, version, mode, path + ["dry_run"])
                self.geometry = self.__class__.geometry(service, version, mode, path + ["geometry"])
                self.distribute_geometry = self.__class__.distribute_geometry(service, version, mode, path + ["distribute_geometry"])
                self.create_stair_step_mesh = self.__class__.create_stair_step_mesh(service, version, mode, path + ["create_stair_step_mesh"])
                self.flow_volume = self.__class__.flow_volume(service, version, mode, path + ["flow_volume"])
                self.reset_bounding_box = self.__class__.reset_bounding_box(service, version, mode, path + ["reset_bounding_box"])
                self.delete_poor_quality_cells = self.__class__.delete_poor_quality_cells(service, version, mode, path + ["delete_poor_quality_cells"])
                self.boundary_treatment = self.__class__.boundary_treatment(service, version, mode, path + ["boundary_treatment"])
                self.estimate_cell_count = self.__class__.estimate_cell_count(service, version, mode, path + ["estimate_cell_count"])
                self.undo_last_meshing_operation = self.__class__.undo_last_meshing_operation(service, version, mode, path + ["undo_last_meshing_operation"])
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                self.improve_geometry_resolution = self.__class__.improve_geometry_resolution(service, version, mode, path + ["improve_geometry_resolution"])
                self.boundary_mesh_optimization_scheme = self.__class__.boundary_mesh_optimization_scheme(service, version, mode, path + ["boundary_mesh_optimization_scheme"])
                self.verbosity = self.__class__.verbosity(service, version, mode, path + ["verbosity"])
                self.is_manifold_geo = self.__class__.is_manifold_geo(service, version, mode, path + ["is_manifold_geo"])
                super().__init__(service, version, mode, path)
            class boundary_mesh_optimization(TUIMethod):
                """
                Enable optimization to improve orthogonality at the boundary mesh.
                """
            class bounding_box(TUIMethod):
                """
                Defines/modifies the bounding box around the geometry.
                """
            class dry_run(TUIMethod):
                """
                If yes: Just print diagnostic information, do not create a mesh.
                """
            class geometry(TUIMethod):
                """
                Allows you to apply the Rapid Octree mesher to a defined mesh object or geometry object rather than all available surface zones. Note that using a mesh object with multiple volumetric regions allows you to generate multiple disconnected cell zones that can be coupled by a non-conformal mesh interface in the solution mode; all other input objects result in the creation of a single volume / cell zone.
                """
            class distribute_geometry(TUIMethod):
                """
                Enables/disables the distribution of the input geometry across partitions / compute nodes, so that it is not copied to each process. This reduces the memory requirements of the mesh generation significantly, especially for geometries with a high number of triangles. Note that this geometric distribution is enabled by default and is automatically deactivated if the geometry is not fully enclosed by the defined bounding box.
                """
            class create_stair_step_mesh(TUIMethod):
                """
                Create rapid octree mesh with a cartesian boundary approximation.
                """
            class flow_volume(TUIMethod):
                """
                Specifies the volume to be filled by the mesh.
                """
            class reset_bounding_box(TUIMethod):
                """
                Redefines the bounding box extents to encompass all of the surfaces of the currently selected geometry, and updates the base length scale used in the mesh generation process.
                """
            class delete_poor_quality_cells(TUIMethod):
                """
                Delete all cells with orthogonal-quality less than 0.01.
                """
            class boundary_treatment(TUIMethod):
                """
                Selects the boundary treatment option. Enter 0 for the Boundary Projection treatment or 1 for the Cartesian Snapping treatment.
                """
            class estimate_cell_count(TUIMethod):
                """
                Give a quick estimate about the expected number of cells.
                """
            class undo_last_meshing_operation(TUIMethod):
                """
                Attempts to restore the object state (including its surfaces) as it was prior to the meshing operation performed by the Rapid Octree mesher.
                """
            class create(TUIMethod):
                """
                Creates a mesh using the Rapid Octree mesher.
                """
            class improve_geometry_resolution(TUIMethod):
                """
                Enables improved geometry resolution.
                """
            class boundary_mesh_optimization_scheme(TUIMethod):
                """
                Set optimization scheme for boundary mesh optimization in projection meshing.
                """
            class verbosity(TUIMethod):
                """
                Sets the verbosity of the messages printed by the Rapid Octree mesher.
                """
            class is_manifold_geo(TUIMethod):
                """
                Set to yes if the geomety is manifold (speed up mesh generation).
                """

            class advanced_meshing_options(TUIMenu):
                """
                Advanced and experimental options for octree mesh generation.
                """
                def __init__(self, service, version, mode, path):
                    self.target_int_face_warp = self.__class__.target_int_face_warp(service, version, mode, path + ["target_int_face_warp"])
                    self.aspect_ratio_skewness_limit = self.__class__.aspect_ratio_skewness_limit(service, version, mode, path + ["aspect_ratio_skewness_limit"])
                    self.improved_proximity_for_projection = self.__class__.improved_proximity_for_projection(service, version, mode, path + ["improved_proximity_for_projection"])
                    self.rename_bounding_box_zones = self.__class__.rename_bounding_box_zones(service, version, mode, path + ["rename_bounding_box_zones"])
                    self.distance_erosion_factor = self.__class__.distance_erosion_factor(service, version, mode, path + ["distance_erosion_factor"])
                    self.max_num_inflection_point_iter = self.__class__.max_num_inflection_point_iter(service, version, mode, path + ["max_num_inflection_point_iter"])
                    self.planar_feature_recovery_mode = self.__class__.planar_feature_recovery_mode(service, version, mode, path + ["planar_feature_recovery_mode"])
                    self.target_cell_orthoskew = self.__class__.target_cell_orthoskew(service, version, mode, path + ["target_cell_orthoskew"])
                    self.projection_priority_zones = self.__class__.projection_priority_zones(service, version, mode, path + ["projection_priority_zones"])
                    self.pseudo_normal_mode = self.__class__.pseudo_normal_mode(service, version, mode, path + ["pseudo_normal_mode"])
                    self.target_bnd_face_warp = self.__class__.target_bnd_face_warp(service, version, mode, path + ["target_bnd_face_warp"])
                    self.extract_refinement_levels = self.__class__.extract_refinement_levels(service, version, mode, path + ["extract_refinement_levels"])
                    self.activate_projection_layer_improvement_algorithm = self.__class__.activate_projection_layer_improvement_algorithm(service, version, mode, path + ["activate_projection_layer_improvement_algorithm"])
                    super().__init__(service, version, mode, path)
                class target_int_face_warp(TUIMethod):
                    """
                    Set target face warpage for interior faces in mesh (-1.0 - 1.0). Higher values are likely to increase pullback.
                    """
                class aspect_ratio_skewness_limit(TUIMethod):
                    """
                    Ignore cells with higher skew in aspect ratio improvement.
                    """
                class improved_proximity_for_projection(TUIMethod):
                    """
                    Activate the imporved version of proximity refinement for projection boundary treatment.
                    """
                class rename_bounding_box_zones(TUIMethod):
                    """
                    Set flag to change naming scheme of bounding box surface zones.
                    """
                class distance_erosion_factor(TUIMethod):
                    """
                    Set distance erosion factor as a factor of prism edge length.
                    """
                class max_num_inflection_point_iter(TUIMethod):
                    """
                    Sets the maximum number of iterations for inflection point removal during projection front fix.
                    """
                class planar_feature_recovery_mode(TUIMethod):
                    """
                    Set the mode for planar feature recovery from 0:off to 2: with hanging nodes.
                    """
                class target_cell_orthoskew(TUIMethod):
                    """
                    Set target orthoskew in mesh (0.0-1.0). Smaller values are likely to increase pullback.
                    """
                class projection_priority_zones(TUIMethod):
                    """
                    Prioritize zone association of faces crossing multiple boundary zones.
                    """
                class pseudo_normal_mode(TUIMethod):
                    """
                    Sets the mode for cumputing projection front sudo normals.
                    """
                class target_bnd_face_warp(TUIMethod):
                    """
                    Set target face warpage for boundary faces in mesh (-1.0 - 1.0). Higher values are likely to increase pullback.
                    """
                class extract_refinement_levels(TUIMethod):
                    """
                    Enables computation of refinement levels for PUMA.
                    """
                class activate_projection_layer_improvement_algorithm(TUIMethod):
                    """
                    Force the projection algorithm to do smoothing expansion without prisms defined.
                    """

            class mesh_sizing(TUIMenu):
                """
                Enters the mesh sizing menu, which allows you to define the cell sizes.
                """
                def __init__(self, service, version, mode, path):
                    self.add_surface_sizing = self.__class__.add_surface_sizing(service, version, mode, path + ["add_surface_sizing"])
                    self.volume_transition_exponent = self.__class__.volume_transition_exponent(service, version, mode, path + ["volume_transition_exponent"])
                    self.surface_transition_layers = self.__class__.surface_transition_layers(service, version, mode, path + ["surface_transition_layers"])
                    self.max_cell_size = self.__class__.max_cell_size(service, version, mode, path + ["max_cell_size"])
                    self.boundary_layers = self.__class__.boundary_layers(service, version, mode, path + ["boundary_layers"])
                    self.clear_all_surface_sizings = self.__class__.clear_all_surface_sizings(service, version, mode, path + ["clear_all_surface_sizings"])
                    self.change_surface_sizing = self.__class__.change_surface_sizing(service, version, mode, path + ["change_surface_sizing"])
                    self.smooth_mesh_coarsening = self.__class__.smooth_mesh_coarsening(service, version, mode, path + ["smooth_mesh_coarsening"])
                    self.buffer_layers = self.__class__.buffer_layers(service, version, mode, path + ["buffer_layers"])
                    self.surface_coarsening_layers = self.__class__.surface_coarsening_layers(service, version, mode, path + ["surface_coarsening_layers"])
                    self.feature_angle_refinement = self.__class__.feature_angle_refinement(service, version, mode, path + ["feature_angle_refinement"])
                    self.boundary_cell_size = self.__class__.boundary_cell_size(service, version, mode, path + ["boundary_cell_size"])
                    self.mesh_coarsening_exponent = self.__class__.mesh_coarsening_exponent(service, version, mode, path + ["mesh_coarsening_exponent"])
                    self.list_surface_sizings = self.__class__.list_surface_sizings(service, version, mode, path + ["list_surface_sizings"])
                    self.delete_surface_sizing = self.__class__.delete_surface_sizing(service, version, mode, path + ["delete_surface_sizing"])
                    super().__init__(service, version, mode, path)
                class add_surface_sizing(TUIMethod):
                    """
                    Add a size function definition.
                    """
                class volume_transition_exponent(TUIMethod):
                    """
                    Set the exponent (power of two) for the mesh coarsening transition. A higher value results in a slower transition from fine to coarse cells.
                    """
                class surface_transition_layers(TUIMethod):
                    """
                    Set the minimum number of constant-size cells adjacent to the geometry layer.
                    """
                class max_cell_size(TUIMethod):
                    """
                    Sets the maximum cell size in the octree mesh.
                    """
                class boundary_layers(TUIMethod):
                    """
                    Set the minimum number of constant-size cells adjacent to the geometry.
                    """
                class clear_all_surface_sizings(TUIMethod):
                    """
                    Delete all size function definitions.
                    """
                class change_surface_sizing(TUIMethod):
                    """
                    Change a size function definition.
                    """
                class smooth_mesh_coarsening(TUIMethod):
                    """
                    Enable smoothing of the transitions between regions of different mesh sizes.
                    """
                class buffer_layers(TUIMethod):
                    """
                    Set the number of buffer layers.
                    """
                class surface_coarsening_layers(TUIMethod):
                    """
                    Set the minimum number of constant-size cells adjacent to the geometry.
                    """
                class feature_angle_refinement(TUIMethod):
                    """
                    Defines the angular threshold and number of refinement levels for features. This text command is only available when the Boundary Projection treatment is selected through the /mesh/rapid-octree/boundary-treatment text command.
                    """
                class boundary_cell_size(TUIMethod):
                    """
                    Sets the default cell size for the geometry.
                    """
                class mesh_coarsening_exponent(TUIMethod):
                    """
                    Set the exponent (power of two) for mesh coarsening. Higher values will lead to a slower transiton from fine to coarse cells.
                    """
                class list_surface_sizings(TUIMethod):
                    """
                    List all size function definitions.
                    """
                class delete_surface_sizing(TUIMethod):
                    """
                    Delete a size function definition.
                    """

            class boundary_layer_mesh_configuration(TUIMenu):
                """
                Define anisotropic refinements of the projection layer (prismatic layers).
                """
                def __init__(self, service, version, mode, path):
                    self.list = self.__class__.list(service, version, mode, path + ["list"])
                    self.delete_all = self.__class__.delete_all(service, version, mode, path + ["delete_all"])
                    self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                    self.add = self.__class__.add(service, version, mode, path + ["add"])
                    self.edit = self.__class__.edit(service, version, mode, path + ["edit"])
                    super().__init__(service, version, mode, path)
                class list(TUIMethod):
                    """
                    Specify the number of prismatic layers for surface zones.
                    """
                class delete_all(TUIMethod):
                    """
                    Specify the number of prismatic layers for surface zones.
                    """
                class delete(TUIMethod):
                    """
                    Specify the number of prismatic layers for surface zones.
                    """
                class add(TUIMethod):
                    """
                    Add a boudnary layer definition.
                    """
                class edit(TUIMethod):
                    """
                    Specify the number of prismatic layers for surface zones.
                    """

            class refinement_regions(TUIMenu):
                """
                Enters the rapid octree refinement region menu, which allows you to manage the refinement regions.
                """
                def __init__(self, service, version, mode, path):
                    self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                    self.list = self.__class__.list(service, version, mode, path + ["list"])
                    self.list_properties = self.__class__.list_properties(service, version, mode, path + ["list_properties"])
                    self.edit = self.__class__.edit(service, version, mode, path + ["edit"])
                    self.add = self.__class__.add(service, version, mode, path + ["add"])
                    super().__init__(service, version, mode, path)
                class delete(TUIMethod):
                    """
                    Deletes a refinement region.
                    """
                class list(TUIMethod):
                    """
                    Lists all of the refinement regions.
                    """
                class list_properties(TUIMethod):
                    """
                    List the properties of a refinement region definition.
                    """
                class edit(TUIMethod):
                    """
                    Edit a refinement region definition.
                    """
                class add(TUIMethod):
                    """
                    Adds a refinement region to the domain.
                    """
