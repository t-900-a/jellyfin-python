from mediaServer.item import Item, Movie, Episode

class ItemHelper(object):
    def to_item_obj(self, dict_item) -> Item:
        item_obj = None
        if dict_item['Type'] == 'Movie':
            item_obj = Movie(id=dict_item.get('Id'),
                             name=dict_item.get('Name')
                             )

        if dict_item['Type'] == 'Episode':
            item_obj = Episode(id=dict_item.get('Id'),
                             name=dict_item.get('Name')
                             )

        if item_obj == None:
            item_obj = Item(id=dict_item.get('Id'),
                            name=dict_item.get('Name'),
                            item_type = dict_item.get('ItemType'),
                            media_type=dict_item.get('MediaType'),
                            is_folder=(True if dict_item.get('IsFolder') == "true" else False)
                            )

        return item_obj
