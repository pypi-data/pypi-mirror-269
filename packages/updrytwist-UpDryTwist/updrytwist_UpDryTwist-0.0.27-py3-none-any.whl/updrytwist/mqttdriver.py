#!/usr/bin/env python

#  Copyright (c) 2024. All rights reserved.

import asyncio
import enum
import json
import logging
import os
import sys

from aiomqtt import Client, MqttError

from updrytwist import config

_LOGGER = logging.getLogger(__name__)
# _LOGGER.setLevel( logging.DEBUG )
DEBUG_ASYNCIO = False

DEFAULT_RECONNECT_SECONDS = 60
DEFAULT_BASE_TOPIC        = "driver"
DEFAULT_MQTT_SERVER       = "shasta.tath-home.com"
DEFAULT_MQTT_PORT         = 1883
DEFAULT_QOS               = 2

# MQTT_LOGGER = logging.getLogger('mqtt')
# MQTT_LOGGER.setLevel(logging.INFO)


class MqttDriverCommand :

    def __init__ ( self, topicFilter : str, callback ):

        self.topicFilter = topicFilter
        self.callback = callback


class MqttDriver :

    class State (enum.Enum):
        DISCONNECTED = 1
        CONNECTING   = 2
        CONNECTED    = 3

    def __init__ ( self, configuration : config.Config ):

        self.commands = []

        if configuration:
            queueConfig = configuration.value( "MQTT" )
        else:
            queueConfig = None

        self.reconnectSeconds = config.dictread( queueConfig, "ReconnectSeconds", DEFAULT_RECONNECT_SECONDS )
        self.mqttServer       = config.dictread( queueConfig, "MqttServer", DEFAULT_MQTT_SERVER )
        self.clientId         = config.dictread( queueConfig, "ClientId", 'mqttdriver-%s' % os.getpid() )
        self.port             = config.dictread( queueConfig, "MqttPort", DEFAULT_MQTT_PORT )
        self.username         = config.dictread( queueConfig, "username" )
        self.password         = config.dictread( queueConfig, "password" )
        self.qos              = config.dictread( queueConfig, "qos", DEFAULT_QOS )

        self.keepLooping = True
        self.state = MqttDriver.State.DISCONNECTED
        self.stateChange = None
        self.client = None
        self.exception = None
        self.tasks = set()

        self.loop = None

    def setState ( self, state : State ):
        self.state = state
        if self.stateChange:
            self.stateChange.set()
        self.stateChange = asyncio.Event()

    async def waitForStateChange ( self, expectedState : State = None ):
        await self.stateChange.wait()
        if expectedState:
            if self.state != expectedState:
                raise ValueError(f"Invalid state on MQTT driver {self.state}")

    def addCommand ( self, topicFilter : str, callback, _notAsync : bool = False ) :

        command = MqttDriverCommand( topicFilter, callback )
        self.commands.append( command )

    async def runListen( self ):

        try:
            await self.forceClient()
            async with self.client.messages() as messages:
                for command in self.commands:
                    await self.client.subscribe( command.topicFilter )
                async for message in messages:
                    for command in self.commands:
                        if message.topic.matches( command.topicFilter ):
                            await self.processGenericMessage( command, message )
        except Exception as e:
            self.exception = e
            raise
        finally:
            self.tasks  = set()
            self.client = None
            self.setState( MqttDriver.State.DISCONNECTED )

    @staticmethod
    async def processGenericMessage ( command : MqttDriverCommand, message ):

        msg   = message.payload
        topic = message.topic

        _LOGGER.debug( "Received generic message on topic {}: {}".format( topic, msg ))

        topics = topic.value.split('/')

        if len(msg) > 0:
            try:
                payload = json.loads(msg.decode('utf-8', 'ignore'))
            except json.JSONDecodeError:
                payload = msg.decode('utf-8', 'ignore')
        else:
            payload = None

        try:
            await command.callback( topics, payload )
        except Exception as e:
            _LOGGER.error( f'Failed to process message {msg} with exception {e}', exc_info=True)

    async def forceClient ( self ):
        # Connect to the MQTT broker
        try:
            if not self.client:
                self.setState( MqttDriver.State.DISCONNECTED )
                self.exception = None
                self.client = Client( self.mqttServer, port=self.port, username=self.username,
                                      password=self.password, identifier=self.clientId, logger=_LOGGER )

            if self.state == MqttDriver.State.DISCONNECTED:
                self.setState( MqttDriver.State.CONNECTING )
                await self.client.connect()
                self.setState( MqttDriver.State.CONNECTED )
            elif self.state == MqttDriver.State.CONNECTING:
                await self.waitForStateChange( MqttDriver.State.CONNECTED )
            elif self.state == MqttDriver.State.CONNECTED:
                    pass

        except Exception as e:
            self.exception = e
            raise
        finally:
            self.client = None
            self.setState( MqttDriver.State.DISCONNECTED )

    def postMessage ( self, topic, data ):

        asyncio.run_coroutine_threadsafe( self.publishMessage(topic, data), self.getMessageLoop() )

    async def publishMessage( self, topic, data ):
        await self.forceClient()
        await self.client.publish( topic, data )

    @staticmethod
    async def cancelTasks ( tasks ):

        _LOGGER.debug( f'mqttDriver Cleaning up tasks with cancelTasks()')
        for task in tasks:
            if task.done():
                continue
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    async def asyncQuitLoop ( self ):
        self.keepLooping = False
        await self.cancelTasks(self.tasks)

    def quitLoop ( self ) :
        #loop = asyncio.get_event_loop()
        #coroutine = MqttDriver.cancelTasks(self.tasks)
        #loop.run_until_complete(coroutine)
        asyncio.run(self.asyncQuitLoop())

    async def messageLoop( self ):

        # Change to the "Selector" event loop if platform is Windows
        if sys.platform.lower() == "win32" or os.name.lower() == "nt":
            from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy
            set_event_loop_policy( WindowsSelectorEventLoopPolicy() )

        self.keepLooping = True
        self.loop = asyncio.get_event_loop()
        while self.keepLooping:
            try:
                await self.runListen()
            except asyncio.CancelledError:
                self.keepLooping = False
                await self.cancelTasks(self.tasks)
                _LOGGER.info( f'Run loop was cancelled.  Exiting loop.')
            except MqttError as error:
                _LOGGER.info( f'Error "{error}". Reconnecting in {self.reconnectSeconds} seconds.')
            finally:
                if self.keepLooping:
                    await asyncio.sleep( self.reconnectSeconds )
        _LOGGER.info( f'Exiting the mqttdriver message loop')

    def getMessageLoop ( self ) :
        return self.loop

    def runMessageLoop ( self ) :
        asyncio.run( self.messageLoop(), debug=DEBUG_ASYNCIO )
