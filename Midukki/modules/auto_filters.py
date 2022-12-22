import os, aiohttp, re, asyncio
from asyncio import sleep
from pyrogram import filters, enums
from Midukki.midukki import Midukki_RoboT
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified
from pyrogram.errors import UserIsBlocked, MessageNotModified, PeerIdInvalid, FloodWait
from Midukki.database import db, Media, save_file, get_file_details, get_search_results
from Midukki.functions.commands import button, markup, message
from Midukki.functions.handlers import AutoFilter, Admins
from Midukki.functions.settings import get_settings, save_group_settings
from Midukki.functions.unpack_file_id import unpack_new_file_id
from Midukki.functions.user_details import user_mention
from Midukki.functions.media_details import get_size
from Midukki import Configs, Index, Bots, Customize
from logging import getLogger, ERROR

logger = getLogger(__name__)
logger.setLevel(ERROR)

lock = asyncio.Lock()

media_filter = filters.document | filters.video | filters.audio

@Midukki_RoboT.on_message(filters.chat(Configs.CHANNELS) & media_filter)
async def media(client, message):
    """Media Handler"""
    for file_type in ("document", "video", "audio"):
        media = getattr(message, file_type, None)
        if media is not None:
            break
    else:
        return

    media.file_type = file_type
    media.caption = message.caption
    await save_file(media)

async def send_for_index(client, message):
    frw_ch_type = message.forward_from_chat.type if message.forward_from_chat else None
    if message.text:
        regex = re.compile("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
        match = regex.match(message.text)
        if not match:
            return await message.reply('Invalid link')
        chat_id = match.group(4)
        last_msg_id = int(match.group(5))
        if chat_id.isnumeric():
            chat_id = int(("-100" + chat_id))

    elif frw_ch_type == enums.ChatType.CHANNEL:
        last_msg_id = message.forward_from_message_id
        chat_id = message.forward_from_chat.username or message.forward_from_chat.id
    else:
        return
    try:
        try: await client.get_chat(chat_id)
        except Exception as e:
            return await message.reply(f"Error : `{e}`")
    except ChannelInvalid:
        return await message.reply('This may be a private channel / group. Make me an admin over there to index the files.')
    except (UsernameInvalid, UsernameNotModified):
        return await message.reply('Invalid Link specified.')
    except Exception as e:
        logger.exception(e)
        return await message.reply(f'Errors - {e}')
    try:
        k = await client.get_messages(chat_id, last_msg_id)
    except:
        return await message.reply('Make Sure That Iam An Admin In The Channel, if channel is private')
    if k.empty:
        return await message.reply('This may be group and iam not a admin of the group.')

    if message.from_user.id in Configs.ADMINS_ID:
        buttons = [
            [
                button()
                    (
                        'Yes',
                            callback_data=f'index#accept#{chat_id}#{last_msg_id}#{message.from_user.id}')
            ],
            [
                button()
                    (
                        'close',
                            callback_data='close_data'
                    )
            ]
        ]

        reply_markup = markup()(buttons)
        return await message.reply(
            f'Do you Want To Index This Channel/ Group ?\n\nChat ID/ Username: <code>{chat_id}</code>\nLast Message ID: <code>{last_msg_id}</code>',
            reply_markup=reply_markup
        )

    if type(chat_id) is int:
        try:
            link = (await client.create_chat_invite_link(chat_id)).invite_link
        except ChatAdminRequired:
            return await message.reply('Make sure iam an admin in the chat and have permission to invite users.')
    else:
        link = f"@{message.forward_from_chat.username}"
    buttons = [
        [
            button()
                (
                    'Accept Index',
                        callback_data=f'index#accept#{chat_id}#{last_msg_id}#{message.from_user.id}'
                )
        ],
        [
            button()
                (
                    'Reject Index',
                        callback_data=f'index#reject#{chat_id}#{message.id}#{message.from_user.id}'
                )
        ]
    ]
    reply_markup = markup()(buttons)
    if Configs.LOG_CHANNEL:
        await client.send_message(Configs.LOG_CHANNEL,
            f'#IndexRequest\n\nBy : {message.from_user.mention} (<code>{message.from_user.id}</code>)\nChat ID/ Username - <code> {chat_id}</code> Message ID - <code>{last_msg_id}</code>\nInviteLink - {link}',
            reply_markup=reply_markup
        )
        await message.reply('ThankYou For the Contribution, Wait For My Moderators to verify the files.')

async def index_files(client, query):
    if query.data.startswith('index_cancel'):
        temp.CANCEL = True
        return await query.answer("Cancelling Indexing")
    _, muhammed, chat, lst_msg_id, from_user = query.data.split("#")
    if muhammed == 'reject':
        await query.message.delete()
        await client.send_message(int(from_user),
                               f'Your Submission for indexing {chat} has been decliened by our moderators.',
                               reply_to_message_id=int(lst_msg_id)
        )
        return

    if lock.locked():
        return await query.answer('Wait until previous process complete.', show_alert=True)
    msg = query.message

    await query.answer('Processing...⏳', show_alert=True)
    if int(from_user) not in Configs.ADMINS_ID:
        await client.send_message(int(from_user),
                               f'Your Submission for indexing {chat} has been accepted by our moderators and will be added soon.',
                               reply_to_message_id=int(lst_msg_id)
        )
    await msg.edit(
        "Starting Indexing",
        reply_markup=markup()
            (
                [
                    [
                        button()
                            (
                                'Cancel',
                                    callback_data='index_cancel'
                            )
                    ]
                ]
           )
       )
    try:
        chat = int(chat)
    except:
        chat = chat
    await index_files_to_db(int(lst_msg_id), chat, msg, client)


@Midukki_RoboT.on_message(AutoFilter.b)
async def save_template(client: Midukki_RoboT, message: message()):
    sts = await message.reply_text("⏳️")
    await sleep(0.3)
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply_text(f"Your Anonymous Admin. `/connect {update.chat.id}` in pm")

    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        grpid = await db.active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await sts.edit("Make sure iam present in your group..!", quote=True)
                return
        else:
            await sts.edit("iam not connect any group..!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title
    else:
        return

    motechyt = await client.get_chat_member(grp_id, userid)
    if (motechyt.status != enums.ChatMemberStatus.ADMINISTRATOR and motechyt.status != enums.ChatMemberStatus.OWNER and userid not in Configs.ADMINS_ID):
        await sts.delete()
        return

    if len(message.command) < 2:
        return await sts.edit("None")

    pr0fess0r_99 = message.text.split(" ", 1)[1]
    await save_group_settings(grp_id, 'template', pr0fess0r_99)
    await sts.edit(f"""Successfully Changed Temp (Autofilter) for {title} to \n\n{pr0fess0r_99}""")


@Midukki_RoboT.on_message(AutoFilter.c)
async def reset_template(client: Midukki_RoboT, message: message()):
    sts = await message.reply_text("⏳️")
    await sleep(0.3)
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply_text(f"Your Anonymous Admin. `/connect {update.chat.id}` in pm")

    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        grpid = await db.active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await sts.edit("Make sure iam present in your group..!", quote=True)
                return
        else:
            await sts.edit("iam not connect any group..!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title
    else:
        return

    motechyt = await client.get_chat_member(grp_id, userid)
    if (motechyt.status != enums.ChatMemberStatus.ADMINISTRATOR and motechyt.status != enums.ChatMemberStatus.OWNER and userid not in Configs.ADMINS_ID):
        await sts.delete()
        return

    await save_group_settings(grp_id, 'template', Customize.IMDB_TEMPLATE)
    await sts.edit(f"""Successfully Restarted Autofilter""")


@Midukki_RoboT.on_message(AutoFilter.d)
async def set_filecaption(client: Midukki_RoboT, message: message()):
    sts = await message.reply_text("⏳️")
    await sleep(0.3)
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply_text(f"Your Anonymous Admin. `/connect {update.chat.id}` in pm")

    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        grpid = await db.active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await sts.edit("Make sure iam present in your group..!", quote=True)
                return
        else:
            await sts.edit("iam not connect any group..!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title
    else:
        return

    motechyt = await client.get_chat_member(grp_id, userid)
    if (motechyt.status != enums.ChatMemberStatus.ADMINISTRATOR and motechyt.status != enums.ChatMemberStatus.OWNER and userid not in Configs.ADMINS_ID):
        await sts.delete()
        return

    if len(message.command) < 2:
        return await sts.edit("None")

    pr0fess0r_99 = message.text.split(" ", 1)[1]
    await save_group_settings(grp_id, 'caption', pr0fess0r_99)
    await sts.edit(f"""Successfully Changed FileCaption (Autofilter) for {title} to \n\n{pr0fess0r_99}""")


@Midukki_RoboT.on_message(AutoFilter.e)
async def reset_caption(client: Midukki_RoboT, message: message()):
    sts = await message.reply_text("⏳️")
    await sleep(0.3)
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply_text(f"Your Anonymous Admin. `/connect {update.chat.id}` in pm")

    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        grpid = await db.active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await sts.edit("Make sure iam present in your group..!", quote=True)
                return
        else:
            await sts.edit("iam not connect any group..!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title
    else:
        return

    motechyt = await client.get_chat_member(grp_id, userid)
    if (motechyt.status != enums.ChatMemberStatus.ADMINISTRATOR and motechyt.status != enums.ChatMemberStatus.OWNER and userid not in Configs.ADMINS_ID):
        await sts.delete()
        return

    await save_group_settings(grp_id, 'caption', Customize.FILE_CAPTION)
    await sts.edit("Successfully Restarted FileCaption")


@Midukki_RoboT.on_message(AutoFilter.f)
async def set_spellmode(client: Midukki_RoboT, message: message()):
    sts = await message.reply_text("⏳️")
    await sleep(0.3)
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply_text(f"Your Anonymous Admin. `/connect {update.chat.id}` in pm")

    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        grpid = await db.active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await sts.edit("Make sure iam present in your group..!", quote=True)
                return
        else:
            await sts.edit("iam not connect any group..!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title
    else:
        return

    motechyt = await client.get_chat_member(grp_id, userid)
    if (motechyt.status != enums.ChatMemberStatus.ADMINISTRATOR and motechyt.status != enums.ChatMemberStatus.OWNER and userid not in Configs.ADMINS_ID):
        await sts.delete()
        return

    if len(message.command) < 2:
        return await sts.edit("None")

    pr0fess0r_99 = message.text.split(" ", 1)[1]
    await save_group_settings(grp_id, 'spell_caption', pr0fess0r_99)
    await sts.edit(f"""Successfully Changed SpellCheck Message (Autofilter) for {title} to \n\n{pr0fess0r_99}""")


@Midukki_RoboT.on_message(AutoFilter.g)
async def reset_spellmode(client: Midukki_RoboT, message: message()):
    sts = await message.reply_text("⏳️")
    await sleep(0.3)
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply_text(f"Your Anonymous Admin. `/connect {update.chat.id}` in pm")

    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        grpid = await db.active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await sts.edit("Make sure iam present in your group..!", quote=True)
                return
        else:
            await sts.edit("iam not connect any group..!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title
    else:
        return

    motechyt = await client.get_chat_member(grp_id, userid)
    if (motechyt.status != enums.ChatMemberStatus.ADMINISTRATOR and motechyt.status != enums.ChatMemberStatus.OWNER and userid not in Configs.ADMINS_ID):
        await sts.delete()
        return

    await save_group_settings(grp_id, 'spell_caption', Customize.SPELLCHECK_CAPTION)
    await sts.edit("Successfully Restarted SpellCheck Message")

@Midukki_RoboT.on_message(AutoFilter.h)
async def set_autodel(client: Midukki_RoboT, message: message()):
    sts = await message.reply_text("⏳️")
    await sleep(0.3)
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply_text(f"Your Anonymous Admin. `/connect {update.chat.id}` in pm")

    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        grpid = await db.active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await sts.edit("Make sure iam present in your group..!", quote=True)
                return
        else:
            await sts.edit("iam not connect any group..!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title
    else:
        return

    motechyt = await client.get_chat_member(grp_id, userid)
    if (motechyt.status != enums.ChatMemberStatus.ADMINISTRATOR and motechyt.status != enums.ChatMemberStatus.OWNER and userid not in Configs.ADMINS_ID):
        await sts.delete()
        return

    if len(message.command) < 2:
        return await sts.edit("Please enter command with delete time in seconds eg:-  /auto_delete 600")

    pr0fess0r_99 = message.text.split(" ", 1)[1]
    try: pr0fess0r_99 = int(pr0fess0r_99)
    except:
        await message.reply("Eg : `/set_autodelete 100`")
        return
    await save_group_settings(grp_id, 'auto_del', pr0fess0r_99)
    await sts.edit(f"""Successfully Changed Auto Delete Time (Autofilter) for {title}""")


@Midukki_RoboT.on_message(Admins.a)
async def channel_info(client, message):
           
    """Send basic information of channel"""
    if isinstance(Configs.CHANNELS, (int, str)):
        channels = [Configs.CHANNELS]
    elif isinstance(Configs.CHANNELS, list):
        channels = Configs.CHANNELS
    else:
        raise ValueError("Unexpected type of CHANNELS")

    text = '📑 **Indexed channels/groups**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n**Total:** {len(Configs.CHANNELS)}'

    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)

@Midukki_RoboT.on_message(Admins.b)
async def total(client, message):
    msg = await message.reply_text("Processing...⏳", quote=True)
    try:
        total = await Media.count_documents()
        await msg.edit(f'📁 Saved files: {total}')
    except Exception as e:
        logger.exception('Failed To Check Total Files')
        await msg.edit(f'Error: {e}')

@Midukki_RoboT.on_message(Admins.c)
async def delete(client, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("Processing...⏳", quote=True)
    else:
        await message.reply('Reply to file with /delete which you want to delete', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('This is not supported file format')
        return
    
    file_id, file_ref = unpack_new_file_id(media.file_id)

    result = await Media.collection.delete_one({
        '_id': file_id,
    })
    if result.deleted_count:
        await msg.edit('File is successfully deleted from database')
    else:
        file_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
        result = await Media.collection.delete_many({
            'file_name': file_name,
            'file_size': media.file_size,
            'mime_type': media.mime_type
            })
        if result.deleted_count:
            await msg.edit('File is successfully deleted from database')
        else:
            # files indexed before https://github.com/EvamariaTG/EvaMaria/commit/f3d2a1bcb155faf44178e5d7a685a1b533e714bf#diff-86b613edf1748372103e94cacff3b578b36b698ef9c16817bb98fe9ef22fb669R39 
            # have original file name.
            result = await Media.collection.delete_many({
                'file_name': media.file_name,
                'file_size': media.file_size,
                'mime_type': media.mime_type
            })
            if result.deleted_count:
                await msg.edit('File is successfully deleted from database')
            else:
                await msg.edit('File not found in database')

@Midukki_RoboT.on_message(Admins.d)
async def delete_all_index(client, message):
    await message.reply_text(
        'This will delete all indexed files.\nDo you want to continue??',
        reply_markup=markup()(
            [
                [
                    button()(
                        text="YES", callback_data="autofilter_delete"
                    )
                ],
                [
                    button()(
                        text="CANCEL", callback_data="close_data"
                    )
                ],
            ]
        ),
        quote=True,
    )

@Midukki_RoboT.on_message(Admins.e)
async def set_skip_number(client, message):
    if ' ' in message.text:
        _, skip = message.text.split(" ")
        try:
            skip = int(skip)
        except:
            return await message.reply("Skip number should be an integer.")
        await message.reply(f"Successfully set SKIP number as {skip}")
        Index.CURRENT = int(skip)
    else:
        await message.reply("Give me a skip number")

@Midukki_RoboT.on_message(Admins.f)
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.txt')
    except Exception as e:
        await message.reply(str(e))

@Midukki_RoboT.on_callback_query(filters.regex(r'^autofilter_delete'))
async def delete_all_index_confirm(client, message):
    await Media.collection.drop()
    await message.answer('Piracy Is Crime')
    await message.message.edit('Succesfully Deleted All The Indexed Files.')

async def index_files_to_db(lst_msg_id, chat, msg, bot):
    total_files = 0
    duplicate = 0
    errors = 0
    deleted = 0
    no_media = 0
    unsupported = 0
    async with lock:
        try:
            current = Index.CURRENT
            Index.CANCEL = False
            async for message in bot.iter_messages(chat, lst_msg_id, Index.CURRENT):
                if Index.CANCEL:
                    await msg.edit(f"Successfully Cancelled!!\n\nSaved <code>{total_files}</code> files to dataBase!\nDuplicate Files Skipped: <code>{duplicate}</code>\nDeleted Messages Skipped: <code>{deleted}</code>\nNon-Media messages skipped: <code>{no_media + unsupported}</code>(Unsupported Media - `{unsupported}` )\nErrors Occurred: <code>{errors}</code>")
                    break
                current += 1
                if current % 20 == 0:
                    can = [
                        [
                            button()
                                (
                                    'Cancel',
                                         callback_data='index_cancel'
                                )
                        ]
                    ]
                    reply = markup()(can)
                    await msg.edit_text(
                        text=f"Total messages fetched: <code>{current}</code>\nTotal messages saved: <code>{total_files}</code>\nDuplicate Files Skipped: <code>{duplicate}</code>\nDeleted Messages Skipped: <code>{deleted}</code>\nNon-Media messages skipped: <code>{no_media + unsupported}</code>(Unsupported Media - `{unsupported}` )\nErrors Occurred: <code>{errors}</code>",
                        reply_markup=reply)
                if message.empty:
                    deleted += 1
                    continue
                elif not message.media:
                    no_media += 1
                    continue
                elif message.media not in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.AUDIO, enums.MessageMediaType.DOCUMENT]:
                    unsupported += 1
                    continue
                media = getattr(message, message.media.value, None)
                if not media:
                    unsupported += 1
                    continue
                media.file_type = message.media.value
                media.caption = message.caption
                aynav, vnay = await save_file(media)
                if aynav:
                    total_files += 1
                elif vnay == 0:
                    duplicate += 1
                elif vnay == 2:
                    errors += 1
        except Exception as e:
            logger.exception(e)
            await msg.edit(f'Error: {e}')
        else:
            await msg.edit(f'Succesfully saved <code>{total_files}</code> to dataBase!\nDuplicate Files Skippmarkup()ode>{duplicate}</code>\nDeleted Messages Skipped: <code>{deleted}</code>\nNon-Media messages skipped: <code>{no_media + unsupported}</code>(Unsupported Media - `{unsupported}` )\nErrors Occurred: <code>{errors}</code>')

async def get_result_file(client, query):
    ident, file_id = query.data.split("#")
    files_ = await get_file_details(file_id)
    if not files_:
        return await query.answer('No such file exist.')
    files = files_[0]
    title = files.file_name
    size = get_size(files.file_size)
    f_caption = files.caption
    settings = await get_settings(query.message.chat.id)


    f_caption = settings["caption"].format(
       mention= query.from_user.mention if query.from_user else None,
       file_name='' if title is None else title,
       file_size='' if size is None else size,
       file_caption='' if f_caption is None else f_caption
    )
 
    try:
        if Configs.AUTH_CHANNEL and not await client.is_subscribed(client, query):
            await query.answer(url=f"https://t.me/{Bots.BOT_USERNAME}?start=Midukki_-_{file_id}")
            return
        else:     
            await client.send_cached_media(
                chat_id=query.from_user.id,
                file_id=file_id,
                caption=f_caption                    
            )
            await query.answer('Check PM, I have sent files in pm', show_alert=True)
    except UserIsBlocked:
        await query.answer('Unblock the bot mahn !', show_alert=True)
    except PeerIdInvalid:
        await query.answer(url=f"https://t.me/{Bots.BOT_USERNAME}?start=Midukki_-_{file_id}")
    except Exception as e:
        await query.answer(url=f"https://t.me/{Bots.BOT_USERNAME}?start=Midukki_-_{file_id}")

async def auto_filters(client: Midukki_RoboT, message: message()):

    if 2 < len(message.text) < 100:    
        btn = []
        search = message.text
        settings = await get_settings(message.chat.id)
        
        files, offset, total_results = await get_search_results(search.lower(), offset=0, filter=True)

        if not files:
            if settings["spell_check"]:
                await check_correct_spelling(message, settings)
            if not await db.get_chat(message.chat.id):
                await db.add_chat(message.chat.id, message.chat.title)
                if Configs.LOG_CHANNEL != 0:
                    total=await client.get_chat_members_count(message.chat.id)
                    mrk = message.from_user.mention if message.from_user else "Anonymous" 
                    await client.send_message(Configs.LOG_CHANNEL, text="""name : {}\nid : `{}`\ntotal users : {}\nuser : `{}`""".format(message.chat.title, message.chat.id, total, mrk))      
                return
            return

        if files:
            for file in files:
                file_id = file.file_id
                filesize = f"[{get_size(file.file_size)}]"
                filename = f"{file.file_name}"
                
                if settings["buttons"]:
                    if Configs.WEB_API:
                        btn.append(
                            [
                                button()
                                    (
                                        f"{filesize} {filename}",
                                            url=await get_shortlink(f"http://telegram.dog/{Bots.BOT_USERNAME}?start=muhammedrk_-_{file_id}_-_{message.chat.id}")
                                    )
                            ]
                        )
                    else:
                        btn.append(
                            [
                                button()
                                    (
                                        f"{filesize} {filename}",
                                            url=f"http://telegram.dog/{Bots.BOT_USERNAME}?start=muhammedrk_-_{file_id}_-_{message.chat.id}"
                                    )
                            ]
                        )
                else:
                    if Configs.WEB_API:
                        btn.append(
                            [
                                button()
                                    (
                                        f"{filesize}",
                                            url=await get_shortlink(f"http://telegram.dog/{Bots.BOT_USERNAME}?start=muhammedrk_-_{file_id}_-_{message.chat.id}")
                                    ),
                                button()
                                    (
                                        f"{filename}",
                                            url=await get_shortlink(f"http://telegram.dog/{Bots.BOT_USERNAME}?start=muhammedrk_-_{file_id}_-_{message.chat.id}")
                                    )
                            ]
                        )
                    else:
                        btn.append(
                            [
                                button()
                                    (
                                        f"{filesize}",
                                            url=f"http://telegram.dog/{Bots.BOT_USERNAME}?start=muhammedrk_-_{file_id}_-_{message.chat.id}"
                                    ),
                                button()
                                    (
                                        f"{filename}",
                                            url=f"http://telegram.dog/{Bots.BOT_USERNAME}?start=muhammedrk_-_{file_id}_-_{message.chat.id}"
                                    )
                            ]
                        )
                   
        else:
            return

        if not btn:
            return

        if len(btn) > Configs.FILTER_RESULTS: 
            btns = list(split_list(btn, Configs.FILTER_RESULTS)) 
            keyword = f"{message.chat.id}-{message.id if message else None}"
            Configs.FILTER_BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
            data = Configs.FILTER_BUTTONS[keyword]
            buttons = data['buttons'][0].copy()
   
            buttons.append(
                [
                    button()
                        (
                            f"📃 1/{data['total']}",
                                callback_data="pages"
                        ),
                    button()
                        (
                            "🗑️",
                                callback_data="close"
                        ),
                    button()
                        (
                            "➡",
                                callback_data=f"nextgroup_0_{keyword}"
                        )
                ]
            )
            if settings["file_mode"]:
                buttons.append(
                    [
                        button()
                            (
                                "🤖 Check My Pm 🤖",
                                    url=f"https://telegram.dog/{Bots.BOT_USERNAME}"
                            )
                    ]
                )
            Del_Time = settings["auto_del"]  
            try:
                result = await message.reply_text(text=settings["template"].format(mention=user_mention(message), query=message.text, group_name = f"[{message.chat.title}](t.me/{message.chat.username})" or f"[{message.chat.title}](t.me/{message.from_user.username if message.from_user else 'Pr0fess0r_99'})"), reply_markup=markup()(buttons))
                await asyncio.sleep(Del_Time)
                await result.delete()
            except Exception as e:
                result = await message.reply_text(text=Customize.IMDB_TEMPLATE.format(mention=user_mention(message), query=message.text, group_name = f"[{message.chat.title}](t.me/{message.chat.username})" or f"[{message.chat.title}](t.me/{message.from_user.username if message.from_user else 'Pr0fess0r_99'})"), reply_markup=markup()(buttons))
                await message.reply(e)
                await asyncio.sleep(Del_Time)
                await result.delete()

            if not await db.get_chat(message.chat.id):
                await db.add_chat(message.chat.id, message.chat.title)
                if Configs.LOG_CHANNEL != 0:
                    total=await client.get_chat_members_count(message.chat.id)
                    mrk = message.from_user.mention if message.from_user else "Anonymous" 
                    await client.send_message(Configs.LOG_CHANNEL, text="""name : {}\nid : `{}`\ntotal users : {}\nuser : `{}`""".format(message.chat.title, message.chat.id, total, mrk))      


        else:
            buttons = btn
            buttons.append(
                [
                    button()
                        (
                            "📃 Pages 1/1",
                                callback_data="pages"
                        ),
                    button()
                        (
                            "Close 🗑️",
                                callback_data="close"
                        )
                ]
            )
            if settings["file_mode"]:
                buttons.append(
                    [
                        button()
                            (
                                "🤖 Check My Pm 🤖",
                                    url=f"https://telegram.dog/{Bots.BOT_USERNAME}"
                            )
                    ]
                )

            Del_Time = settings["auto_del"]  
            try:
                result = await message.reply_text(text=settings["template"].format(mention=user_mention(message), query=message.text, group_name = f"[{message.chat.title}](t.me/{message.chat.username})" or f"[{message.chat.title}](t.me/{message.from_user.username if message.from_user else 'Pr0fess0r_99'})"), reply_markup=markup()(buttons))
                await asyncio.sleep(Del_Time)
                await result.delete()
            except Exception as e:
                result = await message.reply_text(text=Customize.IMDB_TEMPLATE.format(mention=user_mention(message), query=message.text, group_name = f"[{message.chat.title}](t.me/{message.chat.username})" or f"[{message.chat.title}](t.me/{message.from_user.username if message.from_user else 'Pr0fess0r_99'})"), reply_markup=markup()(buttons))
                await message.reply(e)
                await asyncio.sleep(Del_Time)
                await result.delete()

            if not await db.get_chat(message.chat.id):
                await db.add_chat(message.chat.id, message.chat.title)
                if Configs.LOG_CHANNEL != 0:
                    total=await client.get_chat_members_count(message.chat.id)
                    mrk = message.from_user.mention if message.from_user else "Anonymous" 
                    await client.send_message(Configs.LOG_CHANNEL, text="""name : {}\nid : `{}`\ntotal users : {}\nuser : `{}`""".format(message.chat.title, message.chat.id, total, mrk))      


def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

async def next_page_(message):
    mrk, index, keyword = message.data.split("_")
    try:
        data = Configs.FILTER_BUTTONS[keyword]
    except KeyError:
        await message.answer("𝚃𝙷𝙸𝚂 𝙼𝚈 𝙾𝙻𝙳 𝙼𝙴𝚂𝚂𝙰𝙶𝙴 𝚂𝙾 𝙿𝙻𝙴𝙰𝚂𝙴 𝚁𝙴𝚀𝚄𝙴𝚂𝚃 𝙰𝙶𝙰𝙸𝙽 🙏",show_alert=True)
        return

    settings = await get_settings(message.message.chat.id)
        
    if int(index) == int(data["total"]) - 2:
        buttons = data['buttons'][int(index)+1].copy()
        buttons.append(
            [
                button()
                    (
                        "🔙",
                            callback_data=f"backgroup_{int(index)+1}_{keyword}"
                    ),
                button()
                    (
                        f"📃 {int(index)+2}/{data['total']}",
                            callback_data="pages"
                    ),
                button()
                    (
                        "🗑️",
                            callback_data="close"
                    )           
            ]
        )
        if settings["file_mode"]:
            buttons.append(
                [
                    button()
                        (
                            "🤖 𝙲𝙷𝙴𝙲𝙺 𝙼𝚈 𝙿𝙼 🤖",
                                url=f"https://telegram.dog/{temp.Bot_Username}"
                        )
                ]
            )
        
        try:
            await message.edit_message_reply_markup( 
                reply_markup=markup()
                    (
                        buttons
                    )
            )
        except MessageNotModified:
            pass
        except FloodWait as x:
            await asyncio.sleep(x.value)
        return
    else:
        buttons = data['buttons'][int(index)+1].copy()
        buttons.append(
            [
                button()
                    (
                        "🔙",
                            callback_data=f"backgroup_{int(index)+1}_{keyword}"
                    ),
                button()
                    (
                        f"📃 {int(index)+2}/{data['total']}",
                            callback_data="pages"
                    ),
                button()
                    (
                        "🗑️",
                            callback_data="close"
                    ),
                button()
                    (
                        "➡",
                            callback_data=f"nextgroup_{int(index)+1}_{keyword}"
                    )
            ]
        )
        if settings["file_mode"]:
            buttons.append(
                [
                    button()
                        (
                            "🤖 𝙲𝙷𝙴𝙲𝙺 𝙼𝚈 𝙿𝙼 🤖",
                                url=f"https://telegram.dog/{temp.Bot_Username}"
                        )
                ]
            )
        
        try:
            await message.edit_message_reply_markup( 
                reply_markup=markup()
                    (
                        buttons
                    )
            )
        except MessageNotModified:
            pass
        except FloodWait as x:
            await asyncio.sleep(x.value)
        return

async def back_page_(message):
    mrk, index, keyword = message.data.split("_")
    try:
        data = Configs.FILTER_BUTTONS[keyword]
    except KeyError:
        await message.answer("𝚃𝙷𝙸𝚂 𝙼𝚈 𝙾𝙻𝙳 𝙼𝙴𝚂𝚂𝙰𝙶𝙴 𝚂𝙾 𝙿𝙻𝙴𝙰𝚂𝙴 𝚁𝙴𝚀𝚄𝙴𝚂𝚃 𝙰𝙶𝙰𝙸𝙽 🙏",show_alert=True)
        return

    settings = await get_settings(message.message.chat.id)
        
    if int(index) == 1:
        buttons = data['buttons'][int(index)-1].copy()
        buttons.append(
            [
                button()
                    (
                        f"📃 {int(index)}/{data['total']}",
                            callback_data="pages"
                    ),
                button()
                    (
                        "🗑️",
                            callback_data="close"
                    ),
                button()
                    (
                        "➡",
                            callback_data=f"nextgroup_{int(index)-1}_{keyword}"
                    )
            ]
        )
        if settings["file_mode"]:
            buttons.append(
                [
                    button()
                        (
                            "🤖 𝙲𝙷𝙴𝙲𝙺 𝙼𝚈 𝙿𝙼 🤖",
                                url=f"https://telegram.dog/{temp.Bot_Username}"
                        )
                ]
            )
        
        try:
            await message.edit_message_reply_markup( 
                reply_markup=markup()
                    (
                        buttons
                    )
            )
        except MessageNotModified:
            pass
        except FloodWait as x:
            print(x.value)
        return
    else:
        buttons = data['buttons'][int(index)-1].copy()
        buttons.append(
            [
                button()
                    (
                        "🔙",
                            callback_data=f"backgroup_{int(index)-1}_{keyword}"
                    ),
                button()
                    (
                        f"📃 {int(index)}/{data['total']}",
                            callback_data="pages"
                    ),
                button()
                    (
                        "🗑️",
                            callback_data="close"
                    ),
                button()
                    (
                        "➡",
                            callback_data=f"nextgroup_{int(index)-1}_{keyword}"
                        )
                ]
            )

        if settings["file_mode"]:
        
            buttons.append(
                [
                    button()
                        (
                            "🤖 𝙲𝙷𝙴𝙲𝙺 𝙼𝚈 𝙿𝙼 🤖",
                                url=f"https://telegram.dog/{temp.Bot_Username}"
                        )
                ]
            )

        try:
            await message.edit_message_reply_markup( 
                reply_markup=markup()
                    (
                        buttons
                    )
            )
        except MessageNotModified:
            pass
        except FloodWait as x:
            await asyncio.sleep(x.value)
            pass
        return

async def get_shortlink(link):

    url = f'{Configs.WEB_URL}/api'
    params = {
      'api': Configs.WEB_API,
      'url': link,
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
                data = await response.json()
                if data["status"] == "success":
                    return data['shortenedUrl']
                else:
                    logger.error(f"Error: {data['message']}")
                    return link
    except Exception as e:
        logger.error(e)
        return link

async def check_correct_spelling(message, settings):
    try:
        await message.reply(settings["spell_caption"].format(mention=user_mention(message), title=message.chat.title, query=message.text),
            reply_markup=markup()
            (
                [
                    [
                        button()
                            (
                                "🔍 Search In Google 🔎",
                                    url="https://www.google.com/"
                            )
                    ]
                ]
            )
        )     
    except Exception as e:
        await message.reply(Customize.SPELLCHECK_CAPTION.format(mention=user_mention(message), title=message.chat.title, query=message.text),
            reply_markup=markup()
            (
                [
                    [
                        button()
                            (
                                "🔍 Search In Google 🔎",
                                    url="https://www.google.com/"
                            )
                    ]
                ]
            )
        )
        await message.reply(e)
