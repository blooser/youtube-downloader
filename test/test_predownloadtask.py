import sys
import os.path
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader import PreDownloadTask, PreDownload

class PreDownloadTest(unittest.TestCase):
    
    def setUp(self):
        self.options = {
                "type": "mp3",
                "output_path": "/foo/bar/path"
        }
    
    def test_preDownloadCollectsInfoFromURL(self):
        url = "https://www.youtube.com/watch?v=4a2C4keyL7I"
        predownload_task = PreDownloadTask(url)
        predownload = PreDownload(url, self.options)
        predownload_task.communication.progress.connect(predownload.collect_info)

        predownload_task.run()

        self.assertTrue(predownload.title)
        self.assertTrue(predownload.uploader)
        self.assertTrue(predownload.thumbnail)
        self.assertTrue(predownload.duration)


if __name__ == "__main__":
    unittest.main()
