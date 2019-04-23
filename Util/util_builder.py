import sys
import os

class UtilBuilder(object):

    def __init__(self, config):
        self.config_file = config
        self.config_parameters = {}
        self.util_pipeline = []
        self.working_directory = ''
        self.input_file = ''
        self.output_file = ''
        self.exif = ''
        self.segment = ''
        self.frames = ''
        self.rescale = ''

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
        self.input_file = self.config_parameters["input"]
        self.output_file = self.config_parameters["output"]
        self.exif = self.config_parameters["exif"]
        self.segment = self.config_parameters["segment"]
        self.frames = self.config_parameters["frames"]
        self.rescale = self.config_parameters["rescale"]

        if self.input_file == '':
            print("INVALID INPUT FILE")
            sys.exit(0)

        if self.exif == '1':
            self.build_exif()

        self.build_ffmpeg()

        return self.util_pipeline

    # Build the exif command
    def build_exif(self):
        exif = "exiftool "+ self.input_file
        self.util_pipeline.append(exif)

    def build_ffmpeg(self):
        ffmpeg = "ffmpeg -i " + self.input_file
        if self.segment == '1':
            try:
                start_stamp = self.config_parameters["start time"]
                duration = self.config_parameters["duration"]
            except:
                print("INVALID SEGMENTING CONFIG")
                sys.exit(0)
            ffmpeg = ffmpeg + " -ss " + start_stamp + " -t " + duration

        if self.rescale == '1':
            try:
                resolution = self.config_parameters["resolution"]
            except:
                print("INVALID RESCALING CONFIG")
                sys.exit(0)
            ffmpeg = ffmpeg + " -s " + resolution

        # If we are extracting frames, extract frames, otherwise convert the video
        if self.frames == '1':
            try:
                framerate = self.config_parameters["framerate"]
                images = self.config_parameters["images"]
            except:
                print("INVALID FRAMES CONFIG")
                sys.exit(0)
            ffmpeg = ffmpeg + " -vf fps=" + framerate + " " + images
        else :
            ffmpeg = ffmpeg + " " + self.output_file
        self.util_pipeline.append(ffmpeg)

if __name__ == '__main__':
    print("This is the util builder. It reads the 'util-conf.txt' file and outputs the "
          "equivalent chain of commands for the pipeline to be executed.")

    # Open the file
    util_builder = UtilBuilder('./util-conf.txt')
    util_builder.read_config()
    util_builder.build_util()
    for line in util_builder.util_pipeline:
        print(line)