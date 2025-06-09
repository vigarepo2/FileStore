import asyncio
import pyromod.listen
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait
from bot import Bot
from config import *
from helper_func import *
from database.database import *

@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id

    # Add user if not already present
    if not await db.present_user(user_id):
        try:
            await db.add_user(user_id)
        except:
            pass

    # Handle file links
    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except IndexError:
            return

        string = await decode(base64_string)
        argument = string.split("-")

        ids = []
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
                ids = range(start, end + 1) if start <= end else list(range(start, end - 1, -1))
            except:
                return
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return

        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Something went wrong!")
            return
        finally:
            await temp_msg.delete()

        for msg in messages:
            try:
                await msg.copy(
                    chat_id=message.from_user.id,
                    protect_content=PROTECT_CONTENT
                )
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(
                    chat_id=message.from_user.id,
                    protect_content=PROTECT_CONTENT
                )
            except:
                pass
    else:
        # Start message with updates channel button
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(UPDATES_CHANNEL_NAME, url=UPDATES_CHANNEL)],
            [InlineKeyboardButton("Help", callback_data="help")]
        ])
        
        await message.reply_text(
            START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup
        )

@Bot.on_callback_query()
async def cb_handler(client: Bot, query):
    data = query.data
    
    if data == "help":
        await query.message.edit_text(
            text=HELP_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Back", callback_data="start")]
            ])
        )
    elif data == "start":
        await query.message.edit_text(
            text=START_MSG.format(
                first=query.from_user.first_name,
                last=query.from_user.last_name,
                username=None if not query.from_user.username else '@' + query.from_user.username,
                mention=query.from_user.mention,
                id=query.from_user.id
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(UPDATES_CHANNEL_NAME, url=UPDATES_CHANNEL)],
                [InlineKeyboardButton("Help", callback_data="help")]
            ])
        )
