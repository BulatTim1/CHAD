from pydantic import BaseModel
from pony.orm import PrimaryKey, Required, Set, Optional

from src.models import db

# test_json = {
#     "id": 485498234,
#     "first_name": "Булат",
#     "username": "BulatTim",
#     "photo_url": "https://t.me/i/userpic/320/unKzZW_RKjaEedTEwiOuGMeEe3OmS30ciYxrBzPz7MI.jpg",
#     "auth_date": 1699270274,
#     "hash": "d80819f49422783911b29b13da1e9c231ca04216ba093878148e1e40621a2e3b"
# }

class UserView(BaseModel):
    id: int
    first_name: str
    username: str
    photo_url: str
    auth_date: int


class User(db.Entity):
    id = PrimaryKey(int, size=64)
    first_name = Required(str)
    username = Required(str)
    photo_url = Required(str)
    auth_date = Required(int, size=64)
    channels = Set("Channel")

    def toModel(self):
        return UserView(id=self.id, first_name=self.first_name, auth_date=self.auth_date, username=self.username, photo_url=self.photo_url)
