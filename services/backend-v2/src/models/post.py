import time
from typing import List, Optional, Union
from pydantic import BaseModel, Field
from pony.orm import PrimaryKey, Required

from src.models import db

# test_json = {
#     "id": 485498234,
#     "first_name": "Булат",
#     "username": "BulatTim",
#     "photo_url": "https://t.me/i/userpic/320/unKzZW_RKjaEedTEwiOuGMeEe3OmS30ciYxrBzPz7MI.jpg",
#     "auth_date": 1699270274,
#     "hash": "d80819f49422783911b29b13da1e9c231ca04216ba093878148e1e40621a2e3b"
# }

class PostView(BaseModel):
    id: Union[int, None] = None
    text: str
    send_time: int = int(time.time()) + 30
    # media: List[bytes]


class Post(db.Entity):
    id = PrimaryKey(int, size=64, auto=True)
    text = Required(str)
    send_time = Required(int, size=64)
    channel = Required("Channel")
    
    def toModel(self):
        return PostView(id=self.id, text=self.text, send_time=self.send_time)
