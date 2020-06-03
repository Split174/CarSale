from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
"""
В файле описаны все таблицы БД
"""

class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    first_name = Column(Text)
    last_name = Column(Text)
    email = Column(Text, unique=True)
    password = Column(Text)

    def as_dict(self):
        acc = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        acc.pop('password')
        return acc


class Ad(Base):
    __tablename__ = 'ad'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    date = Column(Integer)
    seller_id = Column(Integer, ForeignKey('seller.id'))
    car_id = Column(Integer, ForeignKey('car.id'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class AdTag(Base):
    __tablename__ = 'adtag'
    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey('tag.id'))
    ad_id = Column(Integer, ForeignKey('ad.id'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Car(Base):
    __tablename__ = 'car'
    id = Column(Integer, primary_key=True)
    make = Column(Text)
    model = Column(Text)
    mileage = Column(Integer)
    num_owners = Column(Integer, default=1)
    reg_number = Column(Text)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class CarColor(Base):
    __tablename__ = 'carcolor'
    id = Column(Integer, primary_key=True)
    color_id = Column(Integer, ForeignKey('color.id'))
    car_id = Column(Integer,  ForeignKey('car.id'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Color(Base):
    __tablename__ = 'color'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    hex = Column(Text, unique=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    url = Column(Text)
    car_id = Column(Integer, ForeignKey('car.id'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Seller(Base):
    __tablename__ = 'seller'
    id = Column(Integer, primary_key=True)
    zip_code = Column(Integer, ForeignKey('zipcode.zip_code'))
    street = Column(Text)
    home = Column(Text)
    phone = Column(Text)
    account_id = Column(Integer, ForeignKey('account.id'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class ZipCode(Base):
    __tablename__ = 'zipcode'
    zip_code = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('city.id'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

