# -*- coding: utf-8 -*-

import enum


class Scope(enum.Enum):
    READ_STATION = enum.auto()
    READ_THERMOSTAT = enum.auto()
    WRITE_THERMOSTAT = enum.auto()
    READ_CAMERA = enum.auto()
    WRITE_CAMERA = enum.auto()
    ACCESS_CAMERA = enum.auto()
    READ_PRESENCE = enum.auto()
    ACCESS_PRESENCE = enum.auto()
    READ_HOMECOACH = enum.auto()

    def __str__(self) -> str:
        return self.name.lower()

    @classmethod
    def default(cls) -> 'Scope':
        return cls.READ_STATION
