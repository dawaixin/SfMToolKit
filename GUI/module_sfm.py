from tkinter import *
from GUI.tooltip import CreateToolTip
from tkinter.ttk import *
from sfm import SfM
from GUI.commands import load_file, load_directory



class ModuleSfM(Frame):

    def __init__(self, master):
        super().__init__()
        self.master = master

        # General parameters and outputs
        self.working_dir = ''
        self.image_dir = ''
        self.pipeline_type = BooleanVar()
        self.robust = BooleanVar()
        self.colourised = BooleanVar()
        self.dense = BooleanVar()
        self.dense_mesh = BooleanVar()
        self.sparse_mesh = BooleanVar()
        self.refine = BooleanVar()
        self.texture = BooleanVar()

        # Image listing
        self.focal = StringVar()
        self.intrinsics = StringVar()
        self.camera_model = StringVar()
        self.group_camera_model = BooleanVar()
        self.pose_prior = StringVar()
        self.xyz_coordinate = BooleanVar()

        # Feature Detection
        self.FD_recompute = BooleanVar()
        self.FD_describer_method = StringVar()
        self.FD_describer_presets = StringVar()
        self.FD_upright = BooleanVar()

        # Feature Matching
        self.FM_recompute = BooleanVar()
        self.FM_ratio = StringVar()
        self.FM_geometric_model = StringVar()
        self.FM_video_mode = StringVar()
        self.FM_pair_list = ''
        self.FM_nearest_matching_method = StringVar()

        # Global Reconstruction
        self.GR_rotation = StringVar()
        self.GR_translation = StringVar()
        self.GR_refine = StringVar()

        # Incremental Reconstruction
        self.IR_refine = StringVar()
        self.IR_camera = StringVar()

        # Robust Recontruction
        self.RR_bundle = BooleanVar()
        self.RR_residual = StringVar()

        # PC Densification
        self.DPC_resolution = StringVar()
        self.DPC_min_resolution = StringVar()
        self.DPC_views = StringVar()
        self.DPC_views_fuse = StringVar()
        self.DPC_sample = StringVar()
        self.DPC_color = BooleanVar()
        self.DPC_normals = BooleanVar()

        # Mesh Reconstruction
        self.MR_min = StringVar()
        self.MR_quality = StringVar()
        self.MR_decimate = StringVar()
        self.MR_spurious = StringVar()
        self.MR_spikes = BooleanVar()
        self.MR_holes = StringVar()
        self.MR_smooth = StringVar()

        # Mesh Refinement
        self.MF_resolution = StringVar()
        self.MF_min = StringVar()
        self.MF_max = StringVar()
        self.MF_decimate = StringVar()
        self.MF_holes = StringVar()
        self.MF_face_area = StringVar()
        self.MF_scales = StringVar()
        self.MF_scale_step = StringVar()

        # Mesh Texturing
        self.TM_resolution = StringVar()
        self.TM_min = StringVar()
        self.TM_outlier = StringVar()
        self.TM_heuristic = StringVar()


    def build_form(self):
        rowTitle = Text(self, height=3)
        rowTitle.insert(END,"\nMODULE I - Structure from Motion\n")
        rowTitle.config(state=DISABLED)
        rowTitle.pack(side=TOP, fill=X)

        # add the notebook
        notebook = Notebook(self, width=800)

        general_parameters = Frame(notebook)
        notebook.add(general_parameters, text="General Parameters")
        self.build_general(general_parameters)

        image_listing = Frame(notebook)
        notebook.add(image_listing, text="Image Listing")
        self.build_IL(image_listing)

        feature_detection = Frame(notebook)
        notebook.add(feature_detection, text="Feature Detection")
        self.build_FD(feature_detection)

        feature_matching = Frame(notebook)
        self.build_FM(feature_matching)
        notebook.add(feature_matching, text="Feature Matching")

        global_reconstruction = Frame(notebook)
        self.build_reconstruction(global_reconstruction)
        notebook.add(global_reconstruction, text="Reconstruction")

        notebook2 = Notebook(self, width=800)

        densification = Frame(notebook2)
        self.build_densification(densification)
        notebook2.add(densification, text="Densify Point Cloud")

        reconstruction = Frame(notebook2)
        self.build_mesh(reconstruction)
        notebook2.add(reconstruction, text="Mesh Reconstruction")

        refinement = Frame(notebook2)
        self.build_refinement(refinement)
        notebook2.add(refinement, text="Mesh Refinement")

        texturing = Frame(notebook2)
        self.build_texturing(texturing)
        notebook2.add(texturing, text="Mesh Texturing")

        notebook.pack(side=TOP)
        notebook2.pack(side=TOP)
        #########################################
        # GENERATE THE CONFIGURATION AND RUN IT #
        #########################################

        row_run = Frame(self)
        run_button = Button(row_run, text="Run module", command=lambda: self.run_module(), width=10)
        row_run.pack(side=TOP, fill=X)
        run_button.pack(side=RIGHT)

    def build_general(self, master):
        ######################
        # GENERAL PARAMETERS #
        ######################

        row1 = Frame(master)
        lab1 = Label(row1, width=15, text='Working Directory', anchor='w')
        self.working_dir = Entry(row1)
        browse1 = Button(row1, text='Browse...', command=lambda: load_directory(self.working_dir, self), width=10)
        CreateToolTip(browse1, "Select the working directory for the SfM pipeline")

        row1.pack(side=TOP, fill=X)
        lab1.pack(side=LEFT)
        self.working_dir.pack(side=RIGHT, expand=YES, fill=X)
        browse1.pack(side=RIGHT)

        row2 = Frame(master)
        lab2 = Label(row2, width=15, text='Image Directory', anchor='w')
        self.image_dir = Entry(row2)
        browse2 = Button(row2, text='Browse...', command=lambda: load_directory(self.image_dir, self), width=10)
        CreateToolTip(browse2, "Select the directory containing the images for the SfM pipeline")

        row2.pack(side=TOP, fill=X)
        lab2.pack(side=LEFT)
        self.image_dir.pack(side=RIGHT, expand=YES, fill=X)
        browse2.pack(side=RIGHT)

        #########################
        # BUILD DESIRED OUTPUTS #
        #########################

        row_outputs = Frame(master)
        row_outputs2 = Frame(master)

        pipeline_type_chk = Checkbutton(row_outputs, text="Pipeline Global", variable=self.pipeline_type)
        robust_chk = Checkbutton(row_outputs, text="Robust reconstruction", variable=self.robust)
        colourised_chk = Checkbutton(row_outputs, text="Colourised point clouds", variable=self.colourised)
        dense_chk = Checkbutton(row_outputs, text="Dense reconstruction", variable=self.dense)
        sparse_mesh_chk = Checkbutton(row_outputs2, text="Sparse mesh", variable=self.sparse_mesh)
        dense_mesh_chk = Checkbutton(row_outputs2, text="Dense mesh", variable=self.dense_mesh)
        refine_chk = Checkbutton(row_outputs2, text="Refine mesh", variable=self.refine)
        texture_chk = Checkbutton(row_outputs2, text="Texture mesh", variable=self.texture)

        row_outputs.pack(side=TOP, fill=X)
        row_outputs2.pack(side=TOP, fill=X)

        pipeline_type_chk.pack(side=LEFT)
        CreateToolTip(pipeline_type_chk, "Select this to use the Global Pipeline. The Sequential Pipeline is run otherwise.")
        robust_chk.pack(side=LEFT)
        CreateToolTip(robust_chk, "If selected, the robust sparse reconstruction is created")
        colourised_chk.pack(side=LEFT)
        CreateToolTip(colourised_chk, "Colourise the point clouds")
        dense_chk.pack(side=LEFT)
        CreateToolTip(dense_chk, "Densify the point cloud")
        sparse_mesh_chk.pack(side=LEFT)
        CreateToolTip(sparse_mesh_chk, "Create the sparse mesh")
        dense_mesh_chk.pack(side=LEFT)
        CreateToolTip(dense_mesh_chk, "Create the dense mesh")
        refine_chk.pack(side=LEFT)
        CreateToolTip(refine_chk, "Refine the meshes")
        texture_chk.pack(side=LEFT)
        CreateToolTip(texture_chk, "Texture the meshes")


    def build_IL(self, master):

        row_il = Frame(master)
        row_il2 = Frame(master)
        row_il3 = Frame(master)
        # focal
        focal_label = Label(row_il, width=20, text='Focal Length (pixels)', anchor='w')
        self.focal = Entry(row_il)
        # intrinsics
        intrinsics_label = Label(row_il, width=20, text='Intrinsics', anchor='w')
        self.intrinsics = Entry(row_il)
        # camera model
        models = ["", "1", "2", "3", "4", "5", "7"]
        camera_model_label = Label(row_il2, width=20, text='Camera model', anchor='w')
        camera_model = OptionMenu(row_il2, self.camera_model, *models)
        self.camera_model.set(models[3])
        # group camera model
        group_camera_model_chk = Checkbutton(row_il2, text="Group Camera Model", variable=self.group_camera_model)
        self.group_camera_model.set(True)
        # pose prior
        pose_prior_chk = Checkbutton(row_il3, text="Use pose priors if available", variable=self.pose_prior)
        self.pose_prior.set(True)
        # XYZ coordinate system
        xyz_coordinate_chk = Checkbutton(row_il3, text="Coordinate system, 0=ECEF 1=UTM", variable=self.xyz_coordinate)

        row_il.pack(side=TOP, fill=X)
        focal_label.pack(side=LEFT)
        CreateToolTip(focal_label, "Express the focal length of the camera in pixels, if unknown, you can multiply the largest image dimension by 1.2")
        self.focal.pack(side=LEFT)
        intrinsics_label.pack(side=LEFT)
        self.intrinsics.pack(side=LEFT)
        CreateToolTip(intrinsics_label, "Express the camera intrinsics, in the form of the Kmatrix \"f;0;ppx;0;f;ppy;0;0;1\"")

        row_il2.pack(side=TOP, fill=X)
        camera_model_label.pack(side=LEFT)
        camera_model.pack(side=LEFT)
        CreateToolTip(camera_model_label, "Camera model type:\n1: Pinhole\n2: Pinhole radial 1\n3: Pinhole radial 3 (default)\n4: Pinhole brown 2\n5: Pinhole with a simple Fish-eye distortion\n7: Spherical camera")
        group_camera_model_chk.pack(side=LEFT)
        CreateToolTip(group_camera_model_chk, "Check if cameras can share intrinsics (default)")
        row_il3.pack(side=TOP, fill=X)
        pose_prior_chk.pack(side=LEFT)
        xyz_coordinate_chk.pack(side=LEFT)

    def build_FD(self, master):
        row_fd = Frame(master)
        row_fd2 = Frame(master)

        force_chk = Checkbutton(row_fd, text="Recompute Feature Detection", variable=self.FD_recompute)
        CreateToolTip(force_chk, "Check this if you want to recompute the features")
        upright_chk = Checkbutton(row_fd, text="Force upright", variable=self.FD_upright)
        CreateToolTip(upright_chk, "Use upright features")
        describer_method_label = Label(row_fd2, text="Describer Method", width=20, anchor='w')
        describers = ["", "SIFT", "SIFT_ANATOMY", "AKAZE_FLOAT", "AKAZE_MLDB"]
        describer_method = OptionMenu(row_fd2, self.FD_describer_method, *describers)
        CreateToolTip(describer_method_label, "Method to use to describe an image:\nSIFT (default)\nSIFT_ANATOMY,\nAKAZE_FLOAT: AKAZE with floating point descriptors,\nAKAZE_MLDB:  AKAZE with binary descriptors")
        self.FD_describer_method.set(describers[1])
        describer_preset_label = Label(row_fd2, text="Describer Preset", width=20, anchor='w')
        describer_presets = ["", "NORMAL", "HIGH", "ULTRA"]
        describer_preset = OptionMenu(row_fd2, self.FD_describer_presets, *describer_presets)
        CreateToolTip(describer_preset_label, "Used to control the Image_describer configuration:\nNORMAL (default)\nHIGH\nULTRA: !!Can take long time!!")
        self.FD_describer_presets.set(describer_presets[1])

        row_fd.pack(side=TOP, fill=X)
        row_fd2.pack(side=TOP, fill=X)
        force_chk.pack(side=LEFT)
        upright_chk.pack(side=LEFT)
        describer_method_label.pack(side=LEFT)
        describer_method.pack(side=LEFT)
        describer_preset_label.pack(side=LEFT)
        describer_preset.pack(side=LEFT)

    def build_FM(self, master):
        row_fm = Frame(master)
        row_fm2 = Frame(master)
        row_fm3 = Frame(master)

        force_chk = Checkbutton(row_fm, text="Recompute Feature Detection", variable=self.FM_recompute)
        CreateToolTip(force_chk, "Check this if you want to recompute the data")

        ratio_label = Label(row_fm, text="Distance ratio", width=15, anchor='w')
        self.FM_ratio = Entry(row_fm)
        self.FM_ratio.insert(END, "0.8")
        CreateToolTip(ratio_label, "Distance ratio to discard non meaningful matches")

        geometric_model_label = Label(row_fm, text="Geometric model", width=15, anchor='w')
        geometric_models = ["", "f", "e", "h", "a", "o"]
        CreateToolTip(geometric_model_label, "f: (default) fundamental matrix\ne: essential matrix\nh: homography matrix\na: essential matrix with an angular parametrization\no: orthographic essential matrix")
        self.FM_geometric_model.set(geometric_models[0])
        geometric_model = OptionMenu(row_fm, self.FM_geometric_model, *geometric_models)

        video_mode_label = Label(row_fm2, text="Video mode", width=10, anchor='w')
        self.FM_video_mode = Entry(row_fm2)
        CreateToolTip(video_mode_label, "(sequence matching with an overlap of X images)\nX: with match 0 with (1->X), ...]\n2: will match 0 with (1,2), 1 with (2,3), ...\n3: will match 0 with (1,2,3), 1 with (2,3,4), ...")

        pair_list_label = Label(row_fm2, width=15, text='Pair List file', anchor='w')
        self.FM_pair_list = Entry(row_fm2)
        browse_pair_list = Button(row_fm2, text='Browse...', command=lambda: load_file(self.FM_pair_list, self), width=10)
        CreateToolTip(browse_pair_list, "Select the Pair List file for the SfM pipeline")

        nearest_matching_method_label = Label(row_fm3, text="Nearest Matching Method", width=20, anchor='w')
        nearest_matching_methods = ["", "AUTO", "BRUTEFORCEL2", "ANNL2", "CASCADEHASHINGL2", "FASTCASCADEHASHINGL2", "BRUTEFORCEHAMMING"]
        CreateToolTip(nearest_matching_method_label, "AUTO: auto choice from regions type\nFor Scalar based regions descriptor:\nBRUTEFORCEL2: L2 BruteForce matching\nANNL2: L2 Approximate Nearest Neighbor matching\nCASCADEHASHINGL2: L2 Cascade Hashing matching\nFASTCASCADEHASHINGL2: (default)\nL2 Cascade Hashing with precomputed hashed regions\n(faster than CASCADEHASHINGL2 but use more memory)\nFor Binary based descriptor:\nBRUTEFORCEHAMMING: BruteForce Hamming matching\n")
        self.FM_nearest_matching_method.set(nearest_matching_methods[1])
        nearest_matching_method = OptionMenu(row_fm3, self.FM_nearest_matching_method, *nearest_matching_methods)

        row_fm.pack(side=TOP, fill=X)
        force_chk.pack(side=LEFT)
        ratio_label.pack(side=LEFT)
        self.FM_ratio.pack(side=LEFT)
        geometric_model_label.pack(side=LEFT)
        geometric_model.pack(side=LEFT)

        row_fm2.pack(side=TOP, fill=X)
        video_mode_label.pack(side=LEFT)
        self.FM_video_mode.pack(side=LEFT)
        pair_list_label.pack(side=LEFT)
        self.FM_pair_list.pack(side=LEFT)
        browse_pair_list.pack(side=LEFT)

        row_fm3.pack(side=LEFT, fill=X)
        nearest_matching_method_label.pack(side=LEFT)
        nearest_matching_method.pack(side=LEFT)

    def build_reconstruction(self, master):
        rowTitle = Text(master, height=1)
        rowTitle.insert(END, "Global Reconstruction")
        rowTitle.config(state=DISABLED)
        rowTitle.pack(side=TOP, fill=X)

        row_bg = Frame(master)

        rotation_label = Label(row_bg, text="Rotation", width=15, anchor='w')
        rotations = ["", "1", "2"]
        CreateToolTip(rotation_label, "1 -> L1 minimization\n2 -> L2 minimization (default)")
        self.GR_rotation.set(rotations[2])
        rotation = OptionMenu(row_bg, self.GR_rotation, *rotations)

        translation_label = Label(row_bg, text="Translation", width=15, anchor='w')
        translations = ["", "1", "2", "3"]
        CreateToolTip(translation_label, "1 -> L1 minimization\n2 -> L2 minimization of sum of squared Chordal distances\n3 -> SoftL1 minimization (default)")
        self.GR_translation.set(translations[3])
        translation = OptionMenu(row_bg, self.GR_translation, *translations)

        refine_label = Label(row_bg, text="Refine Intrinsics", width=15, anchor='w')
        refines = ["", "ADJUST_ALL", "NONE", "ADJUST_FOCAL_LENGTH", "ADJUST_PRINCIPAL_POINT", "ADJUST_DISTORTION", "ADJUST_FOCAL_LENGTH|ADJUST_PRINCIPAL_POINT", "ADJUST_FOCAL_LENGTH|ADJUST_DISTORTION", "ADJUST_PRINCIPAL_POINT|ADJUST_DISTORTION"]
        CreateToolTip(refine_label, "ADJUST_ALL -> refine all existing parameters (default)\nNONE -> intrinsic parameters are held as constant\nADJUST_FOCAL_LENGTH -> refine only the focal length\nADJUST_PRINCIPAL_POINT -> refine only the principal point position\nADJUST_DISTORTION -> refine only the distortion coefficient(s) (if any)\n-> NOTE: options can be combined thanks to '|'\nADJUST_FOCAL_LENGTH|ADJUST_PRINCIPAL_POINT\n-> refine the focal length & the principal point position\nADJUST_FOCAL_LENGTH|ADJUST_DISTORTION\n-> refine the focal length & the distortion coefficient(s) (if any)\nADJUST_PRINCIPAL_POINT|ADJUST_DISTORTION\n-> refine the principal point position & the distortion coefficient(s) (if any)")
        self.GR_refine.set(refines[1])
        refine = OptionMenu(row_bg, self.GR_refine, *refines)

        row_bg.pack(side=TOP, fill=X)
        rotation_label.pack(side=LEFT)
        rotation.pack(side=LEFT)
        translation_label.pack(side=LEFT)
        translation.pack(side=LEFT)
        refine_label.pack(side=LEFT)
        refine.pack(side=LEFT)

        rowTitle2 = Text(master, height=1)
        rowTitle2.insert(END, "Incremental Reconstruction")
        rowTitle2.config(state=DISABLED)
        rowTitle2.pack(side=TOP, fill=X)

        row_bi = Frame(master)

        refine_label = Label(row_bi, text="Refine Intrinsics", width=15, anchor='w')
        refines = ["", "ADJUST_ALL", "NONE", "ADJUST_FOCAL_LENGTH", "ADJUST_PRINCIPAL_POINT", "ADJUST_DISTORTION",
                   "ADJUST_FOCAL_LENGTH|ADJUST_PRINCIPAL_POINT", "ADJUST_FOCAL_LENGTH|ADJUST_DISTORTION",
                   "ADJUST_PRINCIPAL_POINT|ADJUST_DISTORTION"]
        CreateToolTip(refine_label,
                      "ADJUST_ALL -> refine all existing parameters (default)\nNONE -> intrinsic parameters are held as constant\nADJUST_FOCAL_LENGTH -> refine only the focal length\nADJUST_PRINCIPAL_POINT -> refine only the principal point position\nADJUST_DISTORTION -> refine only the distortion coefficient(s) (if any)\n-> NOTE: options can be combined thanks to '|'\nADJUST_FOCAL_LENGTH|ADJUST_PRINCIPAL_POINT\n-> refine the focal length & the principal point position\nADJUST_FOCAL_LENGTH|ADJUST_DISTORTION\n-> refine the focal length & the distortion coefficient(s) (if any)\nADJUST_PRINCIPAL_POINT|ADJUST_DISTORTION\n-> refine the principal point position & the distortion coefficient(s) (if any)")
        self.IR_refine.set(refines[0])
        refine = OptionMenu(row_bi, self.IR_refine, *refines)

        models = ["", "1", "2", "3", "4", "5"]
        camera_model_label = Label(row_bi, width=20, text='Camera model', anchor='w')
        camera_model = OptionMenu(row_bi, self.camera_model, *models)
        CreateToolTip(camera_model_label,
                      "Camera model type:\n1: Pinhole\n2: Pinhole radial 1\n3: Pinhole radial 3 (default)\n4: Pinhole 3 + Tangential 2\n5: Pinhole Fisheye")
        self.camera_model.set(models[3])

        row_bi.pack(side=TOP, fill=X)
        refine_label.pack(side=LEFT)
        refine.pack(side=LEFT)
        camera_model_label.pack(side=LEFT)
        camera_model.pack(side=LEFT)

        rowTitle3 = Text(master, height=1)
        rowTitle3.insert(END, "Robust Reconstruction")
        rowTitle3.config(state=DISABLED)
        rowTitle3.pack(side=TOP, fill=X)

        row_br = Frame(master)

        bundle_adjustment_chk = Checkbutton(row_br, text="Bundle Adjustment", variable=self.RR_bundle)
        CreateToolTip(bundle_adjustment_chk, "Check this to perform bundle adjustment during the robust reconstruction")

        residual_label = Label(row_br, width=20, text='Residual Treshold', anchor='w')
        self.RR_residual = Entry(row_br)
        CreateToolTip(residual_label,
                      "maximal pixels reprojection error that will be considered for triangulations (4.0 by default)")

        row_br.pack(side=TOP, fill=X)
        bundle_adjustment_chk.pack(side=LEFT)
        residual_label.pack(side=LEFT)
        self.RR_residual.pack(side=LEFT)

    def build_densification(self, master):

        row1 = Frame(master)
        row2 = Frame(master)
        row3 = Frame(master)

        resolution_level_label = Label(row1, text="Resolution Level", width=15, anchor='w')
        CreateToolTip(resolution_level_label, "The number of times to scale down the images for the dense reconstruction")
        self.DPC_resolution = Entry(row1)

        resolution_min_label = Label(row1, text="Min Resolution", width=15, anchor='w')
        CreateToolTip(resolution_min_label, "The minimum image resolution")
        self.DPC_min_resolution = Entry(row1)

        views_label = Label(row2, text="Views", width=15, anchor='w')
        CreateToolTip(views_label, "The number of views for depth map estimation")
        self.DPC_views = Entry(row2)

        views_fuse_label = Label(row2, text="Views", width=15, anchor='w')
        CreateToolTip(views_fuse_label, "Number of agreeing views for a point to be considered an inlier")
        self.DPC_views_fuse = Entry(row2)

        sample_label = Label(row3, text="Samples", width=15, anchor='w')
        CreateToolTip(sample_label, "uniformly samples points on a mesh (0 - disabled, <0 - number of points, >0 - sample density per square unit")
        self.DPC_sample = Entry(row3)

        color_chk = Checkbutton(row3, text="Estimate colours", variable=self.DPC_color)
        CreateToolTip(color_chk, "Check this if you want to recompute the features")
        normals_chk = Checkbutton(row3, text="Estimate normals", variable=self.DPC_normals)
        CreateToolTip(normals_chk, "Check this if you want to recompute the features")

        row1.pack(side=TOP, fill=X)
        row2.pack(side=TOP, fill=X)
        row3.pack(side=TOP, fill=X)

        resolution_level_label.pack(side=LEFT)
        self.DPC_resolution.pack(side=LEFT)
        resolution_min_label.pack(side=LEFT)
        self.DPC_min_resolution.pack(side=LEFT)
        views_label.pack(side=LEFT)
        self.DPC_views.pack(side=LEFT)
        views_fuse_label.pack(side=LEFT)
        self.DPC_views_fuse.pack(side=LEFT)
        sample_label.pack(side=LEFT)
        self.DPC_sample.pack(side=LEFT)
        color_chk.pack(side=LEFT)
        normals_chk.pack(side=LEFT)

    def build_mesh(self, master):
        row1 = Frame(master)
        row2 = Frame(master)
        row3 = Frame(master)

        min_point_label = Label(row1, text="Min point distance", width=20, anchor='w')
        CreateToolTip(min_point_label,
                      "minimum distance in pixels between the projection of two 3D points to consider them different while triangulating (0 - disabled)")
        self.MR_min = Entry(row1)

        quality_label = Label(row1, text="Quality factor", width=15, anchor='w')
        CreateToolTip(quality_label, "multiplier adjusting the quality weight considered during graph-cut")
        self.MR_quality = Entry(row1)

        decimate_label = Label(row2, text="Decimate", width=15, anchor='w')
        CreateToolTip(decimate_label, "decimation factor in range (0..1] to be applied to the reconstructed surface (1 - disabled)")
        self.MR_decimate = Entry(row2)

        spurious_label = Label(row2, text="Remove Spurious", width=15, anchor='w')
        CreateToolTip(spurious_label, "spurious factor for removing faces with too long edges or isolated components (0 - disabled)")
        self.MR_spurious = Entry(row2)

        spikes_chk = Checkbutton(row3, text="Remove Spikes", variable=self.MR_spikes)
        self.MR_spikes.set(True)
        CreateToolTip(spikes_chk, "Check this if you want to remove spike surfaces")

        holes_label = Label(row3, text="Close Holes", width=15, anchor='w')
        CreateToolTip(holes_label,
                      "try to close small holes in the reconstructed surface (0 - disabled)")
        self.MR_holes = Entry(row3)

        smooth_label = Label(row3, text="Smooth", width=15, anchor='w')
        CreateToolTip(smooth_label,
                      "number of iterations to smooth the reconstructed surface (0 - disabled")
        self.MR_smooth = Entry(row3)

        row1.pack(side=TOP, fill=X)
        row2.pack(side=TOP, fill=X)
        row3.pack(side=TOP, fill=X)

        min_point_label.pack(side=LEFT)
        self.MR_min.pack(side=LEFT)
        quality_label.pack(side=LEFT)
        self.MR_quality.pack(side=LEFT)
        decimate_label.pack(side=LEFT)
        self.MR_decimate.pack(side=LEFT)
        spurious_label.pack(side=LEFT)
        self.MR_spurious.pack(side=LEFT)
        holes_label.pack(side=LEFT)
        self.MR_holes.pack(side=LEFT)
        smooth_label.pack(side=LEFT)
        self.MR_smooth.pack(side=LEFT)
        spikes_chk.pack(side=LEFT)

    def build_refinement(self, master):
        row1 = Frame(master)
        row2 = Frame(master)
        row3 = Frame(master)
        row4 = Frame(master)

        resolution_label = Label(row1, text="Resolution level", width=20, anchor='w')
        CreateToolTip(resolution_label, "How many times we scale the images down before refinement")
        self.MF_resolution = Entry(row1)

        min_label = Label(row1, text="Minimum resolution", width=20, anchor='w')
        CreateToolTip(min_label, "The minimum resolution of images for the refinement")
        self.MF_min = Entry(row1)

        max_label = Label(row2, text="Max views", width=20, anchor='w')
        CreateToolTip(max_label, "Max views used for refinement")
        self.MF_max = Entry(row2)

        decimate_label = Label(row2, text="Decimate", width=20, anchor='w')
        CreateToolTip(decimate_label, "Decimation factor between 0 and 1")
        self.MF_decimate = Entry(row2)

        holes_label = Label(row3, text="Close Holes", width=20, anchor='w',)
        CreateToolTip(holes_label, "try to close small holes in the reconstructed surface (0 - disabled)")
        self.MF_holes = Entry(row3)

        area_label = Label(row3, text="Max Face Area", width=20, anchor='w')
        CreateToolTip(area_label, "maximum face area projected in any pair of images that is not subdivided (0 - disabled)")
        self.MF_face_area = Entry(row3)

        scales_label = Label(row4, text="Scales", width=20, anchor='w')
        CreateToolTip(scales_label, "how many iterations to run mesh optimization on multi-scale images")
        self.MF_scales = Entry(row4)

        step_label = Label(row4, text="Scale Step", width=20, anchor='w')
        CreateToolTip(step_label, "image scale factor used at each mesh optimization step")
        self.MF_scale_step = Entry(row4)

        row1.pack(side=TOP, fill=X)
        row2.pack(side=TOP, fill=X)
        row3.pack(side=TOP, fill=X)
        row4.pack(side=TOP, fill=X)

        resolution_label.pack(side=LEFT)
        self.MF_resolution.pack(side=LEFT)
        min_label.pack(side=LEFT)
        self.MF_min.pack(side=LEFT)
        max_label.pack(side=LEFT)
        self.MF_max.pack(side=LEFT)
        decimate_label.pack(side=LEFT)
        self.MF_decimate.pack(side=LEFT)
        holes_label.pack(side=LEFT)
        self.MF_holes.pack(side=LEFT)
        area_label.pack(side=LEFT)
        self.MF_face_area.pack(side=LEFT)
        scales_label.pack(side=LEFT)
        self.MF_scales.pack(side=LEFT)
        step_label.pack(side=LEFT)
        self.MF_scale_step.pack(side=LEFT)

    def build_texturing(self, master):
        row1 = Frame(master)
        row2 = Frame(master)

        resolution_label = Label(row1, text="Resolution level", width=25, anchor='w')
        CreateToolTip(resolution_label, "How many times we scale the images down before texturing")
        self.TM_resolution = Entry(row1)

        min_label = Label(row1, text="Minimum resolution", width=25, anchor='w')
        CreateToolTip(min_label, "The minimum resolution of images for the texturing")
        self.TM_min = Entry(row1)

        outlier_label = Label(row2, text="Outlier Threshold", width=25, anchor='w')
        CreateToolTip(outlier_label, "threshold used to find and remove outlier face textures (0 - disabled)")
        self.TM_outlier = Entry(row2)

        heuristic_label = Label(row2, text="Patch Packing Heuristic", width=25, anchor='w')
        CreateToolTip(heuristic_label, "specify the heuristic used when deciding where to place a new patch (0 - best fit, 3 - good speed, 100 - best speed)")
        self.TM_heuristic = Entry(row2)

        row1.pack(side=TOP, fill=X)
        row2.pack(side=TOP, fill=X)

        resolution_label.pack(side=LEFT)
        self.TM_resolution.pack(side=LEFT)
        min_label.pack(side=LEFT)
        self.TM_min.pack(side=LEFT)
        outlier_label.pack(side=LEFT)
        self.TM_outlier.pack(side=LEFT)
        heuristic_label.pack(side=LEFT)
        self.TM_heuristic.pack(side=LEFT)


    def run_module(self):
        self.build_conf()
        sfm = SfM("./sfm-conf.txt")
        pipeline = sfm.build_pipeline()
        sfm.execute_pipeline_alt(pipeline)

    def run_module(self):
        self.build_conf()
        sfm = SfM("./sfm-conf.txt")
        pipeline = sfm.build_pipeline()
        sfm.execute_pipeline_alt(pipeline)

    # write the configuation file
    def build_conf(self):
        configuration = open('sfm-conf.txt', 'w+')

        configuration.write("# GENERAL PARAMETERS\n")
        configuration.write("working directory : " + self.working_dir.get() + "\n")
        configuration.write("image directory : " + self.image_dir.get() + "\n")

        configuration.write("\n# DESIRED OUTPUTS\n")
        configuration.write("pipeline type : " + str(int(self.pipeline_type.get())) + "\n")
        configuration.write("robust reconstruction : " + str(int(self.robust.get())) + "\n")
        configuration.write("colourised pointclouds : " + str(int(self.colourised.get())) + "\n")
        configuration.write("dense reconstruction : " + str(int(self.dense.get())) + "\n")
        configuration.write("sparse mesh : " + str(int(self.sparse_mesh.get())) + "\n")
        configuration.write("dense mesh : " + str(int(self.dense_mesh.get())) + "\n")
        configuration.write("refine mesh : " + str(int(self.refine.get())) + "\n")
        configuration.write("texture mesh : " + str(int(self.texture.get())) + "\n")

        configuration.write("\n# IMAGE LISTING\n")
        configuration.write("IL focal : " + self.focal.get() + "\n")
        configuration.write("IL intrinsics : " + self.intrinsics.get() + "\n")
        configuration.write("IL camera model : " + self.camera_model.get() + "\n")
        configuration.write("IL group camera model : " + str(int(self.group_camera_model.get())) + "\n")

        configuration.write("\n# FEATURE DESCRIPTION\n")
        configuration.write("FD recompute data : " + str(int(self.FD_recompute.get())) + "\n")
        configuration.write("FD describer method : " + self.FD_describer_method.get() + "\n")
        configuration.write("FD upright : " + str(int(self.FD_upright.get())) + "\n")
        configuration.write("FD describer preset : " + self.FD_describer_presets.get() + "\n")

        configuration.write("\n# FEATURE MATCHING\n")
        configuration.write("FM recompute data : " + str(int(self.FM_recompute.get())) + "\n")
        configuration.write("FM ratio : " + self.FM_ratio.get() + "\n")
        configuration.write("FM geometric model : " + self.FM_geometric_model.get() + "\n")
        configuration.write("FM video mode : " + self.FM_video_mode.get() + "\n")
        configuration.write("FM pair list : " + self.FM_pair_list.get() + "\n")
        configuration.write("FM nearest matching method : " + self.FM_nearest_matching_method.get() + "\n")

        configuration.write("\n# GLOBAL RECONSTRUCTION\n")
        configuration.write("GR rotation averaging : " + self.GR_rotation.get() + "\n")
        configuration.write("GR translation averaging : " + self.GR_translation.get() + "\n")
        configuration.write("GR refine intrinsics : " + self.GR_refine.get() + "\n")

        configuration.write("\n# INCREMENTAL RECONSTRUCTION\n")
        configuration.write("IR camera model : " + self.IR_camera.get() + "\n")
        configuration.write("IR refine intrinsics : " + self.IR_refine.get() + "\n")

        configuration.write("\n# ROBUST RECONSTRUCTION\n")
        configuration.write("RR bundle adjustment : " + str(int(self.RR_bundle.get())) + "\n")
        configuration.write("RR residual threshold : " + self.RR_residual.get() + "\n")

        configuration.write("\n# POINT CLOUD DENSIFICATION\n")
        configuration.write("DPC resolution level : " + self.DPC_resolution.get() + "\n")
        configuration.write("DPC min resolution : " + self.DPC_min_resolution.get() + "\n")
        configuration.write("DPC number of views : " + self.DPC_views.get() + "\n")
        configuration.write("DPC number of views fuse : " + self.DPC_views_fuse.get() + "\n")
        configuration.write("DPC estimate color : " + str(int(self.DPC_color.get())) + "\n")
        configuration.write("DPC estimate normals : " + str(int(self.DPC_normals.get())) + "\n")
        configuration.write("DPC sample mesh : " + self.DPC_sample.get() + "\n")

        configuration.write("\n# MESH RECONSTRUCTION\n")
        configuration.write("MR min point distance : " + self.MR_min.get() + "\n")
        configuration.write("MR quality factor : " + self.MR_quality.get() + "\n")
        configuration.write("MR decimate : " + self.MR_decimate.get() + "\n")
        configuration.write("MR remove spurious : " + self.MR_spurious.get() + "\n")
        configuration.write("MR remove spikes : " + str(int(self.MR_spikes.get())) + "\n")
        configuration.write("MR close holes : " + self.MR_holes.get() + "\n")
        configuration.write("MR smooth : " + self.MR_smooth.get() + "\n")

        configuration.write("\n# MESH REFINEMENT\n")
        configuration.write("MF resolution level : " + self.MF_resolution.get() + "\n")
        configuration.write("MF min resolution : " + self.MF_min.get() + "\n")
        configuration.write("MF max views : " + self.MF_max.get() + "\n")
        configuration.write("MF decimate : " + self.MF_decimate.get() + "\n")
        configuration.write("MF close holes : " + self.MF_holes.get() + "\n")
        configuration.write("MF max face area :" + self.MF_face_area.get() + "\n")
        configuration.write("MF scales : " + self.MF_scales.get() + "\n")
        configuration.write("MF scale step : " + self.MF_scale_step.get() + "\n")

        configuration.write("\n# MESH TEXTURING\n")
        configuration.write("TM resolution level : " + self.TM_resolution.get() + "\n")
        configuration.write("TM min resolution : " + self.TM_min.get() + "\n")
        configuration.write("TM outlier threshold : " + self.TM_outlier.get() + "\n")
        configuration.write("TM patch packing heuristic : " + self.TM_heuristic.get() + "\n")
