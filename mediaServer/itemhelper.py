from mediaServer.item import Item, Movie, Episode

class ItemHelper(object):
    def to_item_obj(self, dict_item) -> Item:
        item_obj = None
        if dict_item['Type'] == 'Movie':
            mediasources = dict_item.get("MediaSources")
            mediastreams = mediasources[0].get("MediaStreams")
            item_obj = Movie(id=dict_item.get('Id'),
                             name=dict_item.get('Name'),
                             path=dict_item.get('Path'),
                             date_created=dict_item.get('DateCreated'),
                             community_rating=dict_item.get('CommunityRating'),
                             genres=dict_item.get('Genres'),
                             critic_rating=dict_item.get('CriticRating'),
                             official_rating=dict_item.get('OfficialRating'),
                             production_year=dict_item.get('ProductionYear'),
                             totalbitrate=mediastreams[0].get('BitRate'),
                             width=mediastreams[0].get('Width'),
                             height=mediastreams[0].get('Height'),
                             size=mediasources[0].get('Size'),
                             framerate=mediastreams[0].get('AverageFrameRate'),
                             samplingrate=mediastreams[1].get('SampleRate'),
                             channels=mediastreams[1].get('Channels'),
                             duration_in_sec=mediasources[0].get('RunTimeTicks')*.0000001,
                             container=dict_item.get("Container"),
                             premieredate=dict_item.get("PremiereDate"),
                             lang=mediastreams[0].get('Language')
                             )

        if dict_item['Type'] == 'Episode':
            mediasources = dict_item.get("MediaSources")
            if mediasources[0] is not None:
                mediastreams = mediasources[0].get("MediaStreams")
            item_obj = Episode(id=dict_item.get('Id'),
                             name=dict_item.get('Name'),
                             path=dict_item.get('Path'),
                             date_created=dict_item.get('DateCreated'),
                             community_rating=dict_item.get('CommunityRating'),
                             genres=dict_item.get('Genres'),
                             critic_rating=dict_item.get('CriticRating'),
                             official_rating=dict_item.get('OfficialRating'),
                             production_year=dict_item.get('ProductionYear'),
                             totalbitrate=mediastreams[0].get('BitRate'),
                             width=mediastreams[0].get('Width'),
                             height=mediastreams[0].get('Height'),
                             size=mediasources[0].get('Size'),
                             framerate=mediastreams[0].get('AverageFrameRate'),
                             samplingrate=mediastreams[1].get('SampleRate'),
                             channels=mediastreams[1].get('Channels'),
                             duration_in_sec=mediasources[0].get('RunTimeTicks')*.0000001,
                             container=dict_item.get("Container"),
                             premieredate=dict_item.get("PremiereDate"),
                             lang=mediastreams[0].get('Language')
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
