import sys
import os.path
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader import SupportedSitesModel, StringFilterModel

class ModelsTest(unittest.TestCase):
    
    def test_supportedSitesModelCollectsSites(self):
        supported_sites_model = SupportedSitesModel()
        self.assertTrue(supported_sites_model.rowCount() > 0)

    def test_stringFilterModelFiltersData(self):
        supported_sites_model = SupportedSitesModel()
        self.assertTrue(supported_sites_model.rowCount() > 0)
        
        string_filter_model = StringFilterModel()
        string_filter_model.setSourceModel(supported_sites_model)
        string_filter_model.set_filter_role_name("name")
        string_filter_model.set_string("youtube")
        self.assertEqual(string_filter_model.rowCount(), 15)


if __name__ == "__main__":
    unittest.main()

