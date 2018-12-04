# -*- coding: utf-8 -*-

import enum
from typing import Union
import sqlalchemy.ext.declarative


class SQLLogging(enum.Enum):
    NONE = enum.auto()
    STATEMENTS = enum.auto()
    STATEMENTS_AND_ROWS = enum.auto()

    def sqlalchemy_echo(self) -> Union[bool, str]:
        if self is self.__class__.STATEMENTS:
            return True
        elif self is self.__class__.STATEMENTS_AND_ROWS:
            return 'debug'
        else:
            return False


_DeclarativeBase = sqlalchemy.ext.declarative.declarative_base()
