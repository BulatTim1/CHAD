from enum import Enum
import time
from pydantic import BaseModel
from pony.orm import PrimaryKey, Required, Set
from src.models import db

class MediaTypes(str, Enum):
    photo = "photo"
    video = "video"

class MediaView(BaseModel):
    id: int|None = None
    file: str
    type: MediaTypes

class Media(db.Entity):
    id = PrimaryKey(int, size=64, auto=True)
    file = Required(bytes)
    type = Required(MediaTypes)
    post = Required("Post")

    def toModel(self):
        model = MediaView(id=self.id, file=self.file.decode(), type=self.type)
        return model

class PostView(BaseModel):
    id: int|None = None
    text: str
    send_time: int = int(time.time()) + 30
    media: list[MediaView]|None = None
    channel: int|None = None


class Post(db.Entity):
    id = PrimaryKey(int, size=64, auto=True)
    text = Required(str)
    send_time = Required(int, size=64)
    channel = Required("Channel")
    media = Set("Media")
    
    def toModel(self):
        model = PostView(id=self.id, text=self.text, send_time=self.send_time, channel=self.channel.id, media=[])
        if len(self.media) > 0:
            model.media = [i.toModel() for i in self.media]
        return model
