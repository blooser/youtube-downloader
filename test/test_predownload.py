import sys
import os
import os.path
import unittest
import pickle

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader import PreDownload

class PreDownloadTest(unittest.TestCase):
    
    def test_preDownloadSerialization(self):
        data = {
                "title": "TestTitle",
                "uploader": "anonymous",
                "thumbnail": "Empty",
                "duration": 100
        }
        
        options = {
                "type": "mp3",
                "output_path": "/foo/bar/path"
        }
        
        tmp_filename = "predownload_test_pickle"
        predownload = PreDownload("https://www.youtube.com/watch?v=3L65PG_eZFg", options)
        predownload.collect_info(data)
        
        with open(tmp_filename, "wb") as f:
            pickle.dump(predownload, f)

        self.assertTrue(os.path.isfile(tmp_filename))

        with open(tmp_filename, "rb") as f:
            unpickled_predownload = pickle.load(f)
        
        self.assertEqual(unpickled_predownload.title, data["title"])    
        self.assertEqual(unpickled_predownload.uploader, data["uploader"])
        self.assertEqual(unpickled_predownload.thumbnail, data["thumbnail"])
        self.assertEqual(unpickled_predownload.duration, data["duration"])
        self.assertEqual(unpickled_predownload.download_options.type, "mp3")
        self.assertEqual(unpickled_predownload.download_options.output_path, "/foo/bar/path")
        
        os.remove(tmp_filename) 
        self.assertFalse(os.path.isfile(tmp_filename))


if __name__ == "__main__":
    unittest.main()
