from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import Literal, Union, List

app = FastAPI()

# Extra Models

class UserBase(BaseModel):
    username : str
    email : EmailStr
    full_name : str | None = None

class UserIn(UserBase):
    password : str
    
class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password : str

def fake_password_hasher(raw_password : str):
    return f'supersecret{raw_password}'

def fake_save_user(user_in : UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)

    print("User Saved")
    return user_in_db

@app.post("/user/", response_model=UserOut)
async def create_user(user_in : UserIn):
    user_saved = fake_save_user(user_in)

    return user_saved

# # # # # # # # # # # # # # # # # # # # # # # # # #

class BaseItem(BaseModel):
    description : str
    type : str

class CarItem(BaseItem):
    type = "car"

class PlaneItem(BaseItem):
    type = "plane"
    size : int

items = {
    "item1" : {"description" : "Life is a Haaaiwaaay, I wanna ride it oll nigh loonggg", "type" : "car"},
    "item2" : {"description" : "Fly me to the mOOOOOn and let me PLaaaayy among the stars", "type" : "plane", "size" : 5}
}

@app.get("/item/{id}", response_model=Union[PlaneItem, CarItem])
async def get_item(id : Literal["item1", "item2"]):
    result = items[id]

    return result

# # # # # # # # # # # # # # # # # # # # # # # # # #

class ListItem(BaseModel):
    name : str
    description : str

list_items = [
    {"name" : "abc", "description" : "item 1 description"},
    {"name" : "def", "description" : "item 2 description"},
]

# Response models can be lists and dictionaries as well

@app.get("/list_items/", response_model=List[ListItem])
async def read_items():
    return items

@app.get("/arbitrary", response_model=dict[str, float])
async def get_arbitrary():
    return {"hello" : 2.3, "world" : "4.2"}


# Status Codes

from fastapi import status

# for successful response

@app.post("/items/", status_code=201)
async def create_item(name : str):
    return {"name" : name}

# status_code=status.HTTP... to not memorise the status codes

@app.delete("/items/{pk}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(pk : str):
    print("pk", pk)
    return pk