from mediaServer.userpolicy import Policy
from mediaServer.userconfig import Configuration
from mediaServer.user import User

class UserHelper(object):
    def toUserObj(self, dictUser):
        policyObj = self.toPolicyObj(dictUser.get('Policy'))
        configObj = self.toConfigObj(dictUser.get('Configuration'))
        userObj = User(Name= dictUser.get('Name'),
                       ServerId= dictUser.get('ServerId'),
                       Id= dictUser.get('Id'),
                       HasPassword= dictUser.get('HasPassword'),
                       HasConfiguredEasyPassword= dictUser.get('HasConfiguredEasyPassword'),
                       HasConfiguredPassword= dictUser.get('HasConfiguredPassword'),
                       Policy = policyObj,
                       Configuration = configObj,
                       AccessToken = dictUser.get('AccessToken'))
        return userObj

    def toPolicyObj(self, dictPolicy):
        policyObj = Policy()
        policyObj.IsAdministrator = dictPolicy.get('IsAdministrator')
        policyObj.IsHidden = dictPolicy.get('IsHidden')
        policyObj.IsDisabled = dictPolicy.get('IsDisabled')
        policyObj.BlockedTags = dictPolicy.get('BlockedTags')
        policyObj.EnableUserPreferenceAccess = dictPolicy.get('EnableUserPreferenceAccess')
        policyObj.AccessSchedules = dictPolicy.get('AccessSchedules')
        policyObj.BlockUnratedItems = dictPolicy.get('BlockUnratedItems')
        policyObj.EnableRemoteControlOfOtherUsers = dictPolicy.get('EnableRemoteControlOfOtherUsers')
        policyObj.EnableSharedDeviceControl = dictPolicy.get('EnableSharedDeviceControl')
        policyObj.EnableRemoteAccess = dictPolicy.get('EnableRemoteAccess')
        policyObj.EnableLiveTvManagement = dictPolicy.get('EnableLiveTvManagement')
        policyObj.EnableLiveTvAccess = dictPolicy.get('EnableLiveTvAccess')
        policyObj.EnableMediaPlayback = dictPolicy.get('EnableMediaPlayback')
        policyObj.EnableAudioPlaybackTranscoding = dictPolicy.get('EnableAudioPlaybackTranscoding')
        policyObj.EnableVideoPlaybackTranscoding = dictPolicy.get('EnableVideoPlaybackTranscoding')
        policyObj.EnablePlaybackRemuxing = dictPolicy.get('EnablePlaybackRemuxing')
        policyObj.EnableContentDeletion = dictPolicy.get('EnableContentDeletion')
        policyObj.EnableContentDeletionFromFolders = dictPolicy.get('EnableContentDeletionFromFolders')
        policyObj.EnableContentDownloading = dictPolicy.get('EnableContentDownloading')
        policyObj.EnableSubtitleDownloading = dictPolicy.get('EnableSubtitleDownloading')
        policyObj.EnableSubtitleManagement = dictPolicy.get('EnableSubtitleManagement')
        policyObj.EnableSyncTranscoding = dictPolicy.get('EnableSyncTranscoding')
        policyObj.EnableMediaConversion = dictPolicy.get('EnableMediaConversion')
        policyObj.EnabledDevices = dictPolicy.get('EnabledDevices')
        policyObj.EnableAllDevices = dictPolicy.get('EnableAllDevices')
        policyObj.EnabledChannels = dictPolicy.get('EnabledChannels')
        policyObj.EnableAllChannels = dictPolicy.get('EnableAllChannels')
        policyObj.EnabledFolders = dictPolicy.get('EnabledFolders')
        policyObj.EnableAllFolders = dictPolicy.get('EnableAllFolders')
        policyObj.InvalidLoginAttemptCount = dictPolicy.get('InvalidLoginAttemptCount')
        policyObj.EnablePublicSharing = dictPolicy.get('EnablePublicSharing')
        policyObj.RemoteClientBitrateLimit = dictPolicy.get('RemoteClientBitrateLimit')
        if dictPolicy.get('AuthenticationProviderId') is not None:
            policyObj.AuthenticationProviderId = dictPolicy.get('AuthenticationProviderId')
        policyObj.ExcludedSubFolders = dictPolicy.get('ExcludedSubFolders')
        policyObj.DisablePremiumFeatures = dictPolicy.get('DisablePremiumFeatures')
        return policyObj

    def toConfigObj(self, dictConfig):
        configObj = Configuration()
        configObj.PlayDefaultAudioTrack = dictConfig.get('PlayDefaultAudioTrack')
        configObj.DisplayMissingEpisodes = dictConfig.get('DisplayMissingEpisodes')
        configObj.GroupedFolders = dictConfig.get('GroupedFolders')
        configObj.SubtitleMode = dictConfig.get('SubtitleMode')
        configObj.DisplayCollectionsView = dictConfig.get('DisplayCollectionsView')
        configObj.EnableLocalPassword = dictConfig.get('EnableLocalPassword')
        configObj.OrderedViews = dictConfig.get('OrderedViews')
        configObj.LatestItemsExcludes = dictConfig.get('LatestItemsExcludes')
        configObj.MyMediaExcludes = dictConfig.get('MyMediaExcludes')
        configObj.HidePlayedInLatest = dictConfig.get('HidePlayedInLatest')
        configObj.RememberAudioSelections = dictConfig.get('RememberAudioSelections')
        configObj.RememberSubtitleSelections = dictConfig.get('RememberSubtitleSelections')
        configObj.EnableNextEpisodeAutoPlay = dictConfig.get('EnableNextEpisodeAutoPlay')
        return configObj

    def todictUser(self, userObj):
        dictUser = userObj.__dict__
        dictUser['Policy'] = userObj.Policy.__dict__
        dictUser['Configuration'] = userObj.Configuration.__dict__
        return dictUser
