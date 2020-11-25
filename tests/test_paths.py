import sys
import os.path
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader import paths

class DownloaProgressTest(unittest.TestCase):

    def test_pathsRetunsNewExtension(self):
        self.assertEqual(paths.new_extension("file.mp3", "flac"), "file.flac")

    def test_pathsReturnsFileType(self):
        data = [
            {
                "file": "file.mp3",
                "type": "audio"
            },
            {
                "file": "file.mp4",
                "type": "video"
            },
            {
                "file": "file.flac",
                "type": "audio"
            },
            {
                "file": "file.webm",
                "type": "video"
            }
        ]

        for item in data:
            self.assertEqual(paths.get_file_type(item["file"]), item["type"])

    def test_pathsReturnCleanPath(self): 
        qpaths = paths.QPaths()
        url = os.path.join(paths.FILE_PREFIX, "/foo/bar/path")
        self.assertEqual(qpaths.cleanPath(url), "/foo/bar/path")
                            
        url = "https:///server/path/foo"
        self.assertEqual(qpaths.cleanPath(url), "/server/path/foo")

    def test_pathsReturnPathType(self):
        qpaths = paths.QPaths()

        file_path = "/foo/bar/path"
        self.assertEqual(qpaths.getPathType(file_path), "file")
        
        remote_path = "https:///server/path/foo"
        self.assertEqual(qpaths.getPathType(remote_path), "remote")


if __name__ == "__main__":
    unittest.main()
