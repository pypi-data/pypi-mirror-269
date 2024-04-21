import unittest
import logging
import inspect
from updrytwist import config

DEFAULT_CONFIG_FILE = "testing.yaml"
DEFAULT_BLOCK = "BasicBlockTesting"

class ConfigTest ( unittest.TestCase):

    def test_get_succeed ( self ):
        configuration = config.Config(DEFAULT_CONFIG_FILE)
        self.assertEqual( str(configuration.value( "Integer", None, DEFAULT_BLOCK )), "3" )

    def test_get_fail_default ( self ):
        configuration = config.Config(DEFAULT_CONFIG_FILE)
        self.assertEqual( configuration.value( "MissingInteger", "4", DEFAULT_BLOCK), "4")

    def test_get_fail_exception ( self ):
        configuration = config.Config(DEFAULT_CONFIG_FILE)
        with self.assertRaises(ValueError):
            configuration.intValue( "MissingInteger", fromBlock=DEFAULT_BLOCK)

    def test_get_int_succeed ( self ):
        configuration = config.Config(DEFAULT_CONFIG_FILE)
        self.assertEqual( configuration.intValue("Integer", fromBlock=DEFAULT_BLOCK), 3)

    def test_get_int_badint ( self ):
        configuration = config.Config(DEFAULT_CONFIG_FILE)
        with self.assertRaises(ValueError):
            configuration.intValue( "NonInteger", fromBlock=DEFAULT_BLOCK)

    def test_get_int_none_ok ( self ):
        configuration = config.Config(DEFAULT_CONFIG_FILE)
        self.assertIsNone( configuration.intValueNoneOk( "MissingInteger", fromBlock=DEFAULT_BLOCK))

    def test_get_int_none_not_ok ( self ):
        configuration = config.Config(DEFAULT_CONFIG_FILE)
        with self.assertRaises(ValueError):
            configuration.intValue( "MissingInteger", fromBlock=DEFAULT_BLOCK)

    def test_get_bool_succeed ( self ):
        configuration = config.Config(DEFAULT_CONFIG_FILE)
        self.assertEqual( configuration.boolValue("Bool", fromBlock=DEFAULT_BLOCK), True)

    def test_get_bool_badbool ( self ):
        configuration = config.Config(DEFAULT_CONFIG_FILE)
        with self.assertRaises(ValueError):
            configuration.boolValue( "NonBool", fromBlock=DEFAULT_BLOCK)

    def test_get_bool_none_ok ( self ):
        configuration = config.Config(DEFAULT_CONFIG_FILE)
        self.assertIsNone( configuration.boolValueNoneOk( "MissingBool", fromBlock=DEFAULT_BLOCK))

    def test_get_bool_none_not_ok ( self ):
        configuration = config.Config(DEFAULT_CONFIG_FILE)
        with self.assertRaises(ValueError):
            configuration.boolValue( "MissingBool", fromBlock=DEFAULT_BLOCK)

    def test_get_list_succeed ( self ):
        configuration = config.Config(DEFAULT_CONFIG_FILE)
        self.assertListEqual( configuration.listValue( "List", fromBlock=DEFAULT_BLOCK), ["A", "B", "C"])

    def test_get_list_badlist ( self ):
        configuration = config.Config(DEFAULT_CONFIG_FILE)
        with self.assertRaises(ValueError):
            configuration.listValue("NonList", fromBlock=DEFAULT_BLOCK)

    def test_get_list_empty ( self ):
        configuration = config.Config(DEFAULT_CONFIG_FILE)
        self.assertListEqual( configuration.listValue( "MissingList", fromBlock=DEFAULT_BLOCK), [])

    def test_get_list_default ( self ):
        configuration = config.Config(DEFAULT_CONFIG_FILE)
        self.assertListEqual( configuration.listValue( "MissingList", ["D", "E"], fromBlock=DEFAULT_BLOCK), ["D", "E"])


class LoggingTest( unittest.TestCase ):

    def test_overriding_debug_level_incremental ( self ):
        configuration = config.Config('testing.yaml')
        config.LoggingConfiguration.initLogging( configuration, 'DebugLogging', 'DebugLogging' )
        logger = logging.getLogger('test.warnlevel')
        logger.debug(f'{inspect.currentframe().f_code.co_name} debug message - should see')
        logger.info(f'{inspect.currentframe().f_code.co_name} info message - should see')
        logger.warning( f'{inspect.currentframe().f_code.co_name} warning message - should see')

    def test_overriding_warning_level_incremental ( self ):
        configuration = config.Config('testing.yaml')
        config.LoggingConfiguration.initLogging( configuration, 'WarningLogging', 'WarningLogging' )
        logger = logging.getLogger('test.warnlevel')
        logger.debug(f'{inspect.currentframe().f_code.co_name} debug message - should NOT see')
        logger.info(f'{inspect.currentframe().f_code.co_name} info message - should NOT see')
        logger.warning( f'{inspect.currentframe().f_code.co_name} warning message - should see')

    def test_overriding_debug_level_full ( self ):
        configuration = config.Config('testing.yaml')
        config.LoggingConfiguration.initLogging( configuration, 'DebugFullConfigLogging', 'DebugFullConfigLogging' )
        logger = logging.getLogger('test.warnlevel')
        logger.debug(f'{inspect.currentframe().f_code.co_name} debug message - should see')
        logger.info(f'{inspect.currentframe().f_code.co_name} info message - should see')
        logger.warning( f'{inspect.currentframe().f_code.co_name} warning message - should see')

    def test_overriding_warning_level_full ( self ):
        configuration = config.Config('testing.yaml')
        config.LoggingConfiguration.initLogging( configuration, 'WarningFullConfigLogging', 'WarningFullConfigLogging' )
        logger = logging.getLogger('test.warnlevel')
        logger.debug(f'{inspect.currentframe().f_code.co_name} debug message - should NOT see')
        logger.info(f'{inspect.currentframe().f_code.co_name} info message - should NOT see')
        logger.warning( f'{inspect.currentframe().f_code.co_name} warning message - should see')


if __name__ == '__main__':
    unittest.main()
