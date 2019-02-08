from mediaServer.userpolicy import Policy
from mediaServer.userconfig import Configuration

class User(object):
    """Jellyfin user.

    Provides interface to create and modify users within the Jellyfin server (emby is also supported)

    :param
    """
    server = None
    AccessToken = None

    def __init__(self,
                 Name=None,
                 ServerId = None,
                 Id = None,
                 HasPassword = None,
                 HasConfiguredEasyPassword = None,
                 HasConfiguredPassword = None,
                 Policy = Policy(),
                 Configuration = Configuration(),
                 AccessToken = None,
                 server = None
                 ):
        self.Name = Name
        self.ServerId = ServerId
        self.Id = Id
        self.HasPassword = HasPassword
        self.HasConfiguredEasyPassword = HasConfiguredEasyPassword
        self.HasConfiguredPassword = HasConfiguredPassword
        self.Policy = Policy
        self.Configuration = Configuration
        if AccessToken is not None:
            self.AccessToken = AccessToken
        if server is not None:
            self.server = server

    def logout(self):
        self.server.logoutuser(userId=self.Id, AccessToken=self.AccessToken)

    def delete(self):
        self.server.deleteuser(userId=self.Id)

    def authenticate(self, password):
        getuser = self.server.authenticatebyname(self.Name, password=password)
        self.Name = getuser.Name
        self.ServerId = getuser.ServerId
        self.Id = getuser.Id
        self.HasPassword = getuser.HasPassword
        self.HasConfiguredEasyPassword = getuser.HasConfiguredEasyPassword
        self.HasConfiguredPassword = getuser.HasConfiguredPassword
        self.Policy = getuser.Policy
        self.Configuration = getuser.Configuration
        self.AccessToken = getuser.AccessToken

    def updatepassword(self, currentPw, newPw):
        self.server.updateuserpassword(userId=self.Id,
                                    AccessToken=self.AccessToken,
                                    currentPw=currentPw,
                                  newPw=newPw)