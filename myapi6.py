from fastapi import FastAPI

app = FastAPI()

# Error Handling

items = {
    "a" : "apple",
    "b" : "ball",
    "c" : "cat"
}

from fastapi import HTTPException

@app.get("/items/{item_id}")
async def get_item(item_id : str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found", headers={"X-Error" : "This is my error"})

    return {"item" : items[item_id]}

# User Exception

class UnicornException(Exception):
    def __init__(self, name : str):
        self.name = name

from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(UnicornException)
async def request_object(request : Request,exc : UnicornException):
    return JSONResponse(status_code=410, content={"message" : f"Oops! {exc.name} did something."})

@app.get("/unicorn/{name}")
async def read_unicorn(name : str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name" : name}

# for a user readable friendy format:

from fastapi.responses import PlainTextResponse
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)

from starlette.exceptions import HTTPException

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code= exc.status_code)

@app.get("/validation_items/{item_id}")
async def read_validation_items(item_id : int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="No, this is wrong")
    return {"item_id" : item_id}
