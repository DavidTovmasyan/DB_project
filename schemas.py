from typing import List, Optional

from pydantic import BaseModel

class VacationPlaceBase(BaseModel):
    country: str
    place: str
    hotel: str
    main_speciality: Optional[str] = None
    sea: str

class VacationPlaceCreate(VacationPlaceBase):
    pass

class VacationPlace(VacationPlaceBase):
    id: int

    class Config:
        orm_mode = True

# Added for querry
class GetVacationPlacesFilter(BaseModel):
    country: Optional[str] = None

class PersonBase(BaseModel):
    passport: str
    foreign_passport: Optional[str] = None
    country: str
    contacts: str
    name: str
    surname: str
    second_name: Optional[str] = None

class PersonCreate(PersonBase):
    pass

class Person(PersonBase):
    id: int
    tours: List["Tour"] = []

    class Config:
        orm_mode = True

class TourBase(BaseModel):
    price: float
    discount: float
    start_date: str
    end_date: str

class TourCreate(TourBase):
    vacation_place_id: int
    person_id: int

class Tour(TourBase):
    id: int
    vacation_place: VacationPlace
    person: Person

    class Config:
        orm_mode = True


# New query schemas
class SelectQuery(BaseModel):
    condition1: str
    condition2: str

class JoinQuery(BaseModel):
    pass

class UpdateQuery(BaseModel):
    condition: str
    update_field: str

class GroupByQuery(BaseModel):
    field: str

class SortQuery(BaseModel):
    field: str

'''
Example code
from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
'''