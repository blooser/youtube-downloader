# This Python file uses the following encoding: utf-8

from PySide2.QtQml import QQmlApplicationEngine, QQmlContext
from PySide2.QtCore import QObject, QAbstractListModel, QFileInfo, QFileSystemWatcher, QModelIndex, QDateTime, QThreadPool, QRunnable, QTimer, Qt, QStandardPaths, Slot, Signal, Property

import os.path
import pathlib
import pickle
import youtube_dl

from logger import create_logger

class DownloadProgress(QObject):
    changed = Signal()

    def __init__(self):
        super(DownloadProgress, self).__init__(None)
        self.status = str("Starting")
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

        self.changed.emit() # TODO: Maybe separated signl for each property?

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
        "postprocessors": [{
            "key": "FFmpegVideoConvertor",
            "preferredformat": "mp4"
        }]
    }

    WEBM_TEMPLATE = {}

    def __init__(self, options):
        self.type = options["type"]
        self.output_path = options["output_path"]
        self.ydl_opts = {
            "format": "bestaudio/best"
        }

    def to_ydl_opts(self):
        template = self.ydl_opts
        template.update(self.output_template())
        template.update(self.post_processors())
        return template

    def need_post_process(self):
        return self.type in ["mp3", "mp4"]

    def output_template(self):
        return {
            "outtmpl": self.output_path + "/" + DownloadOptions.OUTPUT_FILE
        }

    def post_processors(self):
        if "mp3" in self.type:
            return DownloadOptions.MP3_TEMPLATE

        elif "mp4" in self.type:
            return DownloadOptions.MP4_TEMPLATE

        elif "webm" in self.type:
            return DownloadOptions.WEBM_TEMPLATE

        return {}

    @staticmethod
    def pack(download_options):
        return {
            "type": download_options.type,
            "output_path": download_options.output_path
        }

    @staticmethod
    def unpack(data):
        download_options = DownloadOptions(data)
        return download_options


class DownloadCommunication(QObject):
    updated = Signal(str)
    progress = Signal(dict)
    start = Signal()


class Download(QObject):
    def __init__(self, predownload):
        super(Download, self).__init__(None)
        self.id = predownload.id
        self.url = predownload.url
        self.title = predownload.title
        self.uploader = predownload.uploader
        self.duration = predownload.duration
        self.thumbnail = predownload.thumbnail
        self.download_options = predownload.download_options

        self.progress = DownloadProgress()
        self.communication = DownloadCommunication()

    @Slot(dict)
    def update(self, data):
        self.progress.update(data)
        self.communication.updated.emit(str(self.id))

    def __eq__(self, other):
        return self.id == other.id

    def __getstate__(self):
        return {
            "id": self.id,
            "url": self.url,
            "title": self.title,
            "uploader": self.uploader,
            "thumbnail": self.thumbnail,
            "download_options": DownloadOptions.pack(self.download_options),
            "progress": DownloadProgress.pack(self.progress)
        }

    def __setstate__(self, data):
        self.id = data["id"]
        self.url = data["url"]
        self.title = data["title"]
        self.uploader = data["uploader"]
        self.thumbnail = data["thumbnail"]
        self.download_options = DownloadOptions.unpack(data["download_options"])
        self.progress = DownloadProgress.unpack(data["progress"])


class DownloadPostProcess(QObject):
    bytes_processed = Signal(int)

    def __init__(self):
        super(DownloadPostProcess, self).__init__(None)

        self.file_watcher = QFileSystemWatcher()
        self.file_watcher.fileChanged.connect(self.read_bytes)

        self.logger = create_logger(__name__)

    def track(self, url):
        track_success = self.file_watcher.addPath(url)
        self.logger.info("Track {file} success={success}".format(file=url, success=track_success))

    @Slot(str)
    def read_bytes(self, path):
        bytes = QFileInfo(path).size()
        self.bytes_processed.emit(bytes)
        self.logger.debug("Read {bytes} bytes".format(bytes=bytes))


class PreDownloadTask(QRunnable):
    def __init__(self, url):
        super(PreDownloadTask, self).__init__(None)
        self.url = url
        self.communication = DownloadCommunication()

    def run(self):
        with youtube_dl.YoutubeDL() as ydl:
            info = ydl.extract_info(self.url, download=False)

        self.communication.progress.emit(info)


class DownloadTask(QRunnable):
    def __init__(self, url, options):
        super(DownloadTask, self).__init__(None)
        self.url = url
        self.options = options
        self.ydl_opts = self.options.to_ydl_opts()

        self.ydl_opts["progress_hooks"] = [self.process]

        self.communication = DownloadCommunication()

        self.download_post_process = DownloadPostProcess()
        self.post_process_file = str()
        self.post_process_timer = QTimer()
        self.post_process_timer.setInterval(250) # TODO: Check interval time depends on file size
        self.post_process_timer.setSingleShot(True)
        self.post_process_timer.timeout.connect(lambda: self.download_post_process.track(self.post_process_file))

        self.communication.start.connect(self.post_process_timer.start)
        self.download_post_process.bytes_processed.connect(lambda bytes: self.communication.progress.emit({"downloaded_bytes": bytes}))

    def process(self, data):
        self.communication.progress.emit(data)

        if self.options.need_post_process() and data["status"] == "finished":
            self.post_process_file = os.path.join(self.options.output_path, "{file}.{ext}".format(file=pathlib.PurePath(data["filename"]).stem, ext=self.options.type))
            self.communication.start.emit()
            self.communication.progress.emit({"status": "Converting to {0}".format(self.options.type)})

    def run(self):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([self.url])


class PreDownload(object):
    def __init__(self, url, options):
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
        self.title = info["title"]
        self.uploader = info["uploader"]
        self.thumbnail = info["thumbnail"]
        self.duration = QDateTime.fromSecsSinceEpoch(int(info["duration"])).toString("mm:ss")

        self.communication.updated.emit(str(self.id))

    def __getstate__(self):
        return {
            "id": self.id,
            "url": self.url,
            "title": self.title,
            "uploader": self.uploader,
            "thumbnail": self.thumbnail,
            "duration": self.duration,
            "download_options": DownloadOptions.pack(self.download_options)
        }

    def __setstate__(self, data):
        self.id = data["id"]
        self.url = data["url"]
        self.title = data["title"]
        self.uploader = data["uploader"]
        self.thumbnail = data["thumbnail"]
        self.duration = data["duration"]
        self.download_options = DownloadOptions.unpack(data["download_options"])
        self.communication = DownloadCommunication()


class PreDownloadModel(QAbstractListModel):
    PREDOWNLOADS_FILE = QStandardPaths.writableLocation(QStandardPaths.ConfigLocation) + "/.ydpredownloads"
    COLUMNS = ("title", "uploader", "thumbnail", "duration", "type")
    FIRST_COLUMN = 0
    LAST_COLUMN = len(COLUMNS)

    def __init__(self, config_path=None):
        super(PreDownloadModel, self).__init__(None)
        self.predownloads = []

        self.config_path = config_path if config_path is not None else PreDownloadModel.PREDOWNLOADS_FILE

        if os.path.isfile(self.config_path):
            with open(self.config_path, "rb") as f:
                self.predownloads = pickle.load(f)

    def __del__(self):
        with open(self.config_path, "wb") as f:
            pickle.dump(self.predownloads, f)

    def rowCount(self, index=QModelIndex()):
        return len(self.predownloads)

    def roleNames(self, index=QModelIndex()):
        return {
            0: b"title",
            1: b"uploader",
            2: b"thumbnail",
            3: b"duration",
            4: b"type"
        }

    def index(self, row, column, parent):
        return self.createIndex(row, column, parent)

    def refresh(self, id):
        id = int(id) # PySide2's Signal doesn't handle such big number, to avoid Overflowing we use string
        for row, predownload in enumerate(self.predownloads):
            if predownload.id == id:
                self.dataChanged.emit(self.index(row, PreDownloadModel.FIRST_COLUMN, QModelIndex()), self.index(row, PreDownloadModel.LAST_COLUMN, QModelIndex()))
                break

    def add_predownload(self, predownload):
        self.beginInsertRows(QModelIndex(), len(self.predownloads), len(self.predownloads))
        predownload.communication.updated.connect(self.refresh)
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
            return predownload.title

        elif role == 1:
            return predownload.uploader

        elif role == 2:
            return predownload.thumbnail

        elif role == 3:
            return predownload.duration

        elif role == 4:
            return predownload.download_options.type

        return None


class DownloadModel(QAbstractListModel):
    DOWNLOADS_FILE = QStandardPaths.writableLocation(QStandardPaths.ConfigLocation) + "/.yddownloads"
    COLUMNS = ("title", "uploader", "duration", "progress", "thumbnail", "output_path", "type")
    FIRST_COLUMN = 0
    LAST_COLUMN = len(COLUMNS)

    def __init__(self, config_path=None):
        super(DownloadModel, self).__init__(None)
        self.downloads = []

        self.config_path = config_path if config_path is not None else DownloadModel.DOWNLOADS_FILE

        if os.path.isfile(self.config_path):
            with open(self.config_path, "rb") as f:
                self.downloads = pickle.load(f)

    def __del__(self):
         with open(self.config_path, "wb") as f:
            pickle.dump(self.downloads, f)

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
            5: b"output_path",
            6: b"type"
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
            return download.duration

        elif role == 3:
            return download.progress

        elif role == 4:
            return download.thumbnail

        elif role == 5:
            return download.download_options.output_path

        elif role == 6:
            return download.download_options.type

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
        predownload_task.communication.progress.connect(predownload.collect_info)
        self.predownload_model.add_predownload(predownload)
        self.start(predownload_task)

    @Slot()
    def download(self):
        self.logger.info("Starting download {items} items".format(items=len(self.predownload_model.predownloads)))

        for predownload in self.predownload_model.predownloads:
            download = Download(predownload)
            download_task = DownloadTask(download.url, download.download_options)
            download_task.communication.progress.connect(download.update)
            self.download_model.add_download(download)
            self.start(download_task)

        self.predownload_model.clear()

    def setQMLContext(self, engine):
        engine.rootContext().setContextProperty("downloadModel", self.download_model)
        engine.rootContext().setContextProperty("predownloadModel", self.predownload_model)
