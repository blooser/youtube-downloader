# This Python file uses the following encoding: utf-8
import sys, os

from PySide2.QtQml import QQmlApplicationEngine, QQmlContext, qmlRegisterType
from PySide2.QtQuick import QQuickView
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt, QUrl, QResource
from PySide2.QtWidgets import QApplication

from .download import DownloadManager, FileDownloader
from .models import StringFilterModel, SupportedSitesModel, HistoryModel
from .component_changer import ComponentChanger, Change
from .dialog_manager import DialogManager
from .resources import Resources
from .theme import Theme
from .paths import Paths
from .settings import Settings
from .database import Database
from .browser import Browsers

def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    app.setApplicationName("youtube downloader")
    app.setApplicationVersion("0.4.0")
    app.setOrganizationName("blooser")
    app.setWindowIcon(QIcon(Resources.YD_LOGO))

    database = Database(Settings.DB_PATH)
    download_manager = DownloadManager()
    settings = Settings()
    dialog_manager = DialogManager()
    resources = Resources()
    paths = Paths()
    browsers = Browsers()
    supported_sites_model = SupportedSitesModel()
    history_model = HistoryModel(database.session)
    file_downloader = FileDownloader()

    qmlRegisterType(Change, "yd.items", 0, 1, "Change")
    qmlRegisterType(ComponentChanger, "yd.items", 0, 1, "ComponentChanger")
    qmlRegisterType(StringFilterModel, "yd.items", 0, 1, "StringFilterModel")

    qml_file = os.path.join(os.path.dirname(__file__), "qml/main.qml")
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("Theme", Theme)
    engine.rootContext().setContextProperty("Resources", resources)
    engine.rootContext().setContextProperty("Settings", settings)
    engine.rootContext().setContextProperty("downloadManager", download_manager)
    engine.rootContext().setContextProperty("dialogManager", dialog_manager)
    engine.rootContext().setContextProperty("Paths", paths)
    engine.rootContext().setContextProperty("fileDownloader", file_downloader)
    engine.rootContext().setContextProperty("supportedSitesModel", supported_sites_model)
    engine.rootContext().setContextProperty("historyModel", history_model)
    engine.rootContext().setContextProperty("WebBrowsers", browsers)
    download_manager.setQMLContext(engine)
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())

