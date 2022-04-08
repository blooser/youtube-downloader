﻿from PySide6.QtCore import (
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

class Resources(QObject):
    CORE_PATH: str = os.path.dirname(__file__)
    YD_LOGO: str = os.path.join(CORE_PATH, "youtube-downloader.svg")

    def __init__(self):
        super(Resources, self).__init__(None)

        self.logger = create_logger(__name__)
        self.logger.info("YD Logo loaded {status}".format(status=os.path.exists(Resources.YD_LOGO)))

        self.icon_paths = paths.collect_files(os.path.join(Resources.CORE_PATH, "icons"))
        self.logger.info("Loaded {icons} icons".format(icons=len(self.icon_paths)))

    @Property("QVariantMap")
    def icons(self) -> dict:
        return self.icon_paths

    @Property("QUrl")
    def logo(self) -> str:
        return os.path.join(paths.FILE_PREFIX, Resources.YD_LOGO)
