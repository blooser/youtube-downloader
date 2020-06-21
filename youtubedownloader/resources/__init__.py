from PySide2.QtCore import QObject, Qt, QStandardPaths, Slot, Signal, Property

import sys, os, pathlib

from ..paths import Paths
from ..logger import create_logger

class Resources(QObject):
    CORE_PATH = os.path.dirname(__file__)
    YD_LOGO = os.path.join(CORE_PATH, "youtube-downloader.svg")

    def __init__(self):
        super(Resources, self).__init__(None)

        self.logger = create_logger(__name__)
        self.logger.info("YD Logo loaded {status}".format(status=os.path.exists(Resources.YD_LOGO)))

        self.icon_paths = Paths.collect_files(os.path.join(Resources.CORE_PATH, "icons"))
        self.logger.info("Loaded {icons} icons".format(icons=len(self.icon_paths)))

    @Property("QVariantMap", constant=True)
    def icons(self):
        return self.icon_paths

    @Property("QUrl", constant=True)
    def logo(self):
        return os.path.join(Paths.FILE_PREFIX, Resources.YD_LOGO)
