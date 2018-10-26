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
    device = sqlalchemy.orm.relationship('Device', back_populates='modules')

    def __repr__(self) -> str:
        mapper = sqlalchemy.inspect(self.__class__)
        return '{0}.{1}({2})'.format(
                self.__class__.__module__,
                self.__class__.__name__,
                ', '.join(
                        '{0}={1}'.format(column.key,
                                         repr(getattr(self, column.key)))
                        for column in mapper.column_attrs))


Device.modules = sqlalchemy.orm.relationship(
        'Module',
        order_by=Module.id,
        back_populates='device')
