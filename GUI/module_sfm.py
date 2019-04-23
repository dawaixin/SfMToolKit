from tkinter import *
from tkinter.ttk import *
from SfM import sfm as sfm
from ICP import *
from Util import util as util
from tkinter import filedialog
from GUI.commands import *
from pathlib import *
import subprocess


class ModuleSfM(Frame):

    def __init__(self, master):
        super().__init__()
        self.master = master
        self.entries = []
        self.console_call = ''
        self.module = ''
        self.config = ''
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
        self.focal = StringVar()
        self.intrinsics = StringVar()
        self.camera_model = StringVar()
        self.group_camera_model = BooleanVar()
        self.pose_prior = StringVar()
        self.xyz_coordinate = BooleanVar()
        self.FD_recompute = BooleanVar()
        self.FD_describer_method = StringVar()
        self.FD_describer_presets = StringVar()
        self.FD_upright = BooleanVar()

    def build_form(self):
        rowTitle = Text(self, height=1)
        rowTitle.insert(END,"MODULE I - Structure from Motion")
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

        notebook.pack(side=TOP)
        #########################################
        # GENERATE THE CONFIGURATION AND RUN IT #
        #########################################

        row_run = Frame(self)
        run_button = Button(row_run, text="Run module", command=lambda: self.build_conf(), width=10)
        row_run.pack(side=TOP, fill=X)
        run_button.pack(side=RIGHT)

    def build_general(self, master):
        ######################
        # GENERAL PARAMETERS #
        ######################

        row1 = Frame(master)
        lab1 = Label(row1, width=15, text='Working Directory', anchor='w')
        self.working_dir = Entry(row1)
        browse1 = Button(row1, text='Browse...', command=lambda: load_file(self.working_dir, self), width=10)

        row1.pack(side=TOP, fill=X)
        lab1.pack(side=LEFT)
        self.working_dir.pack(side=RIGHT, expand=YES, fill=X)
        browse1.pack(side=RIGHT)

        row2 = Frame(master)
        lab2 = Label(row2, width=15, text='Image Directory', anchor='w')
        self.image_dir = Entry(row2)
        browse2 = Button(row2, text='Browse...', command=lambda: load_file(self.image_dir, self), width=10)

        row2.pack(side=TOP, fill=X)
        lab2.pack(side=LEFT)
        self.image_dir.pack(side=RIGHT, expand=YES, fill=X)
        browse2.pack(side=RIGHT)

        #########################
        # BUILD DESIRED OUTPUTS #
        #########################

        row_outputs = Frame(master)
        row_outputs2 = Frame(master)
        pipeline_type_chk = Checkbutton(row_outputs, text="Pipeline Global", variable=self.pipeline_type,
                                        foreground='WHITE', selectcolor='BLACK')
        robust_chk = Checkbutton(row_outputs, text="Robust reconstruction", variable=self.robust, foreground='WHITE',
                                 selectcolor='BLACK')
        colourised_chk = Checkbutton(row_outputs, text="Colourised point clouds", variable=self.colourised,
                                     foreground='WHITE', selectcolor='BLACK')
        dense_chk = Checkbutton(row_outputs, text="Dense reconstruction", variable=self.dense, foreground='WHITE',
                                selectcolor='BLACK')
        sparse_mesh_chk = Checkbutton(row_outputs2, text="Sparse mesh", variable=self.sparse_mesh, foreground='WHITE',
                                      selectcolor='BLACK')
        dense_mesh_chk = Checkbutton(row_outputs2, text="Dense mesh", variable=self.dense_mesh, foreground='WHITE',
                                     selectcolor='BLACK')
        refine_chk = Checkbutton(row_outputs2, text="Refine mesh", variable=self.refine, foreground='WHITE',
                                 selectcolor='BLACK')
        texture_chk = Checkbutton(row_outputs2, text="Texture mesh", variable=self.texture, foreground='WHITE',
                                  selectcolor='BLACK')

        row_outputs.pack(side=TOP, fill=X)
        row_outputs2.pack(side=TOP, fill=X)
        pipeline_type_chk.pack(side=LEFT)
        robust_chk.pack(side=LEFT)
        colourised_chk.pack(side=LEFT)
        dense_chk.pack(side=LEFT)
        sparse_mesh_chk.pack(side=LEFT)
        dense_mesh_chk.pack(side=LEFT)
        refine_chk.pack(side=LEFT)
        texture_chk.pack(side=LEFT)

    ##################################
    # BUILD IMAGE LISTING PARAMETERS #
    ##################################
    def build_IL(self, master):

        row_il = Frame(master)
        row_il2 = Frame(master)
        row_il3 = Frame(master)
        # focal
        focal_label = Label(row_il, width=20, text='Focal Length (pixels)', anchor='w', padx=5, pady=5)
        self.focal = Entry(row_il)
        # intrinsics
        intrinsics_label = Label(row_il, width=20, text='Intrinsics', anchor='w', padx=5, pady=5)
        self.intrinsics = Entry(row_il)
        # camera model
        camera_model_label = Label(row_il2, width=20, text='Camera model', anchor='w', padx=5, pady=5)
        self.camera_model = Entry(row_il2)
        # group camera model
        group_camera_model_chk = Checkbutton(row_il2, text="Group Camera Model", variable=self.group_camera_model, foreground='WHITE', selectcolor='BLACK')

        # pose prior
        pose_prior_label = Label(row_il3, width=20, text='Pose prior', anchor='w', padx=5, pady=5)
        self.pose_prior = Entry(row_il3)
        # XYZ coordinate system
        xyz_coordinate_chk = Checkbutton(row_il3, text="Coordinate system, 0=ECEF 1=UTM", variable=self.xyz_coordinate, foreground='WHITE', selectcolor='BLACK')

        row_il.pack(side=TOP, fill=X)
        focal_label.pack(side=LEFT)
        self.focal.pack(side=LEFT)
        intrinsics_label.pack(side=LEFT)
        self.intrinsics.pack(side=LEFT)
        row_il2.pack(side=TOP, fill=X)
        camera_model_label.pack(side=LEFT)
        self.camera_model.pack(side=LEFT)
        group_camera_model_chk.pack(side=LEFT)
        row_il3.pack(side=TOP, fill=X)
        pose_prior_label.pack(side=LEFT)
        self.pose_prior.pack(side=LEFT)
        xyz_coordinate_chk.pack(side=LEFT)

    def build_FD(self, master):
        row_fd = Frame(master)
        row_fd2 = Frame(master)

        force_chk = Checkbutton(row_fd, text="Recompute Feature Detection", variable=self.FD_recompute,  foreground='WHITE', selectcolor='BLACK')
        upright_chk = Checkbutton(row_fd, text="Force upright", variable=self.FD_upright,  foreground='WHITE', selectcolor='BLACK')
        describer_method_label = Label(row_fd2, text="Describer Method", width=20, anchor='w', padx=5, pady=5)
        describers = ["SIFT", "SIFT_ANATOMY", "AKAZE_FLOAT", "AKAZE_MLDB"]
        describer_method = OptionMenu(row_fd2, self.FD_describer_method, *describers)
        self.FD_describer_method.set(describers[0])
        describer_preset_label = Label(row_fd2, text="Describer Preset", width=20, anchor='w', padx=5, pady=5)
        describer_presets = ["NORMAL", "HIGH", "ULTRA"]
        describer_preset = OptionMenu(row_fd2, self.FD_describer_presets, *describer_presets)
        self.FD_describer_presets.set(describer_presets[0])

        row_fd.pack(side=TOP, fill=X)
        row_fd2.pack(side=TOP, fill=X)
        force_chk.pack(side=LEFT)
        upright_chk.pack(side=LEFT)
        describer_method_label.pack(side=LEFT)
        describer_method.pack(side=LEFT)
        describer_preset_label.pack(side=LEFT)
        describer_preset.pack(side=LEFT)


    # write the configuation file
    def build_conf(self):
        print("RUN")
        configuration = open('sfm-conf.txt', 'w+')

        configuration.write("# GENERAL PARAMETERS\n")
        configuration.write("working directory : " + self.working_dir.get() + "\n")
        configuration.write("image directory : " + self.image_dir.get() + "\n")

        configuration.write("# DESIRED OUTPUTS\n")
        configuration.write("pipeline type : " + str(int(self.pipeline_type.get())) + "\n")
        configuration.write("robust reconstruction : " + str(int(self.robust.get())) + "\n")
        configuration.write("colourised pointclouds : " + str(int(self.colourised.get())) + "\n")
        configuration.write("dense reconstruction : " + str(int(self.dense.get())) + "\n")
        configuration.write("sparse mesh : " + str(int(self.sparse_mesh.get())) + "\n")
        configuration.write("dense mesh : " + str(int(self.dense_mesh.get())) + "\n")
        configuration.write("refine mesh : " + str(int(self.refine.get())) + "\n")
        configuration.write("texture mesh : " + str(int(self.texture.get())) + "\n")

        configuration.write("# IMAGE LISTING\n")
        configuration.write("IL focal : " + self.focal.get() + "\n")
        configuration.write("IL intrinsics : " + self.intrinsics.get() + "\n")
        configuration.write("IL camera model : " + self.camera_model.get() + "\n")
        configuration.write("IL group camera model : " + str(int(self.group_camera_model.get())) + "\n")



