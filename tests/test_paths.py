import sys
import os.path
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader import Paths

class DownloaProgressTest(unittest.TestCase):
        
    def test_pathsReturnCleanPath(self):
        paths = Paths()
        
        url = os.path.join(Paths.FILE_PREFIX, "/foo/bar/path")
        self.assertEqual(paths.cleanPath(url), "/foo/bar/path")
                            
        url = "https:///server/path/foo"
        self.assertEqual(paths.cleanPath(url), "/server/path/foo")

    def test_pathsReturnPathType(self):
        paths = Paths()
        
        file_path = "/foo/bar/path"
        self.assertEqual(paths.getPathType(file_path), "file")
        
        remote_path = "https:///server/path/foo"
        self.assertEqual(paths.getPathType(remote_path), "remote")
