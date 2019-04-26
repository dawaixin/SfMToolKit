from tkinter import *
from tkinter import filedialog
from pathlib import *


def load_file(ent, master):
    filename = filedialog.askopenfilename(parent=master, initialdir=Path(), title='Select a file')
    if filename:
        ent.delete(0, END)
        ent.insert(0, filename)


def load_directory(ent, master):
    dirname = filedialog.askdirectory(parent=master, initialdir=Path(), title='Select a directory')
    if dirname:
        ent.delete(0, END)
        ent.insert(0, dirname + '/')