
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
        # TODO unit testing
        self.community_rating = kwargs.get("community_rating")
        self.genre_items = kwargs.get("genre_items")
        self.critic_rating = kwargs.get("critic_rating")
        self.official_rating = kwargs.get("official_rating")
        self.production_year = kwargs.get("production_year")
        self.overview = kwargs.get("overview")
        self.studios = kwargs.get("studios")
        self.providerids = kwargs.get("providerids")
        self.totalbitrate = kwargs.get("totalbitrate")
        self.width = kwargs.get("width")
        self.height = kwargs.get("height")
        self.size = kwargs.get("size")
        self.container = kwargs.get("container")
        self.duration_in_sec = kwargs.get("duration_in_sec")
        self.premieredate = kwargs.get("premiereDate")
        self.samplingrate = kwargs.get("samplingrate")
        self.framerate = kwargs.get("framerate")
        self.lang = kwargs.get("lang")
        self.channels = kwargs.get("channels")

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