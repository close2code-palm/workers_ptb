"""Contains data models for sqlalchemy and data passages"""


import datetime
from dataclasses import dataclass

from sqlalchemy import Column, Integer, Date, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


@dataclass
class UserData:
    nsp: str
    birth_date: datetime.date
    role: str


class Roles(Base):
    __tablename__ = 'roles'

    role_id = Column(Integer, primary_key=True)
    role_name = Column(String)


class Worker(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    birth_date = Column(Date)
    name_surname_patronymic = Column(String)
    role_id = Column(Integer, ForeignKey("roles.role_id"))
    updated_at = Column(DateTime)  # for sorting


worker_table = Worker.__table__
roles_table = Roles.__table__
