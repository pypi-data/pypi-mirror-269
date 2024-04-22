import os
import sys
import errno
import logging
import configparser
from os.path import join as make_path
import etcd3
from enum import Enum

class Provider(Enum):
        AUTO = 0
        ETCD = 1,
        FILE = 2,

class Config(object):
    # region members

    _logformat = '%(asctime)s : %(levelname)s - %(filename)s (line: %(lineno)d) %(funcName)s() -> %(message)s'
    _rundir_ = 'run'
    _tmpdir_ = 'tmp'
    _etcd_host = os.getenv('ETCD_HOST', '')
    _etcd_port = int(os.getenv('ETCD_PORT', 2379))
    _etcd_root = os.getenv('ETCD_ROOT', '/')
    _provider = Provider.AUTO

    WAR_OPTIONVAL = 'Unable to parse value for option [{0}::{1}].'
    ERR_PARSEFAIL = 'Error parsing config file.'

    # endregion

    # region properties

    @property
    def apphost(self) -> str:
        return self._host

    @property
    def appport(self) -> int:
        return self._port

    @property
    def appuser(self) -> str:
        return self._user

    @property
    def apppass(self) -> str:
        return self._pass

    @property
    def etcdctl(self) -> any:
        if not self._provider != Provider.ETCD: raise NotImplementedError
        return etcd3.client(host= Config._etcd_host,
            port= Config._etcd_port)

    @property
    def s3_host(self) -> str:
        if not self._s3: raise NotImplementedError
        return self._s3['host']

    @property
    def s3_port(self) -> int:
        if not self._s3: raise NotImplementedError
        return self._s3['port']

    @property
    def s3_tls(self) -> str:
        if not self._s3: raise NotImplementedError
        return self._s3['tls']
    
    @property
    def mq_host(self) -> str:
        if not self._mq: raise NotImplementedError
        return self._mq['host']

    @property
    def mq_port(self) -> int:
        if not self._mq: raise NotImplementedError
        return self._mq['port']

    @property
    def mq_binding_exchange(self) -> str:
        if not self._mq: raise NotImplementedError
        return self._mq['binding_exchange']

    @property
    def mq_binding_key(self) -> str:
        if not self._mq: raise NotImplementedError
        return self._mq['binding_key']

    @property
    def mq_posting_exchange(self) -> str:
        if not self._mq: raise NotImplementedError
        return self._mq['posting_exchange']

    @property
    def mq_routing_key(self) -> str:
        if not self._mq: raise NotImplementedError
        return self._mq['routing_key']

    @property
    def mqtt_host(self) -> str:
        if not self._mqtt: raise NotImplementedError
        return self._mqtt['host']

    @property
    def mqtt_port(self) -> int:
        if not self._mqtt: raise NotImplementedError
        return self._mqtt['port']

    @property
    def mqtt_topic(self) -> str:
        if not self._mqtt: raise NotImplementedError
        return self._mqtt['topic']

    @property
    def mqtt_value(self) -> str:
        if not self._mqtt: raise NotImplementedError
        return self._mqtt['value']

    # endregion
    
    # region methods

    def __init__(self, provider: Provider = Provider.AUTO):
        if provider == Provider.AUTO: provider = Provider.FILE if not Config._etcd_host else Provider.ETCD
        Config._provider = provider

        # base path; all other folders will be relative to this path
        self._moddir = os.path.dirname(
            sys.modules[self.__class__.__module__].__file__)

        # the run folder; if not available make one
        self._rundir = make_path(self._moddir, Config._rundir_)
        if not os.path.isdir(self._rundir):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self._rundir)

        # temp path; if not available make one
        self._tmpdir = make_path(self._rundir, Config._tmpdir_)
        if not os.path.isdir(self._tmpdir):
            os.makedirs(self._tmpdir)

        # create a logfile in the run folder if one does not exists
        self._logfile = make_path(self._rundir, 'service.log')

        # empty s3 settings
        self._s3 = {}

        # empty mq settings
        self._mq = {}

        # empty mqtt settings
        self._mqtt = {}

        if len(Config._etcd_root) > 0 and Config._etcd_root[-1] != '/':
            Config._etcd_root = Config._etcd_root + '/'

        if Config._provider == Provider.ETCD:
            self._parse()
            return

        # default config file; should be located in run folder
        # if not provided by an user try to use this
        self._cnffile = make_path(self._rundir, 'config.cnf')

        # if the config file, whether default or user provided does not exists
        # we have to stop the execution
        if not os.path.isfile(self._cnffile):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self._cnffile)

        # try to read the config file; if for some reason we cannot read it
        # then there is no point in proceding further
        self.cf = configparser.ConfigParser()
        if len(self.cf.read(self._cnffile)) <= 0:
            raise Exception(Config.ERR_PARSEFAIL)

        self._parse()

    def _parse(self):
        # set the log level; by default it is 20 which is information
        self._loglevel = self._parse_value('log', 'loglevel', 20, 'int', False)

        # some basic settings taht are expcted to be found in the config file
        self._host = self._parse_value('app', 'host', 'localhost', '', False)
        self._port = self._parse_value('app', 'port', 8080, 'int', False)
        self._user = self._parse_value('app', 'username', '', '', False)
        self._pass = self._parse_value('app', 'password', '', '', False)

    def parse_std_s3_settings(self):
        self._s3['host'] = self._parse_value('s3', 'host', 'localhost', '', True)
        self._s3['port'] = self._parse_value('s3', 'port', 9001, 'int', False)
        self._s3['tls']  = self._parse_value('s3', 'tls', False, 'boolean', False)

    def parse_std_mq_settings(self):
        self._mq['host'] = self._parse_value('mq', 'host', 'localhost', '', True)
        self._mq['port'] = self._parse_value('mq', 'port', 5672, 'int', False)
        self._mq['binding_exchange'] = self._parse_value('mq', 'binding_exchange', 'default_binding_exchange', '', True)
        self._mq['binding_key'] = self._parse_value('mq', 'binding_key', 'default_binding_key', '', True)
        self._mq['posting_exchange'] = self._parse_value('mq', 'posting_exchange', 'default_posting_exchange', '', True)
        self._mq['routing_key'] = self._parse_value('mq', 'routing_key', 'default_routing_key', '', True)

    def parse_std_mqtt_settings(self):
        self._mqtt['host'] = self._parse_value('mqtt', 'host', 'localhost', '', True)
        self._mqtt['port'] = self._parse_value('mqtt', 'port', 1883, 'int', False)
        self._mqtt['topic'] = self._parse_value('mqtt', 'topic', 'unknowntopic', '', True)
        self._mqtt['value'] = self._parse_value('mqtt', 'value', '', '', False)

    def start_logging(self, console: bool = False) -> None:
        # a service can be started either in interective mode or
        # in daemon mode. it is decided by the command line argument
        # the program was started with. the command line args are parsed
        # and in case we are running in interactive mode, we log everything to console

        if console:
            logging.basicConfig(format=self._logformat, level=self._loglevel, handlers=[
                logging.StreamHandler(sys.stdout)
        ])

        # othrwise log everything to the specified logfile
           # while running in daemon mode, console is not available
        else:
            logging.basicConfig(format=self._logformat, level=self._loglevel, handlers=[
                logging.FileHandler(self._logfile)
        ])

    def set_etcd_key(self, key: str, value: str)-> None:
        if not self._provider != Provider.ETCD: raise NotImplementedError
        etcd= etcd3.client(host= Config._etcd_host, port= Config._etcd_port)
        etcd.put(Config._etcd_root + key, value)

    def _parse_value(self, section: str, option: str, default: any, data_type='', throw_error=False) -> any:
        try:
            if Config._provider== Provider.FILE:
                return getattr(self.cf, ('get' + data_type))(section, option)

            etcdctl = etcd3.client(host=self._etcd_host, port=self._etcd_port)
            ret, _ = etcdctl.get(Config._etcd_root + section + '/' + option)
            if ret== None:
                raise Exception()

            ret = ret.decode().strip()

            if data_type == "int":
                ret = int(ret)
            elif data_type == 'float':
                ret= float(ret)
            elif data_type == 'boolean':
                ret= ret.lower() in ['true', '1', 't', 'y', 'yes']
            else:
                pass

            return ret

        except (configparser.Error, Exception) as e:
            # wll, we encountered an error
            message = Config.WAR_OPTIONVAL.format(section, option)

            # if this setting is absolutely mandatory
            # raise an exception and stop execution
            if throw_error:
                raise Exception(message)

            # otherwise just log a warning and move on
            logging.warning(message)
            logging.debug('assuming [ {0} ] to continue.'.format(default))

            return default

    # endregion
    