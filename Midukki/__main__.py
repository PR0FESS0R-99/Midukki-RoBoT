from os import environ
from random import choice 
from pyrogram import filters, enums
from pyrogram.errors import UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
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
from Midukki.functions.traceback import send_msg

import os, asyncio, aiofiles, aiofiles.os, datetime, random, string, time


@Midukki_RoboT.on_message(Command.a)
async def start_command(client: Midukki_RoboT, message: message()):

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

    if message.text.startswith("/start muhammedrk"):
        if Configs.AUTH_CHANNEL:
            try: mrk, file_id, grp_id = message.text.split("_-_")
            except Exception as x:
                return await message.reply("**Error :** `{x}")

            if Configs.FORCES_SUB_LINK:
                invite_link = Configs.FORCES_SUB_LINK
            else:
                try: invite_link = await client.create_chat_invite_link(int(Configs.AUTH_CHANNEL))
                except FloodWait as x:
                    await asyncio.sleep(x.value)
                    return await message.reply(f"FloodWait Error : {x.value}")
            try:
                user = await client.get_chat_member(Configs.AUTH_CHANNEL, user_ids)
                if user.status == enums.ChatMemberStatus.BANNED: # Banned chat member
                    await message.reply(text="""Please Join My pdf Channel to use this Bot!""", disable_web_page_preview=True)                  
                    return
            except UserNotParticipant:
                FORCES = ["https://telegra.ph/file/b2acb2586995d0e107760.jpg"]
                pr0fess0r_99 = [
                    [
                        button()
                            (
                                "📚 Join My Pdf Channel 📚",
                                    url=invite_link.invite_link
                            )
                    ]
                ]    
                pr0fess0r_99 = markup()(pr0fess0r_99)
                await message.reply_photo(photo=choice(FORCES), caption=f"""Hello {message.from_user.mention}. \nYou Have <a href="{invite_link.invite_link}">Not Subscribed</a> 𝚃𝙾 <a href="{invite_link.invite_link}">my updates channel</a>.so you do not get the files on here""", reply_markup=pr0fess0r_99)                
                return
            except FloodWait as x:
                await asyncio.sleep(x.value)
                FORCES = ["https://telegra.ph/file/b2acb2586995d0e107760.jpg"]
                pr0fess0r_99 = [
                    [
                        button()
                            (
                                "📚 Join My Pdf Channel 📚",
                                    url=invite_link.invite_link
                            )
                    ]
                ]    
                pr0fess0r_99 = markup()(pr0fess0r_99)
                await message.reply_photo(photo=choice(FORCES), caption=f"""Hello {message.from_user.mention}. \nYou Have <a href="{invite_link.invite_link}">Not Subscribed</a> 𝚃𝙾 <a href="{invite_link.invite_link}">my updates channel</a>.so you do not get the files on here""", reply_markup=pr0fess0r_99)                
                return    
            except UserIsBlocked:
                await message.reply(f"{mention} : blocked the bot")
                FORCES = ["https://telegra.ph/file/b2acb2586995d0e107760.jpg"]
                pr0fess0r_99 = [
                    [
                        button()
                            (
                                "📚 Join My Pdf Channel 📚",
                                    url=invite_link.invite_link
                            )
                    ]
                ]    
                pr0fess0r_99 = markup()(pr0fess0r_99)
                await message.reply_photo(photo=choice(FORCES), caption=f"""Hello {message.from_user.mention}. \nYou Have <a href="{invite_link.invite_link}">Not Subscribed</a> 𝚃𝙾 <a href="{invite_link.invite_link}">my updates channel</a>.so you do not get the files on here""", reply_markup=pr0fess0r_99)                
                return
            except PeerIdInvalid:
                await message.reply(f"{mention} : user id invalid")
                FORCES = ["https://telegra.ph/file/b2acb2586995d0e107760.jpg"]
                pr0fess0r_99 = [
                    [
                        button()
                            (
                                "📚 Join My Pdf Channel 📚",
                                    url=invite_link.invite_link
                            )
                    ]
                ]    
                pr0fess0r_99 = markup()(pr0fess0r_99)
                await message.reply_photo(photo=choice(FORCES), caption=f"""Hello {message.from_user.mention}. \nYou Have <a href="{invite_link.invite_link}">Not Subscribed</a> 𝚃𝙾 <a href="{invite_link.invite_link}">my updates channel</a>.so you do not get the files on here""", reply_markup=pr0fess0r_99)                


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

    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        if Configs.LOG_CHANNEL is not None:
           await client.send_message(Configs.LOG_CHANNEL, "Name: {}\nId: `{}`".format(message.from_user.id, message.from_user.mention))




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

    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        if Configs.LOG_CHANNEL is not None:
           await client.send_message(Configs.LOG_CHANNEL, "Name: {}\nId: `{}`".format(message.from_user.id, message.from_user.mention))


            
@Midukki_RoboT.on_message(Command.c)
async def about_command(client: Midukki_RoboT, message: message()):
    mention = user_mention(message)
    bot_name = Bots.BOT_NAME
    bot_username = Bots.BOT_USERNAME    
    if environ.get("BOT_PICS"):
        await message.reply_photo(photo=choice(Configs.START_PICS), caption=ABOUT_TXT.format(mention=mention, name=bot_name, username=bot_username), reply_markup=markup()(vars.help_buttons))         
    else:
        await message.reply_text(text=ABOUT_TXT.format(mention=mention, name=bot_name, username=bot_username), reply_markup=markup()(vars.about_buttons))

    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        if Configs.LOG_CHANNEL is not None:
           await client.send_message(Configs.LOG_CHANNEL, "Name: {}\nId: `{}`".format(message.from_user.id, message.from_user.mention))
      
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

    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        if Configs.LOG_CHANNEL is not None:
           await client.send_message(Configs.LOG_CHANNEL, "Name: {}\nId: `{}`".format(message.from_user.id, message.from_user.mention))


@Midukki_RoboT.on_message(Command.e)
async def broadcast_command(client: Midukki_RoboT, message: message()):
    x = message.from_user.id if message.from_user else None
    if x in Configs.ADMINS_ID:
        await send_broadcast(client, message, db, send_msg, Configs)
    else:
        await message.delete()

async def send_broadcast(client, message, db, send_msg, temp):    
    all_users = await db.get_all_users()
    broadcast_msg = message.reply_to_message
    while True:
        broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
        if not temp.broadcast_ids.get(broadcast_id):
            break
    out = await message.reply_text(text="**𝙱𝚁𝙾𝙰𝙳𝙲𝙰𝚂𝚃 𝙸𝙽𝙸𝚃𝙸𝙰𝚃𝙴𝙳..📣**\n   𝚈𝙾𝚄 𝚆𝙸𝙻𝙻 𝙱𝙴 𝙽𝙾𝚃𝙸𝙵𝙸𝙴𝙳 𝚆𝙸𝚃𝙷 𝙻𝙾𝙶 𝙵𝙸𝙻𝙴 𝚆𝙷𝙴𝙽 𝙰𝙻𝙻 𝚃𝙷𝙴 𝚄𝚂𝙴𝚁𝚂 𝙰𝚁𝙴 𝙽𝙾𝚃𝙸𝙵𝙸𝙴𝙳 🔔")
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    success = 0
    temp.broadcast_ids[broadcast_id] = dict(total = total_users, current = done, failed = failed, success = success)
    async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
        async for user in all_users:
            sts, msg = await send_msg(user_id = int(user['id']), message = broadcast_msg)            
            if msg is not None:
                await broadcast_log_file.write(msg)
            if sts == 200:
                success += 1
            else:
                failed += 1
            if sts == 400:
                await db.delete_user(user['id'])
            done += 1
            if temp.broadcast_ids.get(broadcast_id) is None:
                break
            else:
                temp.broadcast_ids[broadcast_id].update(dict(current = done, failed = failed, success = success))
    if temp.broadcast_ids.get(broadcast_id):
        temp.broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time()-start_time))
    await asyncio.sleep(3)    
    await out.delete()
    if failed == 0:
        await message.reply_text(text=f"""**📣 𝙱𝚁𝙾𝙰𝙳𝙲𝙰𝚂𝚃 𝙲𝙾𝙼𝙿𝙻𝙴𝚃𝙴𝙳 𝙸𝙽** - `{completed_in}`\n\n𝚃𝙾𝚃𝙰𝙻 𝚄𝚂𝙴𝚁𝚂 {total_users}.\n𝚃𝙾𝚃𝙰𝙻 𝙳𝙾𝙽𝙴 {done}, {success} 𝚂𝚄𝙲𝙲𝙴𝚂𝚂 & {failed} 𝙵𝙰𝙸𝙻𝙴𝙳""", quote=True)        
    else:
        await message.reply_document(document='broadcast.txt', caption=f"""** 📣 𝙱𝚁𝙾𝙰𝙳𝙲𝙰𝚂𝚃 𝙲𝙾𝙼𝙿𝙻𝙴𝚃𝙴𝙳 𝙸𝙽**- `{completed_in}`\n\n𝚃𝙾𝚃𝙰𝙻 𝚄𝚂𝙴𝚁𝚂 {total_users}.\n𝚃𝙾𝚃𝙰𝙻 𝙳𝙾𝙽𝙴 {done}, {success} 𝚂𝚄𝙲𝙲𝙴𝚂𝚂 & {failed} 𝙵𝙰𝙸𝙻𝙴𝙳""", quote=True)
    await aiofiles.os.remove('broadcast.txt')
    
if __name__ == "__main__":
    Midukki_RoboT().run()
