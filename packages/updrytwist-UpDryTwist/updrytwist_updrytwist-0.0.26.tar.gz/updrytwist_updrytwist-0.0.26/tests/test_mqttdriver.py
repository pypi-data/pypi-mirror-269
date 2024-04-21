import asyncio
import unittest
import sys
import os
from updrytwist import mqttdriver
from updrytwist import config
from updrytwist import loop_runner

BASE_TOPIC = "mqtt_test"

class MqttDriverTest ( unittest.IsolatedAsyncioTestCase ):

    CANNED_CONFIG = {
        "MQTT" : {
#            "ReconnectSeconds" : "",
#            "MqttServer" : "localhost",
            "ClientId"   : "mqtt_test",
#            "MqttPort" : "",
            "username" : "homeassistant",
            "password" : "GooglyEyes242",
#            "qos" : ""
        }
    }

    def setUp ( self ):
        # Change to the "Selector" event loop if platform is Windows
        if sys.platform.lower() == "win32" or os.name.lower() == "nt":
            from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy
            set_event_loop_policy( WindowsSelectorEventLoopPolicy() )
        self.runner = loop_runner.LoopRunner(asyncio.new_event_loop())
        self.runner.start()

    def tearDown ( self ):
        self.runner.stop()
        self.runner.join()

    @staticmethod
    def getConfig ( ):
        return config.CannedConfig( MqttDriverTest.CANNED_CONFIG )

    def startServer ( self ) -> mqttdriver.MqttDriver :
        self.mqtt = mqttdriver.MqttDriver ( MqttDriverTest.getConfig() )
        loop = self.runner.run_task(self.mqtt.messageLoop())
        self.mqtt.tasks.add(loop)
        return self.mqtt

    @staticmethod
    async def quitLoop ( mqtt : mqttdriver.MqttDriver ):
        await mqtt.quitLoop()

    async def test_simpleConnect ( self ):

        mqtt = self.startServer()
        while mqtt.keepLooping:
            await asyncio.sleep( 2 )
            await mqtt.asyncQuitLoop()

    async def topicReceived ( self, _topics : [], payload  ):
        self.topicReceived = payload

    async def test_and_read ( self ):

        return

        server = self.startServer()
        self.topicReceived = None
        server.addCommand( BASE_TOPIC, self.topicReceived )

        client = None
        try:
            client = mqttdriver.MqttDriver ( MqttDriverTest.getConfig() )
            await client.publishMessage( BASE_TOPIC, "testrun" )
            await asyncio.sleep( 5 )
        except Exception as e:
            abc = e
            raise
        finally:
            await server.asyncQuitLoop()
            await client.asyncQuitLoop()

        self.assertEqual( self.topicReceived, "testrun" )


if __name__ == '__main__':
    unittest.main()