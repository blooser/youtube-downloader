# This Python file uses the following encoding: utf-8

from PySide2.QtQml import QQmlApplicationEngine, QQmlContext
from PySide2.QtCore import QObject, QAbstractListModel, QFileInfo, QFileSystemWatcher, QModelIndex, QDateTime, QThreadPool, QThread, QTimer, Qt, QSettings, QStandardPaths, Slot, Signal, Property

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
    collected_info = Signal(dict)


class PreDownloadTask(QThread):
    collected_info = Signal(dict)

    def __init__(self, url):
        super(PreDownloadTask, self).__init__(None)
        self.url = url

    def __eq__(self, other):
        return self.url == other.url

    def run(self):
        with youtube_dl.YoutubeDL() as ydl:
            info = ydl.extract_info(self.url, download=False)

        self.collected_info.emit(info)


class PreDownloadData(object):
    def __init__(self):
        self.title = str()
        self.uploader = str()
        self.thumbnail = str()
        self.duration = str()

    def collect_info(self, info):
        self.title = info["title"]
        self.uploader = info["uploader"]
        self.thumbnail = info["thumbnail"]
        self.duration = int(info["duration"])

    @staticmethod
    def pack(predownloaddata):
        return {
            "title": predownloaddata.title,
            "uploader": predownloaddata.uploader,
            "thumbnail": predownloaddata.thumbnail,
            "duration": predownloaddata.duration,
        }

    @staticmethod
    def unpack(data):
        predownloaddata = PreDownloadData()
        predownloaddata.title = data["title"]
        predownloaddata.uploader = data["uploader"]
        predownloaddata.thumbnail = data["thumbnail"]
        predownloaddata.duration = data["duration"]
        return predownloaddata


class PreDownload(QObject):
    readyToDownload = Signal(str)

    def __init__(self, url, options):
        super(PreDownload, self).__init__(None)

        self.ready = False
        self.id = hash(url)
        self.url = url
        self.options = DownloadOptions(options)

        self.data = PreDownloadData()
        self.task = PreDownloadTask(self.url)

        self.task.collected_info.connect(self.prepare_data)
        self.task.finished.connect(self.setReady)

    def __del__(self):
        if self.task.isRunning():
            self.task.terminate()
            self.task.wait()

    def collect_info(self):
        self.task.start()

    @Slot()
    def setReady(self):
        self.ready = True
        self.readyToDownload.emit(str(self.id))

    @Slot()
    def prepare_data(self, info):
        self.data.collect_info(info)

        if self.options.need_post_process():
            self.options.calc_post_process_file_size(self.data.duration) # TODO: Add choice to select bitrate, mp3 in the only one which need post process?

    @staticmethod
    def pack(predownload):
        return {
            "url": predownload.url,
            "ready": predownload.ready,
            "data": PreDownloadData.pack(predownload.data),
            "options": DownloadOptions.pack(predownload.options)
        }

    @staticmethod
    def unpack(data):
        predownload = PreDownload(data["url"], data["options"])
        predownload.ready = data["ready"]
        predownload.data = PreDownloadData.unpack(data["data"])
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
        predownload.readyToDownload.connect(self.refresh, Qt.QueuedConnection)
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
            return predownload.data.title

        elif role == 2:
            return predownload.data.uploader

        elif role == 3:
            return predownload.data.thumbnail

        elif role == 4:
            return QDateTime.fromSecsSinceEpoch(int(predownload.data.duration)).toString("mm:ss")

        elif role == 5:
            return predownload.options

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

    @Slot(dict)
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


class DownloadTask(QThread):
    post_process_started = Signal()
    progress = Signal(dict)

    def __init__(self, url, options):
        super(DownloadTask, self).__init__(None)
        self.url = url
        self.options = options
        self.ydl_opts = self.options.to_ydl_opts()

        self.paused = False

        self.ydl_opts["progress_hooks"] = [self.process]

        # TODO: Use Operating System's filesystem events to handle when to start post process tracking
        self.download_post_process = DownloadPostProcess()
        self.download_post_process.total_bytes = self.options.post_process_file_size
        self.post_process_file = str()
        self.post_process_timer = QTimer()
        self.post_process_timer.setInterval(500)
        self.post_process_timer.setSingleShot(True)
        self.post_process_timer.timeout.connect(lambda: self.download_post_process.track(self.post_process_file))

        self.post_process_started.connect(self.post_process_timer.start)
        self.download_post_process.bytes_processed.connect(lambda bytes: self.progress.emit({"downloaded_bytes": bytes}), Qt.QueuedConnection)
        self.download_post_process.finished.connect(lambda: self.progress.emit({"status": "finished"}), Qt.QueuedConnection)
        self.download_post_process.started.connect(lambda: self.progress.emit({"status": "Converting to {0}".format(self.options.file_format),
                                                                                         "total_bytes": self.options.post_process_file_size}), Qt.QueuedConnection)
    def process(self, data):
        if self.paused:
            raise ValueError()

        if self.options.need_post_process() and data["status"] == "finished":
            self.post_process_file = os.path.join(self.options.output_path, "{file}.{ext}".format(file=pathlib.PurePath(data["filename"]).stem, ext=self.options.file_format))
            self.post_process_started.emit()

        else:
            self.progress.emit(data)

    def run(self):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([self.url])


class DownloadData(object):
    def __init__(self, data):
        self.title = data["title"]
        self.uploader = data["uploader"]
        self.thumbnail = data["thumbnail"]
        self.duration = data["duration"]

    @staticmethod
    def pack(download):
        return {
            "title": download.title,
            "uploader": download.uploader,
            "thumbnail": download.thumbnail,
            "duration": download.duration,
        }

    @staticmethod
    def unpack(data):
        return DownloadData(data)


class Download(QObject):
    updated = Signal(str)

    def __init__(self, url, options, data):
        super(Download, self).__init__(None)
        self.id = hash(url)
        self.url = url

        self.options = DownloadOptions(options)
        self.data = DownloadData(data)
        self.progress = DownloadProgress()
        self.task = DownloadTask(self.url, self.options)

        self.task.progress.connect(self.progress.update)

    def start(self):
        self.task.start()

    def pause(self):
        if self.task.isRunning():
            self.progress.status = "paused"
            self.task.paused = True

    def wait(self):
        while self.task.isRunning():
            continue

    @Slot(str)
    def update(self, progress):
        self.progress.update(progress)
        self.updated.emit(str(self.id))

    @staticmethod
    def pack(download):
        return {
            "url": download.url,
            "options": DownloadOptions.pack(download.options),
            "data": DownloadData.pack(download.data),
            "progress": DownloadProgress.pack(download.progress),
        }

    @staticmethod
    def unpack(data):
        download =  Download(data["url"], data["options"], data["data"])
        download.progress = DownloadProgress.unpack(data["progress"])
        return download

    @classmethod
    def fromPreDownload(cls, predownload):
        return Download(predownload.url, DownloadOptions.pack(predownload.options), PreDownloadData.pack(predownload.data))


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
        for download in self.downloads:
            download.pause()
            download.wait() # TODO: Upgrade wait to max the one longest thread's wait of all threads, not sum of all

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

    @Slot(str) # PySide2's Signal doesn't handle such big number, to avoid overflowing we use string
    def refresh(self, id):
        id = int(id)
        for row, download in enumerate(self.downloads):
            if download.id == id:
                self.dataChanged.emit(self.index(row, DownloadModel.FIRST_COLUMN, QModelIndex()), self.index(row, DownloadModel.LAST_COLUMN, QModelIndex()))
                break

    def add_download(self, download):
        self.beginInsertRows(QModelIndex(), len(self.downloads), len(self.downloads))
        download.updated.connect(self.refresh, Qt.QueuedConnection)
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
            return download.data.title

        elif role == 1:
            return download.data.uploader

        elif role == 2:
            return QDateTime.fromSecsSinceEpoch(download.data.duration).toString("mm:ss")

        elif role == 3:
            return download.progress

        elif role == 4:
            return download.data.thumbnail

        elif role == 5:
            return download.options

        return None


class DownloadManager(QObject):
    def __init__(self):
        super(DownloadManager, self).__init__(None)
        self.predownload_model = PreDownloadModel()
        self.download_model = DownloadModel()
        self.logger = create_logger(__name__)

    @Slot(str, "QVariantMap")
    def predownload(self, url, options):
        predownload = PreDownload(url, options)
        self.predownload_model.add_predownload(predownload)
        predownload.collect_info()

    @Slot()
    def download(self):
        self.logger.info("Downloading {items} items".format(items=len(self.predownload_model.predownloads)))

        for predownload in self.predownload_model.predownloads:
            download = Download.fromPreDownload(predownload)
            self.download_model.add_download(download)
            download.start()

        self.predownload_model.clear()

    def setQMLContext(self, engine):
        engine.rootContext().setContextProperty("downloadModel", self.download_model)
        engine.rootContext().setContextProperty("predownloadModel", self.predownload_model)
