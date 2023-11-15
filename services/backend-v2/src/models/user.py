from pydantic import BaseModel
from pony.orm import PrimaryKey, Required, Set, Optional

from src.models import db

class UserView(BaseModel):
    id: int
    first_name: str
    last_name: str = ""
    username: str = ""
    photo_url: str = ""
    auth_date: int = 0


class User(db.Entity):
    id = PrimaryKey(int, size=64)
    first_name = Required(str)
    last_name = Optional(str)
    username = Optional(str)
    photo_url = Optional(str)
    auth_date = Optional(int, size=64)
    channels = Set("Channel")

    def toModel(self):
        model = UserView(id=self.id, first_name=self.first_name)
        if (self.username != ""):
            model.username = self.username
        if (self.last_name != ""):
            model.last_name = self.last_name
        if (self.photo_url != ""):
            model.photo_url = self.photo_url
        if (self.auth_date != 0):
            model.auth_date = self.auth_date
        return model
