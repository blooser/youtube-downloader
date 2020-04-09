from PySide2.QtCore import QObject, Qt, QStandardPaths, Slot, Signal, Property

import sys, os, pathlib

from ..paths import Paths
from ..logger import create_logger

class Resources(QObject):
    CORE_PATH = os.path.dirname(__file__)

    def __init__(self):
        super(Resources, self).__init__(None)

        self.logger = create_logger(__name__)
        self.icon_paths = Paths.collect_files(os.path.join(Resources.CORE_PATH, "icons"))
        self.logger.info("Loaded {icons} icons".format(icons=len(self.icon_paths)))

    def get_icons(self):
        return self.icon_paths

    icons = Property("QVariantMap", get_icons, constant=True)
