# -*- coding: utf-8 -*-

import enum
from typing import Union
import sqlalchemy.ext.declarative


class SQLLoggingLevel(enum.Enum):
    NONE = enum.auto()
    STATEMENTS = enum.auto()
    STATEMENTS_AND_ROWS = enum.auto()

    def sqlalchemy_echo(self) -> Union[bool, str]:
        if self is SQLLoggingLevel.STATEMENTS:
            return True
        if self is SQLLoggingLevel.STATEMENTS_AND_ROWS:
            return 'debug'
        return False


_DeclarativeBase = sqlalchemy.ext.declarative.declarative_base()
