from fastapi import FastAPI,Path
from enum import Enum
from pydantic import BaseModel

app = FastAPI()

# GET - To Fetch info
# POST - To create something
# PUT - Updating
# DELETE - Delete something


@app.get("/")

def root():
    return {"message" : "Hello World"}

@app.post("/")

def post():
    return {"message" : "Hello World from post route"}

@app.put("/")

def put():
    return {"message" : "Hello from the put route"}


# # # # # # # # # # # # # # # # # # # 

# @app.get("/items")
# def list_items():
#     return {"message" : "list items route"}

@app.get("/items/{item_id}")
def get_item(item_id : int):
    return {"item_id" : item_id}


@app.get("/users/{user_id}")
def getuser(user_id : str):
    return {"user" : user_id}

@app.get("/users/me")
def getcurrentuser():
    return {"message" : "this is the current user"}

# # # # # # # # # # # # # # # # # # # 

class FoodEnum(str, Enum):
    fruits = "fruits"
    vegetables = "vegetables"
    dairy = "dairy"

@app.get("/food/{food_name}")
def getfood(food_name : FoodEnum):
    if food_name == FoodEnum.vegetables:
        return {"food_name" : food_name, "message" : "You are Healthy"}
    
    if food_name.value == "fruits":
        return {"food_name" : food_name, "message" : "Still healthy but like sweeter options"}
    
    else:
        return {"food_name" : food_name, "message" : "You like Dairy Items"}
    

# # # # # # # # # # # # # # # # # # #  Query Parameters

fake_items_db = [{"item_name" : "Soh"}, {"item_name" : "Cah"}, {"item_name" : "Toa"}]

@app.get("/item")
def list_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip+limit]

@app.get("/users/{user_id}/item/{item_id}")
def getitem(user_id : str,item_id : str, q: str | None = None, short : bool = False):
    item = {"item_id" : item_id, "user_id" : user_id}
    if q:
        item.update({"q" : q})
    
    if not short:
        item.update({"description" : "lorem ipsum nmano nnhg hgh w hiwh helo nhi fhi whi sbbb"})
    
    return item

# # # # # # # # # # # # # # # # #
class Item(BaseModel):
    name : str
    description : str | None = None
    price : float
    tax : float | None = None
    
@app.post("/item")
def create_item(item : Item):
    item_dict = item.dict()

    if item.tax:
        price_after_tax = item.tax + item.price
        item_dict.update({"Price after Tax" : price_after_tax})

    return item_dict

@app.put("/item/{item_id}")
def create_item_withput(item_id : int, item : Item):
    return {"item_id" : item_id, **item.dict()}


# # # #  # # # #  # # # # #  # # # #  # # # # 
from fastapi import Query

# Query attributes:
# None = value is optional
# ... = default value can be anything but is required field (or no default value)
# min_length = minimum length
# max_length = maximum length
# regex = regular expression
# title=
# description=
# alias = access query with an alias

@app.get("/items")
def get_items_(q: list[str] = Query(..., min_length=2, max_length=10, regex="[A-Z]")):
    results = {"sample" : [{"1": "hello", "2": "world"}]}

    if q:
        results.update({"q":q}) # type: ignore
    return results

# Hidden Query

@app.get("/items_/hidden")
async def hiddenquery(hidden_query : str | None = Query(None, include_in_schema=False)):
    if hidden_query:
        return {"hidden query" : hidden_query}
    else:
        return {"hidden_query" : "Not found"}
    
@app.get("/items_validation/{item_id}")
async def read_items_validation(item_id : int = Path(... , title="The id of the item to get"), q : str | None = Query(None, alias="item_query", )):
    results = {"item_id" : item_id}
    if q:
        results.update({"q" : q})  # type: ignore
    
    return results


## for numeric validation: 
# use parameters like:
# ge= : greater than or equal to
# le= : lesser than or equal to
# gt= : greater than
# lt= : lesser than

@app.get("/items__validation/{item_id}")
async def read_i_validation(q : str, item_id : int = Path(... , title="The id of the item to get")):
    results = {"item_id" : item_id}
    if q:
        results.update({"q" : q})  # type: ignore
    
    return results

