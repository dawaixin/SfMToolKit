from Util import util_builder as util_builder
from Misc import unbuffered as ub
import subprocess
import sys


class Util(object):

    def __init__(self, config):
        self.util_builder = util_builder.UtilBuilder(config)
        self.pipeline = ""

    def build_util(self):
        self.util_builder.read_config()
        self.pipeline = self.util_builder.build_util()

    def run_util(self):
        for line in self.pipeline:
            subprocess.run(line, stdout=ub.Unbuffered(sys.stdout), stderr=ub.Unbuffered(sys.stderr), shell=True)
        print("\n\n")


if __name__ == "__main__":
    print("This is the pipeline runner. It calls the builder then invokes the elements within "
          "the pipeline at the console\n")

    util = Util("./Util/util-conf.txt")
    util.build_util()
    util.run_util()
