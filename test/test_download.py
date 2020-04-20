import sys
import os
import os.path
import unittest
import pickle

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader import Download, PreDownload


class DownloadTest(unittest.TestCase):
    def setUp(self):
        self.url = "https://www.youtube.com/watch?v=_mVW8tgGY_w"
        
        self.options = {
            "file_format": "mp3",
            "output_path": "/foo/bar/path"
        }
        
        self.data = {
                "title": "test",
                "uploader": "test1",
                "thumbnail": "None",
                "duration": 60,
        }
            
    def test_downloadEqOperator(self):
        download1 = Download(self.url, self.options, self.data)
        download2 = Download(self.url, self.options, self.data)
        self.assertEqual(download1, download2)
        
        options_with_different_file_format = self.options
        options_with_different_file_format.update({"file_format": "mp4"})
        download3 = Download(self.url, options_with_different_file_format, self.data)
        self.assertNotEqual(download1, download3)
        
    def test_downloadPackAndUnPack(self):
        download = Download(self.url, self.options, self.data)
        
        packed = Download.pack(download)
        self.assertTrue(isinstance(packed, dict))
        
        expected_keys = ["url", "options", "data", "progress"]
        for key in packed.keys():
            self.assertTrue(key in expected_keys)
            
        unpacked = Download.unpack(packed)
        self.assertEqual(unpacked.url, download.url)
        self.assertEqual(unpacked.options, download.options)
        self.assertEqual(unpacked.data.title, download.data.title)
        self.assertEqual(unpacked.data.uploader, download.data.uploader)
        self.assertEqual(unpacked.data.thumbnail, download.data.thumbnail)
        self.assertEqual(unpacked.data.duration, download.data.duration)
        
                    
    def test_downloadInitializesByPreDownload(self):
        data = {
                "title": "test1",
                "uploader": "admin",
                "thumbnail": "None",
                "duration": 60
        }
        
        predownload = PreDownload(self.url, self.options)
        predownload.data.collect(data)
        
        download = Download.fromPreDownload(predownload)
        self.assertEqual(download.url, predownload.url)
        self.assertEqual(download.options, predownload.options)
        self.assertEqual(download.data.title, predownload.data.title)
        self.assertEqual(download.data.uploader, predownload.data.uploader)
        self.assertEqual(download.data.thumbnail, predownload.data.thumbnail)
        self.assertEqual(download.data.duration, predownload.data.duration)
        
