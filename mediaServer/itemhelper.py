from mediaServer.item import Item, Movie, Episode

class ItemHelper(object):
    def to_item_obj(self, dict_item) -> Item:
        item_obj = None
        if dict_item['Type'] == 'Movie':
            item_obj = Movie(id=dict_item.get('Id'),
                             name=dict_item.get('Name'),
                             path=dict_item.get('Path'),
                             date_created=dict_item.get('DateCreated'),
                             community_rating=dict_item.get('CommunityRating'),
                             genres=dict_item.get('Genres'),
                             critic_rating=dict_item.get('CriticRating'),
                             official_rating=dict_item.get('OfficialRating'),
                             production_year=dict_item.get('ProductionYear'),
                             totalbitrate=dict_item.get("TotalBitrate"),
                             width=dict_item.get("Width"),
                             height=dict_item.get("Height"),
                             size=dict_item.get("Size"),
                             container=dict_item.get("Container"),
                             premieredate=dict_item.get("PremiereDate")
                             )

        if dict_item['Type'] == 'Episode':
            item_obj = Episode(id=dict_item.get('Id'),
                             name=dict_item.get('Name'),
                             path=dict_item.get('Path'),
                             date_created=dict_item.get('DateCreated'),
                             community_rating=dict_item.get('CommunityRating'),
                             genres=dict_item.get('Genres'),
                             critic_rating=dict_item.get('CriticRating'),
                             official_rating=dict_item.get('OfficialRating'),
                             production_year=dict_item.get('ProductionYear'),
                             totalbitrate=dict_item.get("TotalBitrate"),
                             width=dict_item.get("Width"),
                             height=dict_item.get("Height"),
                             size=dict_item.get("Size"),
                             container=dict_item.get("Container"),
                             premieredate=dict_item.get("PremiereDate")
                             )

        if item_obj == None:
            item_obj = Item(id=dict_item.get('Id'),
                            name=dict_item.get('Name'),
                            item_type = dict_item.get('ItemType'),
                            media_type=dict_item.get('MediaType'),
                            is_folder=(True if dict_item.get('IsFolder') == "true" else False),
                            path=dict_item.get('Path'),
                            date_created=dict_item.get('DateCreated')
                            )

        return item_obj
