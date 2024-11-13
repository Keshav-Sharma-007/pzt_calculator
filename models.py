from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)  # "admin" or "planner"

class PZTTile(Base):
    __tablename__ = "pzt_tiles"
    id = Column(Integer, primary_key=True, index=True)
    size = Column(Float)  # in square meters
    power_capacity = Column(Float)  # watts per footstep
    cost = Column(Float)  # cost per tile
