from PySide6.QtCore import (
    QObject,
    Qt,
    QStandardPaths,
    Slot,
    Signal,
    Property
)

import sys, os, pathlib

from .. import paths
from ..logger import create_logger

logger = create_logger(__name__)

class Resources(QObject):
    CORE_PATH = os.path.dirname(__file__)
    LOGO = os.path.join(CORE_PATH, "youtube-downloader.svg")

    def __init__(self):
        super().__init__()

        logger.info("YD Logo loaded {status}".format(status=os.path.exists(self.LOGO)))

        self._icons = paths.collect_files(os.path.join(self.CORE_PATH, "icons"))
        logger.info("Loaded {icons} icons".format(icons=len(self._icons)))

    @Property("QVariantMap", constant=True)
    def icons(self):
        return self._icons

    @Property("QUrl", constant=True)
    def logo(self):
        return os.path.join(paths.FILE_PREFIX, self.LOGO)
