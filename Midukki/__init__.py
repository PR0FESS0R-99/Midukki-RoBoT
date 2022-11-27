from aiohttp import web
from os import environ
from re import compile
from time import time
from .scripts import START_TXT, FILE_CAPTION_TXT, SPELLCHECK_TXT, IMDB_TEMPLATE_TXT, WELCOME_TXT

routes = web.RouteTableDef()
find = compile(r'^.\d+$')

def who_is_creator(id1, id2):
  # print(pass)
  text = (
   f"\nBot Created By {id2.first_name}" + "\n"
   f"\nBot Deployed By {id1.first_name}"
  )
  return text
    
class Accounts(object):
    API_ID = int(environ.get("API_ID", 0))
    API_HASH = environ.get("API_HASH")
    BOT_TOKEN = environ.get("BOT_TOKEN")
    BOT_PLUGINS = environ.get("BOT_PLUGINS", "Midukki")
    BOT_SESSIONS = environ.get("BOT_SESSION", "Midukki-RoboT")

class Bots(object):
    BOT_ID = int(environ.get("BOT_ID", Accounts.BOT_TOKEN.split(":")[0]))
    BOT_NAME = environ.get("BOT_NAME", None)
    BOT_MENTION = environ.get("BOT_MENTION", None)
    BOT_USERNAME = environ.get("BOT_USERNAME", None)
    #bot up time
    BOT_START_TIME = time()

class Customize(object):
    FILE_CAPTION = environ.get("FILE_CAPTION", FILE_CAPTION_TXT)
    SPELLCHECK_CAPTION = environ.get("SPELLCHECK_CAPTION", SPELLCHECK_TXT)
    IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", IMDB_TEMPLATE_TXT)
    WELCOME_CAPTION = environ.get("WELCOME_CAPTION", WELCOME_TXT)
    AUTO_DEL_TIME = int(environ.get("AUTO_DEL_TIME", "900"))

class Configs(object):
    # admins id
    ADMINS_ID = [int(admin) if find.search(admin) else admin for admin in environ.get('ADMINS_ID', '5601313788').split()]

    # bot information   
    COMMAND_PREFIXES = environ.get("COMMAND_PREFIXES", "/")
    if environ.get("BOT_PICS"):
        START_PICS = (environ.get("BOT_PICS", "https://telegra.ph/file/5ad2c57ae74bafb6efec1.jpg")).split()
    START_MESSAGE = environ.get("START_MESSAGE", START_TXT)

    # MongoDB information
    DATABASE_NAME = environ.get("DATABASE_NAME", "Muhammed")
    DATABASE_URL = environ.get("DATABASE_URL", None)
    COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

    # Groups & Channels
    LOG_CHANNEL = int(environ.get('LOG_CHANNEL', 0))
    SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'https://t.me/Mo_Tech_YT')
    CHANNELS = [int(ch) if find.search(ch) else ch for ch in environ.get('CHANNELS', '0').split()]
    AUTH_CHANNEL = int(environ.get('FORCE_SUB', 1))

    # Media Caption
    USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', False))
    CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", Customize.FILE_CAPTION)

    # Filters Control
    FILTER_RESULTS = int(environ.get("FILTER_RESULTS", "10"))
    FILTER_BUTTONS = {}

    # Ads Controls
    WEB_URL = environ.get("ADS_WEB_URL")
    WEB_API = environ.get("ADS_WEB_API")

    # other
    DONATE_LINKS = environ.get("DONATE_LINK", "https://p.paytm.me/xCTH/7yzmtgie")
    LOADING_SYMBOL = environ.get("LOADING_MODE", "ON")
    LOADING_A = environ.get("LOADING_SYMBOL_A", "⚪️")
    LOADING_B = environ.get("LOADING_SYMBOL_B", "⚫️")
    STOP_BOT = bool(environ.get("DEFAULT", False))
    PORT_CODE = environ.get("PORT", "8080")

class Index(object):
    CURRENT = int(environ.get("SKIP", 2))
    CANCEL = False

# bot management 
async def bot_run():
    _app = web.Application(client_max_size=30000000)
    _app.add_routes(routes)
    return _app

# class Settings(object):
#     IMDB_POSTER = False / "off"
#     WELCOME = True / "on"
#     BUTTON_SIZE = False / "off"
#     SPELLCHECK = True / "off"
#     FILE_MODE = False / "callback"
