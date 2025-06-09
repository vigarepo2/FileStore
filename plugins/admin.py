from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import OWNER_ID
from helper_func import admin
from database.database import db

@Bot.on_message(filters.command('users') & filters.private & admin)
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text="Getting users...")
    users = await db.full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.command('add_admin') & filters.private & filters.user(OWNER_ID))
async def add_admins(client: Client, message: Message):
    pro = await message.reply("Please wait...", quote=True)
    admins = message.text.split()[1:]
    
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]])
    
    if not admins:
        return await pro.edit(
            "You need to provide user ID(s) to add as admin.\n\n"
            "Usage: /add_admin [user_id]\n\n"
            "Example: /add_admin 1234567890",
            reply_markup=reply_markup
        )
    
    admin_list = ""
    for admin_id in admins:
        try:
            admin_id = int(admin_id)
            await db.add_admin(admin_id)
            admin_list += f"✅ Added: {admin_id}\n"
        except:
            admin_list += f"❌ Invalid ID: {admin_id}\n"
    
    await pro.edit(f"Admin addition result:\n\n{admin_list}", reply_markup=reply_markup)

@Bot.on_message(filters.command('del_admin') & filters.private & filters.user(OWNER_ID))
async def delete_admins(client: Client, message: Message):
    pro = await message.reply("Please wait...", quote=True)
    admins = message.text.split()[1:]
    
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]])
    
    if not admins:
        return await pro.edit(
            "Please provide admin ID(s) to remove.\n\n"
            "Usage: /del_admin [user_id]\n"
            "Usage: /del_admin all",
            reply_markup=reply_markup
        )
    
    if len(admins) == 1 and admins[0].lower() == "all":
        admin_ids = await db.get_all_admins()
        if admin_ids:
            for admin_id in admin_ids:
                await db.del_admin(admin_id)
            return await pro.edit("All admin IDs have been removed.", reply_markup=reply_markup)
        else:
            return await pro.edit("No admin IDs to remove.", reply_markup=reply_markup)
    
    admin_list = ""
    for admin_id in admins:
        try:
            admin_id = int(admin_id)
            await db.del_admin(admin_id)
            admin_list += f"✅ Removed: {admin_id}\n"
        except:
            admin_list += f"❌ Invalid ID: {admin_id}\n"
    
    await pro.edit(f"Admin removal result:\n\n{admin_list}", reply_markup=reply_markup)

@Bot.on_message(filters.command('admins') & filters.private & admin)
async def get_admins(client: Client, message: Message):
    pro = await message.reply("Please wait...", quote=True)
    admin_ids = await db.get_all_admins()
    
    if not admin_ids:
        admin_list = "❌ No admins found."
    else:
        admin_list = "\n".join(f"ID: {admin_id}" for admin_id in admin_ids)
    
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]])
    await pro.edit(f"Current Admin List:\n\n{admin_list}", reply_markup=reply_markup)

@Bot.on_callback_query(filters.regex("close"))
async def close_callback(client: Client, callback_query):
    await callback_query.message.delete()
