# import time, requests
import logging

import telegram as tg
from src.config import *
from src.models import *
from typing import Optional, Tuple

from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    ChatMemberHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Enable logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def addChannel(chat: tg.Chat, cause_user: tg.User):
    admins = [cause_user]
    try:
        admins = await chat.get_administrators()
    except:
        pass
    with db_session:
        if select(c for c in Channel if c.id == chat.id).count() == 0:
            channel = Channel(id=chat.id, title=chat.title, joined=True)
        else:
            channel = Channel[chat.id]
            channel.joined = True
        for member in admins:
            tguser = member.user
            if tguser.is_bot:
                continue
            if select(u for u in User if u.id == tguser.id).count() == 0:
                user = User(id=tguser.id, first_name=tguser.first_name, auth_date=-1)
                channel.users.add(user)
            else:
                user = User[tguser.id]
                channel.users.add(user)
        commit()

async def unjoinChannel(chat: tg.Chat):
    with db_session:
        Channel[chat.id].joined = False
        commit()

async def addAdmin(chat: tg.Chat, user: tg.User):
    with db_session:
        if select(u for u in User if u.id == user.id).count() == 0:
            User(id=user.id, first_name=user.first_name, auth_date=-1)
        if select(c for c in Channel if c.id == chat.id).count() == 0:
            return
        channel = Channel[chat.id]
        channel.users.add(User[user.id])
        commit()

async def delAdmin(chat: tg.Chat, user: tg.User):
    with db_session:
        if select(u for u in User if u.id == user.id).count() == 0:
            return
        if select(c for c in Channel if c.id == chat.id).count() == 0:
            return
        channel = Channel[chat.id]
        channel.users.remove(User[user.id])
        commit()

def extract_status_change(chat_member_update: tg.ChatMemberUpdated) -> Optional[Tuple[bool, bool]]:
    """Takes a tg.ChatMemberUpdated instance and extracts whether the 'old_chat_member' was a member
    of the chat and whether the 'new_chat_member' is a member of the chat. Returns None, if
    the status didn't change.
    """
    status_change = chat_member_update.difference().get("status")
    old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))

    if status_change is None:
        return None

    old_status, new_status = status_change
    was_member = old_status in [
        tg.ChatMember.MEMBER,
        tg.ChatMember.OWNER,
        tg.ChatMember.ADMINISTRATOR,
    ] or (old_status == tg.ChatMember.RESTRICTED and old_is_member is True)
    is_member = new_status in [
        tg.ChatMember.MEMBER,
        tg.ChatMember.OWNER,
        tg.ChatMember.ADMINISTRATOR,
    ] or (new_status == tg.ChatMember.RESTRICTED and new_is_member is True)

    return was_member, is_member

async def track_chats(update: tg.Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Tracks the chats the bot is in."""
    result = extract_status_change(update.my_chat_member)
    if result is None:
        return
    was_member, is_member = result

    # Let's check who is responsible for the change
    cause_name = update.effective_user.full_name
    cause_chat = update.effective_user

    # Handle chat types differently:
    chat = update.effective_chat
    if chat.type == tg.Chat.PRIVATE:
        if not was_member and is_member:
            # This may not be really needed in practice because most clients will automatically
            # send a /start command after the user unblocks the bot, and start_private_chat()
            # will add the user to "user_ids".
            # We're including this here for the sake of the example.
            logger.info("%s разблокировал бота", cause_name)
            context.bot_data.setdefault("user_ids", set()).add(chat.id)
            await cause_chat.send_message(
                f"Привет! Если ты хочешь добавить меня в канал, то вот ссылки:\n\nКанал: tg://resolve?domain=chad_panel_bot&startchannel&admin=post_messages+edit_messages", #\nГруппа: tg://resolve?domain=chad_panel_bot&startgroup&admin=post_messages+edit_messages",
                parse_mode=ParseMode.HTML,
            )
        elif was_member and not is_member:
            logger.info("%s заблокировал бота", cause_name)
            context.bot_data.setdefault("user_ids", set()).discard(chat.id)
    # elif chat.type in [tg.Chat.GROUP, tg.Chat.SUPERGROUP]:
    #     if not was_member and is_member:
    #         logger.info("%s добавил бота в группу %s", cause_name, chat.title)
    #         context.bot_data.setdefault("group_ids", set()).add(chat.id)
    #         await update.effective_chat.send_message(
    #             f"тест",
    #             parse_mode=ParseMode.HTML,
    #         )
    #     elif was_member and not is_member:
    #         logger.info("%s удалил бота из группы %s", cause_name, chat.title)
    #         context.bot_data.setdefault("group_ids", set()).discard(chat.id)
    elif not was_member and is_member:
        logger.info("%s добавил бота в канал %s", cause_name, chat.title)
        # context.bot_data.setdefault("channel_ids", set()).add(chat.id)
        await addChannel(chat, cause_chat)
        await cause_chat.send_message(
            f"Вы добавили меня в {chat.title}",
            parse_mode=ParseMode.HTML,
        )
    elif was_member and not is_member:
        logger.info("%s удалил бота из канала %s", cause_name, chat.title)
        # context.bot_data.setdefault("channel_ids", set()).discard(chat.id)
        await unjoinChannel(chat)


# async def show_chats(update: tg.Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Shows which chats the bot is in"""
#     # user_ids = ", ".join(str(uid) for uid in context.bot_data.setdefault("user_ids", set()))
#     # group_ids = ", ".join(str(gid) for gid in context.bot_data.setdefault("group_ids", set()))
#     # channel_ids = ", ".join(str(cid) for cid in context.bot_data.setdefault("channel_ids", set()))
#     # text = (
#     #     f"@{context.bot.username} is currently in a conversation with the user IDs {user_ids}."
#     #     f" Moreover it is a member of the groups with IDs {group_ids} "
#     #     f"and administrator in the channels with IDs {channel_ids}."
#     # )
#     text = (
#         f"Хей, я работаю, не мешай..."
#     )
#     await update.effective_message.reply_text(text)


async def greet_chat_members(update: tg.Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Greets new users in chats and announces when someone leaves"""
    result = extract_status_change(update.chat_member)
    if result is None:
        return

    was_member, is_member = result
    cause_name = update.chat_member.from_user.mention_html()
    member_name = update.chat_member.new_chat_member.user.mention_html()

    if not update.chat_member.new_chat_member.user.is_bot and update.chat_member.new_chat_member.status == tg.ChatMember.ADMINISTRATOR:
        await addAdmin(update.effective_chat, update.chat_member.new_chat_member.user)
    elif not update.chat_member.new_chat_member.user.is_bot and update.chat_member.old_chat_member.status == tg.ChatMember.ADMINISTRATOR and update.chat_member.new_chat_member.status != tg.ChatMember.ADMINISTRATOR:
        await delAdmin(update.effective_chat, update.chat_member.new_chat_member.user)

    if not was_member and is_member and update.effective_chat.type == tg.Chat.GROUP:
        await update.effective_chat.send_message(
            f"{member_name} добавлен {cause_name}. Добро пожаловать!",
            parse_mode=ParseMode.HTML,
        )
    elif was_member and not is_member and update.effective_chat.type == tg.Chat.GROUP:
        # await update.effective_chat.send_message(
        #     f"{member_name} больше не с нами. Молодец, {cause_name}...",
        #     parse_mode=ParseMode.HTML,
        # )
        pass


async def start_private_chat(update: tg.Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Greets the user and records that they started a chat with the bot if it's a private chat.
    Since no `my_chat_member` update is issued when a user starts a private chat with the bot
    for the first time, we have to track it explicitly here.
    """
    user_name = update.effective_user.full_name
    chat = update.effective_chat
    if chat.type != tg.Chat.PRIVATE or chat.id in context.bot_data.get("user_ids", set()):
        return

    logger.info("%s started a private chat with the bot", user_name)
    context.bot_data.setdefault("user_ids", set()).add(chat.id)
    await update.effective_message.reply_text(
        f"Привет {user_name}. Если ты хочешь добавить меня в  канал, то вот ссылки.\n\nДля канала: <a href=\"tg://resolve?domain=chad_panel_bot&startchannel&admin=post_messages+edit_messages\">ссылка</a>", #\nДля группы: <a href=\"tg://resolve?domain=chad_panel_bot&startgroup&admin=post_messages+edit_messages\">ссылка</a>",
            parse_mode=ParseMode.HTML
    )


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Keep track of which chats the bot is in
    application.add_handler(ChatMemberHandler(track_chats, ChatMemberHandler.MY_CHAT_MEMBER))
    # application.add_handler(CommandHandler("show_chats", show_chats))

    # Handle members joining/leaving chats.
    application.add_handler(ChatMemberHandler(greet_chat_members, ChatMemberHandler.CHAT_MEMBER))

    # Interpret any other command or text message as a start of a private chat.
    # This will record the user as being in a private chat with bot.
    application.add_handler(MessageHandler(filters.ALL, start_private_chat))

    # Run the bot until the user presses Ctrl-C
    # We pass 'allowed_updates' handle *all* updates including `chat_member` updates
    # To reset this, simply pass `allowed_updates=[]`
    application.run_polling(allowed_updates=tg.Update.ALL_TYPES)


if __name__ == "__main__":
    main()