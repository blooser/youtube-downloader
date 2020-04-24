# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QObject, Slot

import sys, os, pathlib

class Paths(QObject):
    FILE_PREFIX = "file://" if sys.platform.startswith("linux") else "file:///"
    FILE_TYPE = {
        "video": ["webm", "mp4", "flv", "3gp", "ogg"],
        "audio": ["mp3", "flac", "m4a", "wav"]
    }

    def __init__(self):
        super(Paths, self).__init__(None)

    @staticmethod
    def get_file_type(file):
        suffix = pathlib.PurePath(file).suffix.replace(".", "")

        if suffix in Paths.FILE_TYPE["video"]:
            return "video"

        elif suffix in Paths.FILE_TYPE["audio"]:
            return "audio"

        return "Unknown"

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

