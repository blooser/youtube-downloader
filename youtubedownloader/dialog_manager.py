﻿from PySide2.QtCore import (
    QObject,
    Qt,
    QStandardPaths,
    Slot,
    Signal,
    Property
)
from PySide2.QtQml import QQmlComponent

import sys, os, pathlib

from . import paths
from .logger import create_logger


class DialogManager(QObject):
    DIALOG_PATH: str = os.path.join(os.path.dirname(__file__), "qml/dialogs")

    open = Signal(str, "QVariantMap", "QVariant", arguments=["dialog", "properties", "callback"])
    close = Signal(str, arguments=["dialog"])

    def __init__(self):
        super(DialogManager, self).__init__(None)

        self.logger = create_logger(__name__)
        self.dialogs = paths.collect_files(DialogManager.DIALOG_PATH)
        self.logger.info("Loaded {dialogs} dialogs".format(dialogs=len(self.dialogs)))

    @Slot(str, "QVariantMap" ,"QVariant")
    def open_dialog(self, dialog: str, properties, callback) -> None:
        self.logger.info("Creating {dialog}".format(dialog=dialog))
        self.open.emit(self.dialogs[dialog], properties, callback)

    @Slot(str)
    def close_dialog(self, dialog: str) -> None:
        self.logger.info("Closing {dialog}".format(dialog=dialog))
        self.close.emit(dialog)
