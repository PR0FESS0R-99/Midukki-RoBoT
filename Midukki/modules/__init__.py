import asyncio, time, shutil, psutil, os
from pyrogram import filters, enums
from Midukki.functions.media_details import humanbytes, get_size
from Midukki.functions.commands import button, markup, message               
from Midukki.functions.settings import get_settings 
from Midukki.functions.loadings import loading
from Midukki.database import db, Media
from Midukki import Configs, Index, Bots
from Midukki.midukki import Midukki_RoboT
from Midukki.scripts import Txt
from .auto_filters import index_files, get_result_file, next_page_, back_page_
from .connections import connections_callback_1, connections_callback_2, connections_callback_3, connections_callback_4, connections_callback_5
from .manual_filters import alert_cb, del_all_cancel, del_all_confirm
from .settings_configs import setting_cb

@Midukki_RoboT.on_callback_query(filters.regex("(close_data|groupcb|connectcb|disconnect|deletecb|backcb|index|get_file|nextgroup|backgroup|delallcancel|delallconfirm|alertmessage|settings)"))
async def cb_handler(client, query):

    try: user_id = query.reply_to_message.from_user.id
    except: user_id = query.from_user.id

    if query.data.startswith("index"):
        await index_files(client, query)

    if user_id == query.from_user.id:
        if query.data == "close_data":
            await query.message.delete()

        elif "groupcb" in query.data:
            await connections_callback_1(client, query)

        elif "connectcb" in query.data:
            await connections_callback_2(client, query)

        elif "disconnect" in query.data:
            await connections_callback_3(client, query)

        elif "deletecb" in query.data:
            await connections_callback_4(client, query)

        elif query.data == "backcb":
            await connections_callback_5(client, query)
       
        elif query.data.startswith("get_file"):
            await get_result_file(client, query)

        elif query.data.startswith("nextgroup"):
            await next_page_(query)

        elif query.data.startswith("backgroup"):
            await back_page_(query)

        elif query.data == "delallcancel":
            del_all_cancel(client, query)

        elif query.data == "delallconfirm":
            await del_all_confirm(client, query) 

        elif "alertmessage" in query.data:
            await alert_cb(query)

        elif query.data.startswith("settings"):
            await setting_cb(client, query)

    else:
        await query.answer("This Is not for you", show_alert=True)

@Midukki_RoboT.on_callback_query(filters.create(lambda _, __, query: query.data.startswith("maincb")))
async def callback_ui(client, query):
    cb = query.data.split("+", 1)[1]

    #====(start)===#
    if cb == "start_cb":
        btn, txt = CB.start_cb(client, query)
        if Configs.LOADING_SYMBOL == True:
            await loading(query, Configs.LOADING_A, Configs.LOADING_B, asyncio.sleep)
        try:
            await query.message.edit(
                text=txt,
                reply_markup=btn,
                parse_mode=enums.ParseMode.DEFAULT
            )
        except MessageNotModified:
            pass

    elif cb == "help_cb":
        btn, txt = CB.help_cb(client, query)
        if Configs.LOADING_SYMBOL == True:
            await loading(query, Configs.LOADING_A, Configs.LOADING_B, asyncio.sleep)
        try:
            await query.message.edit(
                text=txt,
                reply_markup=btn,
                parse_mode=enums.ParseMode.DEFAULT
            )
        except MessageNotModified:
            pass

    elif cb == "about_cb":
        btn, txt = CB.about_cb(client, query)
        if Configs.LOADING_SYMBOL == True:
            await loading(query, Configs.LOADING_A, Configs.LOADING_B, asyncio.sleep)
        try:
            await query.message.edit(
                text=txt,
                reply_markup=btn 
            )
        except MessageNotModified:
            pass
    
    ##====(help)====##

    elif cb == "stats_cb":
        btn, txt = await stats_cb(client, query)
        if Configs.LOADING_SYMBOL == True:
            await loading(query, Configs.LOADING_A, Configs.LOADING_B, asyncio.sleep)
        try:
            await query.message.edit(
                text=txt,
                reply_markup=btn 
            )
        except MessageNotModified:
            pass

    elif cb == "auto_cb":
        btn, txt = CB.auto_help(client, query)
        if Configs.LOADING_SYMBOL == True:
            await loading(query, Configs.LOADING_A, Configs.LOADING_B, asyncio.sleep)
        try:
            await query.message.edit(
                text=txt,
                reply_markup=btn 
            )
        except MessageNotModified:
            pass

    elif cb == "manual_cb":
        btn, txt = CB.manual_help(client, query)
        if Configs.LOADING_SYMBOL == True:
            await loading(query, Configs.LOADING_A, Configs.LOADING_B, asyncio.sleep)
        try:
            await query.message.edit(
                text=txt,
                reply_markup=btn 
            )
        except MessageNotModified:
            pass

    elif cb == "info_cb":
        btn, txt = CB.info_help(client, query)
        if Configs.LOADING_SYMBOL == True:
            await loading(query, Configs.LOADING_A, Configs.LOADING_B, asyncio.sleep)
        try:
            await query.message.edit(
                text=txt,
                reply_markup=btn 
            )
        except MessageNotModified:
            pass

    elif cb == "caption_cb":
        btn, txt = CB.cap_help(client, query)
        if Configs.LOADING_SYMBOL == True:
            await loading(query, Configs.LOADING_A, Configs.LOADING_B, asyncio.sleep)
        try:
            await query.message.edit(
                text=txt,
                reply_markup=btn 
            )
        except MessageNotModified:
            pass

    elif cb == "spell_cb":
        btn, txt = CB.spell_help(client, query)
        if Configs.LOADING_SYMBOL == True:
            await loading(query, Configs.LOADING_A, Configs.LOADING_B, asyncio.sleep)
        try:
            await query.message.edit(
                text=txt,
                reply_markup=btn 
            )
        except MessageNotModified:
            pass

    elif cb == "connection_cb":
        btn, txt = CB.connect_help(client, query)
        if Configs.LOADING_SYMBOL == True:
            await loading(query, Configs.LOADING_A, Configs.LOADING_B, asyncio.sleep)
        try:
            await query.message.edit(
                text=txt,
                reply_markup=btn 
            )
        except MessageNotModified:
            pass

    elif cb == "mute_cb":
        btn, txt = CB.mute_help(client, query)
        if Configs.LOADING_SYMBOL == True:
            await loading(query, Configs.LOADING_A, Configs.LOADING_B, asyncio.sleep)
        try:
            await query.message.edit(
                text=txt,
                reply_markup=btn 
            )
        except MessageNotModified:
            pass

    elif cb == "ban_cb":
        btn, txt = CB.ban_help(client, query)
        if Configs.LOADING_SYMBOL == True:
            await loading(query, Configs.LOADING_A, Configs.LOADING_B, asyncio.sleep)
        try:
            await query.message.edit(
                text=txt,
                reply_markup=btn 
            )
        except MessageNotModified:
            pass

    elif cb == "pin_cb":
        btn, txt = CB.pin_help(client, query)
        if Configs.LOADING_SYMBOL == True:
            await loading(query, Configs.LOADING_A, Configs.LOADING_B, asyncio.sleep)
        try:
            await query.message.edit(
                text=txt,
                reply_markup=btn 
            )
        except MessageNotModified:
            pass

    elif cb == "source_cb":
        btn, txt = CB.source_code(client, query)
        if Configs.LOADING_SYMBOL == True:
            await loading(query, Configs.LOADING_A, Configs.LOADING_B, asyncio.sleep)
        try:
            await query.message.edit(
                text=txt,
                reply_markup=btn
            )
        except MessageNotModified:
            pass

    elif cb == "admin_panel_cb":
        btn, txt = CB.admin_panel(client, query)
        if Configs.LOADING_SYMBOL == True:
            await loading(query, Configs.LOADING_A, Configs.LOADING_B, asyncio.sleep)
        if query.from_user.id in Configs.ADMINS_ID:
            await query.message.edit(
                text=txt,
                reply_markup=btn
            )
        else:
            await query.answer("Hey Bro or Sis 🙏 Your Not A Authorized User", show_alert=True)

class vars(object):
    start_buttons = [
        [
            button()
                (
                    "➕️ Add Me To Your Group ➕️",
                        url=f"https://t.me/{Bots.BOT_USERNAME}?startgroup=new"
                )
        ],
        [
            button()
                (
                    "Support",
                        url="https://t.me/+sv5flNs7yew1OTk1"
                ),
            button()
                (
                    "Updates",
                        url="https://t.me/Mo_Tech_YT"
                )
        ],
        [
            button()
                (
                    "Help",
                        callback_data="maincb+help_cb"
                ),
            button()
                (
                    "About",
                       callback_data="maincb+about_cb"
                )
        ]
    ]
    help_buttons = [
        [
            button()(
                "📤AutoFilter", callback_data="maincb+auto_cb"
            ),
            button()(
                "🎛️ManualFilter", callback_data="maincb+manual_cb"
            )
        ],
        [
            button()(
                "🤬Ban", callback_data="maincb+ban_cb"
            ),
            button()(
                "🤐Mute", callback_data="maincb+mute_cb"
            ),
            button()(
                "ℹ️IDs", callback_data="maincb+info_cb"
            )
        ],
        [     
            button()(
                "📌Pin", callback_data="maincb+pin_cb"
            ),
            button()(
                "🗣️Spell", callback_data="maincb+spell_cb"
            ),
            button()(
                "📝Caption", callback_data="maincb+caption_cb"
            )
        ],
        [
            button()(
                "🔗Connection", callback_data="maincb+connection_cb"
            ),
            button()(
                "📡Status", callback_data="maincb+stats_cb"
            )
        ],
        [
            button()(
               "🔐Admin Panel🔐", callback_data="maincb+admin_panel_cb"
            )
        ],
        [
            button()(
                "🚫 Close", callback_data="close_data"
            ),
            button()(
                "<= Back", callback_data="maincb+start_cb"
            )     
        ]
    ]
    about_buttons = [
        [
            button()
                (
                    "Support",
                        url="https://t.me/Mo_Tech_YT"
                ),
            button()
                (
                    "Source",
                        url="https://t.me/+sv5flNs7yew1OTk1"
                )
        ],
        [
            button()
                (
                    "Tutorial",
                        url="https://youtu.be/63K9xkKMBoo"
                ),
            button()
                (
                    "Insta",
                        url="https://www.instagram.com/mrk_yt_"
                )
        ],
        [
            button()
                (
                    "⬅️ Back To Home ➡️",
                        callback_data="maincb+start_cb"
                )
        ]
    ]

    help_emitter_btn = [
        [
            button()
                (
                    "close 🗑️",
                        callback_data="close_data"
                ),
            button()
                (
                    "back <=",
                        callback_data="maincb+help_cb"
                )
        ]
    ]

    start_emitter_btn = [
        [
            button()
                (
                    "close 🗑️",
                        callback_data="close_data"
                ),
            button()
                (
                    "back <=",
                        callback_data="maincb+start_cb"
                )
        ]
    ]

    about_emitter_btn = [
        [
            button()
                (
                    "close 🗑️",
                        callback_data="close_data"
                ),
            button()
                (
                    "back <=",
                        callback_data="maincb+about_cb"
                )
        ]
    ]


class CB:
    def start_cb(client, query):
        txt = Txt.START_TXT.format(bot=Bots.BOT_MENTION, mention=query.from_user.mention)            
        btn = markup()(vars.start_buttons)
        return btn, txt
        
    def help_cb(client, query):
        txt = Txt.HELP_TXT.format(bot=Bots.BOT_MENTION, mention=query.from_user.mention)
        btn = markup()(vars.help_buttons)
        return btn, txt

    def about_cb(client, query):
        txt = Txt.ABOUT_TXT.format(bot=Bots.BOT_MENTION, name=Bots.BOT_NAME, username=Bots.BOT_USERNAME, mention=query.from_user.mention)    
        btn = markup()(vars.start_emitter_btn)
        return btn, txt

    def auto_help(client, query):
        txt = Txt.AUTO_TXT
        btn = markup()(vars.help_emitter_btn)
        return btn, txt

    def manual_help(client, query):
        txt = Txt.MANUAL_TXT
        btn = markup()(vars.help_emitter_btn)
        return btn, txt

    def info_help(client, query):
        txt = Txt.INFO_TXT
        btn = markup()(vars.help_emitter_btn)
        return btn, txt

    def connect_help(client, query):
        txt = Txt.CONNECTION_TXT
        btn = markup()(vars.help_emitter_btn)
        return btn, txt

    def cap_help(client, query):
        txt = Txt.CAP_TXT
        btn = markup()(vars.help_emitter_btn)
        return btn, txt

    def spell_help(client, query):
        txt = Txt.SPELL_TXT
        btn = markup()(vars.help_emitter_btn)
        return btn, txt

    def mute_help(client, query):
        txt = Txt.MUTE_TXT
        btn = markup()(vars.help_emitter_btn)
        return btn, txt

    def ban_help(client, query):
        txt = Txt.BAN_TXT
        btn = markup()(vars.help_emitter_btn)
        return btn, txt

    def pin_help(client, query):
        txt = Txt.PIN_TXT
        btn = markup()(vars.help_emitter_btn)
        return btn, txt
   
    def admin_panel(client, query):
        txt = Txt.ADMIN_PANEL
        btn = markup()(vars.help_emitter_btn)
        return btn, txt

    def source_code(client, query):
        txt = Txt.SOURCE_TXT
        btn = markup()(vars.about_emitter_btn)
        return btn, txt


async def stats_cb(client, query):
    # Server
    currentTime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - Bots.BOT_START_TIME))                    
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    # Database
    try:
        file = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        mons = await db.get_db_size()
        dbfree = 536870912 - mons
        monsize = get_size(mons)
        freedb = get_size(dbfree)
        totdb = get_size(536870912)
    except:
        file, users, chats, monsize, freedb = "Sheriyenna 🫡"
    txt = Txt.STATUS_TXT.format(bot=Bots.BOT_MENTION, a=currentTime, b=cpu_usage, c=ram_usage,
        d=total, e=used, f=disk_usage, g=free, h=file, i=users, j=chats, k=monsize, l=freedb, m=totdb
    )
    btn = markup()(vars.help_emitter_btn)
    return btn, txt
