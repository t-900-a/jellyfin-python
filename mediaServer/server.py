from mediaServer.userhelper import UserHelper
from mediaServer.user import User
#from __init__ import __version__
__version__= 1
from . import exceptions
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
        
    def tokenHeader(self):
        return {'X-Emby-Token:' self.adminUser.AccessToken}

    def authenticateasadmin(self):
        self.adminUser = User(Name=self.serverConfig.user, server=self)
        self.adminUser.authenticate(self.serverConfig.password)

    def authenticatebyname(self, username, password):
        method = '/Users/AuthenticateByName'

        xEmbyAuth = {'X-Emby-Authorization': 'Emby UserId="{UserId}", Client="{Client}", Device="{Device}", DeviceId="{DeviceId}", Version="{Version}", Token="""'.format(
            UserId="", # not required, if it was we would have to first request the UserId from the username
            Client='account-automation',
            Device=socket.gethostname(),
            DeviceId=hash(socket.gethostname()),
            Version=__version__,
            Token="" # not required
        )}

        data = {'Username': username, 'Password': password,
                'Pw': password}
        try:
            response = self.server_request(hdr=xEmbyAuth, method=method, data=data)
            dictUser = response.get('User')
            dictUser['AccessToken'] = response.get('AccessToken')
        except exceptions as e:
            if type(e) == exceptions.JellyfinUnauthorized:
                _log.warning('host: %s username: %s Authentication Failed' % (self.url, username))
        return self.userHelper.toUserObj(dictUser=dictUser)

    def authenticate(self, userid, password):
        #TODO manual testing then unit testing
        method = '/Users/{userid}/Authenticate'.format(userid=userid)
        data = {'Pw': password,
                'Password': password}

        try:
            response = self.server_request(hdr=xEmbyAuth, method=method, data=data)
            dictUser = response.get('User')
            dictUser['AccessToken'] = response.get('AccessToken')
        except exceptions as e:
            if type(e) == exceptions.JellyfinUnauthorized:
                _log.warning('host: %s userid: %s Authentication Failed' % (self.url, userid))
        return self.userHelper.toUserObj(dictUser=dictUser)
    
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
        xEmbyAuth = {'X-Emby-Authorization': 'Emby UserId="{UserId}", Client="{Client}", Device="{Device}", DeviceId="{DeviceId}", Version="{Version}", Token="{Token}"'.format(
            UserId=userId,
            Client='account-automation',
            Device=socket.gethostname(),
            DeviceId=hash(socket.gethostname()),
            Version=__version__,
            Token= self.adminUser.AccessToken
        )}
        try:
            response = self.server_request(hdr=xEmbyAuth, method=method, data=None)
            AccessToken = None
            return True
        except Exception as e:
            _log.warning('host: %s userId: %s Logout Failed' % (self.url, userId))
            _log.critical(type(e))
            _log.critical(e.args)
            _log.critical(e)

    def createuserbyname(self, username):
        method = '/Users/New'
        data = {'Name': username}
        dictUser = self.server_request(hdr=self.tokenHeader(), method=method, data=data)
        _log.info('New user account created: {username}'.format(username=username))
        newuser = self.userHelper.toUserObj(dictUser=dictUser)
        newuser.server = self
        return newuser

    def deleteuser(self, userId):
        method = '/Users/{Id}'.format(Id=userId)
        try:
            response = self.server_delete(hdr=self.tokenHeader(), method=method)
            return True
        except Exception as e:
            _log.warning('host: %s userId: %s User Deletion Failed' % (self.url, userId))
            _log.critical(type(e))
            _log.critical(e.args)
            _log.critical(e)

    def updateuserpolicy(self, user):
        if self.adminUser.AccessToken is None:
            _log.error(__class__+'.updateuserpolicy requires an admins AccessToken before '+user.Name+' can be updated.')
        method = '/Users/{Id}/Policy'.format(Id=user.Id)
        data = self.userHelper.todictPolicy(policyObj=user.Policy)
        try:
            response = self.server_request(hdr=self.tokenHeader(), method=method, data=data)
            return True
        except Exception as e:
            _log.warning('host: %s userId: %s User Policy Update Failed' % (self.url, userId))
            _log.critical(type(e))
            _log.critical(e.args)
            _log.critical(e)

    def updateuserconfig(self, user):
        if self.adminUser.AccessToken is None:
            _log.error(__class__+'.updateuserconfig requires an admins AccessToken before '+user.Name+' can be updated.')
        method = '/Users/{Id}/Configuration'.format(Id=user.Id)
        data = self.userHelper.todictConfig(configObj=user.Configuration)
        try:
            response = self.server_request(hdr=self.tokenHeader(), method=method, data=data)
            return True
        except Exception as e:
            _log.warning('host: %s userId: %s User Config Update Failed' % (self.url, userId))
            _log.critical(type(e))
            _log.critical(e.args)
            _log.critical(e)

    def updateuserpassword(self, AccessToken, userId, currentPw, newPw):
        if AccessToken is None:
            _log.error(__class__+'.updateuserpassword requires an AccessToken before password update for User:'+userId)

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

    def getusers(self, IsHidden = str(''), IsDisabled = str(''), IsGuest = str('')):
        method = '/Users?IsHidden={Hidden}&IsDisabled={Disabled}&IsGuest={Guest}'\
            .format(Hidden=IsHidden,
                     Disabled=IsDisabled,
                     Guest=IsGuest)
        try:
            dictUsers = self.server_getrequest(hdr=self.tokenHeader(), method=method)
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
            info = self.server_getrequest(hdr=self.tokenHeader(), method=method)
            method = '/Library/MediaFolders'
            info['Items'] = self.server_getrequest(hdr=self.tokenHeader(), method=method)['Items']
        except Exception as inst:
            _log.critical(type(inst))
            _log.critical(inst.args)
            _log.critical(inst)
            _log.debug("Cannot retrieve library counts from server: {server}".format(server=self.url))
        
        return info
    
    def searchMovie(self, name, year = 0, itemId = 0, metadataLang = '', metadataCountyCode = ''):
        method = '/Items/RemoteSearch/Movie'
        data = {
            "SearchInfo": {
                "Name": name,
                "MetadataLanguage": metadataLang,
                "MetadataCountryCode": metadataCountyCode,
                "ProviderIds": {
                  "additionalProp1": "",
                  "additionalProp2": "",
                  "additionalProp3": ""
                },
                "Year": year,
                "IndexNumber": 0,
                "ParentIndexNumber": 0,
                "PremiereDate": "",
                "IsAutomated": true
            },
            "ItemId": itemId,
            "SearchProviderName": "",
            "IncludeDisabledProviders": true
        }
        try:
            results = self.server_request(hdr=self.tokenHeader(), method=method, data=data)
        except Exception as inst:
            _log.critical(type(inst))
            _log.critical(inst.args)
            _log.critical(inst)
            _log.debug("Cannot retrieve movie search results from server: {server}".format(server=self.url))
            
        return results
    
    def searchTv(self, name, year = 0, airDate = "", itemId = 0, metadataLang = '', metadataCountyCode = ''):
        method = '/Items/RemoteSearch/Series'
        data = {
            "SearchInfo": {
                "EpisodeAirDate": airDate,
                "Name": name,
                "MetadataLanguage": metadataLang,
                "MetadataCountryCode": metadataCountyCode,
                "ProviderIds": {
                  "additionalProp1": "",
                  "additionalProp2": "",
                  "additionalProp3": ""
                },
                "Year": year,
                "IndexNumber": 0,
                "ParentIndexNumber": 0,
                "PremiereDate": "",
                "IsAutomated": true
            },
            "ItemId": itemId,
            "SearchProviderName": "",
            "IncludeDisabledProviders": true
        }
        try:
            results = self.server_request(hdr=self.tokenHeader(), method=method, data=data)
        except Exception as inst:
            _log.critical(type(inst))
            _log.critical(inst.args)
            _log.critical(inst)
            _log.debug("Cannot retrieve movie search results from server: {server}".format(server=self.url))
            
        return results
    
    def searchAlbum(self, albumName, artistNames = [], songName = "", year = 0, itemId = 0, metadataLang = '', metadataCountyCode = ''):
        method = '/Items/RemoteSearch/MusicAlbum'
        data = {
            "SearchInfo": {
                "AlbumArtists": artistNames,
                "SongInfos": [
                    {
                        "AlbumArtists": artistNames,
                        "Album": albumName,
                        "Artists": artistNames,
                        "Name": songName,
                        "MetadataLanguage": metadataLang,
                        "MetadataCountryCode": metadataCountyCode,
                        "ProviderIds": {
                          "additionalProp1": "",
                          "additionalProp2": "",
                          "additionalProp3": ""
                        },
                        "Year": year,
                        "IndexNumber": 0,
                        "ParentIndexNumber": 0,
                        "PremiereDate": "",
                        "IsAutomated": true
                    }
                ]
                "Name": albumName,
                "MetadataLanguage": metadataLang,
                "MetadataCountryCode": metadataCountyCode,
                "ProviderIds": {
                  "additionalProp1": "",
                  "additionalProp2": "",
                  "additionalProp3": ""
                },
                "Year": year,
                "IndexNumber": 0,
                "ParentIndexNumber": 0,
                "PremiereDate": "",
                "IsAutomated": true
            },
            "ItemId": itemId,
            "SearchProviderName": "",
            "IncludeDisabledProviders": true
        }
        try:
            results = self.server_request(hdr=self.tokenHeader(), method=method, data=data)
        except Exception as inst:
            _log.critical(type(inst))
            _log.critical(inst.args)
            _log.critical(inst)
            _log.debug("Cannot retrieve movie search results from server: {server}".format(server=self.url))
            
        return results
    
    def searchArtist(self, name, year = 0, itemId = 0, metadataLang = '', metadataCountyCode = ''):
        method = '/Items/RemoteSearch/MusicArtist'
        data = {
            "SearchInfo": {
                "Name": name,
                "MetadataLanguage": metadataLang,
                "MetadataCountryCode": metadataCountyCode,
                "ProviderIds": {
                  "additionalProp1": "",
                  "additionalProp2": "",
                  "additionalProp3": ""
                },
                "Year": year,
                "IndexNumber": 0,
                "ParentIndexNumber": 0,
                "PremiereDate": "",
                "IsAutomated": true
            },
            "ItemId": itemId,
            "SearchProviderName": "",
            "IncludeDisabledProviders": true
        }
        try:
            results = self.server_request(hdr=self.tokenHeader(), method=method, data=data)
        except Exception as inst:
            _log.critical(type(inst))
            _log.critical(inst.args)
            _log.critical(inst)
            _log.debug("Cannot retrieve movie search results from server: {server}".format(server=self.url))
            
        return results
    
    def search(self, keyword, year = 0, airDate = '', itemId = 0, metadataLang = '', metadataCountyCode = ''):
        results = {}
        results['Movies'] = self.searchMovie(keyword, year, itemId, metadataLang, metadataCountryCode)
        results['Series'] = self.searchTv(keyword, year, airDate, itemId, metadataLang, metadataCountryCode)
        results['Albums'] = self.searchAlbum(albumName = keyword, year=year, itemId = itemId, metadataLang = metadataLang, metadataCountryCode = metadataCountryCode) # keyword is album name
        results['Albums'].update(self.searchAlbum(artistNames = [keyword], year=year, itemId = itemId, metadataLang = metadataLang, metadataCountryCode = metadataCountryCode)) # keyword is artist name
        results['Artists'] = self.searchArtist(keyword, year, itemId, metadataLang, metadataCountryCode)
        
        return results
    
    def customsql(self, query = str(''), usernamesNotIds = str('')):
        method = '/user_usage_stats/submit_custom_query'
        data = {'CustomQueryString': '"{Query}"', 'ReplaceUserId': '"{replace}"'.format(
            Query = query,
            replace = usernameNotIds
        )}
        try:
            results = self.server_getrequest(hdr=self.tokenHeader(), method=method, data=data)
        except Exception as inst:
            _log.critical(type(inst))
            _log.critical(inst.args)
            _log.critical(inst)
            _log.debug("Cannot retrieve results of custom query from server: {server} \nQuery: {customQuery}".format(server=self.url, customQuery=query))
            
        return results
    
    def info(self):
        method = '/System/Info'
        try:
            info = self.server_getrequest(hdr=self.tokenHeader(), method=method)
        except Exception as inst:
            _log.critical(type(inst))
            _log.critical(inst.args)
            _log.critical(inst)
            _log.debug("Cannot get info for server: {server}".format(server=self.url))
        
        return info
    
    def ping(self):
        info = self.info() # '/System/Ping' not working for some reason
        if info:
            return True
        else:
            return False
        
    def restart(self):
        method = '/System/Restart'
        try:
            response = self.server_request(hdr=self.tokenHeader(), method=method)
            return True
        except exceptions as e:
            return False
        
   def shutdown(self):
        method = '/System/Shutdown'
        try:
            response = self.server_request(hdr=self.tokenHeader(), method=method)
            return True
        except exceptions as e:
            return False
        
    def server_request(self, hdr, method, data=None):
        hdr = {'accept': 'application/json', 'Content-Type': 'application/json', **hdr}
        _log.critical(u"Method: {method}\nHeaders:\n{headers}\nData:\n{data}".format(
            method = method,
            headers = hdr,
            data = data
        ))
        rsp = requests.post(self.url+method, headers=hdr, data=json.dumps(data))

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

        rsp = requests.delete(url=self.url+method, headers=hdr)

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
