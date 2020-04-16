import sys
import os
import os.path
import unittest
import pickle

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader import PreDownload

class PreDownloadTest(unittest.TestCase):

    def setUp(self):
        self.url = "https://www.youtube.com/watch?v=xSUQcQYgQCY"
        self.options = {
                "file_format": "mp3",
                "output_path": "/foo/bar/path1"
        }
        
        self.info = {
                "title": "Test",
                "uploader": "Me",
                "thumbnail": "/foo/bar/path1",
                "duration": 250
        }
        
    def test_preDownloadPackAndUnpack(self):
        predownload = PreDownload(self.url, self.options)
        predownload.ready = True
        predownload.data.collect_info(self.info)
        
        packed = PreDownload.pack(predownload)
        self.assertTrue(isinstance(packed, dict))
        expected_keys = ["url", "ready", "data", "options"]
        for key in packed.keys():
            self.assertTrue(key in expected_keys)
            
        unpacked = PreDownload.unpack(packed)
        self.asserEqual(unpacked.url, self.url)
        self.asserEqual(unpacked.ready, True)
        self.asserEqual(unpacked.options, self.options)
        self.asserEqual(unpacked.info.title, self.options["title"])
        self.asserEqual(unpacked.info.uploader, self.options["uploader"])
        self.asserEqual(unpacked.info.thumbnail, self.options["thumbnail"])
        self.asserEqual(unpacked.info.duration, self.options["duration"])
