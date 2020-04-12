import sys
import os
import os.path
import unittest
import pickle

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader import PreDownload


class PreDownloadTest(unittest.TestCase):
    
    def setUp(self):
        self.yt_url = "https://www.youtube.com/watch?v=3L65PG_eZFg"
        
        self.data = {
                "title": "TestTitle",
                "uploader": "anonymous",
                "thumbnail": "Empty",
                "duration": 100
        }
        
        self.options = {
                "file_format": "mp3",
                "output_path": "/foo/bar/path"
        }
    
    
    def test_predownloadPackAndUnpack(self):
        predownload = PreDownload(self.yt_url, self.options)
        predownload.collect_info(self.data)
        
        packed = PreDownload.pack(predownload)
        self.assertTrue(isinstance(packed, dict))
        expected_keys = ["ready", "id", "url", "title", "uploader", "thumbnail", "duration", "download_options"]
        for key in packed.keys():
            self.assertTrue(key in expected_keys)

        unpacked = PreDownload.unpack(packed)
        self.assertEqual(predownload.id, unpacked.id)
        self.assertEqual(predownload.ready, unpacked.ready)
        self.assertEqual(predownload.url, unpacked.url)
        self.assertEqual(predownload.title, unpacked.title)
        self.assertEqual(predownload.uploader, unpacked.uploader)
        self.assertEqual(predownload.thumbnail, unpacked.thumbnail)
        self.assertEqual(predownload.duration, unpacked.duration)
        self.assertEqual(predownload.download_options, unpacked.download_options)
        

if __name__ == "__main__":
    unittest.main()
