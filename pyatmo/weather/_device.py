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


Device.modules = sqlalchemy.orm.relationship(
        'Module',
        order_by=Module.id,
        back_populates='device')
