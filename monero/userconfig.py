

class Configuration(object):
    """Jellyfin user config.

    Handles user config

    :param
    """

    def __init__(self,
                 PlayDefaultAudioTrack = True,
                 DisplayMissingEpisodes = False,
                 GroupedFolders = [],
                 SubtitleMode = "Default",
                 DisplayCollectionsView = False,
                 EnableLocalPassword = False,
                 OrderedViews = [],
                 LatestItemsExcludes = [],
                 MyMediaExcludes = [],
                 HidePlayedInLatest = True,
                 RememberAudioSelections = True,
                 RememberSubtitleSelections = True,
                 EnableNextEpisodeAutoPlay = True):

        self.PlayDefaultAudioTrack = PlayDefaultAudioTrack
        self.DisplayMissingEpisodes = DisplayMissingEpisodes
        self.GroupedFolders = GroupedFolders
        self.SubtitleMode = SubtitleMode
        self.DisplayCollectionsView = DisplayCollectionsView
        self.EnableLocalPassword = EnableLocalPassword
        self.OrderedViews = OrderedViews
        self.LatestItemsExcludes = LatestItemsExcludes
        self.MyMediaExcludes = MyMediaExcludes
        self.HidePlayedInLatest = HidePlayedInLatest
        self.RememberAudioSelections = RememberAudioSelections
        self.RememberSubtitleSelections = RememberSubtitleSelections
        self.EnableNextEpisodeAutoPlay = EnableNextEpisodeAutoPlay


