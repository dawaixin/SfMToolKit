from tkinter import *


class StdRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.config(state=NORMAL)
        self.text_space.insert(END, string)
        self.text_space.see("end")
        self.text_space.config(state=DISABLED)
