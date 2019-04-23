from tkinter import *
from tkinter import filedialog
from pathlib import *


def load_file(ent, master):
    dirname = filedialog.askdirectory(parent=master, initialdir=Path(), title='Select a directory or file')
    if dirname:
        ent.delete(0, END)
        ent.insert(0, dirname)
