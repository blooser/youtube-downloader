from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide6.QtQuick import QQuickView
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QUrl, QResource
from PySide6.QtWidgets import QApplication

from .download import DownloadManager
from .models import StringFilterModel, SupportedSitesModel, HistoryModel
from .component_changer import ComponentChanger, Change
from .dialog_manager import DialogManager
from .resources import Resources
from .theme import Theme
from .paths import QPaths
from .settings import Settings
from .database import Database
from .browser import Browsers
from .version import __version__

import os, sys


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    app.setApplicationName("youtube downloader")
    app.setApplicationVersion(__version__)
    app.setOrganizationName("blooser")
    app.setWindowIcon(QIcon(Resources.YD_LOGO))

    database = Database(Settings.DB_PATH)
    download_manager = DownloadManager()
    settings = Settings()
    dialog_manager = DialogManager()
    resources = Resources()
    qpaths = QPaths()
    browsers = Browsers()
    supported_sites_model = SupportedSitesModel()
    history_model = HistoryModel(database.session)
    theme = Theme()
    #file_downloader = FileDownloader()

    theme.changeBaseColor(settings.theme_color) # NOTE: Before engine starts

    qmlRegisterType(StringFilterModel, "yd.items", 0, 1, "StringFilterModel")

    qml_file = os.path.join(os.path.dirname(__file__), "qml/main.qml")
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("Theme", theme)
    engine.rootContext().setContextProperty("Resources", resources)
    engine.rootContext().setContextProperty("Settings", settings)
    engine.rootContext().setContextProperty("downloadManager", download_manager)
    engine.rootContext().setContextProperty("dialogManager", dialog_manager)
    engine.rootContext().setContextProperty("Paths", qpaths)
    #engine.rootContext().setContextProperty("fileDownloader", file_downloader)
    engine.rootContext().setContextProperty("supportedSitesModel", supported_sites_model)
    engine.rootContext().setContextProperty("historyModel", history_model)
    engine.rootContext().setContextProperty("WebBrowsers", browsers)
    #download_manager.setQMLContext(engine)
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())

