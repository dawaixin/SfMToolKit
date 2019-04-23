from SfM import pipeline_builder as pb
from Misc import unbuffered as ub
import subprocess
import sys


class SfM(object):

    def __init__(self, config):
        self.pipeline_builder = pb.PipelineBuilder(config)
        self.pipeline = ""

    def build_pipeline(self):
        self.pipeline_builder.read_config()
        self.pipeline = self.pipeline_builder.build_pipeline()

    def execute_pipeline(self):
        for line in self.pipeline:
            subprocess.run(line, stdout=ub.Unbuffered(sys.stdout), stderr=ub.Unbuffered(sys.stderr), shell=True)
        print("\n\n")


if __name__ == "__main__":
    print("This is the pipeline runner. It calls the builder then invokes the elements within "
          "the pipeline at the console\n")

    sfm = SfM("./sfm-conf.txt")
    sfm.build_pipeline()
    sfm.execute_pipeline()
