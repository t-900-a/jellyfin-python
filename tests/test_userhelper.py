import unittest
from mediaServer.user import User
from mediaServer.userconfig import Configuration
from mediaServer.userpolicy import Policy
from mediaServer.userhelper import UserHelper

class UserHelperTestCase(unittest.TestCase):
    userHelper = None

    createuserbyname_response = {'Name': 'success',
                                 'ServerId': '73719e7c60fc423c840d7a49065472ab',
                                 'Id': '9106d249f0ae47a9af49fcc880684758',
                                 'HasPassword': False,
                                 'HasConfiguredPassword': False,
                                 'HasConfiguredEasyPassword': False,
                                 'Configuration':
                                     {'PlayDefaultAudioTrack': True,
                                      'DisplayMissingEpisodes': False,
                                      'GroupedFolders': [],
                                      'SubtitleMode': 'Default',
                                      'DisplayCollectionsView': False,
                                      'EnableLocalPassword': False,
                                      'OrderedViews': [],
                                      'LatestItemsExcludes': [],
                                      'MyMediaExcludes': [],
                                      'HidePlayedInLatest': True,
                                      'RememberAudioSelections': True,
                                      'RememberSubtitleSelections': True,
                                      'EnableNextEpisodeAutoPlay': True},
                                 'Policy':
                                     {'IsAdministrator': False,
                                      'IsHidden': False,
                                      'IsDisabled': False,
                                      'BlockedTags': [],
                                      'EnableUserPreferenceAccess': True,
                                      'AccessSchedules': [],
                                      'BlockUnratedItems': [],
                                      'EnableRemoteControlOfOtherUsers': False,
                                      'EnableSharedDeviceControl': True,
                                      'EnableRemoteAccess': True,
                                      'EnableLiveTvManagement': True,
                                      'EnableLiveTvAccess': True,
                                      'EnableMediaPlayback': True,
                                      'EnableAudioPlaybackTranscoding': True,
                                      'EnableVideoPlaybackTranscoding': True,
                                      'EnablePlaybackRemuxing': True,
                                      'EnableContentDeletion': False,
                                      'EnableContentDeletionFromFolders': [],
                                      'EnableContentDownloading': True,
                                      'EnableSubtitleDownloading': False,
                                      'EnableSubtitleManagement': False,
                                      'EnableSyncTranscoding': True,
                                      'EnableMediaConversion': True,
                                      'EnabledDevices': [],
                                      'EnableAllDevices': True,
                                      'EnabledChannels': [],
                                      'EnableAllChannels': True,
                                      'EnabledFolders': [],
                                      'EnableAllFolders': True,
                                      'InvalidLoginAttemptCount': 0,
                                      'EnablePublicSharing': True,
                                      'RemoteClientBitrateLimit': 0,
                                      'ExcludedSubFolders': [],
                                      'DisablePremiumFeatures': False}}
    policyDict = {'IsAdministrator': False,
                                      'IsHidden': False,
                                      'IsDisabled': False,
                                      'BlockedTags': [],
                                      'EnableUserPreferenceAccess': True,
                                      'AccessSchedules': [],
                                      'BlockUnratedItems': [],
                                      'EnableRemoteControlOfOtherUsers': False,
                                      'EnableSharedDeviceControl': True,
                                      'EnableRemoteAccess': True,
                                      'EnableLiveTvManagement': True,
                                      'EnableLiveTvAccess': True,
                                      'EnableMediaPlayback': True,
                                      'EnableAudioPlaybackTranscoding': True,
                                      'EnableVideoPlaybackTranscoding': True,
                                      'EnablePlaybackRemuxing': True,
                                      'EnableContentDeletion': False,
                                      'EnableContentDeletionFromFolders': [],
                                      'EnableContentDownloading': True,
                                      'EnableSubtitleDownloading': False,
                                      'EnableSubtitleManagement': False,
                                      'EnableSyncTranscoding': True,
                                      'EnableMediaConversion': True,
                                      'EnabledDevices': [],
                                      'EnableAllDevices': True,
                                      'EnabledChannels': [],
                                      'EnableAllChannels': True,
                                      'EnabledFolders': [],
                                      'EnableAllFolders': True,
                                      'InvalidLoginAttemptCount': 0,
                                      'EnablePublicSharing': True,
                                      'RemoteClientBitrateLimit': 0,
                                      'ExcludedSubFolders': [],
                                      'DisablePremiumFeatures': False}
    configDict = {'PlayDefaultAudioTrack': True,
                                      'DisplayMissingEpisodes': False,
                                      'GroupedFolders': [],
                                      'SubtitleMode': 'Default',
                                      'DisplayCollectionsView': False,
                                      'EnableLocalPassword': False,
                                      'OrderedViews': [],
                                      'LatestItemsExcludes': [],
                                      'MyMediaExcludes': [],
                                      'HidePlayedInLatest': True,
                                      'RememberAudioSelections': True,
                                      'RememberSubtitleSelections': True,
                                      'EnableNextEpisodeAutoPlay': True}
    def setUp(self):
        self.userHelper = UserHelper()

    def test_toPolicyObj(self):
        policyObj = self.userHelper.toPolicyObj(self.policyDict)
        self.assertIsInstance(policyObj, Policy)
        self.assertFalse(policyObj.IsAdministrator)
        self.assertTrue(policyObj.EnableAllDevices)
        self.assertIsInstance(policyObj.EnabledFolders, list)
        self.assertTrue(policyObj.EnablePublicSharing)

    def test_toConfigObj(self):
        configObj = self.userHelper.toConfigObj(self.configDict)
        self.assertIsInstance(configObj, Configuration)
        self.assertFalse(configObj.DisplayMissingEpisodes)
        self.assertEqual(configObj.SubtitleMode,'Default')
        self.assertTrue(configObj.HidePlayedInLatest)
        self.assertIsInstance(configObj.MyMediaExcludes, list)

    def test_toUserObj(self):
        userObj = self.userHelper.toUserObj(self.createuserbyname_response)
        self.assertIsInstance(userObj, User)
        self.assertFalse(userObj.HasPassword)
        self.assertEqual(userObj.Id, '9106d249f0ae47a9af49fcc880684758')
        self.assertIsInstance(userObj.Configuration, Configuration)
        self.assertEqual(userObj.Policy.RemoteClientBitrateLimit, 0)

    def test_to_DictUser(self):
        userObj = self.userHelper.toUserObj(self.createuserbyname_response)
        userDict = self.userHelper.todictUser(userObj)
        self.assertIsInstance(userDict, dict)
        self.assertEqual(userDict, self.createuserbyname_response)