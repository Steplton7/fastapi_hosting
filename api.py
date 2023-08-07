import shutil
from typing import List
from fastapi import APIRouter, UploadFile, File, Form,HTTPException, BackgroundTasks
from starlette.responses import StreamingResponse
from starlette.templating import Jinja2Templates

from schemas import UploadVideo, GetVideo, Message
from models import Video, User
from services import write_video

video_router = APIRouter()


@video_router.post("/")
async def create_video(
    background_tasks: BackgroundTasks,
    title: str= Form(...), 
    description: str = Form(...),
    file: UploadFile = File(...)
    ):
    file_name = f'media/{file.filename}'
    if file.content_type == 'video/mp4':
        background_tasks.add_task(write_video, file_name, file)
    else:
        raise HTTPException(status_code=418, detail="It isn't mp4")
    
    info = UploadVideo(title=title, description=description)
    with open(f'{file.filename}', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    user = await User.objects.first()
    return await Video.objects.create(file=file_name, user=user,**info.dict())



@video_router.post("/img", status_code=201)
async def upload_image(files: List[UploadFile] = File(...)):
    for img in files:
        with open(f'{img.filename}', "wb") as buffer:
            shutil.copyfileobj(img.file, buffer)

    return {"file_name": "Good"}



@video_router.get("/video/{video_pk}", response_model = GetVideo, responses={404: {"model": Message}})
async def get_video(video_pk: int):
    return await Video.objects.select_related('user').get(pk=video_pk)