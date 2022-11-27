from os import environ
from random import choice 
from pyrogram import filters, enums
from pyrogram.errors import UserNotParticipant
from . import Bots, Configs
from .midukki import Midukki_RoboT
from .scripts import START_TXT, HELP_TXT, ABOUT_TXT, STATUS_TXT, DONATE_TXT
from Midukki.modules import vars
from Midukki.functions.user_details import user_mention
from Midukki.functions.handlers import Command
from Midukki.functions.media_details import get_size
from Midukki.functions.commands import button, markup, message
from Midukki.database import get_file_details
from Midukki.functions.settings import get_settings
from Midukki.database import db

@Midukki_RoboT.on_message(Command.a)
async def start_command(client: Midukki_RoboT, message: message()):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        if Configs.LOG_CHANNEL is not None:
           await client.send_message(Configs.LOG_CHANNEL, "Name: {}\nId: `{}`".format(message.from_user.id, message.from_user.mention))

    mention = user_mention(message)
    bot_mention = Bots.BOT_MENTION
    bot_name = Bots.BOT_NAME
    bot_username = Bots.BOT_USERNAME
    user_ids = message.from_user.id if message.from_user else None

    if len(message.command) != 2:
        if environ.get("BOT_PICS"):
            try:
                await message.reply_photo(photo=choice(Configs.START_PICS), caption=Configs.START_MESSAGE.format(bot=bot_mention, mention=mention, name=bot_name, username=bot_username), reply_markup=markup()(vars.start_buttons))         
            except Exception as e:
                await message.reply_photo(photo=choice(Configs.START_PICS), caption=START_TXT.format(bot=bot_mention, mention=mention, name=bot_name, username=bot_username), reply_markup=markup()(vars.start_buttons))         
                await message.reply(e)
        else:
            try:
                await message.reply_text(text=Configs.START_MESSAGE.format(bot=bot_mention, mention=mention, name=bot_name, username=bot_username), reply_markup=markup()(vars.start_buttons))
            except Exception as e:
                await message.reply_text(text=START_TXT.format(bot=bot_mention, mention=mention, name=bot_name, username=bot_username), reply_markup=markup()(vars.start_buttons))
                await message.reply(e)
        return

    if message.text.startswith("/start muhammedrk"):
        if Configs.AUTH_CHANNEL != 1:
            invite_link = await client.create_chat_invite_link(int(Configs.AUTH_CHANNEL))
            try:
                user = await client.get_chat_member(int(Configs.AUTH_CHANNEL), user_ids)
                if user.status == enums.ChatMemberStatus.RESTRICTED:
                    await client.send_message(chat_id=message.from_user.id, text="""𝚂𝙾𝚁𝚁𝚈 𝚂𝙸𝚁, 𝚈𝙾𝚄 𝙰𝚁𝙴 𝙱𝙰𝙽𝙽𝙴𝙳 𝚃𝙾 𝚄𝚂𝙴 𝙼𝙴""", disable_web_page_preview=True)                  
                    return
            except UserNotParticipant:
                mrk, file_id, grp_id = message.text.split("_-_")
                FORCES = ["https://telegra.ph/file/b2acb2586995d0e107760.jpg"]
                invite_link = await client.create_chat_invite_link(int(Configs.AUTH_CHANNEL))
                pr0fess0r_99 = [
                    [
                        button()
                            (
                                "🔰 Join My Channel 🔰",
                                    url=invite_link.invite_link
                            )
                    ]
                ]    
                pr0fess0r_99 = markup()
                (
                    pr0fess0r_99
                )
                await message.reply_photo(photo=choice(FORCES), caption=f"""<i><b>𝙷𝙴𝙻𝙻𝙾 {message.from_user.mention}. \n 𝚈𝙾𝚄 𝙷𝙰𝚅𝙴 <a href="{invite_link.invite_link}"> 𝙽𝙾𝚃 𝚂𝚄𝙱𝚂𝙲𝚁𝙸𝙱𝙴𝙳</a> 𝚃𝙾 <a href="{invite_link.invite_link}">𝙼𝚈 𝚄𝙿𝙳𝙰𝚃𝙴 𝙲𝙷𝙰𝙽𝙽𝙴𝙻</a>.𝚂𝙾 𝚈𝙾𝚄 𝙳𝙾 𝙽𝙾𝚃 𝙶𝙴𝚃 𝚃𝙷𝙴 𝙵𝙸𝙻𝙴𝚂 𝙾𝙽 𝙱𝙾𝚃 𝙿𝙼 𝙾𝚁 𝙶𝚁𝙾𝚄𝙿 (𝙵𝙸𝙻𝚃𝙴𝚁)</i></b>""", reply_markup=pr0fess0r_99)                
                return
        try:
            mrk, file_id, grp_id = message.text.split("_-_")
            file_details_pr0fess0r99 = await get_file_details(file_id)
            settings = await get_settings(int(grp_id))
            for mrk in file_details_pr0fess0r99:
                title = mrk.file_name
                size = get_size(mrk.file_size)
                await client.send_cached_media(chat_id=message.from_user.id, file_id=file_id, caption=settings["caption"].format(mention=mention, file_name=title, size=size, caption=mrk.caption))
        except Exception as error:
            await message.reply_text(f"𝚂𝙾𝙼𝙴𝚃𝙷𝙸𝙽𝙶 𝚆𝙴𝙽𝚃 𝚆𝚁𝙾𝙽𝙶.!\n\n𝙴𝚁𝚁𝙾𝚁:`{error}`")

@Midukki_RoboT.on_message(Command.b)
async def help_command(client: Midukki_RoboT, message: message()):
    mention = user_mention(message)
    bot_name = Bots.BOT_NAME
    bot_mention = Bots.BOT_MENTION
    bot_username = Bots.BOT_USERNAME    
    if environ.get("BOT_PICS"):
        await message.reply_photo(photo=choice(Configs.START_PICS), caption=HELP_TXT.format(bot=bot_mention, mention=mention, name=bot_name, username=bot_username), reply_markup=markup()(vars.help_buttons))         
    else:
        await message.reply_text(text=HELP_TXT.format(bot=bot_mention, mention=mention, name=bot_name, username=bot_username), reply_markup=markup()(vars.help_buttons))
            
@Midukki_RoboT.on_message(Command.c)
async def about_command(client: Midukki_RoboT, message: message()):
    mention = user_mention(message)
    bot_name = Bots.BOT_NAME
    bot_username = Bots.BOT_USERNAME    
    if environ.get("BOT_PICS"):
        await message.reply_photo(photo=choice(Configs.START_PICS), caption=ABOUT_TXT.format(mention=mention, name=bot_name, username=bot_username), reply_markup=markup()(vars.help_buttons))         
    else:
        await message.reply_text(text=ABOUT_TXT.format(mention=mention, name=bot_name, username=bot_username), reply_markup=markup()(vars.about_buttons))
          
@Midukki_RoboT.on_message(Command.d)
async def donate_command(client: Midukki_RoboT, message: message()):
    mention = user_mention(message)
    bot_name = Bots.BOT_NAME
    bot_username = Bots.BOT_USERNAME    
    if environ.get("BOT_PICS"):
        await message.reply_photo(photo=choice(Configs.START_PICS), caption=DONATE_TXT.format(mention=mention, name=bot_name, username=bot_username))         
    else:
        await message.reply_text(text=DONATE_TXT.format(mention=mention, name=bot_name, username=bot_username))
    await message.reply(f"You can also donate to the person currently running me [Here]({Configs.DONATE_LINKS})")  
     
if __name__ == "__main__":
    Midukki_RoboT().run()
