# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QObject, QTimer, QFileInfo, QLocale, QUrl, Slot, Signal

import sys, os, pathlib

class Paths(QObject):
    FILE_PREFIX = "file://" if sys.platform.startswith("linux") else "file:///"
    FILE_TYPE = {
        "video": ["webm", "mp4", "mkv"],
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

        return ""

    @staticmethod
    def new_extension(file, new_ext):
        new_ext = new_ext.replace(".", "")
        return "{file}.{ext}".format(file=pathlib.PurePath(file).stem,
                                     ext=new_ext)

    @staticmethod
    def file_name(path):
        return pathlib.PurePath(path).name

    @staticmethod
    def collect_files(core_path):
        files = {}

        for _, _, filenames in os.walk(core_path):
            for filename in filenames:
                files[pathlib.PurePath(filename).stem] = Paths.FILE_PREFIX + os.path.join(core_path, filename)

        return files

    @Slot(int, result="QString")
    def humanSize(self, size):
        locale = QLocale()
        return locale.formattedDataSize(size)

    @Slot(str, result="QString")
    def cleanPath(self, path):
        return QUrl(path).path()

    @Slot(str, result="QString")
    def fileName(self, path):
        return QUrl(path).fileName()

    @Slot(str, result="QString")
    def getFileType(self, format):
        if format in Paths.FILE_TYPE["video"]:
            return "video"

        elif format in Paths.FILE_TYPE["audio"]:
            return "audio"

        return ""

    @Slot(str, result="QString")
    def getPathType(self, path):
        if path.startswith("/") or path.startswith("file://"):
            return "file"

        if path.startswith("http://") or path.startswith("https://"):
            return "remote"

        return ""

    @Slot(str, result="QVariantList")
    def readFile(self, file):
        with open(QUrl(file).path(), "r") as f:
            data = f.readlines()

        return data


class FileExpect(QObject):
    file_exists = Signal()

    def __init__(self):
        super(FileExpect, self).__init__(None)

        self.file = str()
        self.timer = QTimer()
        self.timer.setInterval(500)

        self.timer.timeout.connect(self.check_file_exists)

    def observe(self, file):
        self.file = file
        self.timer.start()

    @Slot()
    def check_file_exists(self):
        if os.path.isfile(self.file):
            self.file_exists.emit()
            self.timer.stop()
