from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func

from . import models, schemas

'''
def initialize_database(db_url: str):
    engine = create_engine(db_url)
    models.Base.metadata.create_all(bind=engine)
'''
# CRUD operations for VacationPlace
def create_vacation_place(db: Session, vacation_place: schemas.VacationPlaceCreate):
    db_vacation_place = models.VacationPlace(**vacation_place.dict())
    db.add(db_vacation_place)
    db.commit()
    db.refresh(db_vacation_place)
    return db_vacation_place

def get_vacation_place(db: Session, vacation_place_id: int):
    return db.query(models.VacationPlace).filter(models.VacationPlace.id == vacation_place_id).first()

def get_vacation_places(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.VacationPlace).offset(skip).limit(limit).all()

def update_vacation_place(db: Session, vacation_place_id: int, vacation_place: schemas.VacationPlaceCreate):
    db_vacation_place = db.query(models.VacationPlace).filter(models.VacationPlace.id == vacation_place_id).first()
    for key, value in vacation_place.dict().items():
        setattr(db_vacation_place, key, value)
    db.commit()
    db.refresh(db_vacation_place)
    return db_vacation_place

def delete_vacation_place(db: Session, vacation_place_id: int):
    db.query(models.VacationPlace).filter(models.VacationPlace.id == vacation_place_id).delete()
    db.commit()

# CRUD operations for Person
def create_person(db: Session, person: schemas.PersonCreate):
    db_person = models.Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

def get_person(db: Session, person_id: int):
    return db.query(models.Person).filter(models.Person.id == person_id).first()

'''def get_persons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Person).offset(skip).limit(limit).all()'''

def get_persons(db: Session, skip: int = 0, limit: int = 100, sort_by: str = None):
    if sort_by == models.Person.id:
        return db.query(models.Person).order_by(sort_by).offset(skip).limit(limit).all()
    elif sort_by == models.Person.name:
        return db.query(models.Person).order_by(sort_by).offset(skip).limit(limit).all()
    else:
        print("Wrong argument!")

def update_person(db: Session, person_id: int, person: schemas.PersonCreate):
    db_person = db.query(models.Person).filter(models.Person.id == person_id).first()
    for key, value in person.dict().items():
        setattr(db_person, key, value)
    db.commit()
    db.refresh(db_person)
    return db_person

def delete_person(db: Session, person_id: int):
    db.query(models.Person).filter(models.Person.id == person_id).delete()
    db.commit()

# CRUD operations for Tour
def create_tour(db: Session, tour: schemas.TourCreate):
    db_tour = models.Tour(**tour.dict())
    db.add(db_tour)
    db.commit()
    db.refresh(db_tour)
    return db_tour

def get_tour(db: Session, tour_id: int):
    return db.query(models.Tour).filter(models.Tour.id == tour_id).first()

def get_tours(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tour).offset(skip).limit(limit).all()

def update_tour(db: Session, tour_id: int, tour: schemas.TourCreate):
    db_tour = db.query(models.Tour).filter(models.Tour.id == tour_id).first()
    for key, value in tour.dict().items():
        setattr(db_tour, key, value)
    db.commit()
    db.refresh(db_tour)
    return db_tour

def delete_tour(db: Session, tour_id: int):
    db.query(models.Tour).filter(models.Tour.id == tour_id).delete()
    db.commit()

# For our queries
    
def get_persons_filtered(db: Session, skip: int = 0, limit: int = 100, **filters):
    return db.query(models.Person).filter_by(**filters).offset(skip).limit(limit).all()

def get_tours_with_places(db: Session):
    return db.query(models.Tour).join(models.VacationPlace).all()

def update_tour_price(db: Session, tour_id: int, new_price: float):
    db_tour = db.query(models.Tour).filter(models.Tour.id == tour_id).first()
    if db_tour:
        db_tour.price = new_price
        db.commit()
        db.refresh(db_tour)
    return db_tour

def get_tours_count_per_place(db: Session):
    return db.query(models.VacationPlace.country, func.count(models.Tour.id).label('tour_count')).join(models.Tour).group_by(models.VacationPlace.country).all()

# For sorting, I have modified the already existing function
