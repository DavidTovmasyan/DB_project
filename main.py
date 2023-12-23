from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="DB_project/templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# UI

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    context = {'request' : request}
    return templates.TemplateResponse("index.html", context)

# On start fills the 'person' if not filled yet
# For 3rd step

@app.on_event("startup")
def startup_populate_db():
    db = SessionLocal()
    num_persons = db.query(models.Person).count()
    if num_persons == 0:
        persons = []
        for i in range(1000):
            temp_person = {'id':i+1, 'passport':'', 'foreign_passport':'',
                           'country': '', 'contacts':'', 'name':f"person {i+1} name",
                           'surname':f"person {i+1} surname", 'second_name':f"person {i+1} second_name"}
            persons.append(temp_person)
        for person in persons:
            db.add(models.Person(**person))
        db.commit()
        db.close()
    else:
        print(f"{num_persons} person(s) already exist")

# Endpoint to create a new vacation place
@app.post("/vacation_places/create", response_model=schemas.VacationPlace)
def create_vacation_place(vacation_place: schemas.VacationPlaceCreate, db: Session = Depends(get_db)):
    return crud.create_vacation_place(db=db, vacation_place=vacation_place)

@app.get("/vacation_places/", response_model=list[schemas.VacationPlace], response_class=HTMLResponse)
def read_vacation_places(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vacation_places = crud.get_vacation_places(db, skip=skip, limit=limit)
    return templates.TemplateResponse("vacation_place_get.html", {"request": request, "vacation_places": vacation_places})

@app.get("/vacation_places/{vacation_place_id}", response_model=schemas.VacationPlace, response_class=HTMLResponse)
def read_vacation_place(request: Request,vacation_place_id: int, db: Session = Depends(get_db)):
    db_vacation_place = crud.get_vacation_place(db, vacation_place_id=vacation_place_id)
    if db_vacation_place is None:
        raise HTTPException(status_code=404, detail="Vacation Place not found")
    return templates.TemplateResponse("vacation_place_get_by_id.html", {"request": request, "vacation_place":db_vacation_place})

@app.put("/vacation_places/update/{vacation_place_id}", response_model=schemas.VacationPlace)
def update_vacation_place(vacation_place_id: int, vacation_place: schemas.VacationPlaceCreate, db: Session = Depends(get_db)):
    return crud.update_vacation_place(db=db, vacation_place_id=vacation_place_id, vacation_place=vacation_place)

@app.delete("/vacation_places/delete/{vacation_place_id}", response_model=schemas.VacationPlace)
def delete_vacation_place(vacation_place_id: int, db: Session = Depends(get_db)):
    return crud.delete_vacation_place(db=db, vacation_place_id=vacation_place_id)


# CRUD operations for Person
@app.post("/persons/create", response_model=schemas.Person)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    return crud.create_person(db=db, person=person)

@app.get("/persons/", response_model=list[schemas.Person], response_class=HTMLResponse)
def read_persons(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    persons = crud.get_persons(db, skip=skip, limit=limit, sort_by=models.Person.id)
    return templates.TemplateResponse("person_get.html", {"request": request, "persons": persons})


@app.get("/persons/{person_id}", response_model=schemas.Person, response_class=HTMLResponse)
def read_person(request:Request, person_id: int, db: Session = Depends(get_db)):
    db_person = crud.get_person(db, person_id=person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return templates.TemplateResponse("person_get_by_id.html", {"request":request, "person":db_person})

@app.put("/persons/update/{person_id}", response_model=schemas.Person)
def update_person(person_id: int, person: schemas.PersonCreate, db: Session = Depends(get_db)):
    return crud.update_person(db=db, person_id=person_id, person=person)

@app.delete("/persons/delete/{person_id}", response_model=schemas.Person)
def delete_person(person_id: int, db: Session = Depends(get_db)):
    return crud.delete_person(db=db, person_id=person_id)


# CRUD operations for Tour
@app.post("/tours/create", response_model=schemas.Tour)
def create_tour(tour: schemas.TourCreate, db: Session = Depends(get_db)):
    return crud.create_tour(db=db, tour=tour)

@app.get("/tours/", response_model=list[schemas.Tour], response_class=HTMLResponse)
def read_tours(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tours = crud.get_tours(db, skip=skip, limit=limit)
    return templates.TemplateResponse("tour_get.html", {"request": request, "tours": tours})

@app.get("/tours/{tour_id}", response_model=schemas.Tour, response_class=HTMLResponse)
def read_tour(request: Request, tour_id: int, db: Session = Depends(get_db)):
    db_tour = crud.get_tour(db, tour_id=tour_id)
    if db_tour is None:
        raise HTTPException(status_code=404, detail="Tour not found")
    return templates.TemplateResponse("tour_get_by_id.html", {"request": request, "tour": db_tour})

@app.put("/tours/update/{tour_id}", response_model=schemas.Tour)
def update_tour(tour_id: int, tour: schemas.TourCreate, db: Session = Depends(get_db)):
    return crud.update_tour(db=db, tour_id=tour_id, tour=tour)

@app.delete("/tours/delete/{tour_id}", response_model=schemas.Tour)
def delete_tour(tour_id: int, db: Session = Depends(get_db)):
    return crud.delete_tour(db=db, tour_id=tour_id)

# Addinq querries

# 1) Assuming you want to filter persons by name and country (SELECT ... WHERE)
@app.get("/persons/filter/{person_name}&&{person_country}", response_model=list[schemas.PersonBase], response_class=HTMLResponse)
def filter_persons(request: Request, name: str = None, country: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    filters = {}
    if name:
        filters["name"] = name
    if country:
        filters["country"] = country

    persons = crud.get_persons_filtered(db, skip=skip, limit=limit, **filters)
    return templates.TemplateResponse("person_get.html", {"request": request, "persons": persons})

# 2) Assuming you want to get tours with corresponding vacation places (JOIN)
@app.get("/tours-with-places", response_model=list[schemas.Tour], response_class=HTMLResponse)
def get_tours_with_places(request: Request, db: Session = Depends(get_db)):
    tours = crud.get_tours_with_places(db)
    return templates.TemplateResponse("tour_with_places.html", {"request": request, "tours": tours})

# 3) Assuming you want to update the price of a tour based on the tour_id (UPDATE with some condition)
@app.put("/tours/update_price/{tour_id}", response_model=schemas.Tour)
def update_tour_price(tour_id: int, new_price: float, db: Session = Depends(get_db)):
    return crud.update_tour_price(db=db, tour_id=tour_id, new_price=new_price)

# 4) Assuming you want to get the count of tours per vacation place
@app.get("/tours_count_per_place", response_model=dict, response_class=HTMLResponse)
def get_tours_count_per_place(request: Request, db: Session = Depends(get_db)):
    tour_count_per_place = crud.get_tours_count_per_place(db)
    return templates.TemplateResponse("tours_count_per_place.html", {"request": request, "tour_count_per_place": tour_count_per_place})

# 5) Assuming you want to get persons with optional sorting by name
@app.get("/persons_sort_by_name/", response_model=list[schemas.Person], response_class=HTMLResponse)
def read_persons(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    persons = crud.get_persons(db, skip=skip, limit=limit, sort_by=models.Person.name)
    return templates.TemplateResponse("person_get.html", {"request": request, "persons": persons})
