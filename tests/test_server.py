import unittest
from mediaServer.user import User
from mediaServer.userconfig import Configuration
from mediaServer.userpolicy import Policy
from configurator.mediaserver import mediaServer_config
from mediaServer.server import MediaServer

try:
    from unittest.mock import patch, Mock, MagicMock
except ImportError:
    from mock import patch, Mock

class ServerTestCase(unittest.TestCase):
    cfg_test = None
    testServer = None
    testUser = None
    getusers_response = [
        {
            "Name": "additionaluser",
            "ServerId": "60b8fc43b399400ea04e9e6cbd7a1f59",
            "Id": "120caf4da6544b90ad61e546af9bb72e",
            "HasPassword": False,
            "HasConfiguredPassword": False,
            "HasConfiguredEasyPassword": False,
            "Configuration": {
                "PlayDefaultAudioTrack": True,
                "DisplayMissingEpisodes": False,
                "GroupedFolders": [],
                "SubtitleMode": "Default",
                "DisplayCollectionsView": False,
                "EnableLocalPassword": False,
                "OrderedViews": [],
                "LatestItemsExcludes": [],
                "MyMediaExcludes": [],
                "HidePlayedInLatest": True,
                "RememberAudioSelections": True,
                "RememberSubtitleSelections": True,
                "EnableNextEpisodeAutoPlay": True
            },
            "Policy": {
                "IsAdministrator": False,
                "IsHidden": False,
                "IsDisabled": False,
                "BlockedTags": [],
                "EnableUserPreferenceAccess": True,
                "AccessSchedules": [],
                "BlockUnratedItems": [],
                "EnableRemoteControlOfOtherUsers": False,
                "EnableSharedDeviceControl": True,
                "EnableRemoteAccess": True,
                "EnableLiveTvManagement": True,
                "EnableLiveTvAccess": True,
                "EnableMediaPlayback": True,
                "EnableAudioPlaybackTranscoding": True,
                "EnableVideoPlaybackTranscoding": True,
                "EnablePlaybackRemuxing": True,
                "EnableContentDeletion": False,
                "EnableContentDeletionFromFolders": [],
                "EnableContentDownloading": True,
                "EnableSubtitleDownloading": False,
                "EnableSubtitleManagement": False,
                "EnableSyncTranscoding": True,
                "EnableMediaConversion": True,
                "EnabledDevices": [],
                "EnableAllDevices": True,
                "EnabledChannels": [],
                "EnableAllChannels": True,
                "EnabledFolders": [],
                "EnableAllFolders": True,
                "InvalidLoginAttemptCount": 0,
                "EnablePublicSharing": True,
                "RemoteClientBitrateLimit": 0,
                "ExcludedSubFolders": [],
                "DisablePremiumFeatures": False
            }
        },
        {
            "Name": "MyEmbyUser",
            "ServerId": "60b8fc43b399400ea04e9e6cbd7a1f59",
            "Id": "3b55ac5646364a45b2d017f5b4be8cfb",
            "HasPassword": False,
            "HasConfiguredPassword": False,
            "HasConfiguredEasyPassword": False,
            "LastLoginDate": "2019-02-09T22:56:46.7788654+00:00",
            "LastActivityDate": "2019-02-09T23:31:08.3019870+00:00",
            "Configuration": {
                "PlayDefaultAudioTrack": True,
                "DisplayMissingEpisodes": False,
                "GroupedFolders": [],
                "SubtitleMode": "Default",
                "DisplayCollectionsView": False,
                "EnableLocalPassword": False,
                "OrderedViews": [],
                "LatestItemsExcludes": [],
                "MyMediaExcludes": [],
                "HidePlayedInLatest": True,
                "RememberAudioSelections": True,
                "RememberSubtitleSelections": True,
                "EnableNextEpisodeAutoPlay": True
            },
            "Policy": {
                "IsAdministrator": True,
                "IsHidden": False,
                "IsDisabled": False,
                "BlockedTags": [],
                "EnableUserPreferenceAccess": True,
                "AccessSchedules": [],
                "BlockUnratedItems": [],
                "EnableRemoteControlOfOtherUsers": True,
                "EnableSharedDeviceControl": True,
                "EnableRemoteAccess": True,
                "EnableLiveTvManagement": True,
                "EnableLiveTvAccess": True,
                "EnableMediaPlayback": True,
                "EnableAudioPlaybackTranscoding": True,
                "EnableVideoPlaybackTranscoding": True,
                "EnablePlaybackRemuxing": True,
                "EnableContentDeletion": True,
                "EnableContentDeletionFromFolders": [],
                "EnableContentDownloading": True,
                "EnableSubtitleDownloading": True,
                "EnableSubtitleManagement": True,
                "EnableSyncTranscoding": True,
                "EnableMediaConversion": True,
                "EnabledDevices": [],
                "EnableAllDevices": True,
                "EnabledChannels": [],
                "EnableAllChannels": True,
                "EnabledFolders": [],
                "EnableAllFolders": True,
                "InvalidLoginAttemptCount": 0,
                "EnablePublicSharing": True,
                "RemoteClientBitrateLimit": 0,
                "AuthenticationProviderId": "Emby.Server.Implementations.Library.DefaultAuthenticationProvider",
                "ExcludedSubFolders": [],
                "DisablePremiumFeatures": False
            }
        },
        {
            "Name": "success",
            "ServerId": "60b8fc43b399400ea04e9e6cbd7a1f59",
            "Id": "5c9ea641b9784a0b8a3af1898a24904d",
            "HasPassword": False,
            "HasConfiguredPassword": False,
            "HasConfiguredEasyPassword": False,
            "Configuration": {
                "PlayDefaultAudioTrack": True,
                "DisplayMissingEpisodes": False,
                "GroupedFolders": [],
                "SubtitleMode": "Default",
                "DisplayCollectionsView": False,
                "EnableLocalPassword": False,
                "OrderedViews": [],
                "LatestItemsExcludes": [],
                "MyMediaExcludes": [],
                "HidePlayedInLatest": True,
                "RememberAudioSelections": True,
                "RememberSubtitleSelections": True,
                "EnableNextEpisodeAutoPlay": True
            },
            "Policy": {
                "IsAdministrator": False,
                "IsHidden": False,
                "IsDisabled": False,
                "BlockedTags": [],
                "EnableUserPreferenceAccess": True,
                "AccessSchedules": [],
                "BlockUnratedItems": [],
                "EnableRemoteControlOfOtherUsers": False,
                "EnableSharedDeviceControl": True,
                "EnableRemoteAccess": True,
                "EnableLiveTvManagement": True,
                "EnableLiveTvAccess": True,
                "EnableMediaPlayback": True,
                "EnableAudioPlaybackTranscoding": True,
                "EnableVideoPlaybackTranscoding": True,
                "EnablePlaybackRemuxing": True,
                "EnableContentDeletion": False,
                "EnableContentDeletionFromFolders": [],
                "EnableContentDownloading": True,
                "EnableSubtitleDownloading": False,
                "EnableSubtitleManagement": False,
                "EnableSyncTranscoding": True,
                "EnableMediaConversion": True,
                "EnabledDevices": [],
                "EnableAllDevices": True,
                "EnabledChannels": [],
                "EnableAllChannels": True,
                "EnabledFolders": [],
                "EnableAllFolders": True,
                "InvalidLoginAttemptCount": 0,
                "EnablePublicSharing": True,
                "RemoteClientBitrateLimit": 0,
                "ExcludedSubFolders": [],
                "DisablePremiumFeatures": False
            }
        }
    ]


    authenticateadminuserbyname_response = {"User":
                            {"Name":"MyEmbyUser",
                             "ServerId":"73719e7c60fc423c840d7a49065472ab",
                             "Id":"9431bee7f286432c9c9b31747cb33fb2",
                             "HasPassword":'false',
                             "HasConfiguredPassword":'false',
                             "HasConfiguredEasyPassword":'false',
                             "LastLoginDate":"2019-01-19T08:19:24.2566183+00:00",
                             "LastActivityDate":"2019-01-19T08:19:24.2574283+00:00",
                             "Configuration":
                                 {"PlayDefaultAudioTrack":'true',
                                              "DisplayMissingEpisodes":'false',
                                              "GroupedFolders":[],
                                              "SubtitleMode":"Default",
                                              "DisplayCollectionsView":'false',
                                              "EnableLocalPassword":'false',
                                              "OrderedViews":[],
                                              "LatestItemsExcludes":[],
                                              "MyMediaExcludes":[],
                                              "HidePlayedInLatest":'true',
                                              "RememberAudioSelections":'true',
                                              "RememberSubtitleSelections":'true',
                                              "EnableNextEpisodeAutoPlay":'true'},
                             "Policy":
                                 {"IsAdministrator":'true',
                                  "IsHidden":'false',
                                  "IsDisabled":'false',
                                  "BlockedTags":[],
                                  "EnableUserPreferenceAccess":'true',
                                  "AccessSchedules":[],
                                  "BlockUnratedItems":[],
                                  "EnableRemoteControlOfOtherUsers":'true',
                                  "EnableSharedDeviceControl":'true',
                                  "EnableRemoteAccess":'true',
                                  "EnableLiveTvManagement":'true',
                                  "EnableLiveTvAccess":'true',
                                  "EnableMediaPlayback":'true',
                                  "EnableAudioPlaybackTranscoding":'true',
                                  "EnableVideoPlaybackTranscoding":'true',
                                  "EnablePlaybackRemuxing":'true',
                                  "EnableContentDeletion":'true',
                                  "EnableContentDeletionFromFolders":[],
                                  "EnableContentDownloading":'true',
                                  "EnableSubtitleDownloading":'true',
                                  "EnableSubtitleManagement":'true',
                                  "EnableSyncTranscoding":'true',
                                  "EnableMediaConversion":'true',
                                  "EnabledDevices":[],
                                  "EnableAllDevices":'true',
                                  "EnabledChannels":[],
                                  "EnableAllChannels":'true',
                                  "EnabledFolders":[],
                                  "EnableAllFolders":'true',
                                  "InvalidLoginAttemptCount":0,
                                  "EnablePublicSharing":'true',
                                  "RemoteClientBitrateLimit":0,
                                  "AuthenticationProviderId":"Emby.Server.Implementations.Library.DefaultAuthenticationProvider",
                                  "ExcludedSubFolders":[],
                                  "DisablePremiumFeatures":'false'}},
                        "SessionInfo":
                            {"PlayState":
                                 {"CanSeek":'false',
                                  "IsPaused":'false',
                                  "IsMuted":'false',
                                  "RepeatMode":"RepeatNone"},
                             "AdditionalUsers":[],
                             "Capabilities":
                                 {"PlayableMediaTypes":[],
                                  "SupportedCommands":[],
                                  "SupportsMediaControl":'false',
                                  "SupportsPersistentIdentifier":'true',
                                  "SupportsSync":'false'},
                             "RemoteEndPoint":"172.17.0.1",
                             "PlayableMediaTypes":[],
                             "Id":"d99097f345c8d1ab5bfcaa3b123ce10d",
                             "ServerId":"73719e7c60fc423c840d7a49065472ab",
                             "UserId":"9431bee7f286432c9c9b31747cb33fb2",
                             "UserName":"MyEmbyUser",
                             "Client":"account-automation",
                             "LastActivityDate":"2019-01-19T08:19:24.2574283Z",
                             "DeviceName":"ThinkPad-E420",
                             "DeviceId":"5702695166790547666",
                             "ApplicationVersion":"0.0.1",
                             "SupportedCommands":[],
                             "SupportsRemoteControl":'false'},
                        "AccessToken":"1ece50b14c424ec88f1197642cafc018",
                        "ServerId":"73719e7c60fc423c840d7a49065472ab"}

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

    @patch('mediaServer.server.requests.post')
    def setUp(self, mock_post):
        self.cfg_test = mediaServer_config(cfg_default=True)

        # instantiate server (retrieve emby token for admin user)
        # a user object is created for the admin user
        # authenticatebyname() is tested
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = self.authenticateadminuserbyname_response
        self.testServer = MediaServer(self.cfg_test)
        self.assertIsInstance(self.testServer.adminUser, User)
        self.assertEqual(self.testServer.adminUser.AccessToken, '1ece50b14c424ec88f1197642cafc018')
        self.assertIsInstance(self.testServer.adminUser.server, MediaServer)

        # create new user by name
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = self.createuserbyname_response
        self.testUser = self.testServer.createuserbyname('success')
        self.assertIsInstance(self.testUser, User)
        self.assertEqual(self.testUser.Name, 'success')

    @patch('mediaServer.server.requests.post')
    def test_updateuserconfig(self, mock_post):
        result = mock_post.return_value.status_code = 204
        updatedUser = self.testUser
        updatedUser.Configuration.EnableNextEpisodeAutoPlay = False
        self.testServer.updateuserconfig(updatedUser)
        # in a live environment we would do this self.assertEqual(updatedUser.Configuration.EnableNextEpisodeAutoPlay, serveruser.Configuration.EnableNextEpisodeAutoPlay)
        self.assertTrue(result)

    @patch('mediaServer.server.requests.post')
    def test_updateuserpolicy(self, mock_post):
        result = mock_post.return_value.status_code = 204
        updatedUser = self.testUser
        updatedUser.Policy.IsHidden = True
        self.testServer.updateuserpolicy(updatedUser)
        # in a live environment we would do this self.assertEqual(updatedUser.Policy.IsHidden, serveruser.Policy.IsHidden)
        self.assertTrue(result)

    @patch('mediaServer.server.requests.post')
    def test_updateuserpassword(self, mock_post):
        mock_post.return_value.status_code = 204
        result = self.testServer.updateuserpassword(userId=self.testServer.adminUser.Id,
                                                    AccessToken=self.testServer.adminUser.AccessToken,
                                                    currentPw='', newPw='set')
        self.assertTrue(result)

    @patch('mediaServer.server.requests.post')
    def test_logout(self, mock_post):
        result = mock_post.return_value.status_code = 204
        self.testServer.logoutuser(userId=self.testUser.Id)
        self.assertTrue(result)
        self.assertIsNone(self.testUser.AccessToken)

    @patch('mediaServer.server.requests.post')
    def test_deleteuser(self, mock_post):
        result = mock_post.return_value.status_code = 204
        self.testServer.deleteuser(userId=self.testUser.Id)
        self.assertTrue(result)
        self.assertIsNone(self.testUser.AccessToken)

    @patch('mediaServer.server.requests.get')
    def test_getusers(self, mock_get):
        result = mock_get.return_value.status_code = 204
        mock_get.return_value.json.return_value = self.getusers_response
        users = self.testServer.getusers()
        self.assertIsInstance(users, list)
        self.assertIsInstance(users[0], User)
        self.assertEqual(users[1].Policy.IsHidden, False)

    def test_authenticate(self):
        #untested
        #unused
        pass

