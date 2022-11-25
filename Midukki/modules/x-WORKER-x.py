from pyrogram import filters
from Midukki.midukki import Midukki_RoboT
from Midukki.modules.auto_filters import auto_filters, send_for_index
from Midukki.modules.manual_filters import manual_filters
from Midukki.functions.settings import get_settings
from Midukki.database import db
from Midukki import Configs

@Midukki_RoboT.on_message(filters.group & filters.text & filters.incoming)
async def give_filter(client, message):

    if not await db.get_chat(message.chat.id):
        if Configs.LOG_CHANNEL != 0:
            total=await client.get_chat_members_count(message.chat.id)
            mrk = message.from_user.mention if message.from_user else "Anonymous" 
            await client.send_message(Configs.LOG_CHANNEL, text="""name : {}\nid : `{}`\ntotal users : {}\nuser : `{}`""".format(message.chat.title, message.chat.id, total, mrk))      
        await db.add_chat(message.chat.id, message.chat.title)

    k = await manual_filters(client, message)
    if k == False:
        settings = await get_settings(message.chat.id)
        if settings["autofilter"]:
            await auto_filters(client, message)

@Midukki_RoboT.on_message((filters.forwarded | (filters.regex("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")) & filters.text ) & filters.private & filters.incoming)
async def start_for_index(client, message):
    await send_for_index(client, message)
