from sqlalchemy import Boolean, Column, Date, Numeric, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class VacationPlace(Base):
    __tablename__ = "vacation_place"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(255))
    place = Column(String(255))
    hotel = Column(String(255))
    main_speciality = Column(String)
    sea = Column(String(255))

    tours = relationship("Tour", back_populates="vacation_place")

class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True, index=True)
    passport = Column(String(255))
    foreign_passport = Column(String(255))
    country = Column(String(255))
    contacts = Column(String(255))
    name = Column(String(255))
    surname = Column(String(255))
    second_name = Column(String(255))

    tours = relationship("Tour", back_populates="person")

class Tour(Base):
    __tablename__ = "tour"

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Numeric(10, 2))
    discount = Column(Numeric(10, 2))
    start_date = Column(Date)
    end_date = Column(Date)
    vacation_place_id = Column(Integer, ForeignKey("vacation_place.id"))
    person_id = Column(Integer, ForeignKey("person.id"))

    vacation_place = relationship("VacationPlace", back_populates="tours")
    person = relationship("Person", back_populates="tours")
