from PySide6.QtCore import (
    QObject,

    Slot
)


import datetime
import time
import subprocess


class Utility(QObject):
    def __init__(self):
        super().__init__()

    @Slot(str, result=str)
    def msToHuman(self, seconds):
        if not seconds:
            return ""

        struct_type = time.gmtime(int(seconds))

        return time.strftime("%H:%M:%S", struct_type)

    @Slot(str, result=str)
    def dateToHuman(self, date):
        if not date:
            return ""

        t_date = datetime.datetime.strptime(date, "%Y%m%d")

        return t_date.strftime("%-d %B %Y")

    @Slot(str, result=str)
    def bigNumberToHuman(self, number):
        if not number:
            return ""

        return format(int(number), ",")

    @Slot(str)
    def openFileExplorer(self, path):
        subprocess.Popen(["xdg-open", path])


