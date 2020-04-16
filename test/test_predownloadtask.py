import sys
import os.path
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader import PreDownloadTask, PreDownloadData
from PySide2.QtCore import Qt

class PreDownloadTaskTest(unittest.TestCase):
    
    def setUp(self):
        self.url = "https://www.youtube.com/watch?v=4a2C4keyL7I"
        
        self.options = {
                "file_format": "mp3",
                "output_path": "/foo/bar/path"
        }
            
    def test_preDownloadTaskCollectsInfoFromURL(self):
        predownload_task = PreDownloadTask(self.url)
        predownload_data = PreDownloadData()
        predownload_task.collected_info.connect(predownload_data.collect_info, Qt.DirectConnection)

        predownload_task.start()
        while predownload_task.isRunning():
            continue

        self.assertEqual(predownload_data.title, "Fall Out Boy - Centuries (LEXIM Remix)")
        self.assertEqual(predownload_data.uploader, "Trap Boost")
        self.assertTrue(predownload_data.thumbnail)
        self.assertEqual(predownload_data.duration, 262)


if __name__ == "__main__":
    unittest.main()
