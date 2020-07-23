from PySide2.QtCore import (
    QObject,
    QSettings,
    QStandardPaths,
    Signal,
    Property
)

import os.path
import atexit

class Settings(QObject):
    CONFIG_PATH: str = os.path.join(QStandardPaths.writableLocation(QStandardPaths.ConfigLocation), "ydsettings")
    DB_PATH: str = os.path.join(QStandardPaths.writableLocation(QStandardPaths.ConfigLocation), "yddatabase.db")

    input_link_changed = Signal(str)
    output_path_changed = Signal(str)
    file_format_changed = Signal(str)
    single_line_changed = Signal(bool)
    theme_color_changed = Signal(str)

    def __init__(self, settings_path=None):
        super(Settings, self).__init__(None)

        self.settings_path = Settings.CONFIG_PATH if settings_path == None else settings_path

        self.input_link = str()
        self.output_path = QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)
        self.file_format = "webm"
        self.single_line = True
        self.theme_color = "#004d99"

        if os.path.isfile(Settings.CONFIG_PATH):
            self.load()

        atexit.register(self.save)

    def load(self) -> None:
        settings = QSettings(self.settings_path)
        settings.beginGroup("Settings")
        self.input_link = settings.value("input_link", "")
        self.output_path = settings.value("output_path", QStandardPaths.writableLocation(QStandardPaths.DownloadLocation))
        self.file_format = settings.value("file_format", "webm")
        self.single_line = bool(settings.value("single_line", "True") == "True")
        self.theme_color = settings.value("theme_color", "#004d99")
        settings.endGroup()

    def save(self) -> None:
        settings = QSettings(self.settings_path)
        settings.beginGroup("Settings")
        settings.setValue("input_link", self.input_link)
        settings.setValue("output_path", self.output_path)
        settings.setValue("file_format", self.file_format)
        settings.setValue("single_line", "True" if self.single_line else "False") # NOTE: QSettings has a problem with bool values(bool("False") = True)
        settings.setValue("theme_color", self.theme_color)
        settings.endGroup()

    def read_input_link(self) -> str:
        return self.input_link

    def set_input_link(self, input_link: str) -> None:
        if self.input_link == input_link:
            return

        self.input_link = input_link
        self.input_link_changed.emit(self.input_link)

    def read_output_path(self) -> str:
        return self.output_path

    def set_output_path(self, output_path: str) -> None:
        if self.output_path == output_path:
            return

        self.output_path = output_path
        self.output_path_changed.emit(self.output_path)

    def read_file_format(self) -> str:
        return self.file_format

    def set_file_format(self, file_format: str) -> None:
        if self.file_format == file_format:
            return

        self.file_format = file_format
        self.file_format_changed.emit(self.file_format)

    def read_single_line(self) -> bool:
        return self.single_line

    def set_single_line(self, new_single_line: bool) -> None:
        if self.single_line == new_single_line:
            return

        self.single_line = new_single_line
        self.single_line_changed.emit(self.single_line)

    def read_theme_color(self) -> str:
        return self.theme_color

    def set_theme_color(self, new_theme_color: str) -> None:
        if self.theme_color == new_theme_color:
            return

        self.theme_color = new_theme_color
        self.theme_color_changed.emit(self.theme_color)


    inputLink = Property(str, read_input_link, set_input_link, notify=input_link_changed)
    outputPath = Property(str, read_output_path, set_output_path, notify=output_path_changed)
    fileFormat = Property(str, read_file_format, set_file_format, notify=file_format_changed)
    singleLine = Property(bool, read_single_line, set_single_line, notify=single_line_changed)
    themeColor = Property(str, read_theme_color, set_theme_color, notify=theme_color_changed)
