from mediaServer.userhelper import UserHelper
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
        self.adminUser = User(Name=self.serverConfig.user, server=self)
        self.adminUser.authenticate(self.serverConfig.password)

    def authenticatebyname(self, username, password):
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
            response = self.server_request(hdr=xEmbyAuth, method=method, data=data)
            dictUser = response.get('User')
            dictUser['AccessToken'] = response.get('AccessToken')
            self.tokenHeader = {'X-Emby-Token:': self.adminUser.AccessToken}
            if dictUser['User']['Policy']['isAdministrator'] == 'true':
                adminUserId = dictUser['User']['Id']
            return self.userHelper.toUserObj(dictUser=dictUser)
        except JellyfinUnauthorized as e:
            _log.warning('host: %s username: %s Authentication Failed' % (self.url, username))

    def authenticate(self, userid, password):
        # TODO manual testing then unit testing
        method = '/Users/{userid}/Authenticate'.format(userid=userid)
        data = {'Pw': password,
                'Password': password}

        try:
            response = self.server_request(hdr=xEmbyAuth, method=method, data=data)
            dictUser = response.get('User')
            dictUser['AccessToken'] = response.get('AccessToken')
            self.tokenHeader = {'X-Emby-Token:': self.adminUser.AccessToken}
            if dictUser['User']['Policy']['isAdministrator'] == 'true':
                adminUserId = dictUser['User']['Id']
            return self.userHelper.toUserObj(dictUser=dictUser)
        except JellyfinUnauthorized as e:
            _log.warning('host: %s userid: %s Authentication Failed' % (self.url, userid))

    def getAdmin(self):
        return adminUser

    def getapikeys(self):
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
            response = self.server_request(hdr=xEmbyAuth, method=method, data=None)
            self.adminUser.AccessToken = None
            return True
        except Exception as e:
            _log.warning('host: %s userId: %s Logout Failed' % (self.url, userId))
            _log.critical(type(e))
            _log.critical(e.args)
            _log.critical(e)

    def createuserbyname(self, username):
        method = '/Users/New'
        data = {'Name': username}
        dictUser = self.server_request(hdr=self.tokenHeader, method=method, data=data)
        _log.info('New user account created: {username}'.format(username=username))
        newuser = self.userHelper.toUserObj(dictUser=dictUser)
        newuser.server = self
        return newuser

    def deleteuser(self, userId):
        method = '/Users/{Id}'.format(Id=userId)
        try:
            response = self.server_delete(hdr=self.tokenHeader, method=method)
            return True
        except Exception as e:
            _log.warning('host: %s userId: %s User Deletion Failed' % (self.url, userId))
            _log.critical(type(e))
            _log.critical(e.args)
            _log.critical(e)

    def updateuserpolicy(self, user):
        if self.adminUser.AccessToken is None:
            _log.error(
                __class__ + '.updateuserpolicy requires an admins AccessToken before ' + user.Name + ' can be updated.')
        method = '/Users/{Id}/Policy'.format(Id=user.Id)
        data = self.userHelper.todictPolicy(policyObj=user.Policy)
        try:
            response = self.server_request(hdr=self.tokenHeader, method=method, data=data)
            return True
        except Exception as e:
            _log.warning('host: %s userId: %s User Policy Update Failed' % (self.url, userId))
            _log.critical(type(e))
            _log.critical(e.args)
            _log.critical(e)

    def updateuserconfig(self, user):
        if self.adminUser.AccessToken is None:
            _log.error(
                __class__ + '.updateuserconfig requires an admins AccessToken before ' + user.Name + ' can be updated.')
        method = '/Users/{Id}/Configuration'.format(Id=user.Id)
        data = self.userHelper.todictConfig(configObj=user.Configuration)
        try:
            response = self.server_request(hdr=self.tokenHeader, method=method, data=data)
            return True
        except Exception as e:
            _log.warning('host: %s userId: %s User Config Update Failed' % (self.url, userId))
            _log.critical(type(e))
            _log.critical(e.args)
            _log.critical(e)

    def updateuserpassword(self, AccessToken, userId, currentPw, newPw):
        if AccessToken is None:
            _log.error(
                __class__ + '.updateuserpassword requires an AccessToken before password update for User:' + userId)

        method = '/Users/{Id}/Password'.format(Id=userId)
        tokenHeader = {'X-Emby-Token': AccessToken}
        data = {'Id': userId, 'CurrentPw': currentPw, 'NewPw': newPw}
        try:
            self.server_request(hdr=tokenHeader, method=method, data=data)
            _log.debug("Passsword updated successfully for user id: {user}".format(user=userId))
            return True
        except Exception as inst:
            _log.critical(type(inst))
            _log.critical(inst.args)
            _log.critical(inst)
            _log.debug("Password update failed for user id: {user}".format(user=userId))

    def getusers(self, IsHidden=str(''), IsDisabled=str(''), IsGuest=str('')):
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

    def getlibraryinfo(self):
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

    def search(self, Name='', Ids='', FolderName='', Years='', IsPlayed='', Artists='', Albums='', Person='',
               Studios='', MinPremiereDate='', MaxPremiereDate='', MaxMPAARating='', MinCommunityRating='',
               MinCriticRating='', IsHD='', Is3D='', IsMissing='', IsUnaired='',
               Fields=['ParentId', 'DateCreated', 'SortName'], ExcludeItemTypes='', SortBy='', SortOrder='Descending',
               Limit=''):
        folderId = ''
        try:
            method = '/User/{UserID}/Items'
            folders = self.server_getrequest(hdr=self.tokenHeader, method=method)
            for f in folders['Items']:
                if f['Name'] == FolderName:
                    folderId = f['Id']
                    break
            s = ","
            t = "|"
            method = '/User/{UserId}/Items?{name}&{ids}&{folderId}&{years}&{isPlayed}&{artists}&{albums}&{person}&{studios}&{minPremiereDate}&{maxPremiereDate}&{maxMPAARating}&{minCommRat}&{minCritRat}&{HD}&{threeD}&{missing}&{unaired}&{fields}&{exclude}&{sortBy}&{order}&{limit}'.format(
                name="NameStartsWith=" + Name,
                ids="Ids=" + s.join(Ids),
                folderId=folderId,
                years="Years=" + s.join(Years),
                isPlayed="IsPlayed=" + IsPlayed,
                artists="Artists=" + t.join(Artists),
                albums="Albums=" + t.join(Albums),
                person="Person=" + Person,
                studios="Studios=" + t.join(Studios),
                minPremiereDate="MinPremiereDate=" + MinPremiereDate,
                maxPremiereDate="MaxPremiereDate=" + MaxPremiereDate,
                maxMPAARating="MaxMPAARating=" + MaxMPAARating,
                minCommRat="MinCommunityRating=" + MinCommunityRating,
                minCritRat="MinCriticRating=" + MinCriticRating,
                HD="IsHD=" + str(IsHD),
                threeD="Is3D=" + str(Is3D),
                missing="IsMissing=" + str(IsMissing),
                unaired="IsUnaired=" + str(IsUnaired),
                fields="Fields=" + s.join(Fields),
                exclude="ExcludeItemTypes=" + s.join(ExcludeItemTypes),
                sortBy="SortBy=" + s.join(SortBy),
                order="SortOrder=" + SortOrder,
                limit="Limit=" + str(Limit)
            )
            return self.server_getrequest(hdr=self.tokenHeader, method=method)
        except Exception as inst:
            _log.critical(type(inst))
            _log.critical(inst.args)
            _log.critical(inst)
            _log.debug("Cannot retrieve search results of custom query from server: {server}".format(server=self.url))

    def customsql(self, query=str(''), usernamesNotIds=str('')):
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

    def info(self):
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
        info = self.info()  # '/System/Ping' not working for some reason
        if info:
            return True
        else:
            return False

    def restart(self):
        method = '/System/Restart'
        try:
            response = self.server_request(hdr=self.tokenHeader, method=method)
            return True
        except exceptions as e:
            _log.critical(e)

    def shutdown(self):
        method = '/System/Shutdown'
        try:
            response = self.server_request(hdr=self.tokenHeader, method=method)
            return True
        except Exception as e:
            return False


    def server_request(self, hdr, method, data=None):
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


    def server_delete(self, hdr, method):
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
