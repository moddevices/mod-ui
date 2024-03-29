#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2012-2023 MOD Audio UG
# SPDX-License-Identifier: AGPL-3.0-or-later

import logging
from tornado.ioloop import IOLoop
from mod.hmi import HMI
from mod.host import Host

class FakeHMI(HMI):
    def __init__(self, init_cb):
        HMI.__init__(self, 0, 0, 0, init_cb, None)

    def isFake(self):
        return True

    def init(self, callback):
        IOLoop.instance().add_callback(callback)

    def set_host_map_callback(self, host_map):
        return

    def send(self, msg, callback=None, datatype='int'):
        logging.info(msg)
        if callback is None:
            return
        if datatype == 'boolean':
            callback(True)
        elif datatype == 'string':
            callback("")
        else:
            callback(0)

class FakeSocket(object):
    def write(self, data):
        return

    def read_until(self, msg, callback):
        return

class FakeHost(Host):
    def __del__(self):
        self.readsock = None
        self.writesock = None

    def open_connection_if_needed(self, websocket):
        if self.readsock is not None and self.writesock is not None:
            self.report_current_state(websocket)
            return

        if self.readsock is None:
            self.readsock = FakeSocket()
        if self.writesock is None:
            self.writesock = FakeSocket()

        self.connected = True
        self.report_current_state(websocket)
        self.statstimer.start()

        if self.memtimer is not None:
            self.memtimer_callback()
            self.memtimer.start()

    # send data to host, set modified flag to true
    def send_modified(self, msg, callback=None, datatype='int'):
        self.pedalboard_modified = True
        if callback is not None:
            callback(True)

    # send data to host, don't change modified flag
    def send_notmodified(self, msg, callback=None, datatype='int'):
        if callback is not None:
            callback(True)
