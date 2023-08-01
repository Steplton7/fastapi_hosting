from typing import List
from pydantic import BaseModel


class UploadVideo(BaseModel):
    title: str
    description: str


class User(BaseModel):
    id: int
    name: str


class GetVideo(BaseModel):
    user: User
    video: UploadVideo


class Message(BaseModel):
    message: str