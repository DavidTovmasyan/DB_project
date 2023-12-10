from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to create a new vacation place
@app.post("/vacation_places/", response_model=schemas.VacationPlace)
def create_vacation_place(vacation_place: schemas.VacationPlaceCreate, db: Session = Depends(get_db)):
    return crud.create_vacation_place(db=db, vacation_place=vacation_place)

@app.get("/vacation_places/", response_model=list[schemas.VacationPlace])
def read_vacation_places(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vacation_places = crud.get_vacation_places(db, skip=skip, limit=limit)
    return vacation_places

@app.get("/vacation_places/{vacation_place_id}", response_model=schemas.VacationPlace)
def read_vacation_place(vacation_place_id: int, db: Session = Depends(get_db)):
    db_vacation_place = crud.get_vacation_place(db, vacation_place_id=vacation_place_id)
    if db_vacation_place is None:
        raise HTTPException(status_code=404, detail="Vacation Place not found")
    return db_vacation_place

@app.put("/vacation_places/{vacation_place_id}", response_model=schemas.VacationPlace)
def update_vacation_place(vacation_place_id: int, vacation_place: schemas.VacationPlaceCreate, db: Session = Depends(get_db)):
    return crud.update_vacation_place(db=db, vacation_place_id=vacation_place_id, vacation_place=vacation_place)

@app.delete("/vacation_places/{vacation_place_id}", response_model=schemas.VacationPlace)
def delete_vacation_place(vacation_place_id: int, db: Session = Depends(get_db)):
    return crud.delete_vacation_place(db=db, vacation_place_id=vacation_place_id)


# CRUD operations for Person
@app.post("/persons/", response_model=schemas.Person)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    return crud.create_person(db=db, person=person)

@app.get("/persons/", response_model=list[schemas.Person])
def read_persons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    persons = crud.get_persons(db, skip=skip, limit=limit)
    return persons

@app.get("/persons/{person_id}", response_model=schemas.Person)
def read_person(person_id: int, db: Session = Depends(get_db)):
    db_person = crud.get_person(db, person_id=person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

@app.put("/persons/{person_id}", response_model=schemas.Person)
def update_person(person_id: int, person: schemas.PersonCreate, db: Session = Depends(get_db)):
    return crud.update_person(db=db, person_id=person_id, person=person)

@app.delete("/persons/{person_id}", response_model=schemas.Person)
def delete_person(person_id: int, db: Session = Depends(get_db)):
    return crud.delete_person(db=db, person_id=person_id)


# CRUD operations for Tour
@app.post("/tours/", response_model=schemas.Tour)
def create_tour(tour: schemas.TourCreate, db: Session = Depends(get_db)):
    return crud.create_tour(db=db, tour=tour)

@app.get("/tours/", response_model=list[schemas.Tour])
def read_tours(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tours = crud.get_tours(db, skip=skip, limit=limit)
    return tours

@app.get("/tours/{tour_id}", response_model=schemas.Tour)
def read_tour(tour_id: int, db: Session = Depends(get_db)):
    db_tour = crud.get_tour(db, tour_id=tour_id)
    if db_tour is None:
        raise HTTPException(status_code=404, detail="Tour not found")
    return db_tour

@app.put("/tours/{tour_id}", response_model=schemas.Tour)
def update_tour(tour_id: int, tour: schemas.TourCreate, db: Session = Depends(get_db)):
    return crud.update_tour(db=db, tour_id=tour_id, tour=tour)

@app.delete("/tours/{tour_id}", response_model=schemas.Tour)
def delete_tour(tour_id: int, db: Session = Depends(get_db)):
    return crud.delete_tour(db=db, tour_id=tour_id)


'''
Example code
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
'''