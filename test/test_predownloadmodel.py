import sys
import os.path
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader import PreDownload, PreDownloadModel, DownloadOptions

class PreDownloadModelTest(unittest.TestCase):
    
    
    def setUp(self):
        self.yt_url = "https://www.youtube.com/watch?v=3L65PG_eZFg"
        
        self.config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "predownloadmodelconfig")
        
        self.options = {
                "file_format": "mp3",
                "output_path": "/foo/bar/path"
        }
        
        
    def tearDown(self):
        if os.path.isfile(self.config_path):
            os.remove(self.config_path)


    def test_preDownloadModelSavesAndLoadData(self):
            if os.path.isfile(self.config_path):
                os.remove(self.config_path)
        
            predownload = PreDownload(self.yt_url, self.options)
            predownload_model = PreDownloadModel(self.config_path)
            predownload_model.add_predownload(predownload)
            self.assertEqual(predownload_model.rowCount(), 1)
            
            del predownload_model
            second_predownload_model = PreDownloadModel(self.config_path)
            self.assertEqual(second_predownload_model.rowCount(), 1)
            
            second_predownload = second_predownload_model.predownloads[0]
            self.assertEqual(second_predownload.download_options, DownloadOptions(self.options))
            self.assertEqual(second_predownload.url, self.yt_url )


if __name__ == "__main__":
    unittest.main()
