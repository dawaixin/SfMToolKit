from tkinter import *
from SfM import sfm as sfm
from ICP import *
from Util import util as util
from tkinter import filedialog
from pathlib import *
import subprocess

class ModuleICP(Frame):

    def __init__(self, master):
        super().__init__()
        self.master = master
        self.entries = []
        self.console_call = ''
        self.module = ''
        self.config = ''



