from os import cpu_count
from aiohttp import web as stop_bot
from logging import getLogger, ERROR
from pyrogram.raw.all import layer
from pyrogram import Client, __version__, types, enums
from pyrogram.errors import UserNotParticipant
from Midukki import Accounts, Bots, who_is_creator, Configs, bot_run
from typing import Union, Optional, AsyncGenerator

logger = getLogger(__name__)
logger.setLevel(ERROR)

class Midukki_RoboT(Client):

    def __init__(self):
        super().__init__(
            name=Accounts.BOT_SESSIONS,
            api_id=Accounts.API_ID,
            api_hash=Accounts.API_HASH,
            bot_token=Accounts.BOT_TOKEN,
            plugins={"root": Accounts.BOT_PLUGINS},
            workers=min(32, cpu_count() + 4),
            sleep_threshold=5,
        )

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
      #  id1 = await self.get_users(Configs.ADMINS_ID[0])
      #  id2 = await self.get_users(int(5601313788))

        Bots.BOT_ID = usr_bot_me.id
        Bots.BOT_NAME = usr_bot_me.first_name
        Bots.BOT_MENTION = usr_bot_me.mention
        Bots.BOT_USERNAME = usr_bot_me.username
        print(
         f"@Midukki_RoboT based on Pyrogram v{__version__} "
         f"(Layer {layer}) started on @{usr_bot_me.username}. "
        )
        print("This BoT Created By @Mo_Tech_YT")        
        if Configs.LOG_CHANNEL:
            await self.send_logs(int(Configs.LOG_CHANNEL))

        if Configs.STOP_BOT == True:
            client = stop_bot.AppRunner(await bot_run())
            await client.setup()
            bind_address = "0.0.0.0"
            await stop_bot.TCPSite(client, bind_address, Configs.PORT_CODE).start()

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped. Bye.")

    async def iter_messages(self, chat_id: Union[int, str], limit: int, offset: int = 0) -> Optional[AsyncGenerator["types.Message", None]]:
        current = offset
        while True:
            new_diff = min(200, limit - current)
            if new_diff <= 0:
                return
            messages = await self.get_messages(chat_id, list(range(current, current+new_diff+1)))
            for message in messages:
                yield message
                current += 1

    async def is_subscribed(self, midukki, bot):
        try:
            user = await midukki.get_chat_member(Configs.AUTH_CHANNEL, bot.from_user.id)
        except UserNotParticipant:
            pass
        except Exception as e:
            logger.exception(e)
        else:
            if user.status != enums.ChatMemberStatus.BANNED:
                return True

        return False

    async def send_logs(self, chat_id):
        await self.send_message(chat_id=chat_id, text="#BoT_Started")
