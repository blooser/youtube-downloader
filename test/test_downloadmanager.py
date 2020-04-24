import sys
import os.path
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader import DownloadManager, Download, PreDownload


class DownloadManagerTest(unittest.TestCase):
    
    def setUp(self):
        self.config_path = "testdownload_manager"
        
        self.url = "https://www.youtube.com/watch?v=wqeJ5Vkb6JE"
        
        self.options = {
                "file_format":  "mp4",
                "output_path": "/foo/bar/path"
        }
        
        # NOTE: Not necessary for __eq__
        self.data = {
                "title": "",
                "uploader": "",
                "uploader_url": "",
                "thumbnail": "",
                "duration": ""
        }
        
    def tearDown(self):
        if os.path.isfile(self.config_path):
            os.remove(self.config_path)
        
    def test_downloadManagerFindsDuplicates(self):
        download_manager = DownloadManager(self.config_path)
        
        predownload = PreDownload(self.url, self.options)
        download_manager.predownload_model.predownloads.append(predownload)
        self.assertTrue(download_manager.exists(self.url, self.options))
        download_manager.predownload_model.predownloads.clear()
        self.assertFalse(download_manager.exists(self.url, self.options))

        download = Download(self.url, self.options, self.data)
        download_manager.download_model.downloads.append(download)
        self.assertTrue(download_manager.exists(self.url, self.options))
        download_manager.download_model.downloads.clear()
        self.assertFalse(download_manager.exists(self.url, self.options))
