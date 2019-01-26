import json
import os.path
import logging

_log = logging.getLogger(__name__)

class mediaServer_config(object):
    protocol = 'http'
    host = '127.0.0.1'
    port = '8096'
    path = '/emby'
    user = 'MyEmbyUser'
    password = ''

    # constructor
    def __init__(self, cfg_dir='./cfg', cfg_file='mediaserver-config.json', cfg_default=False):
        self.cfg_dir = cfg_dir
        self.cfg_file = cfg_file
        self.cfg_default = cfg_default
        self.__configure()


    def __read_config(self):
        print('read config media server')
        with open('%s/%s' % (self.cfg_dir, self.cfg_file), 'r') as infile:
            cfg = json.load(infile)
            self.protocol = cfg['protocol']
            self.host = cfg['host']
            self.port = cfg['port']
            self.path = cfg['path']
            self.user = cfg['user']
        _log.error('%s/%s read successfully' % (self.cfg_dir, self.cfg_file))

    def __write_config(self):
        print("Storing config in " + self.cfg_dir +'/'+ self.cfg_file)
        if not os.path.isdir(self.cfg_dir):
            os.mkdir(self.cfg_dir)
        with open('%s/%s' % (self.cfg_dir, self.cfg_file), 'w') as outfile:
            data = {
                'protocol': self.protocol,
                'host': self.host,
                'port': self.port,
                'path': self.path,
                'user': self.user
            }
            json.dump(data, outfile, sort_keys=True, indent=2, separators=(',', ': '))
            _log.error('%s/%s written successfully' % (self.cfg_dir, self.cfg_file))

    # override set_config if youd like to gather user input another way i.e. user interface
    def __set_config(self, onlyPassword):
        print("Configuring media server connection...")
        if not onlyPassword:
            # gathering input from user should be done on the user layer
            # doing it here for the sake of time
            print("Press enter for defaults")
            self.protocol = input("Specify protocol (Default:http): ")
            if self.protocol != 'http' and self.protocol != 'https':
                self.protocol = 'http'
                self.host = input("Specify host (Default: 127.0.0.1): ")
            if not self.host:
                self.host = '127.0.0.1'
            self.port = input("Specify port (Default: 8096): ")
            if not self.port:
                self.port = '8096'
            self.path = input("Specify path (Default: /: ")
            if not self.path:
                self.path = ''
            self.user = input("Specify admin user: ")
            if self.user:  # ask for password if a user is specified in the config
                self.password = input("Specify admin password: ")
        if onlyPassword:
            if self.user:  # ask for password if a user is specified in the config, default config has no username specified
                self.password = input("Admin user Password needed to continue: ")


    def __configure(self):
        if not self.cfg_default: # default doesn't need to be read or written to file
            if os.path.isfile('%s/%s' % (self.cfg_dir, self.cfg_file)):
                self.__read_config()
                self.__set_config(onlyPassword=True)
            else:
                self.__set_config(onlyPassword=False)
                self.__write_config()

    def get_protocol(self):
        return self.protocol

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def get_path(self):
        return self.path

    def get_adminuser(self):
        return self.user

    def get_password(self):
        return self.password