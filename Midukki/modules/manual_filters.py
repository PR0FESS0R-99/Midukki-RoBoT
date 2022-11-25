import ast
from re import escape, IGNORECASE, search as search_filter
from logging import ERROR, getLogger
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from Midukki.midukki import Midukki_RoboT
from Midukki.functions.handlers import Manual
from Midukki.functions.keyboards import parser, split_quotes
from Midukki.functions.media_details import get_file_id
from Midukki.database import db
from Midukki import Configs

logger = getLogger(__name__)
logger.setLevel(ERROR)

async def manual_filters(client, message, text=False):
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await db.get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + escape(keyword) + r"( |$|[^\w])"
        if search_filter(pattern, name, flags=IGNORECASE):
            reply_text, btn, alert, fileid = await db.find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            await client.send_message(group_id, reply_text, disable_web_page_preview=True)
                        else:
                            button = eval(btn)
                            await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id=reply_id
                            )
                    elif btn == "[]":
                        await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            reply_to_message_id=reply_id
                        )
                    else:
                        button = eval(btn)
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False

@Midukki_RoboT.on_message(Manual.a)
async def addfilter(client: Midukki_RoboT, message: Message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")

    chat_type = message.chat.type
    args = message.text.html.split(None, 1)

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await db.active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
        st.status != enums.ChatMemberStatus.ADMINISTRATOR
        and st.status != enums.ChatMemberStatus.OWNER
        and str(userid) not in Configs.ADMINS_ID
    ):
        return


    if len(args) < 2:
        await message.reply_text("Command Incomplete :(", quote=True)
        return

    extracted = split_quotes(args[1])
    text = extracted[0].lower()

    if not message.reply_to_message and len(extracted) < 2:
        await message.reply_text("Add some content to save your filter!", quote=True)
        return

    if (len(extracted) >= 2) and not message.reply_to_message:
        reply_text, btn, alert = parser(extracted[1], text)
        fileid = None
        if not reply_text:
            await message.reply_text("You cannot have buttons alone, give some text to go with it!", quote=True)
            return

    elif message.reply_to_message and message.reply_to_message.reply_markup:
        try:
            rm = message.reply_to_message.reply_markup
            btn = rm.inline_keyboard
            msg = get_file_id(message.reply_to_message)
            if msg:
                fileid = msg.file_id
                reply_text = message.reply_to_message.caption.html
            else:
                reply_text = message.reply_to_message.text.html
                fileid = None
            alert = None
        except:
            reply_text = ""
            btn = "[]" 
            fileid = None
            alert = None

    elif message.reply_to_message and message.reply_to_message.media:
        try:
            msg = get_file_id(message.reply_to_message)
            fileid = msg.file_id if msg else None
            reply_text, btn, alert = parser(extracted[1], text) if message.reply_to_message.sticker else parser(message.reply_to_message.caption.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None
    elif message.reply_to_message and message.reply_to_message.text:
        try:
            fileid = None
            reply_text, btn, alert = parser(message.reply_to_message.text.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None
    else:
        return

    await db.add_filter(grp_id, text, reply_text, btn, fileid, alert)

    await message.reply_text(
        f"Filter for  `{text}`  added in  **{title}**",
        quote=True,
        parse_mode=enums.ParseMode.MARKDOWN
    )

@Midukki_RoboT.on_message(Manual.b)
async def get_all(client: Midukki_RoboT, message: Message):
    
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")

    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        grpid = await db.active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
        st.status != enums.ChatMemberStatus.ADMINISTRATOR
        and st.status != enums.ChatMemberStatus.OWNER
        and str(userid) not in ADMINS
    ):
        return

    texts = await db.get_filters(grp_id)
    count = await db.count_filters(grp_id)
    if count:
        filterlist = f"Total number of filters in **{title}** : {count}\n\n"

        for text in texts:
            keywords = " ×  `{}`\n".format(text)

            filterlist += keywords

        if len(filterlist) > 4096:
            with io.BytesIO(str.encode(filterlist.replace("`", ""))) as keyword_file:
                keyword_file.name = "keywords.txt"
                await message.reply_document(
                    document=keyword_file,
                    quote=True
                )
            return
    else:
        filterlist = f"There are no active filters in **{title}**"

    await message.reply_text(
        text=filterlist,
        quote=True,
        parse_mode=enums.ParseMode.MARKDOWN
    )

@Midukki_RoboT.on_message(Manual.c)
async def deletefilter(client: Midukki_RoboT, message: Message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await db.active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
        st.status != enums.ChatMemberStatus.ADMINISTRATOR
        and st.status != enums.ChatMemberStatus.OWNER
        and str(userid) not in ADMINS
    ):
        return

    try:
        cmd, text = message.text.split(" ", 1)
    except:
        await message.reply_text(
            "<i>Mention the filtername which you wanna delete!</i>\n\n"
            "<code>/del filtername</code>\n\n"
            "Use /viewfilters to view all available filters",
            quote=True
        )
        return

    query = text.lower()

    await db.delete_filter(message, query, grp_id)
       
@Midukki_RoboT.on_message(Manual.d)
async def delallconfirm(client: Midukki_RoboT, message: Message):

    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")

    chat_type = message.chat.title

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await db.active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in Configs.ADMINS_ID):
        await message.reply_text(
            text=f"This will delete all filters from '{title}'.\nDo you want to continue??",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="YES",callback_data="delallconfirm")],[InlineKeyboardButton(text="CANCEL",callback_data="delallcancel")]]))

async def del_all_confirm(client, query):    
    userid = query.from_user.id
    chat_type = query.message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await db.active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await query.message.edit_text("Make sure I'm present in your group!!", quote=True)
                return await query.answer('Piracy Is Crime')
        else:
            await query.message.edit_text(
                "I'm not connected to any groups!\nCheck /connections or connect to any groups",
                quote=True
            )
            return await query.answer('Piracy Is Crime')

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = query.message.chat.id
        title = query.message.chat.title

    else:
        return await query.answer('Piracy Is Crime')

    st = await client.get_chat_member(grp_id, userid)
    if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in Configs.ADMINS_ID):
        await db.del_all(query.message, grp_id, title)
    else:
        await query.answer("You need to be Group Owner or an Auth User to do that!", show_alert=True)

async def del_all_cancel(client, query):
    userid = query.from_user.id
    chat_type = query.message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        await query.message.reply_to_message.delete()
        await query.message.delete()

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = query.message.chat.id
        st = await client.get_chat_member(grp_id, userid)
        if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in Configs.ADMINS_ID):
            await query.message.delete()
            try:
                await query.message.reply_to_message.delete()
            except:
                pass
        else:
            await query.answer("That's not for you!!", show_alert=True) 

async def alert_cb(query):
    grp_id = query.message.chat.id
    i = query.data.split(":")[1]
    keyword = query.data.split(":")[2]
    reply_text, btn, alerts, fileid = await db.find_filter(grp_id, keyword)
    if alerts is not None:
        alerts = ast.literal_eval(alerts)
        alert = alerts[int(i)]
        alert = alert.replace("\\n", "\n").replace("\\t", "\t")
        await query.answer(alert, show_alert=True)
