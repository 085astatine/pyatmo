# -*- coding: utf-8 -*-

import logging
import pathlib
import sqlite3
from typing import Optional
from .._client import Client


class Database:
    def __init__(
            self,
            path: pathlib.Path,
            client: Client,
            logger: Optional[logging.Logger] = None) -> None:
        # logger
        self._logger = logger or logging.getLogger(__name__)
        # client
        self._client = client
        # connection
        is_initialized = path.exists()
        self._connection = sqlite3.connect(str(path))
        self._connection.row_factory = sqlite3.Row
        if not is_initialized:
            _create_table(self)


def _create_table(self: Database) -> None:
    self._logger.info('create table')
    cursor = self._connection.cursor()
    # devices
    cursor.execute(
            'CREATE TABLE devices'
            '(id text PRIMARY KEY,'
            ' name text,'
            ' latitude real,'
            ' longitude real,'
            ' altitude real)')
    # modules
    cursor.execute(
            'CREATE TABLE modules'
            '(id text PRIMARY KEY,'
            ' device_id text not null,'
            ' name text,'
            ' module_type text,'
            ' data_type text)')
    # meaturements
    cursor.execute(
           'Create Table measurements'
           '(timestamp integer not null,'
           ' module_id text not null,'
           ' temperature real,'
           ' humidity real,'
           ' pressure real,'
           ' co2 real,'
           ' noise real,'
           ' rain real,'
           ' wind_strength real,'
           ' wind_angle real,'
           ' gust_strength real,'
           ' gust_angle real)')
    # commit
    self._connection.commit()
    cursor.close()
