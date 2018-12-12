# -*- coding: utf-8 -*-

import sqlalchemy
from ._sqlalchemy import _DeclarativeBase


class Device(_DeclarativeBase):
    # table naame
    __tablename__ = 'devices'
    # column
    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    latitude = sqlalchemy.Column(sqlalchemy.Float)
    longitude = sqlalchemy.Column(sqlalchemy.Float)
    altitude = sqlalchemy.Column(sqlalchemy.Float)
    # relationship
    modules = sqlalchemy.orm.relationship(
            'Module',
            order_by='Module.id',
            back_populates='device',
            lazy='immediate',
            cascade='all, delete-orphan')

    def __repr__(self) -> str:
        mapper = sqlalchemy.inspect(self.__class__)
        return '{0}.{1}({2})'.format(
                self.__class__.__module__,
                self.__class__.__name__,
                ', '.join(
                        '{0}={1}'.format(column.key,
                                         repr(getattr(self, column.key)))
                        for column in mapper.column_attrs))


class Module(_DeclarativeBase):
    # table name
    __tablename__ = 'modules'
    # column
    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    device_id = sqlalchemy.Column(
            sqlalchemy.String,
            sqlalchemy.ForeignKey('devices.id'))
    name = sqlalchemy.Column(sqlalchemy.String)
    module_type = sqlalchemy.Column(sqlalchemy.String)
    data_type = sqlalchemy.Column(sqlalchemy.String)
    # relationship
    device = sqlalchemy.orm.relationship(
            'Device',
            back_populates='modules',
            lazy='immediate')
    measurements = sqlalchemy.orm.relationship(
            'Measurements',
            cascade='all')

    def __repr__(self) -> str:
        mapper = sqlalchemy.inspect(self.__class__)
        return '{0}.{1}({2})'.format(
                self.__class__.__module__,
                self.__class__.__name__,
                ', '.join(
                        '{0}={1}'.format(column.key,
                                         repr(getattr(self, column.key)))
                        for column in mapper.column_attrs))


class Measurements(_DeclarativeBase):
    # table name
    __tablename__ = 'measurements'
    # column
    timestamp = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    module_id = sqlalchemy.Column(
            sqlalchemy.String,
            sqlalchemy.ForeignKey('modules.id'),
            primary_key=True)
    temperature = sqlalchemy.Column(sqlalchemy.Float)
    humidity = sqlalchemy.Column(sqlalchemy.Float)
    pressure = sqlalchemy.Column(sqlalchemy.Float)
    co2 = sqlalchemy.Column(sqlalchemy.Float)
    noise = sqlalchemy.Column(sqlalchemy.Float)
    rain = sqlalchemy.Column(sqlalchemy.Float)
    wind_strength = sqlalchemy.Column(sqlalchemy.Float)
    wind_angle = sqlalchemy.Column(sqlalchemy.Float)
    gust_strength = sqlalchemy.Column(sqlalchemy.Float)
    gust_angle = sqlalchemy.Column(sqlalchemy.Float)
    # replationship
    module = sqlalchemy.orm.relationship(
            'Module',
            lazy='immediate')

    def __repr__(self) -> str:
        mapper = sqlalchemy.inspect(self.__class__)
        return '{0}.{1}({2})'.format(
                self.__class__.__module__,
                self.__class__.__name__,
                ', '.join(
                        '{0}={1}'.format(column.key,
                                         repr(getattr(self, column.key)))
                        for column in mapper.column_attrs))
