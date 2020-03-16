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

    get_items_response = {
  "Items": [
    {
      "Name": "Big Buck Bunny",
      "ServerId": "d7a01ad1589d43898592e6e91a674cc3",
      "Id": "5",
      "Container": "avi",
      "MediaSources": [
        {
          "Protocol": "File",
          "Id": "049829ec5c2f41a1e627c2f4d51d7e73",
          "Path": "/media/Media/OpenSourceMovies/big_buck_bunny_480p_surround-fix.avi",
          "Type": "Default",
          "Container": "avi",
          "Size": 220514438,
          "Name": "big_buck_bunny_480p_surround-fix",
          "IsRemote": False,
          "RunTimeTicks": 5964580000,
          "SupportsTranscoding": True,
          "SupportsDirectStream": True,
          "SupportsDirectPlay": True,
          "IsInfiniteStream": False,
          "RequiresOpening": False,
          "RequiresClosing": False,
          "RequiresLooping": False,
          "SupportsProbing": False,
          "MediaStreams": [
            {
              "Codec": "mpeg4",
              "CodecTag": "FMP4",
              "TimeBase": "1/24",
              "CodecTimeBase": "1/24",
              "VideoRange": "SDR",
              "DisplayTitle": "480p MPEG4",
              "IsInterlaced": False,
              "BitRate": 2500431,
              "RefFrames": 1,
              "IsDefault": False,
              "IsForced": False,
              "Height": 480,
              "Width": 854,
              "AverageFrameRate": 24,
              "RealFrameRate": 24,
              "Profile": "Simple Profile",
              "Type": "Video",
              "AspectRatio": "16:9",
              "Index": 0,
              "IsExternal": False,
              "IsTextSubtitleStream": False,
              "SupportsExternalStream": False,
              "Protocol": "File",
              "PixelFormat": "yuv420p",
              "Level": 1,
              "IsAnamorphic": False
            },
            {
              "Codec": "ac3",
              "TimeBase": "1/56000",
              "CodecTimeBase": "1/48000",
              "DisplayTitle": "Dolby Digital 5.1",
              "IsInterlaced": False,
              "ChannelLayout": "5.1",
              "BitRate": 448000,
              "Channels": 6,
              "SampleRate": 48000,
              "IsDefault": False,
              "IsForced": False,
              "Type": "Audio",
              "Index": 1,
              "IsExternal": False,
              "IsTextSubtitleStream": False,
              "SupportsExternalStream": False,
              "Protocol": "File",
              "Level": 0
            },
            {
              "Codec": "srt",
              "Language": "eng",
              "DisplayTitle": "English (SRT)",
              "DisplayLanguage": "English",
              "IsInterlaced": False,
              "IsDefault": False,
              "IsForced": False,
              "Type": "Subtitle",
              "Index": 2,
              "IsExternal": True,
              "IsTextSubtitleStream": True,
              "SupportsExternalStream": True,
              "Path": "/var/lib/emby/metadata/library/04/049829ec5c2f41a1e627c2f4d51d7e73/big_buck_bunny_480p_surround-fix.en.srt",
              "Protocol": "File"
            }
          ],
          "Formats": [],
          "Bitrate": 2957650,
          "RequiredHttpHeaders": {},
          "ReadAtNativeFramerate": False
        }
      ],
      "RunTimeTicks": 5964580000,
      "IsFolder": False,
      "Type": "Movie",
      "ImageTags": {
        "Primary": "f6d517fe7402a4bbde69f36c16f672bf",
        "Logo": "a2f0e965628bc8a1d1087af522defa17"
      },
      "BackdropImageTags": [
        "606a215825d638a0c8eee975dd679b18"
      ],
      "MediaType": "Video"
    }
  ],
  "TotalRecordCount": 1
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
        self.assertEqual(self.items[0].duration_in_sec, 596.458)

    @patch('mediaServer.server.requests.get')
    def test_get_items(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.get_items_response
        self.item = self.testServer.get_item(item_id=5,fields="Path,MediaSources")
        self.assertIsInstance(self.item, Item)
        self.assertEqual(self.item.duration_in_sec, 596.458)

    @patch('mediaServer.server.requests.get')
    def test_download_item(self, mock_get):
        mock_get.return_value.status_code = 200
        item_to_dl = Item(id=5)
        download_rsp, content_type = self.testServer.download_item(item=item_to_dl)
        self.assertEqual(download_rsp, "item_5")



