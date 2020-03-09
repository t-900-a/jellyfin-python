
# https://github.com/MediaBrowser/Emby/wiki/Item-Information
class Item(object):
    def __init__(self, id: int, name=str(""), item_type=str(""), media_type=str(""), path=str(""), is_folder=False):
        self.id = id
        self.name = name
        self.type = item_type
        self.media_type = media_type
        self.is_folder = is_folder
        self.path = path

class Video(Item):
    def __init__(self, **kwargs):
        super().__init__(media_type="Video", is_folder=False, **kwargs)

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