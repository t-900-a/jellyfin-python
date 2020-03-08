from mediaServer.userhelper import UserHelper
from mediaServer.itemhelper import ItemHelper
from mediaServer.item import Item
from mediaServer.user import User

# from __init__ import __version__
__version__ = 1

from . import exceptions
from .exceptions import *
import requests
import socket
import json
import logging
import pprint

_log = logging.getLogger(__name__)


class MediaServer(object):
    userHelper = UserHelper()
    itemHelper = ItemHelper()
    url = None
    adminUser = None
    serverConfig = None
    tokenHeader = None
    adminUserId = None

    def __init__(self, myconfig):
        self.serverConfig = myconfig
        self.__configureserver()

    def __configureserver(self):
        self.url = '{protocol}://{host}:{port}{path}'.format(
            protocol=self.serverConfig.protocol,
            host=self.serverConfig.host,
            port=self.serverConfig.port,
            path=self.serverConfig.path)
        self.authenticateasadmin()

    def authenticateasadmin(self):
        """
        Log in as admin
        Stores token header for future API calls
        """
        self.adminUser = User(Name=self.serverConfig.user, server=self)
        self.adminUser.authenticate(password=self.serverConfig.password)
        self.tokenHeader = {'X-Emby-Token': self.adminUser.AccessToken}

    def authenticatebyname(self, username, password):
        """
        Log in as a specific username
        """
        method = '/Users/AuthenticateByName'

        xEmbyAuth = {
            'X-Emby-Authorization': 'Emby UserId="{UserId}", Client="{Client}", Device="{Device}", DeviceId="{DeviceId}", Version="{Version}", Token="""'.format(
                UserId="",  # not required, if it was we would have to first request the UserId from the username
                Client='account-automation',
                Device=socket.gethostname(),
                DeviceId=hash(socket.gethostname()),
                Version=__version__,
                Token=""  # not required
            )}

        data = {'Username': username, 'Password': password,
                'Pw': password}
        try:
            response = self.server_postrequest(hdr=xEmbyAuth, method=method, data=data)
            dictUser = response.get('User')
            dictUser['AccessToken'] = response.get('AccessToken')
            if dictUser is None:
                raise Exception
            return self.userHelper.toUserObj(dictUser=dictUser)
        except JellyfinUnauthorized as e:
            _log.warning('host: %s username: %s Authentication Failed' % (self.url, username))
        except Exception as e:
            _log.warning('host: %s username: %s Something happened, unable to authenticate' % (self.url, username))

    def authenticate(self, userid, password):
        """
        Authenicate user by user ID
        """
        # TODO manual testing then unit testing
        method = '/Users/{userid}/Authenticate'.format(userid=userid)
        data = {'Pw': password,
                'Password': password}

        try:
            response = self.server_postrequest(hdr=xEmbyAuth, method=method, data=data)
            dictUser = response.get('User')
            dictUser['AccessToken'] = response.get('AccessToken')
            return self.userHelper.toUserObj(dictUser=dictUser)
        except JellyfinUnauthorized as e:
            _log.warning('host: %s userid: %s Authentication Failed' % (self.url, userid))

    def getAdmin(self):
        """
        Get admin user object
        """
        return adminUser

    def getapikeys(self):
        """
        Get API keys
        """
        method = '/Auth/Keys'
        xEmbyAuth = {'X-Emby-Authorization': 'Token="{Token}"'.format(
            Token=self.adminUser.AccessToken
        )}
        try:
            response = self.server_getrequest(hdr=xEmbyAuth, method=method, data=None)
            return response['Items']
        except Exception as e:
            _log.warning('host: %s API Key Retrieval Failed' % (self.url))
            return []

    def logoutuser(self, userId):
        """
        Log out specific user ID
        """
        method = '/Sessions/Logout'
        xEmbyAuth = {
            'X-Emby-Authorization': 'Emby UserId="{UserId}", Client="{Client}", Device="{Device}", DeviceId="{DeviceId}", Version="{Version}", Token="{Token}"'.format(
                UserId=userId,
                Client='account-automation',
                Device=socket.gethostname(),
                DeviceId=hash(socket.gethostname()),
                Version=__version__,
                Token=self.adminUser.AccessToken
            )}
        try:
            response = self.server_postrequest(hdr=xEmbyAuth, method=method, data=None)
            self.adminUser.AccessToken = None
            return True
        except Exception as e:
            _log.warning('host: %s userId: %s Logout Failed' % (self.url, userId))
            _log.critical(type(e))
            _log.critical(e.args)
            _log.critical(e)

    def createuserbyname(self, username):
        """
        Create a new user with username
        """
        method = '/Users/New'
        data = {'Name': username}
        dictUser = self.server_postrequest(hdr=self.tokenHeader, method=method, data=data)
        _log.info('New user account created: {username}'.format(username=username))
        newuser = self.userHelper.toUserObj(dictUser=dictUser)
        newuser.server = self
        return newuser

    def deleteuser(self, userId):
        """
        Delete a user with user ID
        """
        method = '/Users/{Id}'.format(Id=userId)
        try:
            response = self.server_deleterequest(hdr=self.tokenHeader, method=method)
            return True
        except Exception as e:
            _log.warning('host: %s userId: %s User Deletion Failed' % (self.url, userId))
            _log.critical(type(e))
            _log.critical(e.args)
            _log.critical(e)

    def updateuserpolicy(self, user):
        """
        Update a user policy with User object
        """
        if self.adminUser.AccessToken is None:
            _log.error(
                __class__ + '.updateuserpolicy requires an admins AccessToken before ' + user.Name + ' can be updated.')
        method = '/Users/{Id}/Policy'.format(Id=user.Id)
        data = self.userHelper.todictPolicy(policyObj=user.Policy)
        try:
            response = self.server_postrequest(hdr=self.tokenHeader, method=method, data=data)
            return True
        except Exception as e:
            _log.warning('host: %s userId: %s User Policy Update Failed' % (self.url, userId))
            _log.critical(type(e))
            _log.critical(e.args)
            _log.critical(e)

    def updateuserconfig(self, user):
        """
        Update a user config with User object
        """
        if self.adminUser.AccessToken is None:
            _log.error(
                __class__ + '.updateuserconfig requires an admins AccessToken before ' + user.Name + ' can be updated.')
        method = '/Users/{Id}/Configuration'.format(Id=user.Id)
        data = self.userHelper.todictConfig(configObj=user.Configuration)
        try:
            response = self.server_postrequest(hdr=self.tokenHeader, method=method, data=data)
            return True
        except Exception as e:
            _log.warning('host: %s userId: %s User Config Update Failed' % (self.url, user.Id))
            _log.critical(type(e))
            _log.critical(e.args)
            _log.critical(e)

    def updateuserpassword(self, userId, currentPw, newPw):
        """
        Update a user password with user ID
        """
        if self.adminUser.AccessToken is None:
            _log.error(
                __class__ + '.updateuserpassword requires an AccessToken before password update for User:' + userId)

        method = '/Users/{Id}/Password'.format(Id=userId)
        data = {'Id': userId, 'CurrentPw': currentPw, 'NewPw': newPw}
        try:
            self.resetuserpassword(userId)  # must reset password first before setting new password
            self.server_postrequest(hdr=self.tokenHeader, method=method, data=data)
            _log.debug("Passsword updated successfully for user id: {user}".format(user=userId))
            return True
        except Exception as inst:
            _log.critical(type(inst))
            _log.critical(inst.args)
            _log.critical(inst)
            _log.debug("Password update failed for user id: {user}".format(user=userId))

    def resetuserpassword(self, userId):
        """
        Reset a user password with user ID
        """
        if self.adminUser.AccessToken is None:
            _log.error(
                __class__ + '.resetuserpassword requires an AccessToken before password reset for User:' + userId)

        method = '/Users/{Id}/Password'.format(Id=userId)
        data = {'Id': userId, 'ResetPassword': 'true'}
        try:
            self.server_postrequest(hdr=self.tokenHeader, method=method, data=data)
            _log.debug("Password reset successfully for user id: {user}".format(user=userId))
            return True
        except Exception as inst:
            _log.critical(type(inst))
            _log.critical(inst.args)
            _log.critical(inst)
            _log.debug("Password reset failed for user id: {user}".format(user=userId))

    def getusers(self, IsHidden=str(''), IsDisabled=str(''), IsGuest=str('')):
        """
        Get all users
        Optional filters
        """
        method = '/Users?IsHidden={Hidden}&IsDisabled={Disabled}&IsGuest={Guest}' \
            .format(Hidden=IsHidden,
                    Disabled=IsDisabled,
                    Guest=IsGuest)
        try:
            dictUsers = self.server_getrequest(hdr=self.tokenHeader, method=method)
        except Exception as inst:
            _log.critical(type(inst))
            _log.critical(inst.args)
            _log.critical(inst)
            _log.debug("Cannot retrieve users from server: {server}".format(server=self.url))

        serverusers = []
        for dictUser in dictUsers:
            serverusers.append(self.userHelper.toUserObj(dictUser=dictUser))

        return serverusers

    # https://github.com/MediaBrowser/Emby/wiki/Browsing-the-Library
    def get_items(self, artist_type=str(''), is_hd=str(''), recursive=str('')) -> list:
        """
        Get items from server
        Optional filters
        """
        method = f"/Items?Recursive={recursive}&IsHD={is_hd}&ArtistType={artist_type}"
        dict_items = self.server_getrequest(hdr=self.tokenHeader, method=method)
        try:
            dict_items = self.server_getrequest(hdr=self.tokenHeader, method=method)
        except Exception as inst:
            _log.critical(type(inst))
            _log.critical(inst.args)
            _log.critical(inst)
            _log.debug("Cannot retrieve items from server: {server}".format(server=self.url))

        items = []
        for dict_item in dict_items['Items']:
            items.append(self.itemHelper.to_item_obj(dict_item=dict_item))
        return items

    def download_item(self, item: Item) -> bool:
        dl_success = False
        method = f"/Items/{str(item.id)}/Download"
        try:
            rsp = self.server_download_item(hdr=self.tokenHeader, method=method, local_filename=f"item_{str(item.id)}")
        except Exception as inst:
            _log.critical(type(inst))
            _log.critical(inst.args)
            _log.critical(inst)
            _log.debug("Cannot download item from server: {server}".format(server=self.url))

        return rsp

    def getlibraryinfo(self):
        """
        Get info of all libraries
        """
        info = {}
        method = '/Items/Counts'
        try:
            info = self.server_getrequest(hdr=self.tokenHeader, method=method)
            method = '/Library/MediaFolders'
            info['Items'] = self.server_getrequest(hdr=self.tokenHeader, method=method)['Items']
        except Exception as inst:
            _log.critical(type(inst))
            _log.critical(inst.args)
            _log.critical(inst)
            _log.debug("Cannot retrieve library counts from server: {server}".format(server=self.url))

        return info

    def search(self, keyword):
        """
        Get media search results
        """
        try:
            method = '/Search/Hints?{}'.format(keyword)
            return self.server_getrequest(hdr=self.tokenHeader, method=method)['SearchHints']
        except Exception as inst:
            _log.critical(type(inst))
            _log.critical(inst.args)
            _log.critical(inst)
            _log.debug("Cannot retrieve search results of custom query from server: {server}".format(server=self.url))

    def customsql(self, query=str(''), usernamesNotIds=str('')):
        """
        Execute custom SQL query
        """
        method = '/user_usage_stats/submit_custom_query'
        data = {'CustomQueryString': '"{Query}"', 'ReplaceUserId': '"{replace}"'.format(
            Query=query,
            replace=usernamesNotIds
        )}
        try:
            results = self.server_getrequest(hdr=self.tokenHeader, method=method, data=data)
        except Exception as inst:
            _log.critical(type(inst))
            _log.critical(inst.args)
            _log.critical(inst)
            _log.debug("Cannot retrieve results of custom query from server: {server} \nQuery: {customQuery}".format(
                server=self.url, customQuery=query))

        return results

    def makeplaylist(self, name):
        """
        Create a playlist
        """
        try:
            method = '/Playlists?Name={}'.format(name)
            response = self.server_postrequest(hdr=self.tokenHeader, method=method)
        except Exception as inst:
            _log.critical(type(inst))
            _log.critical(inst.args)
            _log.critical(inst)
            _log.debug("Cannot make playlist on server: {server}".format(server=self.url))

        return response

    def addtoplaylist(self, playlistId, itemIds):
        """
        Add items to playlist
        itemIds = []
        """
        try:
            itemlist = ','.join(itemIds)
            method = '/Playlists/{}/Items?{}'.format(playlistId, itemlist)
            response = self.server_postrequest(hdr=self.tokenHeader, method=method)
        except Exception as inst:
            _log.critical(type(inst))
            _log.critical(inst.args)
            _log.critical(inst)
            _log.debug("Cannot add items to playlist on server: {server}".format(server=self.url))

        return response

    def updaterating(self, userId, itemId, upvote=True):
        """
        Update rating for a media item
        """
        try:
            method = '/Users/{}/Items/{}/Rating?Likes={}'.format(userId, itemId, ("true" if upvote else "false"))
            response = self.server_postrequest(hdr=self.tokenHeader, method=method)
        except Exception as inst:
            _log.critical(type(inst))
            _log.critical(inst.args)
            _log.critical(inst)
            _log.debug(
                "Cannot update rating for itemId {} for userId {} on server: {}".format(itemId, userId, self.url))

        return response

    def info(self):
        """
        Get server system info
        """
        method = '/System/Info'
        try:
            info = self.server_getrequest(hdr=self.tokenHeader, method=method)
        except Exception as inst:
            _log.critical(type(inst))
            _log.critical(inst.args)
            _log.critical(inst)
            _log.debug("Cannot get info for server: {server}".format(server=self.url))

        return info

    def ping(self):
        """
        Ping the server
        """
        info = self.info()  # '/System/Ping' not working for some reason
        if info:
            return True
        else:
            return False

    def restart(self):
        """
        Restart the server
        """
        method = '/System/Restart'
        try:
            response = self.server_postrequest(hdr=self.tokenHeader, method=method)
            return True
        except exceptions as e:
            _log.critical(e)

    def shutdown(self):
        """
        Shutdown the server
        """
        method = '/System/Shutdown'
        try:
            response = self.server_postrequest(hdr=self.tokenHeader, method=method)
            return True
        except Exception as e:
            return False

    def server_postrequest(self, hdr, method, data=None):
        hdr = {'accept': 'application/json', 'Content-Type': 'application/json', **hdr}
        _log.critical(u"Method: {method}\nHeaders:\n{headers}\nData:\n{data}".format(
            method=method,
            headers=hdr,
            data=data
        ))
        rsp = requests.post(self.url + method, headers=hdr, data=json.dumps(data))

        if rsp.status_code == 400:
            raise exceptions.JellyfinBadRequest(rsp.content)
        if rsp.status_code == 401:
            raise exceptions.JellyfinUnauthorized(rsp.content)
        if rsp.status_code == 403:
            raise exceptions.JellyfinForbidden(rsp.content)
        if rsp.status_code == 404:
            raise exceptions.JellyfinResourceNotFound(rsp.content)
        if rsp.status_code >= 500 and rsp.status_code < 600:
            raise exceptions.JellyfinServerError(rsp.content)
        if rsp.status_code != 200 and rsp.status_code != 204:
            raise exceptions.JellyfinException("Invalid HTTP status {code} for method {method}.".format(
                code=rsp.status_code,
                method=method
            ))
        if rsp.content != b'':
            result = rsp.json()
        else:
            result = rsp.status_code
        _ppresult = pprint.pformat(result)
        _log.critical(u"Result:\n{result}".format(result=_ppresult))
        return result

    def server_getrequest(self, hdr, method, data=None):
        hdr = {'accept': 'application/json', **hdr}
        _log.critical(u"Method: {method}\nHeaders:\n{headers}\nData:\n{data}".format(
            method=method,
            headers=hdr,
            data=data
        ))
        rsp = requests.get(self.url + method, headers=hdr, data=json.dumps(data))

        if rsp.status_code == 400:
            raise exceptions.JellyfinBadRequest(rsp.content)
        if rsp.status_code == 401:
            raise exceptions.JellyfinUnauthorized(rsp.content)
        if rsp.status_code == 403:
            raise exceptions.JellyfinForbidden(rsp.content)
        if rsp.status_code == 404:
            raise exceptions.JellyfinResourceNotFound(rsp.content)
        if rsp.status_code >= 500 and rsp.status_code < 600:
            raise exceptions.JellyfinServerError(rsp.content)
        if rsp.status_code != 200 and rsp.status_code != 204:
            raise exceptions.JellyfinException("Invalid HTTP status {code} for method {method}.".format(
                code=rsp.status_code,
                method=method
            ))
        if rsp.content != b'':
            result = rsp.json()
        else:
            result = rsp.status_code
        _ppresult = pprint.pformat(result)
        _log.critical(u"Result:\n{result}".format(result=_ppresult))
        return result

    def server_download_item(self, hdr, method, local_filename):
        hdr = {'accept': 'application/json', **hdr}
        _log.critical(u"Method: {method}\nHeaders:\n{headers}\nData:\n{data}".format(
            method=method,
            headers=hdr,
            data=None
        ))

        with requests.get(self.url + method, headers=hdr, data=None, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        # f.flush()
        return local_filename

    def server_deleterequest(self, hdr, method):
        hdr = {'accept': '*/*', **hdr}
        _log.critical(u"Method: {method}\nHeaders:\n{headers}".format(
            method=method,
            headers=hdr
        ))

        rsp = requests.delete(url=self.url + method, headers=hdr)

        if rsp.status_code == 400:
            raise exceptions.JellyfinBadRequest(rsp.content)
        if rsp.status_code == 401:
            raise exceptions.JellyfinUnauthorized(rsp.content)
        if rsp.status_code == 403:
            raise exceptions.JellyfinForbidden(rsp.content)
        if rsp.status_code == 404:
            raise exceptions.JellyfinResourceNotFound(rsp.content)
        if rsp.status_code >= 500 and rsp.status_code < 600:
            raise exceptions.JellyfinServerError(rsp.content)
        if rsp.status_code != 200 and rsp.status_code != 204:
            raise exceptions.JellyfinException("Invalid HTTP status {code} for method {method}.".format(
                code=rsp.status_code,
                method=method
            ))
        if rsp.content != b'':
            result = rsp.json()
        else:
            result = rsp.status_code
        _ppresult = pprint.pformat(result)
        _log.critical(u"Result:\n{result}".format(result=_ppresult))
        return result
