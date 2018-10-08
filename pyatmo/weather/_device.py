# -*- coding: utf-8 -*-


class Device:
    def __init__(
            self,
            id: str,
            name: str,
            latitude: float,
            longitude: float,
            altitude: float) -> None:
        self._id = id
        self._name = name
        self._latitude = latitude
        self._longitude = longitude
        self._altitude = altitude

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def latitude(self) -> float:
        return self._latitude

    @property
    def longitude(self) -> float:
        return self._longitude

    @property
    def altitude(self) -> float:
        return self._altitude

    @classmethod
    def create_table_command(cls):
        return ('create table devices'
                '(id text primary key,'
                ' name text,'
                ' latitude real,'
                ' longitude real,'
                ' altitude real)')
