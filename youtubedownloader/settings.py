from PySide6.QtCore import (
    QObject,
    QSettings,
    QStandardPaths,
    Signal,
    Property
)

import os.path
import atexit


from youtubedownloader.logger import create_logger

logger = create_logger("youtubedownloader.settings")


class Paths:
    settings = os.path.join(QStandardPaths.writableLocation(QStandardPaths.ConfigLocation), "ydsettings")
    database = os.path.join(QStandardPaths.writableLocation(QStandardPaths.ConfigLocation), "yddatabase.db")
    dialogs = os.path.join(os.path.dirname(__file__), "qml/dialogs")
    models = QStandardPaths.writableLocation(QStandardPaths.ConfigLocation)


class Attribute:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def attach(self, cls):
        setattr(cls, self.name, self.value)


def attachattributes(*attributes):
    def attachattributeswrapper(cls):
        for attribute in attributes:
            attribute.attach(cls)

        return cls

    return attachattributeswrapper


@attachattributes(
    Attribute("_input", ""),
    Attribute("_output", QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)),
    Attribute("_format", "webm"),
    Attribute("_singleLine", True),
    Attribute("_themeColor", "#004d99"),

)
class Settings(QObject):
    inputChanged = Signal(str)
    outputChanged = Signal(str)
    formatChanged = Signal(str)
    singleLineChanged = Signal(bool)
    themeColorChanged = Signal(str)

    def __init__(self, path=Paths.settings):
        super().__init__()

        self.path = path

        if os.path.isfile(self.path):
            self.load()

        atexit.register(self.save)


    def load(self) -> None:
        settings = QSettings(self.path)
        settings.beginGroup("Settings")

        self._input = settings.value("input", "")
        self._output = settings.value("output", QStandardPaths.writableLocation(QStandardPaths.DownloadLocation))
        self._format = settings.value("format", "webm")
        self._singleLine = bool(settings.value("singleLine", "True"))
        self._themeColor = settings.value("themeColor", "#004d99")

        settings.endGroup()

        logger.info(f"Settings loaded {settings.value('singleLine', 'True')}")

    def save(self) -> None:
        settings = QSettings(self.path)

        settings.beginGroup("Settings")
        settings.setValue("input", self._input)
        settings.setValue("output", self._output)
        settings.setValue("format", self._format)
        settings.setValue("singleLine", "True" if self._singleLine else "False") # NOTE: QSettings has a problem with bool values(bool("False") = True)
        settings.setValue("themeColor", self._themeColor)

        settings.endGroup()


    @Property(str, notify = inputChanged)
    def input(self):
        return self._input

    @input.setter
    def input(self, value):
        self._input = value

        self.inputChanged.emit(self._input)

    @Property(str, notify = outputChanged)
    def output(self):
        return self._output

    @output.setter
    def output(self, value):
        self._output = value

        self.outputChanged.emit(self._output)

    @Property(str, notify = formatChanged)
    def format(self):
        return self._format

    @format.setter
    def format(self, value):
        self._format = value

        self.formatChanged.emit(self._format)

    @Property(bool, notify = singleLineChanged)
    def singleLine(self):
        return self._singleLine

    @singleLine.setter
    def singleLine(self, value):
        self._singleLine = value

        self.singleLineChanged.emit(self._singleLine)

    @Property(str, notify = themeColorChanged)
    def themeColor(self):
        return self._themeColor

    @themeColor.setter
    def themeColor(self, value):
        self._themeColor = value

        self.themeColorChanged.emit(self._themeColor)
