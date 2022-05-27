from PySide6.QtCore import (
    QObject,
    Qt,
    QStandardPaths,
    Slot,
    Signal,
    Property
)
from PySide6.QtQml import QQmlComponent

import sys, os, pathlib

from . import paths
from .logger import create_logger
from youtubedownloader.settings import Paths

logger = create_logger(__name__)


class DialogManager(QObject):
    open = Signal(str, "QVariantMap", "QVariant", arguments=["dialog", "properties", "callback"])
    close = Signal(str, arguments=["dialog"])

    def __init__(self):
        super(DialogManager, self).__init__(None)

        self.dialogs = paths.collect_files(Paths.dialogs)

        logger.info("Loaded {dialogs} dialogs".format(dialogs=len(self.dialogs)))

    @Slot(str, "QVariantMap" ,"QVariant")
    def openDialog(self, dialog: str, properties, callback) -> None:
        logger.info("Opening {dialog}".format(dialog=dialog))

        self.open.emit(self.dialogs[dialog], properties, callback)

    @Slot(str)
    def closeDialog(self, dialog: str) -> None:
        logger.info("Closing {dialog}".format(dialog=dialog))

        self.close.emit(dialog)
