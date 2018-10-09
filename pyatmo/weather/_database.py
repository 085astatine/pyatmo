# -*- coding: utf-8 -*-

import logging
import pathlib
from typing import Optional
import sqlalchemy
from ._device import Device
from ._sqlalchemy import _DeclarativeBase
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
        # sqlalchemy engine
        self._engine = sqlalchemy.create_engine(
                'sqlite:///{0}'.format(path.as_posix()),
                encoding='utf-8')
        _DeclarativeBase.metadata.create_all(self._engine)
