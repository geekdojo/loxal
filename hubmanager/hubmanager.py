#!/usr/bin/env python3
import asyncio
import functools
import logging
import json
from typing import Any, Callable, Optional

import aiopulse2
from aiopulse2 import _LOGGER


class HubManager():

    def __init__(self, event_loop):
        """Init command interface."""
        self._hubs = {}
        self.event_loop = event_loop
        self.running = True
        super().__init__()

    def add_job(self, target: Callable[..., Any], *args: Any) -> None:
        """Add job to the executor pool.

        target: target to call.
        args: parameters for method to call.
        """
        if target is None:
            raise ValueError("Don't call add_job with None")
        self.event_loop.call_soon_threadsafe(self.async_add_job, target, *args)

    def async_add_job(
        self, target: Callable[..., Any], *args: Any
    ) -> Optional[asyncio.Future]:
        """Add a job from within the event loop.

        This method must be run in the event loop.

        target: target to call.
        args: parameters for method to call.
        """
        task = None

        # Check for partials to properly determine if coroutine function
        check_target = target
        while isinstance(check_target, functools.partial):
            check_target = check_target.func

        if asyncio.iscoroutine(check_target):
            task = self.event_loop.create_task(target)  # type: ignore
        elif asyncio.iscoroutinefunction(check_target):
            task = self.event_loop.create_task(target(*args))
        else:
            task = self.event_loop.run_in_executor(None, target, *args)  # type: ignore

        return task

    async def add_hub(self, hub_ip):
        """Add a hub to the prompt."""
        hub = aiopulse2.Hub(hub_ip)
        self._hubs[hub.id] = hub
        hub.callback_subscribe(self.hub_update_callback)
        # Test we can connect OK first.
        self.async_add_job(hub.run)
        # Wait until we have the rollers setup initially
        await hub.rollers_known.wait()
        print("Hub added to prompt")

    async def hub_update_callback(self, hub):
        """Called when a hub reports that its information is updated."""
        print(f"Hub {hub.name!r} updated")
        for roller in hub.rollers.values():
            roller.callback_subscribe(self.roller_update_callback)

    async def roller_update_callback(self, roller):
        """Called when a roller reports it has updated"""
        print(f"Roller Updated: {roller}")

    def _get_roller(self, hub_id, roller_id):
        """Return roller based on string argument."""
        try:
            return list(list(self._hubs.values())[hub_id].rollers.values())[roller_id]
        except Exception:
            print("Invalid arguments {},{}".format(hub_id, roller_id))
            print(
                "Format is <hub index> <roller index>. See 'list' for the index of each device."
            )
            return None

    def do_list(self):
        """Command to list all hubs and rollers."""
        print("Listing hubs...")
        hub_id = 0
        for hub in self._hubs.values():
            hub_id += 1
            print(f"Hub {hub_id}: {hub}")
            roller_id = 0
            for roller in hub.rollers.values():
                roller_id += 1
                print(f"Roller {roller_id}: {roller}")

    def do_moveto(self, hub_id, roller_id, position):
        """Command to tell a roller to move a % closed."""
        print("Sending move to")
        roller = self._get_roller(hub_id, roller_id)
        if roller:
            print("Sending blind move to {}".format(roller.name))
            self.add_job(roller.move_to, position)

    async def do_close(self, hub_id, roller_id):
        """Command to close a roller."""
        roller = self._get_roller(hub_id, roller_id)
        if roller:
            print("Sending blind down to {}".format(roller.name))
            await roller.move_bottom()

    async def do_open(self, hub_id, roller_id):
        """Command to open a roller."""
        roller = self._get_roller(hub_id, roller_id)
        if roller:
            print("Sending blind up to {}".format(roller.name))
            await roller.move_top()

    async def do_stop(self, hub_id, roller_id):
        """Command to stop a moving roller."""
        roller = self._get_roller(hub_id, roller_id)
        if roller:
            print("Sending blind stop to {}".format(roller.name))
            await roller.move_stop()

    def do_send(self, sargs):
        """Send a raw command to each hub."""
        jsargs = json.loads(sargs)
        for hub in self._hubs.values():
            self.add_job(hub.send_payload, jsargs)

    async def do_connect(self, hub_ip):
        await self.add_hub(hub_ip)

    def do_disconnect(self):
        """Command to disconnect all connected hubs."""
        for hub in self._hubs.values():
            self.add_job(hub.stop)

    def do_log(self, level):
        """Change logging level."""
        if level == "critical":
            _LOGGER.setLevel(logging.CRITICAL)
            print("Log level set to critical")
        elif level == "error":
            _LOGGER.setLevel(logging.ERROR)
            print("Log level set to error")
        elif level == "warning":
            _LOGGER.setLevel(logging.WARNING)
            print("Log level set to warning")
        elif level == "info":
            _LOGGER.setLevel(logging.INFO)
            print("Log level set to info")
        elif level == "debug":
            _LOGGER.setLevel(logging.DEBUG)
            print("Log level set to debug")
        else:
            print("Valid log levels are critical, error, warning, info, and debug.")

    def do_exit(self):
        """Command to exit."""
        print("Exiting")
        self.running = False
        for hub in self._hubs.values():
            self.async_add_job(hub.stop())
        return True


