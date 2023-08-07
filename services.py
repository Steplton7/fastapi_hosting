import aiofiles
import shutil
from fastapi import UploadFile


class Video:
    pass

def write_video(file_name: str, file: UploadFile):
    with open(file_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

async def write_picture(file_name: str, file: UploadFile):
    """асинхронная функция (для изображений)"""
    async with aiofiles.open(file_name, "wb") as buffer:
        data = await file.read()
        await buffer.write(data)