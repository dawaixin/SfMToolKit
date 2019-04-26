from tkinter import *
from GUI.tooltip import CreateToolTip
from tkinter.ttk import *
from GUI.commands import load_file, load_directory
import subprocess

class ModuleICP(Frame):

    def __init__(self, master):
        super().__init__()
        self.master = master

        self.working_directory = StringVar()
        self.reference_file = StringVar()
        self.reading_file = StringVar()

        self.MDPDF1 = StringVar()
        self.RSDPF1 = StringVar()

        self.MDPDF2 = StringVar()
        self.RSDPF2 = StringVar()

        self.KDtree_knn = StringVar()
        self.KDtree_epsilon = StringVar()

        self.outlier_filter = StringVar()
        self.counter = StringVar()
        self.min_diff_rot = StringVar()
        self.min_diff_trans = StringVar()
        self.smooth = StringVar()

        self.save_ply = BooleanVar()

    def build_form(self):
        rowTitle = Text(self, height=3)
        rowTitle.insert(END, "\nMODULE II - Iterative Closest Point\n")
        rowTitle.config(state=DISABLED)
        rowTitle.pack(side=TOP, fill=X)

        notebook = Notebook(self, width=800)

        general_parameters = Frame(notebook)
        notebook.add(general_parameters, text="General Parameters")
        self.build_general(general_parameters)

        icp_parameters = Frame(notebook)
        notebook.add(icp_parameters, text="ICP Parameters")
        self.build_icp(icp_parameters)

        notebook.pack(side=TOP)

        row_run = Frame(self)
        run_button = Button(row_run, text="Run module", command=lambda: self.run_module(), width=10)
        row_run.pack(side=TOP, fill=X)
        run_button.pack(side=RIGHT)

    def build_general(self, master):
        row1 = Frame(master)
        lab1 = Label(row1, width=15, text='Working Directory', anchor='w')
        self.working_directory = Entry(row1)
        browse1 = Button(row1, text='Browse...', command=lambda: load_directory(self.working_directory, self), width=10)
        CreateToolTip(browse1, "Select the working directory for the ICP pipeline")

        row1.pack(side=TOP, fill=X)
        lab1.pack(side=LEFT)
        self.working_directory.pack(side=RIGHT, expand=YES, fill=X)
        browse1.pack(side=RIGHT)

        row2 = Frame(master)
        lab2 = Label(row2, width=15, text='Reference File', anchor='w')
        self.reference_file = Entry(row2)
        browse2 = Button(row2, text='Browse...', command=lambda: load_file(self.reference_file, self), width=10)
        CreateToolTip(browse2, "The reference point cloud")

        row2.pack(side=TOP, fill=X)
        lab2.pack(side=LEFT)
        self.reference_file.pack(side=RIGHT, expand=YES, fill=X)
        browse2.pack(side=RIGHT)

        row3 = Frame(master)
        lab3 = Label(row3, width=15, text='Reading File', anchor='w')
        self.reading_file = Entry(row3)
        browse3 = Button(row3, text='Browse...', command=lambda: load_file(self.reading_file, self), width=10)
        CreateToolTip(browse3, "The point cloud you wish to evaluate")

        row3.pack(side=TOP, fill=X)
        lab3.pack(side=LEFT)
        self.reading_file.pack(side=RIGHT, expand=YES, fill=X)
        browse3.pack(side=RIGHT)

        row4 = Frame(master)
        chk_ply = Checkbutton(row4, text="Export files to .ply format", variable=self.save_ply)
        self.save_ply.set(True)

        row4.pack(side=TOP, fill=X)
        chk_ply.pack(side=LEFT)

    def build_icp(self, master):

        row1 = Frame(master)
        row2 = Frame(master)
        row3 = Frame(master)
        row4 = Frame(master)
        row5 = Frame(master)
        row6 = Frame(master)

        labMDPDF1 = Label(row1, text="Reference Min Distance", width=25)
        self.MDPDF1 = Entry(row1)
        self.MDPDF1.insert(END, "1.0")
        labMDPDF1.pack(side=LEFT)
        self.MDPDF1.pack(side=LEFT)

        labRSDPF1 = Label(row1, text="Reference Sampling", width=20)
        self.RSDPF1 = Entry(row1)
        self.RSDPF1.insert(END, "0.05")
        labRSDPF1.pack(side=LEFT)
        self.RSDPF1.pack(side=LEFT)

        labMDPDF2 = Label(row2, text="Reading Min Distance", width=25)
        self.MDPDF2 = Entry(row2)
        self.MDPDF2.insert(END, "1.0")
        labMDPDF2.pack(side=LEFT)
        self.MDPDF2.pack(side=LEFT)

        labRSDPF2 = Label(row2, text="Reading Sampling", width=20)
        self.RSDPF2 = Entry(row2)
        self.RSDPF2.insert(END, "0.05")
        labRSDPF2.pack(side=LEFT)
        self.RSDPF2.pack(side=LEFT)

        labknn = Label(row3, text="KD Tree knn value", width=25)
        self.KDtree_knn = Entry(row3)
        self.KDtree_knn.insert(END, "1")
        labknn.pack(side=LEFT)
        self.KDtree_knn.pack(side=LEFT)

        labepsilon = Label(row3, text="KD Tree epsilon value", width=20)
        self.KDtree_epsilon = Entry(row3)
        self.KDtree_epsilon.insert(END, "3.16")
        labepsilon.pack(side=LEFT)
        self.KDtree_epsilon.pack(side=LEFT)

        laboutlier = Label(row4, text="Distance Outlier filter", width=25)
        self.outlier_filter = Entry(row4)
        self.outlier_filter.insert(END, "0.75")
        laboutlier.pack(side=LEFT)
        self.outlier_filter.pack(side=LEFT)

        labcounter = Label(row4, text="Transformation counter", width=20)
        self.outlier_filter = Entry(row4)
        self.outlier_filter.insert(END, "150")
        labcounter.pack(side=LEFT)
        self.outlier_filter.pack(side=LEFT)

        labrot = Label(row5, text="Rotation Error", width=25)
        self.min_diff_rot = Entry(row5)
        self.min_diff_rot.insert(END, "0.001")
        labrot.pack(side=LEFT)
        self.min_diff_rot.pack(side=LEFT)

        labtrans = Label(row5, text="Transformation error", width=20)
        self.min_diff_trans = Entry(row5)
        self.min_diff_trans.insert(END, "0.01")
        labtrans.pack(side=LEFT)
        self.min_diff_trans.pack(side=LEFT)

        labsmooth = Label(row6, text="Smooth Length", width=25)
        self.smooth = Entry(row6)
        self.smooth.insert(END, "4")
        labsmooth.pack(side=LEFT)
        self.smooth.pack(side=LEFT)

        row1.pack(side=TOP, fill=X)
        row2.pack(side=TOP, fill=X)
        row3.pack(side=TOP, fill=X)
        row4.pack(side=TOP, fill=X)
        row5.pack(side=TOP, fill=X)
        row6.pack(side=TOP, fill=X)

    def run_module(self):
        self.build_conf()
        command = "SfMToolkitICP " + "icp-conf.txt"
        subprocess.run(command, shell=True)


    def build_conf(self):
        configuration = open('icp-conf.txt', 'w+')

        configuration.write("working directory : " + self.working_directory.get() + "\n")
        configuration.write("reference file : " + self.reference_file.get() + "\n")
        configuration.write("reading file : " + self.reading_file.get() + "\n")

        configuration.write("MinDistDataPointsFilter1 : " + self.MDPDF1.get() + "\n")
        configuration.write("RandomSamplingDataPointsFilter1 : " + self.RSDPF1.get() + "\n")
        configuration.write("MinDistDataPointsFilter2 : " + self.MDPDF2.get() + "\n")
        configuration.write("RandomSamplingDataPointsFilter2 : " + self.RSDPF2.get() + "\n")

        configuration.write("KDTreeMatcher knn : " + self.KDtree_knn.get() + "\n")
        configuration.write("KDTreeMatcher epsilon : " + self.KDtree_epsilon.get() + "\n")

        configuration.write("TrimmedDistOutlierFilter : " + self.outlier_filter.get() + "\n")
        configuration.write("CounterTransformationChecker : " + self.counter.get() + "\n")

        configuration.write("DifferentialTransformationChecker minDiffRotErr : " + self.min_diff_rot.get() + "\n")
        configuration.write("DifferentialTransformationChecker minDiffTransErr : " + self.min_diff_trans.get() + "\n")
        configuration.write("DifferentialTransformationChecker smoothLength : " + self.smooth.get() + "\n")

        configuration.write("savePLY : " + str(int(self.save_ply.get())) + "\n")

