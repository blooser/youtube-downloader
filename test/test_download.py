import sys
import os
import os.path
import unittest
import pickle

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader import Download


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
        
