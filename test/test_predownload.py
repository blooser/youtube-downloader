import sys
import os
import os.path
import unittest
import pickle

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader import PreDownload, DownloadOptions

class PreDownloadTest(unittest.TestCase):

    def setUp(self):
        self.url = "https://www.youtube.com/watch?v=xSUQcQYgQCY"
        self.options = {
                "file_format": "mp3",
                "output_path": "/foo/bar/path1"
        }
        
        self.data = {
                "title": "Test",
                "uploader": "Me",
                "thumbnail": "/foo/bar/path1",
                "duration": 250
        }
        
    def test_preDownloadPackAndUnpack(self):
        predownload = PreDownload(self.url, self.options)
        predownload.ready = True
        predownload.data.collect_info(self.data)
        
        packed = PreDownload.pack(predownload)
        self.assertTrue(isinstance(packed, dict))
        expected_keys = ["url", "ready", "data", "options"]
        for key in packed.keys():
            self.assertTrue(key in expected_keys)
            
        unpacked = PreDownload.unpack(packed)
        self.assertEqual(unpacked.url, self.url)
        self.assertEqual(unpacked.ready, True)
        self.assertEqual(unpacked.options, DownloadOptions(self.options))
        self.assertEqual(unpacked.data.title, self.data["title"])
        self.assertEqual(unpacked.data.uploader, self.data["uploader"])
        self.assertEqual(unpacked.data.thumbnail, self.data["thumbnail"])
        self.assertEqual(unpacked.data.duration, self.data["duration"])
