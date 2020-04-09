# This Python file uses the following encoding: utf-8

from PySide2.QtCore import QObject, QSettings, QStandardPaths, Signal, Property

class Settings(QObject):
    CONFIG_PATH = QStandardPaths.writableLocation(QStandardPaths.ConfigLocation) + "/.yddownloadersettings"

    output_path_changed = Signal(str)
    type_changed = Signal(str)

    def __init__(self, settings_path=None):
        super(Settings, self).__init__(None)

        self.settings_path = Settings.CONFIG_PATH if settings_path == None else settings_path

        self.output_path = None
        self.type = None

        self.load()

    def __del__(self):
        self.save()

    def load(self):
        settings = QSettings(self.settings_path)
        settings.beginGroup("Settings")
        self.output_path = settings.value("output_path")
        self.type = settings.value("type")
        settings.endGroup()

    def save(self):
        settings = QSettings(self.settings_path)
        settings.beginGroup("Settings")
        settings.setValue("output_path", self.output_path)
        settings.setValue("type", self.type)
        settings.endGroup()

    def read_output_path(self):
        return self.output_path

    def set_output_path(self, output_path):
        self.output_path = output_path
        self.output_path_changed.emit(self.output_path)

    def read_type(self):
        return self.type

    def set_type(self, type):
        self.type = type
        self.type_changed.emit(self.type)

    outputPath = Property(str, read_output_path, set_output_path, notify=output_path_changed)
    selectedType = Property(str, read_type, set_type, notify=type_changed)
