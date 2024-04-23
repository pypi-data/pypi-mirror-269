"""models.py"""
from sqlalchemy import Column, Integer, String, Boolean,Text
from models.database import Database

#instance for database
db=Database()

#instance for create declarative base
Base=db.create_base()


class Environment(Base):
    """
    Table ENVIRONMENT
    """

    __tablename__='ENVIRONMENT'

    id = Column(Integer, primary_key=True,index=True,autoincrement=True)
    name=Column(String)
    url=Column(String)
    enabled=Column(Boolean,default=bool(True))
    version=Column(String)
    is_latest=Column(Boolean,default=bool(True))
    base_image_id=Column(Integer,default=0)
    short_name = Column(String(5))
    status = Column(String,default="Draft")
    icon=Column(String)
    py_version=Column(String)
    r_version=Column(String)
    py_requirements=Column(Text)
    r_requirements=Column(Text)
    py_requirements_compiled=Column(Text)
    r_requirements_compiled=Column(Text)
    