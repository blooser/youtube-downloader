import sys
import os.path
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader import PreDownload, Download, DownloadModel


class DownloadModelTest(unittest.TestCase):

    def setUp(self):
        self.config_path = "downloadmodelconfig"
        
        self.options = {
                "file_format": "mp3",
                "output_path": "/foo/bar/path"
        }
        
    def tearDown(self):
        if os.path.isfile(self.config_path):
            os.remove(self.config_path)

    def test_downloadModelSavesAndLoadData(self):
         pre_download = PreDownload("https://www.youtube.com/watch?v=3L65PG_eZFg",  self.options)
         download = Download.fromPreDownload(pre_download)
         download_model = DownloadModel(self.config_path)
         download_model.add_download(download)
         self.assertEqual(download_model.rowCount(), 1)
         
         del download_model
         second_download_model = DownloadModel(self.config_path)
         self.assertEqual(second_download_model.rowCount(), 1)


if __name__ == "__main__":
    unittest.main()
