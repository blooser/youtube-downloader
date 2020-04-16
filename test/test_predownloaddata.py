import sys
import os
import os.path
import unittest
import pickle

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader import PreDownloadData


class PreDownloadDataTest(unittest.TestCase):
    
    def setUp(self):        
        self.data = {
                "title": "TestTitle",
                "uploader": "anonymous",
                "thumbnail": "Empty",
                "duration": 100
        }
        
    def test_predownloadDataPackAndUnpack(self):
        predownload_data = PreDownloadData()
        predownload_data.collect_info(self.data)
        
        packed = PreDownloadData.pack(predownload_data)
        self.assertTrue(isinstance(packed, dict))
        
        expected_keys = ["title", "uploader", "thumbnail", "duration"]
        for key in packed.keys():
            self.assertTrue(key in expected_keys)
        
        unpacked = PreDownloadData.unpack(packed)
        self.assertEqual(unpacked.title, predownload_data.title)
        self.assertEqual(unpacked.uploader, predownload_data.uploader)
        self.assertEqual(unpacked.thumbnail, predownload_data.thumbnail)
        self.assertEqual(unpacked.duration, predownload_data.duration)


if __name__ == "__main__":
    unittest.main()
