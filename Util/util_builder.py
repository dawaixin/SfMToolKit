import sys
import os

class UtilBuilder(object):

    def __init__(self, config):
        self.config_file = config
        self.config_parameters = {}
        self.util_pipeline = []
        self.working_directory = ''
        self.input_file = ''
        self.exif = ''
        self.segment = ''
        self.frames = ''
        self.convert = ''

    # Read the config file and build the dictionary of parameters
    def read_config(self):
        # try to open the file
        try:
            cfile = open(self.config_file, "r")
        except:
            print("util-conf.txt file not found. Check the input parameter.")
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

    # Function to build the util parameters
    def build_util(self):
        # Go through the dictionary and build the Util pipeline accordingly

        # Get the general options and desired outputs
        self.working_directory = self.config_parameters["working directory"]
        self.input_file = self.config_parameters["input"]
        self.exif = self.config_parameters["exif"]
        self.segment = self.config_parameters["segment"]
        self.frames = self.config_parameters["frames"]
        self.convert = self.config_parameters["convert"]

        # set an error if the directory and file are invalid
        if self.working_directory == '':
            print("INVALID WORKING DIRECTORY")
            sys.exit(0)
        elif self.input_file == '':
            print("INVALID INPUT FILE DIRECTORY")
            sys.exit(0)

        if self.exif == '1':
            self.build_exif()

        return self.util_pipeline

    # Build the exif command
    def build_exif(self):
        exif = "exiftool "+ self.input_file
        self.util_pipeline.append(exif)

if __name__ == '__main__':
    print("This is the util builder. It reads the 'util-conf.txt' file and outputs the "
          "equivalent chain of commands for the pipeline to be executed.")

    # Open the file
    util_builder = UtilBuilder('./util-conf.txt')
    util_builder.read_config()
    util_builder.build_util()
    for line in util_builder.util_pipeline:
        print(line)