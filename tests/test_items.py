import unittest
from mediaServer.user import User
from mediaServer.item import Item, Movie
from configurator.mediaserver import mediaServer_config
from mediaServer.server import MediaServer

try:
    from unittest.mock import patch, Mock, MagicMock
except ImportError:
    from mock import patch, Mock

class ItemTestCase(unittest.TestCase):
    cfg_test = None
    testServer = None
    items = None

    get_items_response = {"Items": [
                            {
                              "Name": "root",
                              "ServerId": "d7a01ad1589d43898592e6e91a674cc3",
                              "Id": "1",
                              "IsFolder": 'true',
                              "Type": "AggregateFolder",
                              "ImageTags": {},
                              "BackdropImageTags": []
                            },
                            {
                              "Name": "Media Folders",
                              "ServerId": "d7a01ad1589d43898592e6e91a674cc3",
                              "Id": "2",
                              "IsFolder": 'true',
                              "Type": "UserRootFolder",
                              "ImageTags": {},
                              "BackdropImageTags": []
                            },
                            {
                              "Name": "OpenSourceMovies",
                              "ServerId": "d7a01ad1589d43898592e6e91a674cc3",
                              "Id": "3",
                              "IsFolder": 'true',
                              "Type": "Folder",
                              "ImageTags": {},
                              "BackdropImageTags": []
                            },
                            {
                              "Name": "Movies",
                              "ServerId": "d7a01ad1589d43898592e6e91a674cc3",
                              "Id": "f137a2dd21bbc1b99aa5c0f6bf02a805",
                              "IsFolder": 'true',
                              "Type": "CollectionFolder",
                              "CollectionType": "movies",
                              "ImageTags": {
                                "Primary": "86f7e2545dbeb60b5ec19d883086a365"
                              },
                              "BackdropImageTags": []
                            },
                            {
                              "Name": "Big Buck Bunny",
                              "ServerId": "d7a01ad1589d43898592e6e91a674cc3",
                              "Id": "5",
                              "RunTimeTicks": 25000000,
                              "IsFolder": 'false',
                              "Type": "Movie",
                              "ImageTags": {
                                "Primary": "f6d517fe7402a4bbde69f36c16f672bf",
                                "Logo": "a2f0e965628bc8a1d1087af522defa17"
                              },
                              "BackdropImageTags": [
                                "606a215825d638a0c8eee975dd679b18"
                              ],
                              "MediaType": "Video"
                            },
                            {
                              "Name": "Sacha Goedegebure",
                              "ServerId": "d7a01ad1589d43898592e6e91a674cc3",
                              "Id": "6",
                              "Type": "Person",
                              "ImageTags": {},
                              "BackdropImageTags": []
                            },
                            {
                              "Name": "Animation",
                              "ServerId": "d7a01ad1589d43898592e6e91a674cc3",
                              "Id": "7",
                              "Type": "Genre",
                              "ImageTags": {
                                "Primary": "e97e63f9402c8192bb753cd10b5f92a5"
                              },
                              "BackdropImageTags": []
                            },
                            {
                              "Name": "Comedy",
                              "ServerId": "d7a01ad1589d43898592e6e91a674cc3",
                              "Id": "8",
                              "Type": "Genre",
                              "ImageTags": {
                                "Primary": "b0af96fe63612aa31ceaaed5875217ac"
                              },
                              "BackdropImageTags": []
                            },
                            {
                              "Name": "Family",
                              "ServerId": "d7a01ad1589d43898592e6e91a674cc3",
                              "Id": "9",
                              "Type": "Genre",
                              "ImageTags": {
                                "Primary": "275c8dec800e5c09b79ac5e232953a9b"
                              },
                              "BackdropImageTags": []
                            },
                            {
                              "Name": "Blender Foundation",
                              "ServerId": "d7a01ad1589d43898592e6e91a674cc3",
                              "Id": "10",
                              "Type": "Studio",
                              "ImageTags": {},
                              "BackdropImageTags": []
                            },
                            {
                              "Name": "Live TV",
                              "ServerId": "d7a01ad1589d43898592e6e91a674cc3",
                              "Id": "2b2bca16aacc8a14d53a11bb829eafa5",
                              "IsFolder": 'true',
                              "Type": "UserView",
                              "CollectionType": "livetv",
                              "ImageTags": {},
                              "BackdropImageTags": []
                            }
                        ],
                        "TotalRecordCount": 11
                        }

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
                        "AccessToken":"09d2af46d3b14548a2caed6af5417d41",
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
        self.assertEqual(self.testServer.adminUser.AccessToken, '09d2af46d3b14548a2caed6af5417d41')
        self.assertIsInstance(self.testServer.adminUser.server, MediaServer)

        # create new user by name
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = self.createuserbyname_response
        self.testUser = self.testServer.createuserbyname('success')
        self.assertIsInstance(self.testUser, User)
        self.assertEqual(self.testUser.Name, 'success')

    @patch('mediaServer.server.requests.get')
    def test_get_items(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.get_items_response
        self.items = self.testServer.get_items(recursive="true")
        self.assertIsInstance(self.items, list)

    @patch('mediaServer.server.requests.get')
    def test_download_item(self, mock_get):
        mock_get.return_value.status_code = 200
        item_to_dl = Item(id=5)
        download_rsp = self.testServer.download_item(item=item_to_dl)
        self.assertEqual(download_rsp, "item_5")



