import logging
import inspect
import pytest
from updrytwist import config

DEFAULT_CONFIG_FILE = "testing.yaml"
DEFAULT_BLOCK = "BasicBlockTesting"

def test_get_succeed ( ):
    configuration = config.Config(DEFAULT_CONFIG_FILE)
    assert str(configuration.value( "Integer", None, DEFAULT_BLOCK )) == "3"

def test_get_fail_default ( ):
    configuration = config.Config(DEFAULT_CONFIG_FILE)
    assert configuration.value( "MissingInteger", "4", DEFAULT_BLOCK) == "4"

def test_get_fail_exception ( ):
    configuration = config.Config(DEFAULT_CONFIG_FILE)
    with pytest.raises( ValueError ):
        configuration.intValue( "MissingInteger", fromBlock=DEFAULT_BLOCK)

def test_get_int_succeed (  ):
    configuration = config.Config(DEFAULT_CONFIG_FILE)
    assert configuration.intValue("Integer", fromBlock=DEFAULT_BLOCK) == 3

def test_get_int_badint ( ):
    configuration = config.Config(DEFAULT_CONFIG_FILE)
    with pytest.raises(ValueError):
        configuration.intValue( "NonInteger", fromBlock=DEFAULT_BLOCK)

def test_get_int_none_ok ( ):
    configuration = config.Config(DEFAULT_CONFIG_FILE)
    assert configuration.intValueNoneOk( "MissingInteger", fromBlock=DEFAULT_BLOCK) is None

def test_get_int_none_not_ok ( ):
    configuration = config.Config(DEFAULT_CONFIG_FILE)
    with pytest.raises(ValueError):
        configuration.intValue( "MissingInteger", fromBlock=DEFAULT_BLOCK)

def test_get_bool_succeed ( ):
    configuration = config.Config(DEFAULT_CONFIG_FILE)
    assert configuration.boolValue("Bool", fromBlock=DEFAULT_BLOCK)

def test_get_bool_badbool ( ):
    configuration = config.Config(DEFAULT_CONFIG_FILE)
    with pytest.raises(ValueError):
        configuration.boolValue( "NonBool", fromBlock=DEFAULT_BLOCK)

def test_get_bool_none_ok ( ):
    configuration = config.Config(DEFAULT_CONFIG_FILE)
    assert configuration.boolValueNoneOk( "MissingBool", fromBlock=DEFAULT_BLOCK) is None

def test_get_bool_none_not_ok ( ):
    configuration = config.Config(DEFAULT_CONFIG_FILE)
    with pytest.raises(ValueError):
        configuration.boolValue( "MissingBool", fromBlock=DEFAULT_BLOCK)

def test_get_list_succeed (  ):
    configuration = config.Config(DEFAULT_CONFIG_FILE)
    assert configuration.listValue( "List", fromBlock=DEFAULT_BLOCK) == ["A", "B", "C"]

def test_get_list_badlist ( ):
    configuration = config.Config(DEFAULT_CONFIG_FILE)
    with pytest.raises(ValueError):
        configuration.listValue("NonList", fromBlock=DEFAULT_BLOCK)

def test_get_list_empty (  ):
    configuration = config.Config(DEFAULT_CONFIG_FILE)
    assert configuration.listValue( "MissingList", fromBlock=DEFAULT_BLOCK) == []

def test_get_list_default ( ):
    configuration = config.Config(DEFAULT_CONFIG_FILE)
    assert configuration.listValue( "MissingList", ["D", "E"], fromBlock=DEFAULT_BLOCK) == ["D", "E"]



def test_overriding_debug_level_incremental (  ):
    configuration = config.Config('testing.yaml')
    config.LoggingConfiguration.initLogging( configuration, 'DebugLogging', 'DebugLogging' )
    logger = logging.getLogger('test.warnlevel')
    logger.debug(f'{inspect.currentframe().f_code.co_name} debug message - should see')
    logger.info(f'{inspect.currentframe().f_code.co_name} info message - should see')
    logger.warning( f'{inspect.currentframe().f_code.co_name} warning message - should see')

def test_overriding_warning_level_incremental ( ):
    configuration = config.Config('testing.yaml')
    config.LoggingConfiguration.initLogging( configuration, 'WarningLogging', 'WarningLogging' )
    logger = logging.getLogger('test.warnlevel')
    logger.debug(f'{inspect.currentframe().f_code.co_name} debug message - should NOT see')
    logger.info(f'{inspect.currentframe().f_code.co_name} info message - should NOT see')
    logger.warning( f'{inspect.currentframe().f_code.co_name} warning message - should see')

def test_overriding_debug_level_full (  ):
    configuration = config.Config('testing.yaml')
    config.LoggingConfiguration.initLogging( configuration, 'DebugFullConfigLogging', 'DebugFullConfigLogging' )
    logger = logging.getLogger('test.warnlevel')
    logger.debug(f'{inspect.currentframe().f_code.co_name} debug message - should see')
    logger.info(f'{inspect.currentframe().f_code.co_name} info message - should see')
    logger.warning( f'{inspect.currentframe().f_code.co_name} warning message - should see')

def test_overriding_warning_level_full ( ):
    configuration = config.Config('testing.yaml')
    config.LoggingConfiguration.initLogging( configuration, 'WarningFullConfigLogging', 'WarningFullConfigLogging' )
    logger = logging.getLogger('test.warnlevel')
    logger.debug(f'{inspect.currentframe().f_code.co_name} debug message - should NOT see')
    logger.info(f'{inspect.currentframe().f_code.co_name} info message - should NOT see')
    logger.warning( f'{inspect.currentframe().f_code.co_name} warning message - should see')

