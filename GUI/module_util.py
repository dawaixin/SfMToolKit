from tkinter import *
from GUI.tooltip import CreateToolTip
from tkinter.ttk import *
from util import Util
from GUI.commands import load_file

class ModuleUtil(Frame):

    def __init__(self, master):
        super().__init__()
        self.master = master

        self.input = StringVar()
        self.output = StringVar()

        self.exif = BooleanVar()
        self.segment = BooleanVar()
        self.frames = BooleanVar()
        self.rescale = BooleanVar()

        self.start = StringVar()
        self.duration = StringVar()

        self.framerate = StringVar()
        self.images = StringVar()

        self.resolution = StringVar()

    def build_form(self):
        rowTitle = Text(self, height=3)
        rowTitle.insert(END, "\nMODULE III - Utilities\n")
        rowTitle.config(state=DISABLED)
        rowTitle.pack(side=TOP, fill=X)

        notebook = Notebook(self, width=800)

        general_parameters = Frame(notebook)
        notebook.add(general_parameters, text="General Parameters")
        self.build_general(general_parameters)

        notebook.pack(side=TOP)

        row_run = Frame(self)
        run_button = Button(row_run, text="Run module", command=lambda: self.run_module(), width=10)
        row_run.pack(side=TOP, fill=X)
        run_button.pack(side=RIGHT)

    def build_general(self, master):
        row1 = Frame(master)
        lab1 = Label(row1, width=15, text='Input', anchor='w')
        self.input = Entry(row1)
        browse1 = Button(row1, text='Browse...', command=lambda: load_file(self.input, self), width=10)
        CreateToolTip(browse1, "Select the Input file")

        row1.pack(side=TOP, fill=X)
        lab1.pack(side=LEFT)
        self.input.pack(side=RIGHT, expand=YES, fill=X)
        browse1.pack(side=RIGHT)

        row2 = Frame(master)
        lab2 = Label(row2, width=15, text='Output', anchor='w')
        self.output = Entry(row2)
        browse2 = Button(row2, text='Browse...', command=lambda: load_file(self.output, self), width=10)
        CreateToolTip(browse2, "The reference point cloud")

        row2.pack(side=TOP, fill=X)
        lab2.pack(side=LEFT)
        self.output.pack(side=RIGHT, expand=YES, fill=X)
        browse2.pack(side=RIGHT)

        row3 = Frame(master)
        exif_chk = Checkbutton(row3,text="Exif", variable=self.exif)
        segment_chk = Checkbutton(row3, text="Segment", variable=self.segment)
        frames_chk = Checkbutton(row3, text="Extract Frames", variable=self.frames)
        rescale_chk = Checkbutton(row3, text="Rescale", variable=self.rescale)

        row3.pack(side=TOP, fill=X)
        exif_chk.pack(side=LEFT)
        segment_chk.pack(side=LEFT)
        frames_chk.pack(side=LEFT)
        rescale_chk.pack(side=LEFT)

        row4 = Frame(master)
        lab4 = Label(row4, width=15, text='Images', anchor='w')
        self.images = Entry(row4)
        browse4 = Button(row4, text='Browse...', command=lambda: load_file(self.input, self), width=10)
        CreateToolTip(browse4, "Output images to this path. 'out%04d.jpg' will output jpg files numbering them over 4 digits")

        row4.pack(side=TOP, fill=X)
        lab4.pack(side=LEFT)
        self.images.pack(side=RIGHT, expand=YES, fill=X)
        browse4.pack(side=RIGHT)

        row5 = Frame(master)

        lab51 = Label(row5, width=15, text='Framerate', anchor='w')
        self.framerate = Entry(row5)
        CreateToolTip(lab51, "Number of frames to extract per second in the video")

        lab52 = Label(row5, width=15, text='Resolution', anchor='w')
        self.resolution = Entry(row5)
        CreateToolTip(lab52, "Rescaling resolution, written in AAAxBBB format")

        row5.pack(side=TOP, fill=X)
        lab51.pack(side=LEFT)
        self.framerate.pack(side=LEFT)
        lab52.pack(side=LEFT)
        self.resolution.pack(side=LEFT)

        row6 = Frame(master)

        lab61 = Label(row6, width=15, text='Start Time', anchor='w')
        self.start = Entry(row6)
        CreateToolTip(lab61, "Start time of the segment in seconds")

        lab62 = Label(row6, width=15, text='Duration', anchor='w')
        self.duration = Entry(row6)
        CreateToolTip(lab62, "Duration of the segment in seconds")

        row5.pack(side=TOP, fill=X)
        lab51.pack(side=LEFT)
        self.framerate.pack(side=LEFT)
        lab52.pack(side=LEFT)
        self.resolution.pack(side=LEFT)

    def run_module(self):
        self.build_conf()
        util = Util("./util-conf.txt")
        util.build_util()
        util.run_util()

    def build_conf(self):
        configuration = open('util-conf.txt', 'w+')

        configuration.write("input : " + self.input.get() + "\n")
        configuration.write("output : " + self.output.get() + "\n")

        configuration.write("exif : " + str(int(self.exif.get())) + "\n")
        configuration.write("segment : " + str(int(self.segment.get())) + "\n")
        configuration.write("frames : " + str(int(self.frames.get())) + "\n")
        configuration.write("rescale : " + str(int(self.rescale.get())) + "\n")

        configuration.write("start time : " + self.start.get() + "\n")
        configuration.write("duration : " + self.duration.get() + "\n")

        configuration.write("framerate : " + self.framerate.get() + "\n")
        configuration.write("images : " + self.images.get() + "\n")

        configuration.write("resolution : " + self.resolution.get() + "\n")
