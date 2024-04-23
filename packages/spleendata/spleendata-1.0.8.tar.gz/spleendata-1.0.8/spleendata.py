#!/usr/bin/env python

from pathlib import Path
import shutil
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter

from chris_plugin import chris_plugin, PathMapper

from monai.apps.utils import download_and_extract

__version__ = "1.0.8"

DISPLAY_TITLE = r"""
       _                  _                     _       _
      | |                | |                   | |     | |
 _ __ | |______ ___ _ __ | | ___  ___ _ __   __| | __ _| |_ __ _
| '_ \| |______/ __| '_ \| |/ _ \/ _ \ '_ \ / _` |/ _` | __/ _` |
| |_) | |      \__ \ |_) | |  __/  __/ | | | (_| | (_| | || (_| |
| .__/|_|      |___/ .__/|_|\___|\___|_| |_|\__,_|\__,_|\__\__,_|
| |                | |
|_|                |_|
"""


parser = ArgumentParser(
    description="""
    A ChRIS FS plugin that downloads a spleen data set for training
    and inference. Based off a MONAI exemplar:

    https://github.com/Project-MONAI/tutorials/blob/main/3d_segmentation/spleen_segmentation_3d.ipynb
                                    """,
    formatter_class=ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "--skipDownload",
    default=False,
    action="store_true",
    help="""If specified, skip the download. Only useful for debugging/testing really.""",
)
parser.add_argument(
    "--trainingOnly",
    default=False,
    action="store_true",
    help="""If specified, only preserve the training data (saving about 462Mb)""",
)
parser.add_argument(
    "--testingOnly",
    default=False,
    action="store_true",
    help="""If specified, only preserve the testing data (saving about 1.2Gb)""",
)
parser.add_argument(
    "-V", "--version", action="version", version=f"%(prog)s {__version__}"
)


def dir_findAndDelete(startdir: Path, target: str):
    for item in startdir.iterdir():
        if item.is_dir():
            if item.name == target:
                shutil.rmtree(str(item))
                # item.rmdir()
                print(f"Deleted directory: {target}")
                break
            else:
                dir_findAndDelete(item, target)


# The main function of this *ChRIS* plugin is denoted by this ``@chris_plugin`` "decorator."
# Some metadata about the plugin is specified here. There is more metadata specified in setup.py.
#
# documentation: https://fnndsc.github.io/chris_plugin/chris_plugin.html#chris_plugin
@chris_plugin(
    parser=parser,
    title="Spleen data downloader",
    category="",  # ref. https://chrisstore.co/plugins
    min_memory_limit="100Mi",  # supported units: Mi, Gi
    min_cpu_limit="1000m",  # millicores, e.g. "1000m" = 1 CPU core
    min_gpu_limit=0,  # set min_gpu_limit=1 to enable GPU
)
def main(options: Namespace, outputdir: Path):
    """
    *ChRIS* plugins usually have two positional arguments: an **input directory** containing
    input files and an **output directory** where to write output files. Command-line arguments
    are passed to this main method implicitly when ``main()`` is called below without parameters.

    :param options: non-positional arguments parsed by the parser given to @chris_plugin
    :param inputdir: directory containing (read-only) input files
    :param outputdir: directory where to write output files
    """

    print(DISPLAY_TITLE)
    resource: str = "https://msd-for-monai.s3-us-west-2.amazonaws.com/Task09_Spleen.tar"
    md5: str = "410d4a301da4e5b2f6f86ec3ddba524e"

    compressed_file: Path = outputdir / "Task09_Spleen.tar"
    data_dir: Path = outputdir / "Task09_Spleen"
    if not data_dir.exists() or options.skipDownload:
        download_and_extract(resource, str(compressed_file), str(outputdir), md5)

    if compressed_file.exists():
        compressed_file.unlink()
    if options.trainingOnly:
        dir_findAndDelete(outputdir, "imagesTs")
    if options.testingOnly:
        dir_findAndDelete(outputdir, "imagesTr")
        dir_findAndDelete(outputdir, "labelsTr")


if __name__ == "__main__":
    main()
