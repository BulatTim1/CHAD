from pydantic import BaseModel
from typing import List
from pony.orm import PrimaryKey, Required, Set

from src.models import db, User

# "update_id": 245186480,
# "my_chat_member": {
#     "chat": {
#         "id": -1002103221787,
#         "title": "Test",
#         "type": "channel"
#     },
#     "from": {
#         "id": 485498234,
#         "is_bot": false,
#         "first_name": "Булат",
#         "username": "BulatTim",
#         "language_code": "ru",
#         "is_premium": true
#     },
#     "date": 1699210748,
#     "old_chat_member": {
#         "user": {
#             "id": 6667072025,
#             "is_bot": true,
#             "first_name": "CHAD",
#             "username": "chad_panel_bot"
#         },
#         "status": "kicked",
#         "until_date": 0
#     },
#     "new_chat_member": {
#         "user": {
#             "id": 6667072025,
#             "is_bot": true,
#             "first_name": "CHAD",
#             "username": "chad_panel_bot"
#         },
#         "status": "administrator",
#         "can_be_edited": false,
#         "can_manage_chat": true,
#         "can_change_info": false,
#         "can_post_messages": true,
#         "can_edit_messages": true,
#         "can_delete_messages": false,
#         "can_invite_users": false,
#         "can_restrict_members": true,
#         "can_promote_members": false,
#         "can_manage_video_chats": false,
#         "can_post_stories": false,
#         "can_edit_stories": false,
#         "can_delete_stories": false,
#         "is_anonymous": false,
#         "can_manage_voice_chats": false
#     }
# }

class ChannelView(BaseModel):
    id: int
    title: str
    joined: bool
    # users: List[User] = []

class Channel(db.Entity):
    id = PrimaryKey(int, size=64)
    title = Required(str)
    joined = Required(bool)
    users = Set("User")
    posts = Set("Post")

    def toModel(self):
        return ChannelView(id=self.id, title=self.title, joined=self.joined)

