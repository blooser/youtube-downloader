from PySide6.QtCore import (
    QObject,

    Slot
)


import datetime
import time
import re


class Utility(QObject):
    def __init__(self):
        super().__init__()

    @Slot(str, result=str)
    def msToHuman(self, seconds):
        struct_type = time.gmtime(int(seconds))

        return time.strftime("%H:%M:%S", struct_type)

    @Slot(str, result=str)
    def dateToHuman(self, date):
        t_date = datetime.datetime.strptime(date, "%Y%M%d")

        return t_date.strftime("%-M %B %Y")

    @Slot(str, result=str)
    def bigNumberToHuman(self, number):
        return format(int(number), ",")
