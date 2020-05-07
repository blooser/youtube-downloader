# This Python file uses the following encoding: utf-8

from PySide2.QtCore import QObject, QSettings, QRect, QStandardPaths, Signal, Property

import atexit

class Settings(QObject):
    CONFIG_PATH = QStandardPaths.writableLocation(QStandardPaths.ConfigLocation) + "/.yddownloadersettings"

    input_link_changed = Signal(str)
    output_path_changed = Signal(str)
    file_format_changed = Signal(str)
    window_rect_changed = Signal(QRect)

    def __init__(self, settings_path=None):
        super(Settings, self).__init__(None)

        self.settings_path = Settings.CONFIG_PATH if settings_path == None else settings_path

        self.input_link = str()
        self.output_path = QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)
        self.file_format = "webm"
        self.window_rect = QRect(0, 0, 1050, 1050)

        self.load()

        atexit.register(self.save)

    def load(self):
        settings = QSettings(self.settings_path)
        settings.beginGroup("Settings")
        self.input_link = settings.value("input_link")
        self.output_path = settings.value("output_path")
        self.file_format = settings.value("file_format")
        self.window_rect = settings.value("window_rect")
        settings.endGroup()

    def save(self):
        settings = QSettings(self.settings_path)
        settings.beginGroup("Settings")
        settings.setValue("input_link", self.input_link)
        settings.setValue("output_path", self.output_path)
        settings.setValue("file_format", self.file_format)
        settings.setValue("window_rect", self.window_rect)
        settings.endGroup()

    def read_input_link(self):
        return self.input_link

    def set_input_link(self, input_link):
        if self.input_link == input_link:
            return

        self.input_link = input_link
        self.input_link_changed.emit(self.input_link)

    def read_output_path(self):
        return self.output_path

    def set_output_path(self, output_path):
        if self.output_path == output_path:
            return

        self.output_path = output_path
        self.output_path_changed.emit(self.output_path)

    def read_file_format(self):
        return self.file_format

    def set_file_format(self, file_format):
        if self.file_format == file_format:
            return

        self.file_format = file_format
        self.file_format_changed.emit(self.file_format)

    def read_window_rect(self):
        return self.window_rect

    def set_window_rect(self, window_rect):
        if self.window_rect == window_rect:
            return

        self.window_rect = window_rect
        self.window_rect_changed.emit(self.window_rect)

    inputLink = Property(str, read_input_link, set_input_link, notify=input_link_changed)
    outputPath = Property(str, read_output_path, set_output_path, notify=output_path_changed)
    fileFormat = Property(str, read_file_format, set_file_format, notify=file_format_changed)
    windowRect = Property(QRect, read_window_rect, set_window_rect, notify=window_rect_changed)
