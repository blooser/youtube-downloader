# This Python file uses the following encoding: utf-8
import sys, os

from PySide2.QtQml import QQmlApplicationEngine, QQmlContext
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import Qt, QUrl, QResource
from PySide2.QtWidgets import QApplication

from .download import DownloadManager
from .dialog_manager import DialogManager
from .resources import Resources
from .theme import Theme
from .paths import Paths
from .settings import Settings


def start_yddownloader():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    app.setApplicationName("youtube downloader")
    app.setApplicationVersion("0.0.1")
    app.setOrganizationName("blooser")

    download_manager = DownloadManager()
    settings = Settings()
    dialog_manager = DialogManager()
    resources = Resources()
    paths = Paths()

    qml_file = os.path.join(os.path.dirname(__file__), "qml/main.qml")
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("Theme", Theme)
    engine.rootContext().setContextProperty("Resources", resources)
    engine.rootContext().setContextProperty("Settings", settings)
    engine.rootContext().setContextProperty("downloadManager", download_manager)
    engine.rootContext().setContextProperty("dialogManager", dialog_manager)
    engine.rootContext().setContextProperty("paths", paths)
    download_manager.setQMLContext(engine)
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())

