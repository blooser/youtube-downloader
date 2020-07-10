import sys
import os.path
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader.download import PreDownloadTask, DownloadData


class PreDownloadTaskTest(unittest.TestCase):
    
    def setUp(self):
        self.url = "https://www.youtube.com/watch?v=4a2C4keyL7I"
        
        self.options = {
                "file_format": "mp3",
                "output_path": "/foo/bar/path"
        }
            
    def test_preDownloadTaskCollectsInfoFromURL(self):
        predownload_task = PreDownloadTask(self.url)
        download_data = DownloadData()

        predownload_task.start()
        while predownload_task.isRunning():
            continue
        
        download_data.collect(predownload_task.info)
                      
        self.assertEqual(download_data._title, "Fall Out Boy - Centuries (LEXIM Remix)")
        self.assertEqual(download_data._uploader, "Trap Boost")
        self.assertTrue(download_data._thumbnail)
        self.assertEqual(download_data._duration, 262)
        self.assertTrue(download_data._upload_date)
        self.assertTrue(download_data._view_count)


if __name__ == "__main__":
    unittest.main()
