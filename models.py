import enum
import datetime
import alembic
import sqlalchemy.orm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import *

engine = create_engine("mysql+pymysql://root:root@localhost:5900/adservice", echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()
class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(45), nullable=False)
    city = Column(String(45), nullable=False)

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), nullable=False)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstName = Column(String(45),  nullable=False)
    lastName = Column(String(45),  nullable=False)
    email = Column(String(45), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    phone = Column(String(45), nullable=False, unique=True)
    userStatus = Column(Enum('regular', 'premium'), nullable=False, default='regular')
    fk_location_id = Column(Integer, ForeignKey('location.id'), primary_key=True, nullable=False)


class LocalAd(Base):
    __tablename__ = 'localad'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(45), nullable=False)
    fk_category = Column(Integer, ForeignKey('category.id'), primary_key=True, nullable=False)
    status = Column(Enum('active', 'closed', 'confirmed'), nullable=False)
    publishingDate = Column(DateTime, nullable=False, default=datetime.datetime.now())
    about = Column(String(45))
    photoUrls = Column(LargeBinary, nullable=True)
    fk_user_id = Column(Integer, ForeignKey('user.id'), nullable=True, primary_key=True)
    fk_location_id = Column(Integer, ForeignKey('location.id'), nullable=False, primary_key=True)

class PublicAd(Base):
    __tablename__ = 'publicad'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(45), nullable=False)
    fk_category = Column(Integer, ForeignKey('category.id'), primary_key=True, nullable=False)
    status = Column(Enum('active', 'closed', 'confirmed'), nullable=False)
    publishingDate = Column(DateTime, nullable=False, default=datetime.datetime.now())
    about = Column(String(45))
    photoUrls = Column(LargeBinary, nullable=True)
    fk_user_id = Column(Integer, ForeignKey('user.id'), nullable=True, primary_key=True)