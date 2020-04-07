# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QObject, Slot

import sys, os, pathlib

class Paths(QObject):
    FILE_PREFIX = "file://" if sys.platform.startswith("linux") else "file:///"

    def __init__(self):
        super(Paths, self).__init__(None)

    @staticmethod
    def collect_files(core_path):
        files = {}

        for _, _, filenames in os.walk(core_path):
            for filename in filenames:
                files[pathlib.PurePath(filename).stem] = Paths.FILE_PREFIX + os.path.join(core_path, filename)

        return files

    @Slot(str, result="QString")
    def cleanPath(self, path):
        return path.replace(Paths.FILE_PREFIX, "")

