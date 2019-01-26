
class Policy(object):
    """Jellyfin user policy.

    Handles user policy

    :param
    """

    def __init__(self,
                 IsAdministrator = False,
                 IsHidden = True,
                 IsDisabled = False,
                 BlockedTags = [],
                 EnableUserPreferenceAccess = True,
                 AccessSchedules = [],
                 BlockUnratedItems = [],
                 EnableRemoteControlOfOtherUsers = False,
                 EnableSharedDeviceControl = True,
                 EnableRemoteAccess = True,
                 EnableLiveTvManagement = True,
                 EnableLiveTvAccess = True,
                 EnableMediaPlayback = True,
                 EnableAudioPlaybackTranscoding = True,
                 EnableVideoPlaybackTranscoding = True,
                 EnablePlaybackRemuxing = True,
                 EnableContentDeletion = False,
                 EnableContentDeletionFromFolders = [],
                 EnableContentDownloading = True,
                 EnableSubtitleDownloading = False,
                 EnableSubtitleManagement = False,
                 EnableSyncTranscoding = True,
                 EnableMediaConversion = True,
                 EnabledDevices = [],
                 EnableAllDevices = True,
                 EnabledChannels = [],
                 EnableAllChannels = True,
                 EnabledFolders = [],
                 EnableAllFolders = True,
                 InvalidLoginAttemptCount = 0,
                 EnablePublicSharing = False,
                 RemoteClientBitrateLimit = 0,
                 AuthenticationProviderId = None,
                 ExcludedSubFolders = [],
                 DisablePremiumFeatures = False):

        self.IsAdministrator = IsAdministrator
        self.IsHidden = IsHidden
        self.IsDisabled = IsDisabled
        self.BlockedTags = BlockedTags
        self.EnableUserPreferenceAccess = EnableUserPreferenceAccess
        self.AccessSchedules = AccessSchedules
        self.BlockUnratedItems = BlockUnratedItems
        self.EnableRemoteControlOfOtherUsers = EnableRemoteControlOfOtherUsers
        self.EnableSharedDeviceControl = EnableSharedDeviceControl
        self.EnableRemoteAccess = EnableRemoteAccess
        self.EnableLiveTvManagement = EnableLiveTvManagement
        self.EnableLiveTvAccess = EnableLiveTvAccess
        self.EnableMediaPlayback = EnableMediaPlayback
        self.EnableAudioPlaybackTranscoding = EnableAudioPlaybackTranscoding
        self.EnableVideoPlaybackTranscoding = EnableVideoPlaybackTranscoding
        self.EnablePlaybackRemuxing = EnablePlaybackRemuxing
        self.EnableContentDeletion = EnableContentDeletion
        self.EnableContentDeletionFromFolders = EnableContentDeletionFromFolders
        self.EnableContentDownloading = EnableContentDownloading
        self.EnableSubtitleDownloading = EnableSubtitleDownloading
        self.EnableSubtitleManagement = EnableSubtitleManagement
        self.EnableSyncTranscoding = EnableSyncTranscoding
        self.EnableMediaConversion = EnableMediaConversion
        self.EnabledDevices = EnabledDevices
        self.EnableAllDevices = EnableAllDevices
        self.EnabledChannels = EnabledChannels
        self.EnableAllChannels = EnableAllChannels
        self.EnabledFolders = EnabledFolders
        self.EnableAllFolders = EnableAllFolders
        self.InvalidLoginAttemptCount = InvalidLoginAttemptCount
        self.EnablePublicSharing = EnablePublicSharing
        self.RemoteClientBitrateLimit = RemoteClientBitrateLimit
        if AuthenticationProviderId is not None:
            self.AuthenticationProviderId = AuthenticationProviderId
        self.ExcludedSubFolders = ExcludedSubFolders
        self.DisablePremiumFeatures = DisablePremiumFeatures

