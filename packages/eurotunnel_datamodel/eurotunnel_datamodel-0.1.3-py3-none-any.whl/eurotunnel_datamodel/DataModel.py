# -*- coding: utf-8 -*-
"""
This file contains the entire datamodel, otherwise you  get circular references
Created on Mon Mar  4 11:25:18 2024

@author: morriscz
"""

from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


import datetime

from .DatabaseHelpers import get_engine

class Base(DeclarativeBase):
    pass


class SpringLocation(Base):
    __tablename__ = "spring_locations"

    """primary key. DO not display to user"""
    spring_location_id: Mapped[int] = mapped_column(primary_key=True)
    """Foreign key.  which train pass this spring location is part of"""
    train_pass_id: Mapped[int] = mapped_column(ForeignKey("train_pass.train_pass_id"))
    """The sql alchemy link to the train pass"""
    train_pass: Mapped["TrainPass"] = relationship(
        "TrainPass", back_populates="spring_locations"
    )
    """Number of the wagon (ID from RFID? Not sure of source)"""
    carriage_number: Mapped[Optional[int]]
    """The number of the wheel - this is relative to the entire train, not the wagon"""
    wheel_number: Mapped[int]
    """Left not right"""
    side: Mapped[Optional[bool]]
    """How sure are we there's a spring (0-1)"""
    confidence: Mapped[float]
    """Path to the image which should be displayed"""
    best_image_path: Mapped[str]
    """When did this happen"""
    timestamp: Mapped[datetime.datetime]


class TrainPass(Base):
    __tablename__ = "train_pass"

    """Primary key. Do not display"""
    train_pass_id: Mapped[int] = mapped_column(primary_key=True)

    """Pass start time"""
    time_start: Mapped[datetime.datetime]

    """Pass finished time"""
    time_finished: Mapped[datetime.datetime]

    """A train ID code (no idea of source, I was told I needed it, I don't know how we're populating it)"""
    train_id: Mapped[Optional[str]]
    """Much like the above, it's a string telling you what service it is. No idea of source again"""
    train_service_code: Mapped[Optional[str]] = mapped_column(
        comment="headcode or similar"
    )
    """The sqlalchemy link back to the spring locations"""
    spring_locations: Mapped[List["SpringLocation"]] = relationship('SpringLocation',uselist=True, back_populates="train_pass" )


class Users(Base):
    __tablename__ = "users"

    """Primary key."""
    user_id: Mapped[int] = mapped_column(primary_key=True)

    """Username"""
    user_name: Mapped[str]

    """hashed password"""
    password_hash: Mapped[str]

    """password salt"""
    password_salt: Mapped[str]

    """Display name"""
    display_name: Mapped[str]


def createSchema():
    """Creates the database on the server. Not to be used in production"""
    with get_engine() as engine:
        Base.metadata.create_all(engine)
