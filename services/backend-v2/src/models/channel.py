from pydantic import BaseModel
from typing import List
from pony.orm import PrimaryKey, Required, Set, Optional

from src.models import db

class ChannelView(BaseModel):
    id: int
    title: str
    joined: bool = True
    # users: List[User] = []

class Channel(db.Entity):
    id = PrimaryKey(int, size=64)
    title = Required(str)
    joined = Optional(bool)
    users = Set("User")
    posts = Set("Post")
    offers = Set("Offer")

    def toModel(self):
        return ChannelView(id=self.id, title=self.title, joined=self.joined)

