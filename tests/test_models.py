import sys
import os.path
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader.models import SupportedSitesModel, StringFilterModel, HistoryModel, WebTabsModel, AllowFilterModel
from youtubedownloader.database import Database

class ModelsTest(unittest.TestCase):
    
    def test_supportedSitesModelCollectsSites(self):
        supported_sites_model = SupportedSitesModel()
        self.assertTrue(supported_sites_model.rowCount() > 0)

    def test_stringFilterModelFiltersData(self):
        supported_sites_model = SupportedSitesModel()
        self.assertTrue(supported_sites_model.rowCount() > 0)
        
        string_filter_model = StringFilterModel()
        string_filter_model.setSourceModel(supported_sites_model)
        string_filter_model.set_filter_role_names(["name"])
        string_filter_model.set_string("youtube")
        self.assertEqual(string_filter_model.rowCount(), 15)


    def test_historyModelCommunicatesWithDatabase(self):
        db = Database(":memory:")
        
        history_model = HistoryModel(db.session) # NOTE: Load into RAM
    
        history_model.add("t0", "t1", "t2", "t3", "t4")
        history_model.add("f0", "f1", "f2", "f3", "f4")
        
        self.assertEqual(history_model.rowCount(), 2)
        
        history_model.remove("t0")
        
        self.assertEqual(history_model.rowCount(), 1)
        
    
    def test_webTabsModelSetTabs(self):
        web_tabs_model = WebTabsModel()
        tabs = [
            {"url": "", "title": "", "allow": True},
            {"url": "", "title": "", "allow": True},
            {"url": "", "title": "", "allow": True},
            {"url": "", "title": "", "allow": True},
            {"url": "", "title": "", "allow": True},
        ]
            
        web_tabs_model.set_tabs(tabs)
        self.assertEqual(web_tabs_model.rowCount(), 5)
    
    def test_allowFilterModelFiltersByallowProperty(self):
        web_tabs_model = WebTabsModel()
        tabs = [
            {"url": "", "title": "", "allow": True},
            {"url": "", "title": "", "allow": True},
            {"url": "", "title": "", "allow": True},
            {"url": "", "title": "", "allow": False},
            {"url": "", "title": "", "allow": False},
        ]
            
        web_tabs_model.set_tabs(tabs)
        allow_filter_model = AllowFilterModel()
        allow_filter_model.setSourceModel(web_tabs_model)
        
        self.assertEqual(allow_filter_model.rowCount(), 3)

if __name__ == "__main__":
    unittest.main()

