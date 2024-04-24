"""
    This file is part of joo library.
    :copyright: Copyright 1993-2024 Wooloo Studio.  All rights reserved.
    :license: MIT, check LICENSE for details.
"""
import threading
from abc import ABC, abstractmethod
from joo import ManagedObject
from joo.logging import LoggerHelper

class Connection(ABC, ManagedObject, LoggerHelper):
    def __init__(self, **kwargs):
        ManagedObject.__init__(self)
        LoggerHelper.__init__(self)

        # settings
        self._default_params = kwargs

        # control
        self._handle = None
        self._open_params = None

    def __del__(self):
        self.close()
        ManagedObject.__del__(self)

    @property
    def handle(self):
        return self._handle if self._state == "opened" else self.open()
    
    @abstractmethod
    def _open(self, **kwargs): return None

    def open(self, **kwargs):
        if self._state: return None
        self._open_params = self._default_params
        self._open_params.update(kwargs)
        self._handle = self._open(**self._open_params)
        if self._handle is None: return None
        self._state = "opened"
        return self._handle
 
    @abstractmethod
    def _close(self, handle): pass

    def close(self):
        if self._state != "opened": return
        if self._handle: self._close(self._handle)
        self._handle = None
        self._open_params = None
        self._state = None

    def reopen(self):
        if self._state != "opened": return None
        self.debug("Reconnecting database...")
        if self._handle: self._close(self._handle)
        self._handle = self._open(**self._open_params)
        return self._handle

class ConnectionPool(ManagedObject, LoggerHelper):
    def __init__(self, connection_class, min_size=0, max_size=0, init=True, **kwargs):
        ManagedObject.__init__(self)
        LoggerHelper.__init__(self)

        # settings
        self._connection_class = connection_class
        self._connection_params = kwargs
        self._pool_min_size = min_size
        self._pool_max_size = max_size

        # control
        self._pool = None
        self._pool_lock = threading.Lock()

    def __del__(self):
        self.cleanup()
        ManagedObject.__del__(self)

    def __add_connection(self, in_use):
        try:
            connection_obj = self._connection_class(**self._connection_params)
            connection_obj.bind_logger(self.logger)
            if connection_obj.open() is None: return None
            self._pool.append([connection_obj, in_use])
            return connection_obj
        except Exception as ex:
            self.exception(ex)
            return None
        
    def initialize(self):
        if self._state: return False
        self._pool = []
        with self._pool_lock:
            while len(self._pool) < self._pool_min_size:
                if self.__add_connection(False) is None: return False
        self._state = "inited"
        return True

    def cleanup(self):
        # NOTE: not to check state to handle failure case of initialize()
        with self._pool_lock:
            if self._pool:
                while len(self._pool) > 0:
                    item = self._pool.pop()
                    item[0].close()
        self._pool = None
        self._state = None

    def get_connection(self):
        if self._state != "inited": return
        with self._pool_lock:
            # health check
            while True:
                bad_index = None
                for index in range(len(self._pool)):
                    item = self._pool[index]
                    if item[1]: continue
                    if item[0].handle is None:
                        bad_index = index
                        break
                if bad_index is None: break
                item = self._pool.pop(bad_index)
                item[0].close()

            # get existing connection
            for item in self._pool:
                if item[1]: continue
                item[1] = True
                return item[0]
            
            # get new connection
            if self._pool_max_size > 0:
                if len(self._pool) >= self._pool_max_size: return None
            return self.__add_connection(True)
    
    def release_connection(self, connection):
        if self._state != "inited": return
        with self._pool_lock:
            for item in self._pool:
                if item[0] != connection: continue
                item[1] = False
