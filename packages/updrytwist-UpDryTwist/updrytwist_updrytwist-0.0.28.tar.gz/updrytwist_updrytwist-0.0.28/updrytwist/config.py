#!/usr/bin/env python

#  Copyright (c) 2024. All rights reserved.

import distutils.util
import logging
import logging.config
import os
import sys
from typing import Optional, Union

import yaml

from . import __version__
from . import gentleargparser

DEFAULT_CONFIG    = os.getenv( 'CONFIGFILE', 'myapp.yaml' )
DEFAULT_LOGFILE   = os.getenv( 'LOGFILE', 'myapp.log' )

DEFAULT_LOGFORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAULT_LOGLEVEL  = 'INFO'

_LOGGER = logging.getLogger(__name__)

def legacydictread( dictionary, key : str, default=None ):
    if dictionary is None:
        return default
    elif key in dictionary:
        return dictionary[key]
    else:
        return default

def strread ( object, key : str, default : str ) -> str:
    value = dictread( object, key, default )
    return default if value is None else str(value)

def dictread( object, key : str, default=None ):
    if object is None:
        return default
    elif isinstance(object, dict):
        if key in object:
            return object[key]
        else:
            return default
    elif isinstance(object, list):
        if key in object:
            return key
        # could still be a dictionary in the list . . .
        for item in object:
            if isinstance(item, dict):
                if key in item:
                    return item[key]
        return default
    else:
        # this is a weird case we shouldn't encounter . . .
        _LOGGER.warning( f"Configuration yamlread() encountered unexpected case where object *{object}* is of type {type(object)} and trying to read key {key} with default {default}")
        return default

class ConfigReader:

    def __init__ ( self, readerFunction ):
        self.readerFunction = readerFunction

    def read ( self, key : str, default=None):
        return self.readerFunction( key, default )

    def forceread ( self, key : str ):
        value = self.read(key, None )
        if value is None:
            raise ValueError( f'Failed to read value {key} from configuration!')
        return value

    def boolreadNoneOk ( self, key : str, default : Optional[bool] = None ) -> Union[bool, None]:
        val = self.read(key, default)
        if val is not None:
            if isinstance(val, str):
                return distutils.util.strtobool(val)
            else:
                return bool(val)
        else:
            return default

    def boolread ( self, key : str, default : Optional[bool] = None ) -> bool:
        value = self.boolreadNoneOk( key, default )
        if value is not None:
            return value
        else:
            raise ValueError( f'Failed to read value {key} from configuration!')

    def intreadNoneOk ( self, key : str, default : Optional[int] = None ) -> Union[int, None]:
        val = self.read(key, default)
        if val is not None:
            return int(val)
        else:
            return default

    def intread ( self, key : str, default : Optional[int] = None ) -> int:
        value = self.intreadNoneOk( key, default )
        if value is not None:
            return value
        else:
            raise ValueError( f'Failed to read value {key} from configuration!')

    def listread ( self, key : str, default : Optional[list] = None ) -> []:
        value = self.read( key, default)
        if value is None:
            return []
        elif isinstance( value, list ):
            return value
        else:
            raise ValueError( f'Expected a list for configuration value {key} but got {type(value)}')

class DictionaryConfigReader (ConfigReader):

    def __init__ (self, dictionary : {} ):
        self.dictionary = dictionary
        super().__init__(self.reader)

    def reader ( self, key : str, default=None ):
        return dictread( self.dictionary, key, default )

def forceread ( dictionary, key : str ):
    return DictionaryConfigReader(dictionary).forceread( key )

def boolreadNoneOk ( dictionary, key : str, default : Optional[bool] = None ) -> Union[bool, None]:
    return DictionaryConfigReader(dictionary).boolreadNoneOk( key, default)

def boolread ( dictionary, key : str, default : Optional[bool] = None ) -> bool:
    return DictionaryConfigReader(dictionary).boolread(key, default)

def intreadNoneOk ( dictionary, key : str, default : Optional[int] = None ) -> Union[int, None]:
    return DictionaryConfigReader(dictionary).intreadNoneOk(key, default)

def intread ( dictionary, key : str, default : Optional[int] = None ) -> int:
    return DictionaryConfigReader(dictionary).intread(key, default)

def listread ( dictionary, key : str, default : Optional[list] = None ) -> []:
    return DictionaryConfigReader(dictionary).listread(key, default)

class Config:

    c = None

    def __init__ ( self, filename : str = None, optional_config : bool = False, forceDictionary : {} = None ):

        if filename is None:
            filename = DEFAULT_CONFIG

        self.filename = filename
        self.readCommandLine()

        if not forceDictionary:
            try:
                with open(self.filename) as source:
                    self.config = yaml.load( source, Loader=yaml.FullLoader )
            except Exception as e:
                if optional_config:
                    self.config = {}
                else:
                    raise e
        else:
            self.config = forceDictionary

    def blockFor ( self, fromBlock : str = None ) -> {}:
        if not fromBlock:
            return self.config
        elif fromBlock in self.config:
            return self.config[fromBlock]
        else:
            return {}

    def value ( self, key : str, default=None, fromBlock : str = None ):
        return dictread(self.blockFor(fromBlock), key, default)

    def boolValueNoneOk ( self, key : str, default : Optional[bool] = None, fromBlock : str = None) -> Union[bool, None]:
        return boolreadNoneOk(self.blockFor(fromBlock), key, default)

    def boolValue ( self, key : str, default : Optional[bool] = None, fromBlock : str = None ) -> bool:
        return boolread( self.blockFor(fromBlock), key, default)

    def intValueNoneOk ( self, key : str, default : Optional[int] = None, fromBlock : str = None ) -> Union[int, None]:
        return intreadNoneOk( self.blockFor(fromBlock), key, default)

    def intValue ( self, key : str, default : Optional[int] = None, fromBlock : str = None ) -> Union[int, None]:
        return intread( self.blockFor(fromBlock), key, default)

    def listValue( self, key : str, default : Optional[list] = None, fromBlock : str = None ) -> []:
        return listread( self.blockFor(fromBlock), key, default)

    @staticmethod
    def get ( key : str, default=None, fromBlock : str = None ):
        return Config.c.value(key, default, fromBlock)

    @staticmethod
    def getMandatory( key : str, fromBlock : str = None ):
        value = Config.c.value(key, None, fromBlock)
        if value is None:
            raise ValueError( f'Failed to read value {key} from configuration! (block = {fromBlock})')
        return value

    @staticmethod
    def getBoolNoneOk ( key : str, default : Optional[bool] = None, fromBlock : str = None ) -> Union[bool, None]:
        return Config.c.boolValueNoneOk( key, default, fromBlock )

    @staticmethod
    def getBool ( key : str, default : Optional[bool] = None, fromBlock : str = None ) -> Union[bool, None]:
        return Config.c.boolValue( key, default, fromBlock )

    @staticmethod
    def getIntNoneOk ( key : str, default : Optional[int] = None, fromBlock : str = None ) -> Union[int, None]:
        return Config.c.intValueNoneOk( key, default, fromBlock )

    @staticmethod
    def getInt ( key : str, default : Optional[int] = None, fromBlock : str = None ) -> Union[int, None]:
        return Config.c.intValue( key, default, fromBlock )

    @staticmethod
    def getList ( key : str, default : Optional[list] = None, fromBlock : str = None) -> []:
        return Config.c.listValue( key, default, fromBlock )

    def readCommandLine ( self ):

        parser = gentleargparser.GentlerArgParser(description='Generic UpDryTwist Command Parser',
                                         conflict_handler='resolve' )
        parser.throwExceptions = False
        parser.add_argument('--config', help='Path to configuration file', default=None)
        try:
            args = parser.parse_args()
            if 'config' in vars(args):
                fileName = vars(args)['config']
                if fileName is not None:
                    self.filename = fileName
        except Exception as e:
            _LOGGER.debug( f"Encountered unrecognized command-line arguments but continuing on ({e}).")

class CannedConfig ( Config ):
    """
    Used to create a canned configuration that can be passed around.  Mostly for unit testing.
    """

    def __init__ ( self, cannedConfig : {} ) :
        super().__init__(None, False, cannedConfig )

def getConfig () -> Config :
    return Config.c


def loadConfig ( optional_config : bool = False ):
    try:
        Config.c = Config( None, optional_config )
    except Exception as e:
        print( "Cannot load configuration from file {}: {}".format( DEFAULT_CONFIG, str(e)))
        sys.exit(2)


class LoggingConfiguration:

    def __init__ ( self ):
        pass

    @staticmethod
    def initLogging ( config : Config, loggingBlock : str = 'Logging', baseConfigBlock : str = None ):
        loggingConfig = config.value( loggingBlock, None )
        incremental = dictread(loggingConfig, 'incremental', False )

        # Clean all handlers out of root . . . need this for testing when we reinitialize the handlers
        root = logging.getLogger()
        for h in list(root.handlers):
            root.removeHandler(h)

        if incremental or not loggingConfig:
            # if the configuration is incremental, or missing, we set up most of the logging
            # in particular, we need to manage formatter and handler

            logFile      = config.value( 'logfile',      DEFAULT_LOGFILE, baseConfigBlock )
            logFormat    = config.value( 'logformat',    DEFAULT_LOGFORMAT, baseConfigBlock )
            logLevel     = config.value( 'loglevel',     DEFAULT_LOGLEVEL, baseConfigBlock )
            logToConsole = config.value( 'logToConsole', False, baseConfigBlock )
            logToFile    = config.value( 'logToFile',    True, baseConfigBlock )

            root = logging.getLogger()
            root.setLevel( logLevel )

            if logToFile:
                handler = logging.FileHandler( logFile )
                # handler.setLevel( logLevel )
                handler.setFormatter( logging.Formatter(logFormat ))
                root.addHandler( handler )

            if logToConsole:
                handler = logging.StreamHandler( sys.stdout )
                # handler.setLevel( logLevel )
                handler.setFormatter( logging.Formatter(logFormat ))
                root.addHandler( handler )

        if loggingConfig:
            logging.config.dictConfig( loggingConfig )


def initialize ( optional_config = False ):
    loadConfig( optional_config )
    LoggingConfiguration().initLogging( Config.c )
    logger = logging.getLogger(__name__)
    logger.info( f'Using updrytwist version {__version__} (from {__name__})')
