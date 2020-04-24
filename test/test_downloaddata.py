import sys
import os
import os.path
import unittest
import pickle

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader import DownloadData


class DownloadTest(unittest.TestCase):

    def setUp(self):        
        self.data = {
                "title": "test",
                "uploader": "test1",
                "uploader_url": "/foo/bar/uploader",
                "thumbnail": "None",
                "duration": 60,
        }
            
    def test_downloadPackAndUnpackData(self):   
        download_data = DownloadData(self.data)
        
        packed = DownloadData.pack(download_data)
        self.assertTrue(isinstance(packed, dict))
        expected_keys = ["title", "uploader", "uploader_url",  "thumbnail", "duration"]
        for key in packed.keys():
            self.assertTrue(key in expected_keys)
            
        unpacked = DownloadData.unpack(packed)
        self.assertEqual(unpacked.title, download_data.title)
        self.assertEqual(unpacked.uploader, download_data.uploader)
        self.assertEqual(unpacked.uploader_url, download_data.uploader_url)
        self.assertEqual(unpacked.thumbnail, download_data.thumbnail)
        self.assertEqual(unpacked.duration, download_data.duration)
            

if __name__ == "__main__":
    unittest.main()
