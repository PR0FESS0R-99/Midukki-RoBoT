from pyrogram import filters
from .commands import command
from Midukki.database import db

SETTINGS = {}

async def get_settings(group_id):
    settings = SETTINGS.get(group_id)
    if not settings:
        settings = await db.get_settings(group_id)
        SETTINGS[group_id] = settings
    return settings
    
async def save_group_settings(group_id, key, value):
    current = await get_settings(group_id)
    current[key] = value
    SETTINGS[group_id] = current
    await db.update_settings(group_id, current)
    
setting_command = command(["settings"]) & (filters.private | filters.group)
reload_command = command(["clearchatdb"]) & (filters.private | filters.group)
