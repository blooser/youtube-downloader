# This Python file uses the following encoding: utf-8

from PySide2.QtQml import QQmlApplicationEngine, QQmlContext
from PySide2.QtCore import QObject, QAbstractListModel, QFileInfo, QFileSystemWatcher, QModelIndex, QDateTime, QThreadPool, QRunnable, QTimer, Qt, QSettings, QStandardPaths, Slot, Signal, Property

import os.path
import pathlib
import pickle
import youtube_dl

from .logger import create_logger
from .settings import Settings


class DownloadCommunication(QObject):
    updated = Signal(str)
    progress = Signal(dict)
    start = Signal()


class PreDownloadTask(QRunnable):
    def __init__(self, url):
        super(PreDownloadTask, self).__init__(None)
        self.url = url
        self.communication = DownloadCommunication()

    def run(self):
        with youtube_dl.YoutubeDL() as ydl:
            info = ydl.extract_info(self.url, download=False)

        self.communication.progress.emit(info)


class PreDownload(object):
    def __init__(self, url, options):
        self.ready = False
        self.id = hash(url)
        self.url = url
        self.title = str()
        self.uploader = str()
        self.thumbnail = str()
        self.duration = str()
        self.download_options = DownloadOptions(options)
        self.communication = DownloadCommunication()

    @Slot(dict)
    def collect_info(self, info):
        self.ready = True
        self.title = info["title"]
        self.uploader = info["uploader"]
        self.thumbnail = info["thumbnail"]
        self.duration = int(info["duration"])

        self.communication.updated.emit(str(self.id))

        if self.download_options.need_post_process():
            self.download_options.calc_post_process_file_size(self.duration) # TODO: Add choice to select bitrate, mp3 in the only one which need post process?

    @staticmethod
    def pack(predownload):
        return {
            "ready": predownload.ready,
            "id": predownload.id,
            "url": predownload.url,
            "title": predownload.title,
            "uploader": predownload.uploader,
            "thumbnail": predownload.thumbnail,
            "duration": predownload.duration,
            "download_options": DownloadOptions.pack(predownload.download_options)
        }

    @staticmethod
    def unpack(data):
        predownload = PreDownload(data["url"], data["download_options"])
        predownload.ready = bool(data["ready"])
        predownload.id = data["id"]
        predownload.title = data["title"]
        predownload.uploader = data["uploader"]
        predownload.thumbnail = data["thumbnail"]
        predownload.duration = data["duration"]
        return predownload


class PreDownloadModel(QAbstractListModel):
    COLUMNS = ("ready", "title", "uploader", "thumbnail", "duration", "options")
    FIRST_COLUMN = 0
    LAST_COLUMN = len(COLUMNS)

    sizeChanged = Signal(int)

    def __init__(self, config_path=None):
        super(PreDownloadModel, self).__init__(None)
        self.predownloads = []

        self.config_path = config_path if config_path is not None else Settings.CONFIG_PATH

        self.load()

        self.rowsInserted.connect(lambda: self.sizeChanged.emit(len(self.predownloads)))
        self.rowsRemoved.connect(lambda: self.sizeChanged.emit(len(self.predownloads)))

    def __del__(self):
        self.save()

    @Property(int, notify=sizeChanged)
    def size(self):
        return len(self.predownloads)

    def save(self):
        settings = QSettings(self.config_path, QSettings.NativeFormat)

        settings.beginWriteArray("predownloads")
        for i in range(len(self.predownloads)):
            settings.setArrayIndex(i)
            settings.setValue("predownload", PreDownload.pack(self.predownloads[i]))
        settings.endArray()

    def load(self):
        settings = QSettings(self.config_path, QSettings.NativeFormat)

        size = settings.beginReadArray("predownloads")
        for i in range(size):
            settings.setArrayIndex(i)
            self.predownloads.append(PreDownload.unpack(settings.value("predownload")))
        settings.endArray()

    def rowCount(self, index=QModelIndex()):
        return len(self.predownloads)

    def roleNames(self, index=QModelIndex()):
        return {
            0: b"ready",
            1: b"title",
            2: b"uploader",
            3: b"thumbnail",
            4: b"duration",
            5: b"options"
        }

    def index(self, row, column, parent):
        return self.createIndex(row, column, parent)

    def refresh(self, id):
        id = int(id)
        for row, predownload in enumerate(self.predownloads):
            if predownload.id == id:
                self.dataChanged.emit(self.index(row, PreDownloadModel.FIRST_COLUMN, QModelIndex()), self.index(row, PreDownloadModel.LAST_COLUMN, QModelIndex()))
                break

    def add_predownload(self, predownload):
        self.beginInsertRows(QModelIndex(), len(self.predownloads), len(self.predownloads))
        predownload.communication.updated.connect(self.refresh, Qt.QueuedConnection)
        self.predownloads.append(predownload)
        self.endInsertRows()

    @Slot(int)
    def remove_predownload(self, row):
        if row >= len(self.predownloads):
            return

        self.beginRemoveRows(QModelIndex(), row, row)
        self.predownloads.pop(row)
        self.endRemoveRows()

    def clear(self):
        self.beginResetModel()
        self.predownloads.clear()
        self.endResetModel()

    def data(self, index, role):
        if not index.isValid():
            return

        predownload = self.predownloads[index.row()]

        if role == 0:
            return predownload.ready

        elif role == 1:
            return predownload.title

        elif role == 2:
            return predownload.uploader

        elif role == 3:
            return predownload.thumbnail

        elif role == 4:
            return QDateTime.fromSecsSinceEpoch(int(predownload.duration)).toString("mm:ss")

        elif role == 5:
            return predownload.download_options

        return None


class DownloadProgress(QObject):
    changed = Signal()

    def __init__(self):
        super(DownloadProgress, self).__init__(None)
        self.status = str("queued") # NOTE: Think about better status notification
        self.downloaded_bytes = str("0")
        self.total_bytes = str("0")
        self.estimated_time = str("00:00")
        self.speed = str("0 MiB/s")
        self.filename = str("Unknown")

    @Property(str, notify=changed)
    def downloadStatus(self):
        return self.status

    @Property(int, notify=changed)
    def downloadedBytes(self):
        return int(self.downloaded_bytes)

    @Property(int, notify=changed)
    def totalBytes(self):
        return int(self.total_bytes)

    @Property(str, notify=changed)
    def estimatedTime(self):
        return self.estimated_time

    @Property(str, notify=changed)
    def downloadSpeed(self):
        return self.speed

    def update(self, data):
        if "status" in data:
            self.status = data["status"]

        if "downloaded_bytes" in data:
            self.downloaded_bytes = data["downloaded_bytes"]

        if "total_bytes" in data:
            self.total_bytes = data["total_bytes"]

        if "_eta_str" in data:
            self.estimated_time = data["_eta_str"]

        if "_speed_str" in data:
            self.speed = data["_speed_str"]

        if "filename" in data:
            self.filename = data["filename"]

        self.changed.emit() # TODO: Maybe separated signal for each property?

    @staticmethod
    def pack(download_progress):
        return {
            "status": download_progress.status,
            "downloaded_bytes": download_progress.downloaded_bytes,
            "total_bytes": download_progress.total_bytes,
            "estimated_time": download_progress.estimated_time,
            "speed": download_progress.speed,
            "filename": download_progress.filename
        }

    @staticmethod
    def unpack(data):
        download_progress = DownloadProgress()
        download_progress.status = data["status"]
        download_progress.downloaded_bytes = data["downloaded_bytes"]
        download_progress.total_bytes = data["total_bytes"]
        download_progress.estimated_time = data["estimated_time"]
        download_progress.speed = data["speed"]
        download_progress.filename = data["filename"]
        return download_progress


class DownloadOptions(QObject):
    OUTPUT_FILE = "%(title)s.%(ext)s"

    MP3_TEMPLATE = {
        "postprocessors": [{
               "key": 'FFmpegExtractAudio',
               "preferredcodec": 'mp3',
               "preferredquality": "192",
            }]
        }

    MP4_TEMPLATE = {
       "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4"
    }

    WEBM_TEMPLATE = {}

    changed = Signal(str)

    def __init__(self, options):
        super(DownloadOptions, self).__init__(None)
        self.file_format = options["file_format"]
        self.output_path = options["output_path"]
        self.ydl_opts = {
            "format": "bestaudio/best"
        }

        self.post_process_file_size = int(options["post_process_file_size"]) if "post_process_file_size" in options else 0

    def __eq__(self, other):
        return self.file_format == other.file_format and self.output_path == other.output_path

    @Property(str, notify=changed)
    def fileFormat(self):
        return self.file_format

    @Property(str, notify=changed)
    def outputPath(self):
        return self.output_path

    def calc_post_process_file_size(self, duration):
        self.post_process_file_size = (((192 * duration)/8) * 1000)

    def to_ydl_opts(self):
        template = self.ydl_opts
        template.update(self.output_template())
        template.update(self.post_processors())
        return template

    def need_post_process(self):
        return self.file_format in ["mp3"] # TODO: Add more file formats

    def output_template(self):
        return {
            "outtmpl": self.output_path + "/" + DownloadOptions.OUTPUT_FILE
        }

    def post_processors(self):
        if "mp3" in self.file_format:
            return DownloadOptions.MP3_TEMPLATE

        elif "mp4" in self.file_format:
            return DownloadOptions.MP4_TEMPLATE

        elif "webm" in self.file_format:
            return DownloadOptions.WEBM_TEMPLATE

        return {}

    @staticmethod
    def pack(download_options):
        return {
            "file_format": download_options.file_format,
            "output_path": download_options.output_path,
            "post_process_file_size": download_options.post_process_file_size
        }

    @staticmethod
    def unpack(data):
        download_options = DownloadOptions(data)
        return download_options


class DownloadTask(QRunnable):
    def __init__(self, url, options):
        super(DownloadTask, self).__init__(None)
        self.url = url
        self.options = options
        self.ydl_opts = self.options.to_ydl_opts()

        self.ydl_opts["progress_hooks"] = [self.process]

        self.communication = DownloadCommunication()

        self.download_post_process = DownloadPostProcess()
        self.download_post_process.total_bytes = self.options.post_process_file_size
        self.post_process_file = str()
        self.post_process_timer = QTimer()
        self.post_process_timer.setInterval(500)
        self.post_process_timer.setSingleShot(True)
        self.post_process_timer.timeout.connect(lambda: self.download_post_process.track(self.post_process_file))

        self.communication.start.connect(self.post_process_timer.start)
        self.download_post_process.bytes_processed.connect(lambda bytes: self.communication.progress.emit({"downloaded_bytes": bytes}), Qt.QueuedConnection)
        self.download_post_process.finished.connect(lambda: self.communication.progress.emit({"status": "finished"}), Qt.QueuedConnection)
        self.download_post_process.started.connect(lambda: self.communication.progress.emit({"status": "Converting to {0}".format(self.options.file_format),
                                                                                             "total_bytes": self.options.post_process_file_size}), Qt.QueuedConnection)
    def process(self, data):
        self.communication.progress.emit(data)

        if self.options.need_post_process() and data["status"] == "finished":
            self.post_process_file = os.path.join(self.options.output_path, "{file}.{ext}".format(file=pathlib.PurePath(data["filename"]).stem, ext=self.options.file_format))
            self.communication.start.emit()

    def run(self):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([self.url])


class Download(QObject):
    def __init__(self, data):
        super(Download, self).__init__(None)
        self.id = data["id"]
        self.url = data["url"]
        self.title = data["title"]
        self.uploader = data["uploader"]
        self.thumbnail = data["thumbnail"]
        self.duration = data["duration"]
        self.download_options = DownloadOptions.unpack(data["download_options"])

        self.progress = DownloadProgress()
        self.communication = DownloadCommunication()

    def __eq__(self, other):
        return self.id == other.id

    @Slot(dict)
    def update(self, data):
        self.progress.update(data)
        self.communication.updated.emit(str(self.id)) # PySide2's Signal doesn't handle such big number, to avoid Overflowing we use string

    @staticmethod
    def pack(download):
        return {
            "id": download.id,
            "url": download.url,
            "title": download.title,
            "uploader": download.uploader,
            "thumbnail": download.thumbnail,
            "duration": download.duration,
            "download_options": DownloadOptions.pack(download.download_options),
            "progress": DownloadProgress.pack(download.progress)
        }

    @staticmethod
    def unpack(data):
        download = Download(data)
        download.progress = DownloadProgress.unpack(data["progress"])
        return download

    @classmethod
    def fromPreDownload(cls, predownload):
        return cls(PreDownload.pack(predownload))


class DownloadPostProcess(QObject):
    bytes_processed = Signal(int)
    started = Signal()
    finished = Signal()

    def __init__(self):
        super(DownloadPostProcess, self).__init__(None)

        self.file_watcher = QFileSystemWatcher()
        self.file_watcher.fileChanged.connect(self.read_bytes)
        self.total_bytes = None

        self.logger = create_logger(__name__)

    def track(self, url):
        track_success = self.file_watcher.addPath(url)
        self.logger.info("Track {file} success={success}".format(file=url, success=track_success))
        self.started.emit()

    @Slot(str)
    def read_bytes(self, path):
        bytes = QFileInfo(path).size()
        self.bytes_processed.emit(bytes)
        self.logger.debug("Read {bytes} bytes".format(bytes=bytes))

        if bytes >= self.total_bytes:
            self.finished.emit()


class DownloadModel(QAbstractListModel):
    COLUMNS = ("title", "uploader", "duration", "progress", "thumbnail", "output_path", "options")
    FIRST_COLUMN = 0
    LAST_COLUMN = len(COLUMNS)

    sizeChanged = Signal(int)

    def __init__(self, config_path=None):
        super(DownloadModel, self).__init__(None)
        self.downloads = []

        self.config_path = config_path if config_path is not None else Settings.CONFIG_PATH

        self.load()

        self.rowsInserted.connect(lambda: self.sizeChanged.emit(len(self.downloads)))
        self.rowsRemoved.connect(lambda: self.sizeChanged.emit(len(self.downloads)))

    def __del__(self):
        self.save()

    @Property(int, notify=sizeChanged)
    def size(self):
        return len(self.downloads)

    def save(self):
        settings = QSettings(self.config_path)

        settings.beginWriteArray("downloads")
        for i in range(len(self.downloads)):
            settings.setArrayIndex(i)
            settings.setValue("download", Download.pack(self.downloads[i]))
        settings.endArray()

    def load(self):
        settings = QSettings(self.config_path)

        size = settings.beginReadArray("downloads")
        for i in range(size):
            settings.setArrayIndex(i)
            self.downloads.append(Download.unpack(settings.value("download")))
        settings.endArray()

    def rowCount(self, index=QModelIndex()):
        return len(self.downloads)

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return DownloadModel.COLUMNS[col]

        return None

    def roleNames(self, index=QModelIndex()):
        return {
            0: b"title",
            1: b"uploader",
            2: b"duration",
            3: b"progress",
            4: b"thumbnail",
            5: b"options"
        }

    def clear(self):
        self.beginResetModel()
        self.downloads.clear()
        self.endResetModel()

    def index(self, row, column, parent):
        return self.createIndex(row, column, None)

    def refresh(self, id):
        id = int(id) # PySide2's Signal doesn't handle such big number, to avoid overflowing we use string
        for row, download in enumerate(self.downloads):
            if download.id == id:
                self.dataChanged.emit(self.index(row, DownloadModel.FIRST_COLUMN, QModelIndex()), self.index(row, DownloadModel.LAST_COLUMN, QModelIndex()))
                break

    def add_download(self, download):
        self.beginInsertRows(QModelIndex(), len(self.downloads), len(self.downloads))
        download.communication.updated.connect(self.refresh, Qt.QueuedConnection)
        self.downloads.append(download)
        self.endInsertRows()

    @Slot(int)
    def remove_download(self, row):
        if row >= len(self.downloads):
            return

        self.beginRemoveRows(QModelIndex(), row, row)
        self.downloads.pop(row)
        self.endRemoveRows()

    def data(self, index, role):
        if not index.isValid():
            return None

        download = self.downloads[index.row()]

        if role == 0:
            return download.title

        elif role == 1:
            return download.uploader

        elif role == 2:
            return QDateTime.fromSecsSinceEpoch(download.duration).toString("mm:ss")

        elif role == 3:
            return download.progress

        elif role == 4:
            return download.thumbnail

        elif role == 5:
            return download.download_options

        return None


class DownloadManager(QThreadPool):
    def __init__(self):
        super(DownloadManager, self).__init__(None)
        self.predownload_model = PreDownloadModel()
        self.download_model = DownloadModel()
        self.logger = create_logger(__name__)

    @Slot(str, "QVariantMap")
    def predownload(self, url, options):
        predownload = PreDownload(url, options)
        predownload_task = PreDownloadTask(url)
        predownload_task.communication.progress.connect(predownload.collect_info, Qt.QueuedConnection)
        self.predownload_model.add_predownload(predownload)
        self.start(predownload_task)

    @Slot()
    def download(self):
        self.logger.info("Downloading {items} items".format(items=len(self.predownload_model.predownloads)))

        for predownload in self.predownload_model.predownloads:
            download = Download.fromPreDownload(predownload)
            download_task = DownloadTask(download.url, download.download_options)
            download_task.communication.progress.connect(download.update, Qt.QueuedConnection)
            self.download_model.add_download(download)
            self.start(download_task)

        self.predownload_model.clear()

    def setQMLContext(self, engine):
        engine.rootContext().setContextProperty("downloadModel", self.download_model)
        engine.rootContext().setContextProperty("predownloadModel", self.predownload_model)
