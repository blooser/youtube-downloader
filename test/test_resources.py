import sys
import os
import os.path
import unittest
import pickle

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader import Resources, Paths


class ResourcesTest(unittest.TestCase):
    
    def test_resourcesCollectsIcons(self):
        resources = Resources()
        
        resources_icons = resources.icon_paths()
        self.assertEqual(len(resources_icons), 11)
        
        expected_keys = ["download", "delete", "plus", "folder", "redo", "pause", "youtube", "arrowDown", "check", "dizzy", "eye", "calendar"]
        for key in resources_icons.keys():
                self.assertTrue(key in expected_keys)
                
                icon = resources_icons[key]
                self.assertTrue(icon.startswith("file:"))
        
if __name__ == "__main__":
    unittest.main()
