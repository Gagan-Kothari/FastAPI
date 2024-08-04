from fastapi import FastAPI

app = FastAPI()

# Form Fields

from fastapi import Form, Body

# Sent back as form data
@app.post("/login")
async def userlogin(username : str = Form(...), password : str = Form(...)):
    print("password", password)
    return {"username" : username}

# Sent back as json
@app.post("/login_json")
async def user_login(username : str = Body(...), password : str = Body(...)):
    print("password", password)
    return {"username" : username}

# # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Request Files

from fastapi import File

@app.post("/files/")
async def length_file(file : bytes | None = File(None)):
    if not file:
        return {"message" : "No file Uploaded"}
    return {"file" : len(file)}

from fastapi import UploadFile

@app.post("/files/upload")
async def upload_file(file : UploadFile):
    contents = await file.read()
    return {"file" : file.filename}

# Request Forms and Files

@app.post("/files/request")
async def file_request(*, file : bytes = File(...), fileb : UploadFile, Token : str = Form(...)):
    return {
        "file_size" : len(file),
        "token" : Token,
        "fileb_content_type" : fileb.content_type
    }