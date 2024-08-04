# Extra Data Types

from fastapi import FastAPI, Body
from uuid import UUID
from datetime import datetime, time, timedelta

app = FastAPI()

@app.put("/items/{item_id}")
async def read_items(item_id : UUID, 
                     start_date : datetime | None = Body(None), 
                     end_date : datetime | None = Body(None),
                     repeat_at : time | None = Body(None),
                     process_after : timedelta | None = Body(None)):
    
    start_process = start_date + process_after #type: ignore
    duration = end_date - start_process
    return {"item_id" : item_id, 
            "start_date" : start_date,
            "end_date" : end_date,
            "repeat_at" : repeat_at,
            "process_after" : process_after,
            "start_process" : start_process,
            "duration" : duration}


# Cookie and Header Parameters:

from fastapi import Cookie, Header

@app.get("/items")
async def read_cookie_item(cookie_id : str | None = Cookie(None), 
                           accept_encoding : str | None = Header(None),
                           sec_ch_ua : str | None  = Header(None),
                           user_agent : str | None = Header(None),
                           x_token : list[str] | None = Header(None)
):
    return {"cookie_id" : cookie_id, "accept_encoding" : accept_encoding, "sec_ch_ua" : sec_ch_ua, "user_agent" : user_agent, "X-token" : x_token}

# User Response Model

from pydantic import BaseModel,EmailStr

class UserBase(BaseModel):
    username: str
    email : EmailStr
    full_name : str | None = None

# class UserIn(UserBase):
#     password : str

# class UserOut(UserBase):
#     pass

# @app.post("/user/", response_model=UserIn)  # If UserOut is used then it will only return the attributes of UserBase
# async def create_user(User : UserIn):
#     return User


# # # # # #
class Item(BaseModel):
    name : str
    description : str | None = None
    price : float
    tax : float = 10.5
    tags : list[str] = []

Items = {
    "abc" : {"name" : "ABC", "price" : 50.2},
    "def" : {"name" : "DEF", "description" : "This is the description", "price" : 25.3, "tax" : 5.5},
    "fgh" : {"name" : "FGH", "description" : None, "price" : 80.1, "tax" : 20.5, "tags" : []}
}


# response_model_exclude_unset=True
# if False it will return all the values even if they are NULL or empty

@app.get("/item/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def find_item(item_id : str):
    return Items[item_id]


from typing import Literal

# Only "name" and "description" elements will be visible even if other elements may or may not be defined.

# if {"name", "description"} is written like ["name", "description"]
# pydantic will convert this to a set

@app.get("/items/{item_id}/name", response_model=Item, response_model_include={"name", "description"})
async def read_item_name(item_id : Literal["abc", "def", "fgh"]):
    return Items[item_id]

# Only "tax" elements will be excluded even if it is defined.

@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public(item_id : Literal["abc", "def", "fgh"]):
    return Items[item_id]