
# https://github.com/MediaBrowser/Emby/wiki/Item-Information
class Item(object):
    def __init__(self, id: int, name=str(""), item_type=str(""), media_type=str(""), path=str(""), date_created=str(""), is_folder=False):
        self.id = id
        self.name = name
        self.type = item_type
        self.media_type = media_type
        self.is_folder = is_folder
        self.path = path
        self.date_created = date_created

class Video(Item):
    def __init__(self, **kwargs):
        super().__init__(media_type="Video", is_folder=False,
                         id=kwargs.get("id"),name=kwargs.get("name"), item_type=kwargs.get("item_type"),
                         path=kwargs.get("path"), date_created=kwargs.get("date_created"))
        self.community_rating = kwargs.get("CommunityRating")
        self.genre_items = kwargs.get("Genres")
        self.critic_rating = kwargs.get("CriticRating")
        self.official_rating = kwargs.get("OfficialRating")
        self.production_year = kwargs.get("ProductionYear")

class Movie(Video):
    def __init__(self, **kwargs):
        super().__init__(item_type="Movie", **kwargs)

class Episode(Video):
    def __init__(self, **kwargs):
        super().__init__(item_type="TV Shows", **kwargs)

class Folder(Item):
    def __init__(self, **kwargs):
        super().__init__(is_folder=True, **kwargs)

class Series(Folder):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Season(Folder):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)