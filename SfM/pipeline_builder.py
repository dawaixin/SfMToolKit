import sys
import os


class PipelineBuilder(object):
    # Initialise the class
    def __init__(self, config):
        self.config_file = config
        self.config_parameters = {}
        self.pipeline = []
        self.working_directory = ''
        self.image_directory = ''
        self.matches_dir = ''
        self.pipeline_type = ''
        self.robust_reconstruction = ''
        self.colourised = ""
        self.dense_reconstruction = ''
        self.dense = ""
        self.sparse = ""
        self.refine = ""
        self.texture = ""

    # Read the config file and build the dictionary of parameters
    def read_config(self):
        # try to open the file
        try:
            cfile = open(self.config_file, "r")
        except:
            print("sfm-conf.txt file not found. Check the input parameter.")
            sys.exit(1)

        # Read all the lines
        counter = 0
        for line in cfile:
            counter = counter + 1
            if line != '\n' and line != '' and line[0] != '#':
                pair = line.split(':')
                try:
                    value = pair[1][:-1].strip()
                    if value != '':
                        self.config_parameters[pair[0].strip()] = pair[1][:-1].strip()
                except IndexError:
                    print("ERROR READING THE FILE, ON LINE :" + line)
                    sys.exit(1)
        print("Config file read successfully\n")

    # Build the pipeline
    def build_pipeline(self):

        # Go through the dictionary and build the SfM pipeline accordingly

        # Get the general options and desired outputs
        self.working_directory = self.config_parameters["working directory"]
        self.image_directory = self.config_parameters["image directory"]
        self.pipeline_type = self.config_parameters["pipeline type"]
        self.robust_reconstruction = self.config_parameters["robust reconstruction"]
        self.colourised = self.config_parameters["colourised pointclouds"]
        self.dense_reconstruction = self.config_parameters["dense reconstruction"]
        self.sparse = self.config_parameters["sparse mesh"]
        self.dense = self.config_parameters["dense mesh"]
        self.refine = self.config_parameters["refine mesh"]
        self.texture = self.config_parameters["texture mesh"]

        # determine the pipeline type
        if self.pipeline_type == '1':
            global_reconstruction = True
        else:
            global_reconstruction = False

        # set an error if the directories are
        if self.working_directory == '':
            print("INVALID WORKING DIRECTORY")
            sys.exit(0)
        elif self.image_directory == '':
            print("INVALID IMAGE DIRECTORY")
            sys.exit(0)

        self.build_image_listing()
        self.build_feature_description()
        self.build_feature_matching()
        self.build_global()
        self.build_incremental()
        self.convert_to_mvs()

        if self.sparse == '1':
            if global_reconstruction:
                self.reconstruct_mesh('scene_global.mvs')
            else:
                self.reconstruct_mesh('scene_incremental.mvs')

        if self.refine == '1':
            if global_reconstruction:
                self.refine_mesh('scene_global_mesh.mvs')
            else:
                self.refine_mesh('scene_incremental_mesh.mvs')

        if self.texture == '1':
            if self.refine == '1':
                if global_reconstruction:
                    self.texture_mesh('scene_global_mesh_refine.mvs')
                else:
                    self.texture_mesh('scene_incremental_mesh.mvs')
            else:
                if global_reconstruction:
                    self.texture_mesh('scene_global_mesh_refine.mvs')
                else:
                    self.texture_mesh('scene_incremental_mesh.mvs')

        if self.dense_reconstruction == '1':
            self.densify_pointcloud()

        if self.dense == '1':
            if global_reconstruction:
                self.reconstruct_mesh('scene_global_dense.mvs')
            else:
                self.reconstruct_mesh('scene_incremental_dense.mvs')

        if self.refine == '1':
            if global_reconstruction:
                self.refine_mesh('scene_global_dense_mesh.mvs')
            else:
                self.refine_mesh('scene_incremental_dense_mesh.mvs')

        if self.texture == '1':
            if self.refine == '1':
                if global_reconstruction:
                    self.texture_mesh('scene_global_dense_mesh_refine.mvs')
                else:
                    self.texture_mesh('scene_incremental_dense_mesh.mvs')
            else:
                if global_reconstruction:
                    self.texture_mesh('scene_global_dense_mesh_refine.mvs')
                else:
                    self.texture_mesh('scene_incremental_dense_mesh.mvs')

        return self.pipeline

    def build_image_listing(self):
        # Create the image listing command
        self.matches_dir = os.path.join(self.working_directory, "matches")
        image_listing = "openMVG_main_SfMInit_ImageListing" + " -i " + self.image_directory + " -o " + self.matches_dir + " -d " + "./camera_database.txt"

        for key in self.config_parameters:
            if key == "IL focal":
                image_listing = image_listing + " -f " + self.config_parameters["IL focal"]
            if key == "IL intrinsics":
                image_listing = image_listing + " -k " + self.config_parameters["IL intrinsics"]
            if key == "IL camera model":
                image_listing = image_listing + " -c " + self.config_parameters["IL camera model"]
            if key == "IL group camera model":
                image_listing = image_listing + " -g " + self.config_parameters["IL group camera model"]
            if key == "IL pose prior":
                image_listing = image_listing + " -P " + self.config_parameters["IL pose prior"]
            if key == "IL XYZ coordinate system":
                image_listing = image_listing + " -m " + self.config_parameters["IL XYZ coordinate system"]

        self.pipeline.append(image_listing)

    def build_feature_description(self):
        # Create the Feature Description command
        compute_features = "openMVG_main_ComputeFeatures" + " -i " + self.matches_dir + "/sfm_data.json" + " -o " + self.matches_dir

        for key in self.config_parameters:
            if key == "FD recompute data":
                compute_features = compute_features + " -f " + self.config_parameters["FD recompute data"]
            if key == "FD describer method":
                compute_features = compute_features + " -m " + self.config_parameters["FD describer method"]
            if key == "FD upright":
                compute_features = compute_features + " -u " + self.config_parameters["FD upright"]
            if key == "FD describer preset":
                compute_features = compute_features + " -p " + self.config_parameters["FD describer preset"]
            if key == "FD threads":
                compute_features = compute_features + " -n " + self.config_parameters["FD threads"]

        self.pipeline.append(compute_features)

    def build_feature_matching(self):

        # Create the Feature Matching command

        compute_matches = "openMVG_main_ComputeMatches" + " -i " + self.matches_dir + "/sfm_data.json" + " -o " + self.matches_dir

        for key in self.config_parameters:
            if key == "FM recompute data":
                compute_matches = compute_matches + " -f " + self.config_parameters["FM recompute data"]
            if key == "FM ratio":
                compute_matches = compute_matches + " -r " + self.config_parameters["FM ratio"]
            if key == "FM video mode":
                compute_matches = compute_matches + " -v " + self.config_parameters["FM video mode"]
            if key == "FM pair list":
                compute_matches = compute_matches + " -l " + self.config_parameters["FM pair list"]
            if key == "FM nearest matching method":
                compute_matches = compute_matches + " -n " + self.config_parameters["FM nearest matching method"]
            if key == "FM guided matching":
                compute_matches = compute_matches + " -m " + self.config_parameters["FM guided matching"]

        if "FM geometric model" in self.config_parameters.keys():
            compute_matches = compute_matches + " -g " + self.config_parameters["FM geometric model"]
        elif self.pipeline_type == '1':
            compute_matches = compute_matches + " -g e "

        self.pipeline.append(compute_matches)

    def build_global(self):
        # Create the Global Reconstruction command

        if self.pipeline_type == "1":
            reconstruction_dir = os.path.join(self.working_directory, "global_reconstruction")
            global_reconstruction = "openMVG_main_GlobalSfM" + " -i " + self.matches_dir + "/sfm_data.json" + " -m " + self.matches_dir + " -o " + reconstruction_dir
            for key in self.config_parameters:
                if key == "GR rotation averaging":
                    global_reconstruction = global_reconstruction + " -r " + self.config_parameters["GR rotation averaging"]
                if key == "GR translation averaging":
                    global_reconstruction = global_reconstruction + " -t " + self.config_parameters["GR translation averaging"]
                if key == "GR refine inrinsics":
                    global_reconstruction = global_reconstruction + " -f " + self.config_parameters["GR refine intrinsics"]
                if key == "GR prior usage":
                    global_reconstruction = global_reconstruction + " -p " + self.config_parameters["GR prior usage averaging"]

            self.pipeline.append(global_reconstruction)

            if "colourised pointclouds" in self.config_parameters.keys() and self.config_parameters["colourised pointclouds"] == "1":
                self.build_colourised(reconstruction_dir, "/sfm_data.bin", "colourised.ply")

            # Create the Robust Reconstruction command
            if "robust reconstruction" in self.config_parameters.keys() and self.config_parameters["robust reconstruction"] == "1":
                self.build_robust(reconstruction_dir)

    def build_incremental(self):
        # Create the Incremental Reconstruction command
        if self.pipeline_type == "0":

            reconstruction_dir = os.path.join(self.working_directory, "incremental_reconstruction")
            incremental_reconstruction = "openMVG_main_IncrementalSfM" + " -i " + self.matches_dir + "/sfm_data.json" + " -m " + self.matches_dir + " -o " + reconstruction_dir

            for key in self.config_parameters:
                if key == "IR camera model":
                    incremental_reconstruction = incremental_reconstruction + " -t " + self.config_parameters["IR camera model"]
                if key == "IR refine intrinsics":
                    incremental_reconstruction = incremental_reconstruction + " -f " + self.config_parameters["IR refine intrinsics"]
                if key == "IR prior usage":
                    incremental_reconstruction = incremental_reconstruction + " -p " + self.config_parameters["IR prior usage averaging"]

            self.pipeline.append(incremental_reconstruction)

            if "colourised pointclouds" in self.config_parameters.keys() and self.config_parameters["colourised pointclouds"] == "1":
                self.build_colourised(reconstruction_dir, "/sfm_data.bin", "colourised.ply")

            # Create the Robust Reconstruction command
            if "robust reconstruction" in self.config_parameters.keys() and self.config_parameters["robust reconstruction"] == "1":
                self.build_robust(reconstruction_dir)

    def build_colourised(self, reconstruction_dir, data, name):
        colourised = "openMVG_main_ComputeSfM_DataColor" + " -i " + reconstruction_dir + data + " -o " + os.path.join(reconstruction_dir, name)
        self.pipeline.append(colourised)

    def build_robust(self, reconstruction_dir):
        for key in self.config_parameters:
            if key == "FM geometric model":
                geometric_model = self.config_parameters["FM geometric model"]
            else:
                if "pipeline type" in self.config_parameters.keys() and self.config_parameters["pipeline type"] == "1":
                    geometric_model = "e"
                else:
                    geometric_model = "f"

        robust = "openMVG_main_ComputeStructureFromKnownPoses" + " -i " + reconstruction_dir + "/sfm_data.bin" + " -m " + self.matches_dir + " -f " + os.path.join(self.matches_dir, "matches." + geometric_model + ".bin") + " -o " + os.path.join(reconstruction_dir,"robust.bin")
        self.pipeline.append(robust)

        if "colourised pointclouds" in self.config_parameters.keys() and self.config_parameters["colourised pointclouds"] == "1":
            self.build_colourised(reconstruction_dir, "/robust.bin", "robust_colourised.ply")

    def convert_to_mvs(self):
        if "pipeline type" in self.config_parameters.keys() and self.config_parameters["pipeline type"] == "1":
            input = " -i " + os.path.join(self.working_directory, "global_reconstruction/sfm_data.bin")
            name = "scene_global.mvs"
            directory = os.path.join(self.working_directory, "MVS_reconstruction_global")

        else:
            input = " -i " + os.path.join(self.working_directory, "incremental_reconstruction/sfm_data.bin")
            name = "scene_incremental.mvs"
            directory = os.path.join(self.working_directory, "MVS_reconstruction_incremental")
        convert = "openMVG_main_openMVG2openMVS " + input + " -d " + directory + " -o " + directory + "/" + name
        self.pipeline.append(convert)

    def densify_pointcloud(self):
        if self.pipeline_type == "1":
            input = " -i " + os.path.join(self.working_directory, "MVS_reconstruction_global/scene_global.mvs")
            densify = "DensifyPointCloud " + input + " -v 2 " + " -w " + self.working_directory + "MVS_reconstruction_global"
        else:
            input = " -i " + os.path.join(self.working_directory, "MVS_reconstruction_incremental/scene_incremental.mvs")
            densify = "DensifyPointCloud " + input + " -v 2 " + " -w " + self.working_directory+"MVS_reconstruction_incremental"
        for key in self.config_parameters:
            if key == "DPC resolution level":
                densify = densify + " --resolution-level " + self.config_parameters["DPC resolution level"]
            if key == "DPC min resolution":
                densify = densify + " --min-resolution " + self.config_parameters["DPC min resolution"]
            if key == "DPC number of views":
                densify = densify + " --number-views " + self.config_parameters["DPC number of views"]
            if key == "DPC number of views fuse":
                densify = densify + " --number-views-fuse " + self.config_parameters["DPC number of views fuse"]
            if key == "DPC estimate colour":
                densify = densify + " --estimate-colors " + self.config_parameters["DPC estimate colour"]
            if key == "DPC estimate normals":
                densify = densify + " --estimate-normals " + self.config_parameters["DPC estimate normals"]
            if key == "DPC sample mesh":
                densify = densify + " --sample-mesh " + self.config_parameters["DPC sample mesh"]

        self.pipeline.append(densify)

    def reconstruct_mesh(self, name):
        if self.pipeline_type == "1":
            input = " -i " + os.path.join(self.working_directory, "MVS_reconstruction_global/"+name)
            reconstruct = "ReconstructMesh " + input + " -v 2 " + " -w " + self.working_directory + "MVS_reconstruction_global"
        else:
            input = " -i " + os.path.join(self.working_directory, "MVS_reconstruction_incremental/"+name)
            reconstruct = "ReconstructMesh " + input + " -v 2 " + " -w " + self.working_directory + "MVS_reconstruction_incremental"

        for key in self.config_parameters:
            if key == "MR min point distance":
                reconstruct = reconstruct + " --min-point-distance " + self.config_parameters["MR min point distance"]
            if key == "MR quality factor":
                reconstruct = reconstruct + " --quality-factor " + self.config_parameters["MR quality factor"]
            if key == "MR decimate":
                reconstruct = reconstruct + " --decimate " + self.config_parameters["MR decimate"]
            if key == "MR remove spurious":
                reconstruct = reconstruct + " --remove-spurious " + self.config_parameters["MR remove spurious"]
            if key == "MR remove spikes":
                reconstruct = reconstruct + " --remove-spikes " + self.config_parameters["MR remove spikes"]
            if key == "MR close holes":
                reconstruct = reconstruct + " --close-holes " + self.config_parameters["MR close holes"]
            if key == "MR smooth":
                reconstruct = reconstruct + " --smooth " + self.config_parameters["MR smooth"]

        self.pipeline.append(reconstruct)

    def refine_mesh(self, name):

        if self.pipeline_type == "1":
            input = " -i " + os.path.join(self.working_directory, "MVS_reconstruction_global/"+name)
            refine = "RefineMesh " + input + " -v 2 " + " -w " + self.working_directory + "MVS_reconstruction_global"
        else:
            input = " -i " + os.path.join(self.working_directory, "MVS_reconstruction_incremental/"+name)
            refine = "RefineMesh " + input + " -v 2 " + " -w " + self.working_directory + "MVS_reconstruction_incremental"

        for key in self.config_parameters:
            if key == "MF resolution level":
                refine = refine + " --resolution-level " + self.config_parameters["MF resolution level"]
            if key == "MF min resolution":
                refine = refine + " --min-resolution " + self.config_parameters["MF min resolution"]
            if key == "MF max views":
                refine = refine + " --max-views " + self.config_parameters["MF max views"]
            if key == "MF decimate":
                refine = refine + " --decimate " + self.config_parameters["MF decimate"]
            if key == "MF close holes":
                refine = refine + " --close-holes " + self.config_parameters["MF close holes"]
            if key == "MF max face area":
                refine = refine + " --max-face-area " + self.config_parameters["MF max face area"]
            if key == "MF scales":
                refine = refine + " --scales " + self.config_parameters["MF scales"]
            if key == "MF scale step":
                refine = refine + " --scale-step " + self.config_parameters["MF scale step"]
            if key == "MF reduce memory":
                refine = refine + " --reduce-memory " + self.config_parameters["MF reduce memory"]
            if key == "MF alternate pair":
                refine = refine + " --alternate-pair " + self.config_parameters["MF alternate pair"]

        self.pipeline.append(refine)

    def texture_mesh(self, name):

        if self.pipeline_type == "1":
            input = " -i " + os.path.join(self.working_directory, "MVS_reconstruction_global/" + name)
            texture = "TextureMesh " + input + " -v 2 " + " -w " + self.working_directory + "MVS_reconstruction_global"
        else:
            input = " -i " + os.path.join(self.working_directory, "MVS_reconstruction_incremental/" + name)
            texture = "TextureMesh " + input + " -v 2 " + " -w " + self.working_directory + "MVS_reconstruction_incremental"

        for key in self.config_parameters:
            if key == "TM min resolution":
                texture = texture + " --min-resolution " + self.config_parameters["TM min resolution"]
            if key == "TM resolution level":
                texture = texture + " --resolution-level " + self.config_parameters["TM resolution level"]
            if key == "TM outlier threshold":
                texture = texture + " --outlier-thershold " + self.config_parameters["TM outlier threshold"]
            if key == "TM empty colour":
                texture = texture + " --empty-color " + self.config_parameters["TM empty clolour"]
            if key == "TM patch packing heuristic":
                texture = texture + " --patch-packing-heuristic " + self.config_parameters["TM patch packing heuristic"]

        self.pipeline.append(texture)

if __name__ == '__main__':
    print("This is the pipeline builder. It reads the 'sfm-conf.txt' file and outputs the "
          "equivalent chain of commands for the pipeline to be executed.")

    # Open the file
    pipeline = PipelineBuilder('./sfm-conf.txt')
    pipeline.read_config()
    pipeline.build_pipeline()
    for line in pipeline.pipeline:
        print(line)