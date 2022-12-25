from pyrogram import filters
from Midukki.midukki import Midukki_RoboT
from Midukki.modules.auto_filters import auto_filters, send_for_index
from Midukki.modules.manual_filters import manual_filters
from Midukki.functions.settings import get_settings
from Midukki.database import db


@Midukki_RoboT.on_message(filters.group & filters.text & filters.incoming)
async def give_filter(client, message):

    k = await manual_filters(client, message)
    if k == False:
        settings = await get_settings(message.chat.id)
        if settings["autofilter"]:
            await auto_filters(client, message)

@Midukki_RoboT.on_message((filters.forwarded | (filters.regex("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")) & filters.text ) & filters.private & filters.incoming)
async def start_for_index(client, message):
    await send_for_index(client, message)
