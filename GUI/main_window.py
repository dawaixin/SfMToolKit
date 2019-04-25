from tkinter import *
import sys
from GUI.module_sfm import ModuleSfM
from GUI.module_icp import ModuleICP
from GUI.module_util import ModuleUtil
from GUI.std_redirector import StdRedirector


class MainWindow(object):

    def __init__(self):

        #########################
        # INITIALISE THE WINDOW #
        #########################

        self.mainWindow = Tk()
        self.mainWindow.title("SfMToolKit")

        # Add an Icon
        self.icon = Image("photo", file="./assets/sfm.png")
        self.mainWindow.tk.call('wm', 'iconphoto', self.mainWindow._w, self.icon)

        ###################
        # CONFIGURE INTRO #
        ###################

        # Add the intro section
        self.explanationText = Text(self.mainWindow)
        self.explanationText.insert(END, "This is the SfMToolKit. \nREADME available at https://github.com/dawaixin/SfMToolKit")
        self.explanationText.config(state=DISABLED, height=2)

        #########################
        # CONFIGURE THE CONSOLE #
        #########################

        # Add the console output
        self.console_outFrame = Frame(self.mainWindow)
        self.console_outFrame.grid_propagate(FALSE)
        self.console_outFrame.grid_rowconfigure(0, weight=1)
        self.console_outFrame.grid_columnconfigure(0, weight=1)

        # Bind output to the console
        self.console_outText = Text(self.console_outFrame)
        self.console_outText.pack(side=RIGHT, padx=5, pady=5)
        self.console_outText.insert(END, "")
        self.console_outText.config(state=DISABLED, height=20)

        self.console_outScrollbar = Scrollbar(self.console_outFrame, command=self.console_outText.yview)
        self.console_outScrollbar.grid(row=0, column=1, sticky='nsew')
        self.console_outText['yscrollcommand'] = self.console_outScrollbar.set

        #sys.stdin = StdRedirector(self.console_outText)
        #sys.stdout = StdRedirector(self.console_outText)
        #sys.stderr = StdRedirector(self.console_outText)

        ############################
        # CONFIGURE THE SFM MODULE #
        ############################

        self.moduleSfM = ModuleSfM(self.mainWindow)
        self.moduleSfM.build_form()

        ############################
        # CONFIGURE THE ICP MODULE #
        ############################

        self.moduleICP = ModuleICP(self.mainWindow)
        self.moduleICP.build_form()

        #############################
        # CONFIGURE THE UTIL MODULE #
        #############################

        self.moduleUtil = ModuleUtil(self.mainWindow)
        self.moduleUtil.build_form()

        ###################
        # LAYOUT THE GRID #
        ###################

        self.explanationText.grid(row=0, column=0, padx=5, pady=5)
       #self.console_outFrame.grid(row=0, column=1, rowspan=4, padx=5, pady=5)
        self.moduleSfM.grid(row=1, column=0, padx=0, pady=0)
        self.moduleICP.grid(row=2, column=0, padx=0, pady=0)
        self.moduleUtil.grid(row=3, column=0, padx=0, pady=0)
