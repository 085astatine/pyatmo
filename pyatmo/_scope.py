# -*- coding: utf-8 -*-

import enum


class Scope(enum.Enum):
    READ_STATION = 'read_station'
    READ_THERMOSTAT = 'read_thermostat'
    WRITE_THERMOSTAT = 'write_thermostat'
    READ_CAMERA = 'read_camera'
    WRITE_CAMERA = 'write_camera'
    ACCESS_CAMERA = 'accessss_camera'
    READ_PRESENCE = 'read_presence'
    ACCESS_PRESENCE = 'access_presence'
    READ_HOMECOACH = 'read_homecoach'
