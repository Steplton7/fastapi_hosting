import shutil
from typing import List
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

from schemas import UploadVideo, GetVideo, User, Message

video_router = APIRouter()


@video_router.post("/")
async def root(title: str= File(...), description: str = File(...), file: UploadFile = File(...)):
    info = UploadVideo(title=title, description=description)
    with open(f'{file.filename}', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"file_name": file.filename, "info": info}

@video_router.post("/img", status_code=201)
async def upload_image(files: List[UploadFile] = File(...)):
    for img in files:
        with open(f'{img.filename}', "wb") as buffer:
            shutil.copyfileobj(img.file, buffer)

    return {"file_name": "Good"}



@video_router.post("/info")
async def info_set(info: UploadVideo):
    return info


@video_router.get("/video", response_model=GetVideo,responses={404: {"model": Message}})
async def get_video():
    user = User(**{'id':1, 'name': 'Steplton'})
    video = {'title': 'Test', 'description': 'Description'}
    info = GetVideo(user=user, video=video)
    return JSONResponse(status_code=200, content=info.dict())