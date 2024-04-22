"""Test the MQTT driver"""
#  Copyright (c) 2024. All rights reserved.

import asyncio
import pytest

from updrytwist import config, mqttdriver

BASE_TOPIC = "mqtt_test"

CANNED_SERVER_CONFIG = {
    "MQTT": {
        #            "ReconnectSeconds" : "",
        #            "MqttServer" : "localhost",
        "ClientId": "mqtt_test",
        #            "MqttPort" : "",
        "username": "homeassistant",
        "password": "GooglyEyes242",
        #            "qos" : ""
    }
}
CANNED_CLIENT_CONFIG = {
    "MQTT": {
        #            "ReconnectSeconds" : "",
        #            "MqttServer" : "localhost",
        "ClientId": "mqtt_test",
        #            "MqttPort" : "",
        "username": "homeassistant",
        "password": "GooglyEyes242",
        #            "qos" : ""
    }
}

@pytest.fixture
def load_config ( ):
    print("Loading config ...!!!!")
    config.DEFAULT_CONFIG = "testing.yaml"
    config.initialize()


def getClientConfig():
    return config.CannedConfig(CANNED_CLIENT_CONFIG)
def getServerConfig():
    return config.CannedConfig(CANNED_SERVER_CONFIG)

@pytest.mark.asyncio
async def disabled_test_simpleConnect():
    server = mqttdriver.MqttDriver(getServerConfig())
    server.runMessageLoopInCurrentLoop()
    while server.keepLooping:
        await asyncio.sleep(2)
        await server.asyncQuitLoop()

topic_received = None

@pytest.mark.asyncio
async def topicReceived(_topics: [], payload):
    global topic_received
    topic_received = payload

@pytest.mark.asyncio
async def test_and_read():
    # return
    global topic_received

    mqtt = mqttdriver.MqttDriver(getServerConfig())
    topic_received = None
    mqtt.addCommand(BASE_TOPIC, topicReceived)
    mqtt.runMessageLoopInCurrentLoop()
    try:
        await mqtt.publishMessage(BASE_TOPIC, "testrun")
        await asyncio.sleep(5)
    except Exception as e:
        abc = e
        raise
    finally:
        await mqtt.asyncQuitLoop()

    assert topic_received =="testrun"


# if __name__ == "__main__":
#     unittest.main()
