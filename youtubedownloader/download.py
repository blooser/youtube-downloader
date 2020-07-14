from PySide2.QtCore import (
    QObject,
    QAbstractListModel,
    QFileInfo,
    QFile,
    QIODevice,
    QFileSystemWatcher,
    QModelIndex,
    QDateTime,
    QDate,
    QTime,
    QThread,
    QTimer,
    Qt,
    QSettings,
    QStandardPaths,
    Slot,
    Signal,
    Property

)
from PySide2.QtQml import (
    QQmlApplicationEngine,
    QQmlContext
)
from PySide2.QtNetwork import (
    QNetworkAccessManager,
    QNetworkReply,
    QNetworkRequest
)

import os.path
import pathlib
import pickle
import youtube_dl
import atexit
import urllib.request

from .logger import create_logger
from .settings import Settings
from .paths import Paths, FileExpect


def human_time(time: str) -> str:
    if not time:
        return "00:00"

    time = int(time)
    format = "hh:mm:ss" if time >= 60 * 60 else "mm:ss"

    return QTime.fromMSecsSinceStartOfDay(time * 1000).toString(format)


def human_date(date: str) -> str:
    if not date:
        return ""

    return QDate.fromString(date, "yyyyMMdd").toString(Qt.RFC2822Date)


def singleVideoIfPlaylist(url: str) -> str:
    index = url.find("&list=")

    if index != -1:
        url = url[:index]

    return url


class PreDownloadTask(QThread):
    collected_info = Signal(dict)

    def __init__(self, url: str):
        super(PreDownloadTask, self).__init__(None)
        self.url = url
        self.info = None
        self.error = None

    def __eq__(self, other):
        return self.url == other.url

    def run(self) -> None:
        try:
            with youtube_dl.YoutubeDL() as ydl:
                self.info = ydl.extract_info(self.url, download=False)

        except youtube_dl.utils.DownloadError as download_error:
            self.error = str(download_error)


class PreDownload(QObject):
    updated = Signal(str)

    def __init__(self, url: str, options: dict):
        super(PreDownload, self).__init__(None)

        self.status = "processing"
        self.id = hash(url)
        self.url = url
        self.destination_file = str()
        self.options = DownloadOptions(options)

        self.data = DownloadData()
        self.task = PreDownloadTask(self.url)

        self.task.finished.connect(self.handle_finished)

    def __eq__(self, other):
        return self.url == other.url and self.options == other.options

    def start(self) -> None:
        if self.task.error:
            self.task.error = None

        self.task.start()

    def stop(self) -> None:
        while self.task.isRunning(): # NOTE: Collecting data is usually fast, wait until processing and exit
            self.task.exit()

    def destination_file_exists(self) -> bool:
        return os.path.isfile(self.destination_file)

    def update(self) -> None:
        self.destination_file = os.path.join(self.options.output_path, Paths.new_extension(self.data.title, self.options.file_format))

        self.status = "ready" if not self.destination_file_exists() else "exists"

        if self.options.need_post_process():
            self.options.calc_post_process_file_size(self.data._duration)

        self.updated.emit(str(self.id))

    @Slot(int)
    def handle_finished(self) -> None:
        if self.task.info:
            if "is_live" in self.task.info and self.task.info["is_live"]:
                self.status = "ERROR: Unsupported: livestream"
                self.updated.emit(str(self.id))

            else:
                self.data.collect(self.task.info)
                self.update()

        if self.task.error:
            self.status = self.task.error
            self.updated.emit(str(self.id))

    @staticmethod
    def pack(predownload: QObject) -> dict:
        return {
            "url": predownload.url,
            "destination_file": predownload.destination_file,
            "status": predownload.status,
            "data": DownloadData.pack(predownload.data),
            "options": DownloadOptions.pack(predownload.options)
        }

    @staticmethod
    def unpack(data: dict) -> QObject:
        predownload = PreDownload(data["url"], data["options"])
        predownload.destination_file = data["destination_file"]
        predownload.status = data["status"]
        predownload.data = DownloadData.unpack(data["data"])
        return predownload


class PreDownloadModel(QAbstractListModel):
    COLUMNS: tuple = ("url", "destination_file", "status", "download_data", "options")
    FIRST_COLUMN: int = 0
    LAST_COLUMN: int = len(COLUMNS)

    sizeChanged = Signal(int)

    def __init__(self, config_path: str=""):
        super(PreDownloadModel, self).__init__(None)
        self.predownloads = []

        self.config_path = config_path if config_path else Settings.CONFIG_PATH

        self.load()

        self.rowsInserted.connect(lambda: self.sizeChanged.emit(len(self.predownloads)))
        self.rowsRemoved.connect(lambda: self.sizeChanged.emit(len(self.predownloads)))

        atexit.register(self.save)

    def __contains__(self, predownload):
        return predownload in self.predownloads

    @Property(int, notify=sizeChanged)
    def size(self):
        return len(self.predownloads)

    def save(self) -> None:
        settings = QSettings(self.config_path, QSettings.NativeFormat)

        settings.beginWriteArray("predownloads")
        for i in range(len(self.predownloads)):
            settings.setArrayIndex(i)
            settings.setValue("predownload", PreDownload.pack(self.predownloads[i]))
        settings.endArray()

    def load(self) -> None:
        settings = QSettings(self.config_path, QSettings.NativeFormat)

        size = settings.beginReadArray("predownloads")
        for i in range(size):
            settings.setArrayIndex(i)
            self.add_predownload(PreDownload.unpack(settings.value("predownload")))
        settings.endArray()

    def rowCount(self, index: QModelIndex=QModelIndex()) -> int:
        return len(self.predownloads)

    def roleNames(self, index: QModelIndex=QModelIndex()) -> dict:
        return {
            256: b"url",
            257: b"destination_file",
            258: b"status",
            259: b"download_data",
            260: b"options"
        }

    def index(self, row: int, column: int, parent: QModelIndex=QModelIndex()) -> QModelIndex:
        return self.createIndex(row, column, parent)

    def refresh(self, id: str) -> None:
        id = int(id)
        for row, predownload in enumerate(self.predownloads):
            if predownload.id == id:
                self.dataChanged.emit(self.index(row, PreDownloadModel.FIRST_COLUMN, QModelIndex()), self.index(row, PreDownloadModel.LAST_COLUMN, QModelIndex()))

    def add_predownload(self, predownload: PreDownload) -> None:
        self.beginInsertRows(QModelIndex(), len(self.predownloads), len(self.predownloads))
        predownload.updated.connect(self.refresh, Qt.QueuedConnection)
        self.predownloads.append(predownload)
        self.endInsertRows()

    def remove(self, status: str="*") -> None:
        if status == "*":
            self.beginResetModel()
            self.predownloads.clear()
            self.endResetModel()

        else:
            for row in range(len(self.predownloads)-1, -1, -1):
                if self.predownloads[row].status == status:
                    self.beginRemoveRows(QModelIndex(), row, row)
                    self.endRemoveRows()

            self.predownloads = [predownload for predownload in self.predownloads if predownload.status != status]

    @Slot(int)
    def remove_predownload(self, row: int) -> None:
        if row >= len(self.predownloads):
            return

        self.beginRemoveRows(QModelIndex(), row, row)
        self.predownloads[row].stop()
        self.predownloads.pop(row)
        self.endRemoveRows()

    def clear(self) -> None:
        self.beginResetModel()
        self.predownloads.clear()
        self.endResetModel()

    def data(self, index: QModelIndex, role: int): # NOTE: Returns QVariant
        if not index.isValid():
            return

        predownload = self.predownloads[index.row()]

        if role == 256:
            return predownload.url

        elif role == 257:
            return predownload.destination_file

        elif role == 258:
            return predownload.status

        elif role == 259:
            return predownload.data

        elif role == 260:
            return predownload.options

        return None

    def setData(self, index: QModelIndex, value, role: int) -> bool: # TODO: What type value is?
        if not index.isValid():
            return False

        row = index.row()
        predownload = self.predownloads[row]

        # NOTE: Do we want to add option for url changing?

        if role == 260:
            predownload.options.update(value.toVariant())
            predownload.update()
            self.dataChanged.emit(self.index(row, PreDownloadModel.FIRST_COLUMN, QModelIndex()), self.index(row, PreDownloadModel.LAST_COLUMN, QModelIndex()))
            return True

        return False


class DownloadData(QObject):
    def __init__(self, data: dict={}):
        super(DownloadData, self).__init__(None)
        self._title = str()
        self._uploader = str()
        self._uploader_url = str()
        self._thumbnail = str()
        self._duration = int()
        self._upload_date = str()
        self._view_count = int()

        if data:
            self.collect(data)

    @Property(str, constant=True)
    def title(self) -> str:
        return self._title

    @Property(str, constant=True)
    def uploader(self) -> str:
        return self._uploader

    @Property(str, constant=True)
    def uploaderUrl(self) -> str:
        return self._uploader_url

    @Property(str, constant=True)
    def thumbnail(self) -> str:
        return self._thumbnail

    @Property(str, constant=True)
    def duration(self) -> int:
        return human_time(self._duration)

    @Property(str, constant=True)
    def uploadDate(self) -> str:
        return human_date(self._upload_date)

    @Property(int, constant=True)
    def viewCount(self) -> int:
        return self._view_count

    @Slot(dict)
    def collect(self, info: dict) -> None:
        self._title = info["title"] if "title" in info else ""
        self._uploader = info["uploader"] if "uploader" in info else ""
        self._uploader_url = info["uploader_url"] if "uploader_url" in info else ""
        self._thumbnail = info["thumbnail"] if "thumbnail" in info else ""
        self._duration = int(info["duration"]) if "duration" in info and info["duration"] != "" else ""
        self._upload_date = info["upload_date"] if "upload_date" in info else ""
        self._view_count = int(info["view_count"]) if "view_count" in info and info["view_count"] != "" else ""

    @staticmethod
    def pack(download_data: QObject) -> dict:
        return {
            "title": download_data._title,
            "uploader": download_data._uploader,
            "uploader_url": download_data._uploader_url,
            "thumbnail": download_data._thumbnail,
            "duration": download_data._duration,
            "upload_date": download_data._upload_date,
            "view_count": download_data._view_count
        }

    @staticmethod
    def unpack(data: dict) -> QObject:
        download_data = DownloadData()
        download_data._title = data["title"]
        download_data._uploader = data["uploader"]
        download_data._uploader_url = data["uploader_url"]
        download_data._thumbnail = data["thumbnail"]
        download_data._duration = data["duration"]
        download_data._upload_date = data["upload_date"]
        download_data._view_count = data["view_count"]
        return download_data


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
    def downloadStatus(self) -> str:
        return self.status

    @Property(int, notify=changed)
    def downloadedBytes(self) -> str:
        return self.downloaded_bytes

    @Property(int, notify=changed)
    def totalBytes(self) -> str:
        return self.total_bytes

    @Property(str, notify=changed)
    def estimatedTime(self) -> str:
        return self.estimated_time

    @Property(str, notify=changed)
    def downloadSpeed(self) -> str:
        return self.speed

    def invalide(self) -> None:
        self.status = "no file"
        self.downloaded_bytes = 0

    @Slot(dict)
    def update(self, data: dict) -> None:
        if "status" in data:
            self.status = data["status"]

        if "downloaded_bytes" in data and data["downloaded_bytes"] != "":
            self.downloaded_bytes = int(data["downloaded_bytes"])

        if "total_bytes" in data and data["total_bytes"] != "":
            self.total_bytes = int(data["total_bytes"])

        if "_eta_str" in data:
            self.estimated_time = data["_eta_str"]

        if "_speed_str" in data:
            self.speed = data["_speed_str"]

        if "filename" in data:
            self.filename = data["filename"]

        self.changed.emit() # TODO: Maybe separated signal for each property?

    @staticmethod
    def pack(download_progress: QObject) -> dict:
        return {
            "status": download_progress.status,
            "downloaded_bytes": download_progress.downloaded_bytes,
            "total_bytes": download_progress.total_bytes,
            "estimated_time": download_progress.estimated_time,
            "speed": download_progress.speed,
            "filename": download_progress.filename
        }

    @classmethod
    def unpack(cls, data: dict) -> QObject:
        download_progress = cls()
        download_progress.status = data["status"]
        download_progress.downloaded_bytes = data["downloaded_bytes"]
        download_progress.total_bytes = data["total_bytes"]
        download_progress.estimated_time = data["estimated_time"]
        download_progress.speed = data["speed"]
        download_progress.filename = data["filename"]
        return download_progress


class DownloadOptions(QObject):
    OUTPUT_FILE: str = os.path.join("{output_path}", "%(title)s.%(ext)s")

    TEMPLATES: dict = {
        "mp4": {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4"
        },

        "webm": {
            "format": "bestvideo[ext=webm]+bestaudio[ext=webm]/webm"
        },

        "mkv": {
            "format": "bestvideo[ext=webm]+bestaudio[ext=m4a]/mkv"
        },

        "m4a": {
            "format": "bestaudio[ext=m4a]/m4a"
        },

        "flac": {
            "format": "bestaudio/best",
            "postprocessors": [{
               "key": 'FFmpegExtractAudio',
               "preferredcodec": 'flac',
            }]
        },

        "mp3": {
            "format": "bestaudio/best",
            "postprocessors": [{
               "key": 'FFmpegExtractAudio',
               "preferredcodec": 'mp3',
               "preferredquality": "320",
            }]
        },

        "wav": {
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": 'FFmpegExtractAudio',
                "preferredcodec": 'wav',
            }]
        }
    }

    changed = Signal()

    def __init__(self, options):
        super(DownloadOptions, self).__init__(None)
        self.file_format = options["file_format"]
        self.output_path = options["output_path"]
        self.ydl_opts = {
            "format": "bestaudio/best"
        }

        self.post_process_file_size = int(options["post_process_file_size"]) if "post_process_file_size" in options else 1

    def __eq__(self, other):
        return self.file_format == other.file_format and self.output_path == other.output_path

    @Property(str, notify=changed)
    def fileFormat(self) -> str:
        return self.file_format

    @Property(str, notify=changed)
    def outputPath(self) -> str:
        return self.output_path

    def calc_post_process_file_size(self, duration: int) -> None:
        if self.file_format == "mp3":
            self.post_process_file_size = (((320 * duration)/8) * 1000)
        else:
            self.post_process_file_size = 1 # TODO: Try to calculate other file formats size

    def to_ydl_opts(self) -> dict:
        template = self.ydl_opts
        template.update({"outtmpl": DownloadOptions.OUTPUT_FILE.format(output_path=self.output_path)})
        template.update(DownloadOptions.TEMPLATES[self.file_format])
        return template

    def need_post_process(self) -> bool:
        return self.file_format in ["flac", "mp3", "wav"]

    def update(self, options: dict) -> None:
        if "file_format" in options:
            self.file_format = options["file_format"]

        if "output_path" in options:
            self.output_path = options["output_path"]

        self.changed.emit()

    @staticmethod
    def pack(download_options: QObject) -> dict:
        return {
            "file_format": download_options.file_format,
            "output_path": download_options.output_path,
            "post_process_file_size": download_options.post_process_file_size
        }

    @staticmethod
    def unpack(data: dict) -> QObject:
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
        self.error = None

        self.ydl_opts["progress_hooks"] = [self.process]

        self.download_post_process = DownloadPostProcess()

        self.file_expect = FileExpect()
        self.post_process_file = str()

        self.post_process_started.connect(lambda: self.file_expect.observe(self.post_process_file))
        self.file_expect.file_exists.connect(self.download_post_process.track)

        self.download_post_process.bytes_processed.connect(lambda bytes: self.progress.emit({"downloaded_bytes": bytes}), Qt.QueuedConnection)
        self.download_post_process.started.connect(lambda: self.progress.emit({"status": "converting to {0}".format(self.options.file_format),
                                                                                         "total_bytes": self.options.post_process_file_size}), Qt.QueuedConnection)
    def process(self, data: dict) -> None:
        if self.paused:
            raise ValueError()

        if data["status"] == "downloading":
            data.update({"status": "downloading {what}".format(what=Paths.get_file_type(data["filename"]))})

        if self.options.need_post_process() and data["status"] == "finished":
            self.post_process_file = os.path.join(self.options.output_path, Paths.new_extension(data["filename"], self.options.file_format))
            self.post_process_started.emit() # NOTE: Because we can't start timers from another thread

        else:
            self.progress.emit(data)

    def run(self) -> None:
        try:
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([self.url])
        except youtube_dl.utils.DownloadError as download_error:
            self.error = str(download_error)


class Download(QObject):
    updated = Signal(str)

    def __init__(self, url: str, options: dict, data: dict):
        super(Download, self).__init__(None)
        self.id = hash(url)
        self.url = url

        self.options = DownloadOptions(options)
        self.data = DownloadData(data)
        self.progress = DownloadProgress()
        self.task = DownloadTask(self.url, self.options)

        self.destination_file = os.path.join(self.options.output_path, Paths.new_extension(self.data.title, self.options.file_format))

        self.task.progress.connect(self.update, Qt.QueuedConnection)
        self.task.finished.connect(self.handle_finished)


    def __eq__(self, other):
        return self.url == other.url and self.options == other.options

    def check_if_redownload_needed(self) -> None:
        if not os.path.isfile(self.destination_file) and self.progress.status == "finished":
            self.progress.invalide()

    def start(self) -> None:
        if self.running():
            return

        if self.task.paused:
            self.task.paused = False

        self.update({"status": "queued"})
        self.task.start()

    def pause(self) -> None:
        if self.task.isRunning():
            self.task.paused = True

    def running(self) -> bool:
        return self.task.isRunning()

    @Slot(int)
    def handle_finished(self) -> None:
        if self.task.paused:
            self.update({"status": "paused"})
            return

        if self.task.error:
            self.update({"status": self.task.error})
            return

        self.update({"status": "finished"})

    @Slot(str)
    def update(self, progress: dict) -> None:
        self.progress.update(progress)
        self.updated.emit(str(self.id))

    @staticmethod
    def pack(download: QObject) -> dict:
        return {
            "url": download.url,
            "destination_file": download.destination_file,
            "options": DownloadOptions.pack(download.options),
            "data": DownloadData.pack(download.data),
            "progress": DownloadProgress.pack(download.progress),
        }

    @staticmethod
    def unpack(data: dict) -> QObject:
        download =  Download(data["url"], data["options"], data["data"])
        download.progress = DownloadProgress.unpack(data["progress"])
        download.check_if_redownload_needed()
        return download

    @classmethod
    def fromPreDownload(cls: QObject, predownload: QObject) -> QObject:
        return Download(predownload.url, DownloadOptions.pack(predownload.options), DownloadData.pack(predownload.data))


class DownloadPostProcess(QObject):
    bytes_processed = Signal(int)
    started = Signal()

    def __init__(self):
        super(DownloadPostProcess, self).__init__(None)

        self.file_watcher = QFileSystemWatcher()
        self.file_watcher.fileChanged.connect(self.read_bytes)

        self.logger = create_logger(__name__)

    @Slot(str)
    def track(self, url: str) -> None:
        track_success = self.file_watcher.addPath(url)
        self.logger.info("Track {file} success={success}".format(file=url, success=track_success))
        self.started.emit()

    @Slot(str)
    def read_bytes(self, path: str) -> None:
        bytes = QFileInfo(path).size()
        self.bytes_processed.emit(bytes)
        self.logger.debug("Read {bytes} bytes".format(bytes=bytes))


class DownloadModel(QAbstractListModel):
    COLUMNS: tuple = ("url", "destination_file", "download_data", "progress", "options")
    FIRST_COLUMN: int = 0
    LAST_COLUMN: int = len(COLUMNS)

    sizeChanged = Signal(int)

    def __init__(self, config_path: str=""):
        super(DownloadModel, self).__init__(None)
        self.downloads = []

        self.config_path = config_path if config_path else Settings.CONFIG_PATH

        self.load()

        self.rowsInserted.connect(lambda: self.sizeChanged.emit(len(self.downloads)))
        self.rowsRemoved.connect(lambda: self.sizeChanged.emit(len(self.downloads)))

        atexit.register(self.pause_and_save)

    def pause_and_save(self) -> None:
        running_downloads = [True] * len(self.downloads)

        for download in self.downloads:
            download.pause()

        while any(running_downloads):
            for index, download in enumerate(self.downloads):
                running_downloads[index] = download.running()

        self.save()

    def __contains__(self, download):
        return download in self.downloads

    @Property(int, notify=sizeChanged)
    def size(self) -> int:
        return len(self.downloads)

    def save(self) -> None:
        settings = QSettings(self.config_path)

        settings.beginWriteArray("downloads")
        for i in range(len(self.downloads)):
            settings.setArrayIndex(i)
            settings.setValue("download", Download.pack(self.downloads[i]))
        settings.endArray()

    def load(self) -> None:
        settings = QSettings(self.config_path)

        size = settings.beginReadArray("downloads")
        for i in range(size):
            settings.setArrayIndex(i)
            self.add_download(Download.unpack(settings.value("download")))
        settings.endArray()

    def rowCount(self, index: QModelIndex=QModelIndex()) -> int:
        return len(self.downloads)

    def headerData(self, col: int, orientation: int, role: int):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return DownloadModel.COLUMNS[col]

        return None

    def roleNames(self, index: QModelIndex=QModelIndex()) -> dict:
        return {
            256: b"url",
            257: b"destination_file",
            258: b"download_data",
            259: b"progress",
            260: b"options"
        }

    def clear(self) -> None:
        self.beginResetModel()
        self.downloads.clear()
        self.endResetModel()

    def index(self, row: int, column: int, parent: QModelIndex=QModelIndex()) -> QModelIndex:
        return self.createIndex(row, column, parent)

    @Slot(str) # PySide2's Signal doesn't handle such big number, to avoid overflowing we use string
    def refresh(self, id: str) -> None:
        id = int(id)
        for row, download in enumerate(self.downloads):
            if download.id == id:
                self.dataChanged.emit(self.index(row, DownloadModel.FIRST_COLUMN, QModelIndex()), self.index(row, DownloadModel.LAST_COLUMN, QModelIndex()))

    def add_download(self, download: QObject) -> None:
        self.beginInsertRows(QModelIndex(), len(self.downloads), len(self.downloads))
        download.updated.connect(self.refresh, Qt.QueuedConnection)
        self.downloads.append(download)
        self.endInsertRows()

    @Slot(int)
    def remove_download(self, row: int) -> None:
        if row >= len(self.downloads):
            return

        if self.downloads[row].running():
            removable_download = self.downloads[row]
            removable_download.task.finished.connect(lambda: self.remove_download(self.downloads.index(removable_download)))
            removable_download.pause()
            return

        self.beginRemoveRows(QModelIndex(), row, row)
        self.downloads.pop(row)
        self.endRemoveRows()

    @Slot(int)
    def redo(self, row: int) -> None:
        self.downloads[row].start()

    @Slot(int)
    def pause(self, row: int) -> None:
        self.downloads[row].pause()

    def data(self, index: QModelIndex, role: int):
        if not index.isValid():
            return None

        download = self.downloads[index.row()]

        if role == 256:
            return download.url

        elif role == 257:
            return download.destination_file

        elif role == 258:
            return download.data

        elif role == 259:
            return download.progress

        elif role == 260:
            return download.options

        return None


# NOTE: PreDownload and Download have same __eq__ operator, there is no need to initialize Download and PreDownload and all its variables for duplicates checking
# TODO: Implement find duplicate position logic to notify user where duplicate already is
class DownloadDuplicateChecker(object):
    def __init__(self, url: str, options: dict):
        self.url = url
        self.options = DownloadOptions(options)

    def __eq__(self, other):
        return self.url == other.url and self.options == other.options


class DownloadManager(QObject):
    # NOTE: These signals are used in QML
    preDownloadRequest = Signal(str, arguments=["url"])
    newDownload = Signal("QVariant", arguments=["download"])

    def __init__(self, config_path: str=""):
        super(DownloadManager, self).__init__(None)
        self.predownload_model = PreDownloadModel(config_path)
        self.download_model = DownloadModel(config_path)
        self.logger = create_logger(__name__)

    @Slot(str, "QVariantMap")
    def predownload(self, url: str, options: dict) -> None:
        if url:
            predownload = PreDownload(singleVideoIfPlaylist(url), options)
            self.predownload_model.add_predownload(predownload)
            predownload.start()

    @Slot()
    def download(self) -> None:
        for predownload in [ready_predownload for ready_predownload in self.predownload_model.predownloads if ready_predownload.status == "ready"]:
            if predownload.status == "ready":
                download = Download.fromPreDownload(predownload)
                self.download_model.add_download(download)
                self.newDownload.emit(PreDownload.pack(predownload))
                download.start()

        self.predownload_model.remove("ready")

    @Slot(str, "QVariantMap", result="bool")
    def exists(self, url: str, options: dict) -> bool:
        duplicate_checker = DownloadDuplicateChecker(url, options)
        return duplicate_checker in self.predownload_model or duplicate_checker in self.download_model

    def setQMLContext(self, engine: QQmlApplicationEngine) -> None:
        engine.rootContext().setContextProperty("downloadModel", self.download_model)
        engine.rootContext().setContextProperty("predownloadModel", self.predownload_model)


class FileDownload(QObject):
    def __init__(self, manager: QNetworkAccessManager, url: str, output_url: str):
        super(FileDownload, self).__init__(None)

        request = QNetworkRequest(url)

        self.output_url =  output_url
        self.output = QFile(self.output_url)

        self.logger = create_logger(__name__)
        if not self.output.open(QIODevice.WriteOnly):
            self.logger.info("Could not open: {url}".format(url=self.output_url))
            return

        self.current_download = manager.get(request)
        self.current_download_progress = FileDownloadProgress()
        self.current_download.downloadProgress.connect(self.current_download_progress.update)
        self.current_download.readyRead.connect(self.saveFile)
        self.current_download.finished.connect(self.download_finished)

    @Property(str, constant=True)
    def outputUrl(self) -> str:
        return self.output_url

    @Property(QObject, constant=True)
    def progress(self) -> QObject:
        return self.current_download_progress

    @Slot()
    def saveFile(self) -> None:
        self.output.write(self.current_download.readAll())

    @Slot()
    def download_finished(self) -> None:
        self.output.close()


class FileDownloadProgress(QObject):
    updated = Signal()

    def __init__(self):
        super(FileDownloadProgress, self).__init__(None)

        self.read_bytes = int()
        self.total_bytes = int()

    @Property(int, notify=updated)
    def readBytes(self) -> None:
        return self.read_bytes

    @Property(int, notify=updated)
    def totalBytes(self) -> None:
        return self.total_bytes

    @Slot(int, int)
    def update(self, read_bytes: int, total_bytes: int) -> None:
        self.read_bytes = read_bytes
        self.total_bytes = total_bytes
        self.updated.emit()


class FileDownloader(QObject):
    current_download_changed = Signal()

    def __init__(self):
        super(FileDownloader, self).__init__(None)

        self.manager = QNetworkAccessManager()
        self.current_download = None

    @Property("QVariant", notify=current_download_changed)
    def currentDownload(self) -> None:
        return self.current_download

    @Slot()
    def clear(self) -> None:
        self.current_download = None
        self.current_download_changed.emit()

    @Slot(str, str)
    def download(self, url: str, output_url: str) -> None:
        self.current_download = FileDownload(self.manager, url, output_url)
        self.current_download_changed.emit()
