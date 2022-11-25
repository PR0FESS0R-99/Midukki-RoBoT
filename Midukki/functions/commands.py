from Midukki import Configs
from pyrogram import filters
from typing import List, Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

def command(commands: Union[str, List[str]]):
    return filters.command(commands, Configs.COMMAND_PREFIXES)

def message():
    return Message

def markup():
    return InlineKeyboardMarkup

def button():
    return InlineKeyboardButton

