#!/usr/bin/env python

#  Copyright (c) 2024. All rights reserved.

import asyncio
import contextlib
import json
import logging
import os
import sys
from asyncio import TaskGroup
from random import randint

from aiomqtt import Client, MqttError

from updrytwist import config

_LOGGER = logging.getLogger(__name__)
# _LOGGER.setLevel( logging.DEBUG )
DEBUG_ASYNCIO = False

DEFAULT_RECONNECT_SECONDS = 60
DEFAULT_BASE_TOPIC = "driver"
DEFAULT_MQTT_SERVER = "shasta.tath-home.com"
DEFAULT_MQTT_PORT = 1883
DEFAULT_QOS = 2
DEFAULT_PARALLEL_PROCESS = True

# MQTT_LOGGER = logging.getLogger('mqtt')
# MQTT_LOGGER.setLevel(logging.INFO)



def prepare_mqtt_safe_loop():
    """Under Windows, need to change the event loop type.  Call this before
    starting your main event loop!"""
    # Change to the "Selector" event loop if platform is Windows
    # Actually, stick with Proactor
    # WindowsSelectorEventLoopPolicy,
    if sys.platform.lower() == "win32" or os.name.lower() == "nt":
        from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy

        set_event_loop_policy(WindowsSelectorEventLoopPolicy())


class MqttDriverCommand:
    def __init__(self, topicFilter: str, callback):
        self.topicFilter = topicFilter
        self.callback = callback


class MqttDriver:
    """MQTT Driver class for handling MQTT messages."""

    client : Client | None = None

    def __init__(self, configuration: config.Config):
        self.commands = []

        queueConfig = configuration.value("MQTT") if configuration else None

        self.reconnectSeconds = config.dictread(
            queueConfig, "ReconnectSeconds", DEFAULT_RECONNECT_SECONDS
        )
        self.mqttServer = config.dictread(
            queueConfig, "MqttServer", DEFAULT_MQTT_SERVER
        )
        self.clientId = config.dictread(
            queueConfig, "ClientId", "mqttdriver-%s" % os.getpid()
        )
        self.port = config.dictread(queueConfig, "MqttPort", DEFAULT_MQTT_PORT)
        self.username = config.dictread(queueConfig, "username")
        self.password = config.dictread(queueConfig, "password")
        self.qos = config.dictread(queueConfig, "qos", DEFAULT_QOS)
        self.parallel_process = config.dictread(
            queueConfig, "parallel_process", DEFAULT_PARALLEL_PROCESS
        )

        self.keepLooping = True
        self.exception = None
        self.tasks = set()

        self.loop = None

    def addCommand(self, topicFilter: str, callback, _notAsync: bool = False):
        command = MqttDriverCommand(topicFilter, callback)
        self.commands.append(command)

    async def runListen(self):
        try:
            async with self.newClient() as self.client:
                for command in self.commands:
                    await self.client.subscribe(command.topicFilter)
                if self.parallel_process:
                    _LOGGER.debug("Running parallel MQTT listening process")
                    async with TaskGroup() as task_group:
                        async for message in self.client.messages:
                            for command in self.commands:
                                if message.topic.matches(command.topicFilter):
                                    task_group.create_task(
                                        self.processGenericMessage(command, message)
                                    )
                else:
                    _LOGGER.debug("Running serial MQTT listening process")
                    async for message in self.client.messages:
                        for command in self.commands:
                            if message.topic.matches(command.topicFilter):
                                await self.processGenericMessage(command, message)
        except Exception as e:
            self.exception = e
            raise
        finally:
            self.client = None
            self.tasks = set()

    @staticmethod
    async def processGenericMessage(command: MqttDriverCommand, message):
        msg = message.payload
        topic = message.topic

        _LOGGER.debug(f"Received generic message on topic {topic}: {msg}")

        topics = topic.value.split("/")

        if len(msg) > 0:
            try:
                payload = json.loads(msg.decode("utf-8", "ignore"))
            except json.JSONDecodeError:
                payload = msg.decode("utf-8", "ignore")
        else:
            payload = None

        try:
            await command.callback(topics, payload)
        except Exception as e:
            _LOGGER.error(
                f"Failed to process message {msg} with exception {e}", exc_info=True
            )

    def newClient(self) -> Client:

        clientId = self.clientId + "-%s" % str(randint(1, 999999)).zfill(6)
        return Client(
            hostname=self.mqttServer,
            port=self.port,
            username=self.username,
            password=self.password,
            identifier=clientId,
            logger=_LOGGER,
        )

    def postMessage(self, topic, data):
        asyncio.run_coroutine_threadsafe(
            self.publishMessage(topic, data), self.getMessageLoop()
        )

    async def publishMessage(self, topic, data):
        if self.client:
            await self.client.publish(topic, data)
        else:
            async with self.newClient() as client:
                await client.publish(topic, data)

    @staticmethod
    async def cancelTasks(tasks):
        _LOGGER.debug("mqttDriver Cleaning up tasks with cancelTasks()")
        for task in tasks:
            if task.done():
                continue
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await task

    async def asyncQuitLoop(self):
        self.keepLooping = False
        await self.cancelTasks(self.tasks)

    def quitLoop(self):
        # loop = asyncio.get_event_loop()
        # coroutine = MqttDriver.cancelTasks(self.tasks)
        # loop.run_until_complete(coroutine)
        asyncio.run(self.asyncQuitLoop())

    async def messageLoop(self):
        self.keepLooping = True
        self.loop = asyncio.get_event_loop()
        while self.keepLooping:
            try:
                await self.runListen()
            except asyncio.CancelledError:
                self.keepLooping = False
                await self.cancelTasks(self.tasks)
                _LOGGER.info("Run loop was cancelled.  Exiting loop.")
            except MqttError as error:
                _LOGGER.info(
                    f'Error "{error}". Reconnecting in {self.reconnectSeconds} seconds.'
                )
            finally:
                if self.keepLooping:
                    await asyncio.sleep(self.reconnectSeconds)
        _LOGGER.info("Exiting the mqttdriver message loop")

    def getMessageLoop(self):
        return self.loop

    def runMessageLoop(self):
        asyncio.run(self.messageLoop(), debug=DEBUG_ASYNCIO)

    def runMessageLoopInCurrentLoop ( self ):
        loop = asyncio.get_event_loop()
        self.tasks.add(loop.create_task(self.messageLoop()))


