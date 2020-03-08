import unittest
from mediaServer.item import Movie, Item
from mediaServer.itemhelper import ItemHelper

class ItemHelperTestCase(unittest.TestCase):
    item_helper = None

    dict_item_movie = {'Name': 'Big Buck Bunny', 'ServerId': 'd7a01ad1589d43898592e6e91a674cc3', 'Id': '5', 'RunTimeTicks': 25000000, 'IsFolder': 'false', 'Type': 'Movie', 'ImageTags': {'Primary': 'f6d517fe7402a4bbde69f36c16f672bf', 'Logo': 'a2f0e965628bc8a1d1087af522defa17'}, 'BackdropImageTags': ['606a215825d638a0c8eee975dd679b18'], 'MediaType': 'Video'}
    dict_item_folder = {'Name': 'OpenSourceMovies', 'ServerId': 'd7a01ad1589d43898592e6e91a674cc3', 'Id': '3', 'IsFolder': 'true', 'Type': 'Folder', 'ImageTags': {}, 'BackdropImageTags': []}

    def setUp(self):
        self.item_helper = ItemHelper()

    def test_toMovieObj(self):
        item_obj = self.item_helper.to_item_obj(self.dict_item_movie)
        self.assertIsInstance(item_obj, Movie)
        self.assertFalse(item_obj.is_folder)
        self.assertEqual(item_obj.name, 'Big Buck Bunny')

    def test_toItemObj(self):
        item_obj = self.item_helper.to_item_obj(self.dict_item_folder)
        self.assertIsInstance(item_obj, Item)
        self.assertTrue(item_obj.is_folder)
        self.assertEqual(item_obj.name, 'OpenSourceMovies')

