from typing import Annotated
from fastapi import Body, FastAPI, File, Form, HTTPException, Security
from pony.orm import db_session, commit, select
from src.models import *
# from src.telegram.bot import getNewChannels

from hashlib import sha256
import hmac
import json
from base64 import b64decode, urlsafe_b64decode
import time
from fastapi.security import APIKeyHeader
from src.config import TELEGRAM_HASH, AUTH_EXPIRES_IN, ADMINS


async def addUserDB(user: UserView):
    with db_session:
        if select(count(u) for u in User if u.id == user.id)[:][0] == 0:
            User(id=user.id, first_name=user.first_name, username=user.username, photo_url=user.photo_url, auth_date=user.auth_date)
            commit()

async def checkUserChannelPermissionDB(user_id, channel_id):
    with db_session:
        return user_id in ADMINS or select(count(ch) for ch in Channel if User[user_id] in ch.users and ch.id == channel_id)[:][0] == 1

async def addNewChannelDB(user_id, channel_id, title):
    with db_session:
        if select(count(ch) for ch in Channel if ch.id == channel_id)[:][0] == 0:
            Channel(id=channel_id, title=title, joined=True, users=[User[user_id]], posts=[])
            commit()

# async def testDbFunc():
#     with db_session:
#         print(select(count(ch) for ch in Channel if ch.id == 13213123)[:][0])

async def addNewPostDB(user_id, channel_id, post: PostView):
    with db_session:
        if await checkUserChannelPermissionDB(user_id, channel_id):
            dbpost = Post(text=post.text, send_time=post.send_time, channel=Channel[channel_id])
            if post.media and len(post.media) > 0:
                for m in post.media:
                    Media(file=m.file.encode(), type=m.type, post=dbpost)
            commit()
            return True
        else:
            return False


async def updatePostDB(user_id, channel_id, post_id, post: PostView):
    with db_session:
        if await checkUserChannelPermissionDB(user_id, channel_id):
            old_post = select(p for p in Post if p.channel.id == channel_id and p.id == post_id)[:]
            if len(old_post) > 0:
                old_post = old_post[0]
                old_post.text=post.text
                old_post.send_time=post.send_time
                if post.media and len(post.media) > 0:
                    for m in old_post.media:
                        m.delete()
                    for m in post.media:
                        Media(file=m.file.encode(), type=m.type, post=old_post)
                commit()
                return True
            return False
        else:
            return False

async def getChannelPostsDB(user_id: int, channel_id: int):
    with db_session:
        if await checkUserChannelPermissionDB(user_id, channel_id):
            return [i.toModel() for i in select(p for p in Post if p.channel.id == channel_id)]
        return None

async def getPostDB(user_id: int, channel_id: int, post_id: int):
    with db_session:
        if await checkUserChannelPermissionDB(user_id, channel_id):
            post = select(p for p in Post if p.channel.id == channel_id and p.id == post_id)[:]
            if len(post) > 0:
                return post[0].toModel()
            return None
        return None

async def deletePostDB(user_id: int, channel_id: int, post_id: int):
    with db_session:
        if await checkUserChannelPermissionDB(user_id, channel_id):
            post = select(p for p in Post if p.channel.id == channel_id and p.id == post_id)[:]
            if len(post) > 0:
                post[0].delete()
                commit()
                return True
            return False
        return None

async def getUserChannelsDB(user_id: int):
    with db_session:
        channels = []
        entities = select(ch for ch in Channel if ch.joined and User[user_id] in ch.users)[:]
        for entity in entities:
            channels.append(entity.toModel())
        return channels

async def getAllChannelsDB():
    with db_session:
        return [ch.toModel() for ch in Channel.select()]
    
async def getAllUsersDB():
    with db_session:
        return [u.toModel() for u in User.select()]
    
async def getAllPostsDB():
    with db_session:
        return [p.toModel() for p in Post.select()]



app = FastAPI()
api_key_header = APIKeyHeader(name="telegram-token", auto_error=True)



async def decodeToken(token: str = Security(api_key_header)):
    # print(token)
    data = {}
    try:
        data = json.loads(urlsafe_b64decode(token.encode()).decode())
    except Exception as e:
        raise HTTPException(status_code=401, detail={"error": "can't decode token"})
    # print("decoded")
    try:
        auth_hash = data.pop('hash')
    except Exception as e:
        raise HTTPException(status_code=401, detail={"error": "token not valid"})
    msg = ""
    for k in sorted(data.keys()):
        msg += f"{k}={data[k]}\n"
    msg = msg[:-1].encode()
    unix_timestamp = int(time.time())
    if auth_hash == hmac.new(TELEGRAM_HASH, msg, sha256 ).hexdigest() and data['auth_date'] + AUTH_EXPIRES_IN >= unix_timestamp:
        user = UserView.model_validate(data)
        await addUserDB(user)
        return user
    else:
        raise HTTPException(status_code=401, detail="token expired")

@app.get('/')
async def hello():
    return {"message": "Hello World!"}

# @app.post("/uploadfiles/")
# async def create_upload_files(
#     files: Annotated[
#         list[UploadFile], File(description="Multiple files as UploadFile")
#     ],
# ):
#     return {"filenames": [file.filename for file in files]}

# channel section
@app.get('/channels')
async def getChannels(current_user: UserView = Security(decodeToken)) -> List[ChannelView]:
    return await getUserChannelsDB(current_user.id)

# @app.get('/channels/add')
# async def addChannel(current_user: UserView = Security(decodeToken)):
#     channels = await getUserChannelsDB(current_user.id)
#     channels_id = [ch.id for ch in channels]
#     new_channel = getNewChannels(current_user.id, channels_id)
#     keys = new_channel.keys()
#     if 'id' in keys and 'title' in keys:
#         await addNewChannelDB(current_user.id, new_channel['id'], new_channel['title'])
#         return {"detail": "Success!"}
#     else:
#         raise HTTPException(status_code=402, detail="No new channel, try again...")


# post section
@app.get('/channels/{channel_id}')
async def getPosts(channel_id: int, current_user: UserView = Security(decodeToken)) -> List[PostView]:
    posts = await getChannelPostsDB(current_user.id, channel_id)
    return posts

@app.post('/channels/{channel_id}')
async def addPosts(channel_id: int, post: PostView, current_user: UserView = Security(decodeToken)) -> bool:
    if post.media and len(post.media) > 0:
        media = []
        for f in post.media:
            if f.file[:f.file.find(';')] in ["data:image/jpeg", "data:image/png"]:
                # f.file = b64decode(f.file[f.file.find(',')+1:].encode())
                f.type = MediaTypes.photo
                media.append(f)
            else:
                pass
        post.media = media
    return await addNewPostDB(current_user.id, channel_id, post)

@app.get('/channels/{channel_id}/{post_id}')
async def getPost(channel_id: int, post_id: int, current_user: UserView = Security(decodeToken)) -> PostView:
    return await getPostDB(current_user.id, channel_id, post_id)

@app.post('/channels/{channel_id}/{post_id}')
async def updatePost(channel_id: int, post_id: int, post: PostView, current_user: UserView = Security(decodeToken)):
    if post.media and len(post.media) > 0:
        media = []
        for f in post.media:
            if f.file[:f.file.find(';')] in ["data:image/jpeg", "data:image/png"]:
                # f.file = b64decode(f.file[f.file.find(',')+1:].encode())
                f.type = MediaTypes.photo
                media.append(f)
            else:
                pass
        post.media = media
    return await updatePostDB(current_user.id, channel_id, post_id, post)

@app.delete('/channels/{channel_id}/{post_id}')
async def deletePost(channel_id: int, post_id: int, current_user: UserView = Security(decodeToken)):
    return await deletePostDB(current_user.id, channel_id, post_id)

# admin section
@app.get('/admin', include_in_schema=False)
async def adminAuth(current_user: UserView = Security(decodeToken)) -> bool:
    return current_user.id in ADMINS

@app.get('/admin/channels', include_in_schema=False)
async def getAllChannels(current_user: UserView = Security(decodeToken)) -> List[ChannelView]:
    if current_user.id in ADMINS:
        return await getAllChannelsDB()

@app.get('/admin/posts', include_in_schema=False)
async def getAllPosts(current_user: UserView = Security(decodeToken)) -> List[PostView]:
    if current_user.id in ADMINS:
        return await getAllPostsDB()

@app.get('/admin/users', include_in_schema=False)
async def getAllUsers(current_user: UserView = Security(decodeToken)) -> List[UserView]:
    if current_user.id in ADMINS:
        return await getAllUsersDB()
