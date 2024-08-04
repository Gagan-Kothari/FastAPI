from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()

# Body - Multiple Parameters

class Item(BaseModel):
    name : str
    description : str
    price : float
    tax : float

@app.put("/items/{item_id}")
async def update_item(
    *, 
    item_id : int = Path(... , title="ID of the parameter", ge=0 , le=100), 
    q : str | None = None,
    item : Item | None = None,
    user : str = Body(...)):    # to add another paramter like Item, we can use Body(), request body with a key value pair embed=True
    
    results = {"item_id" : item_id}

    if q:
        results.update({"q" : q}) #type: ignore
    
    if item:
        results.update({"item" : item}) #type: ignore

    return results



# Generic types in body elements

class Item2(BaseModel):
    name : str
    description : str | None = Field(None, title="Description of Item2", max_length=100) #######
    salary : float = Field(... , gt=0, description="Price must be greater than zero")
    tax : float | None = None


@app.put("/User/{user_id}")
async def upddate_item(user_id : int, item : Item2 = Body(... , embed=True)):
    result = {"user_id" : user_id}
    if item:
        result.update({"item" : item}) #type: ignore

    return result

## Body Nested Model

class Image(BaseModel):
    url : HttpUrl
    name : str

class Details(BaseModel):
    name : str
    price : float
    tags : list = []   
    
    # to add a specific return type to a list use 

    tag2 : list[str] = [] 

    # Only string elements will be accepted

    tag3 : set[str] = set() 

    # Only unique items will be returned

    image : list[Image]


class Offers(BaseModel):
    name : str
    description : str | None = None
    price : float
    items : list[Details]

@app.put("/details/{detail}")
async def details(detail : int, item : Details = Body(..., embed=True)):
    results = {"item_detail" : detail, "item" : item}

    return results

@app.post("/offers/{offer_id}")
async def post_offer(offer_id : int, offer : Offers = Body(..., embed=True)):
    results =  {"offer_id" : offer_id, "Offer" : offer}

    return results


# Decaring Request Example Data

class Item3(BaseModel):
    name : str
    description : str | None = None
    price : float
    tax : float | None = None

    class Config:
        schema_extra = {
            "example" : {
                "name" : "ABC",
                "description" : "this is description",
                "price" : 16.25,
                "tax" : 1.25
            }
        }

        # Can also be declared int function by using Body(..., "name": "ABC") 
        # and using Field(... / None, example="") on each item

        # __bold__ , _italics_

@app.put("/Item3/{item_id}")
async def update_the_item(item_id : int, item : Item3 = Body(..., embed=True)):
    result = {"item_id" : item_id, "item" : item}

    return result