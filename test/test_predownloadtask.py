import sys
import os.path
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader import PreDownloadTask, PreDownload
from PySide2.QtCore import Qt

class PreDownloadTest(unittest.TestCase):
    
    def setUp(self):
        self.options = {
                "file_format": "mp3",
                "output_path": "/foo/bar/path"
        }
    
    def test_preDownloadCollectsInfoFromURL(self):
        url = "https://www.youtube.com/watch?v=4a2C4keyL7I"
        predownload_task = PreDownloadTask(url)
        predownload = PreDownload(url, self.options)
        predownload_task.collected_info.connect(predownload.collect_info, Qt.DirectConnection)

        predownload_task.start()
        while predownload_task.isRunning():
            continue

        self.assertEqual(predownload.title, "Fall Out Boy - Centuries (LEXIM Remix)")
        self.assertEqual(predownload.uploader, "Trap Boost")
        self.assertTrue(predownload.thumbnail)
        self.assertEqual(predownload.duration, 262)


if __name__ == "__main__":
    unittest.main()
