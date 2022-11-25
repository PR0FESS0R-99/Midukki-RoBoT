from logging import getLogger, ERROR
from pyrogram import enums
from Midukki.midukki import Midukki_RoboT
from Midukki.functions.handlers import Connection
from Midukki.functions.commands import button, markup, message
from Midukki.database import db
from Midukki import Configs

logger = getLogger(__name__)
logger.setLevel(ERROR)

@Midukki_RoboT.on_message(Connection.a)
async def add_new_connection(client: Midukki_RoboT, message: message()):

    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        try:
            cmd, group_id = message.text.split(" ", 1)
        except:
            await message.reply_text(
                "<b>Enter in correct format!</b>\n\n"
                "<code>/connect groupid</code>\n\n"
                "<i>Get your Group id by adding this bot to your group and use  <code>/id</code></i>",
                quote=True
            )
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        group_id = message.chat.id

    try:
        st = await client.get_chat_member(group_id, userid)
        if (
                st.status != enums.ChatMemberStatus.ADMINISTRATOR
                and st.status != enums.ChatMemberStatus.OWNER
                and userid not in Configs.ADMINS_ID
        ):
            await message.reply_text("You should be an admin in Given group!", quote=True)
            return
    except Exception as e:
        logger.exception(e)
        await message.reply_text(
            "Invalid Group ID!\n\nIf correct, Make sure I'm present in your group!!",
            quote=True,
        )

        return
    try:
        st = await client.get_chat_member(group_id, "me")
        if st.status == enums.ChatMemberStatus.ADMINISTRATOR:
            ttl = await client.get_chat(group_id)
            title = ttl.title

            addcon = await db.add_connection(str(group_id), str(userid))
            if addcon:
                await message.reply_text(
                    f"Successfully connected to **{title}**\nNow manage your group from my pm !",
                    quote=True,
                    parse_mode=enums.ParseMode.MARKDOWN
                )
                if chat_type in ["group", "supergroup"]:
                    await client.send_message(
                        userid,
                        f"Connected to **{title}** !",
                        parse_mode=enums.ParseMode.MARKDOWN
                    )
            else:
                await message.reply_text(
                    "You're already connected to this chat!",
                    quote=True
                )
        else:
            await message.reply_text("Add me as an admin in group", quote=True)
    except Exception as e:
        logger.exception(e)
        await message.reply_text('Some error occurred! Try again later.', quote=True)
        return

@Midukki_RoboT.on_message(Connection.b)
async def delete_old_connection(client, Midukki_RoboT, message: message()):

    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        await message.reply_text("Run /connections to view or disconnect from groups!", quote=True)

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        group_id = message.chat.id

        st = await client.get_chat_member(group_id, userid)
        if (
                st.status != enums.ChatMemberStatus.ADMINISTRATOR
                and st.status != enums.ChatMemberStatus.OWNER
                and str(userid) not in Configs.ADMINS_ID
        ):
            return

        delcon = await db.delete_connection(str(userid), str(group_id))
        if delcon:
            await message.reply_text("Successfully disconnected from this chat", quote=True)
        else:
            await message.reply_text("This chat isn't connected to me!\nDo /connect to connect.", quote=True)

@Midukki_RoboT.on_message(Connection.c)
async def all_connections_command(client: Midukki_RoboT, message: message()):
    userid = message.from_user.id

    groupids = await db.all_connections(str(userid))
    if groupids is None:
        await message.reply_text("There are no active connections!! Connect to some groups first.", quote=True)
        return

    keyboard = []
    for groupid in groupids:
        try:
            ttl = await client.get_chat(int(groupid))
            title = ttl.title
            active = await db.if_active(str(userid), str(groupid))
            act = " - ACTIVE" if active else ""
            keyboard1 = [
             button()(text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}")
            ]
            keyboard.append(keyboard1)
        except:
            pass
    if keyboard:
        await message.reply_text(
            "Your connected group details ;\n\n",
            reply_markup=markup()(keyboard),
            quote=True
        )
    else:
        await message.reply_text(
            "There are no active connections!! Connect to some groups first.",
            quote=True
        )

async def connections_callback_1(client, query):
    await query.answer()

    group_id = query.data.split(":")[1]

    act = query.data.split(":")[2]
    hr = await client.get_chat(int(group_id))
    title = hr.title
    user_id = query.from_user.id

    if act == "":
        stat = "CONNECT"
        cb = "connectcb"
    else:
        stat = "DISCONNECT"
        cb = "disconnect"

    kb = [
        [
            button()
                (
                    f"{stat}",
                        callback_data=f"{cb}:{group_id}"
                ),
            button()
                (
                    "DELETE",
                        callback_data=f"deletecb:{group_id}"
                )
        ],
        [
            button()
                (
                    "BACK",
                        callback_data="backcb")
        ]
    ]
    keyboard = markup()(kb)

    await query.message.edit_text(
        f"Group Name : **{title}**\nGroup ID : `{group_id}`",
        reply_markup=keyboard,
        parse_mode=enums.ParseMode.MARKDOWN
    )
    return await query.answer('Piracy Is Crime')

async def connections_callback_2(client, query):
    await query.answer()

    group_id = query.data.split(":")[1]

    hr = await client.get_chat(int(group_id))

    title = hr.title

    user_id = query.from_user.id

    mkact = await db.make_active(str(user_id), str(group_id))

    if mkact:
        await query.message.edit_text(
            f"Connected to **{title}**",
            parse_mode=enums.ParseMode.MARKDOWN
        )
    else:
        await query.message.edit_text('Some error occurred!!', parse_mode=enums.ParseMode.MARKDOWN)
    return await query.answer('Piracy Is Crime')


async def connections_callback_3(client, query):    
    await query.answer()

    group_id = query.data.split(":")[1]

    hr = await client.get_chat(int(group_id))

    title = hr.title
    user_id = query.from_user.id

    mkinact = await db.make_inactive(str(user_id))

    if mkinact:
        await query.message.edit_text(
            f"Disconnected from **{title}**",
            parse_mode=enums.ParseMode.MARKDOWN
        )
    else:
        await query.message.edit_text(
            f"Some error occurred!!",
            parse_mode=enums.ParseMode.MARKDOWN
        )
    return await query.answer('Piracy Is Crime')


async def connections_callback_4(client, query):    

    await query.answer()

    user_id = query.from_user.id
    group_id = query.data.split(":")[1]

    delcon = await db.delete_connection(str(user_id), str(group_id))

    if delcon:
        await query.message.edit_text(
            "Successfully deleted connection"
        )
    else:
        await query.message.edit_text(
            f"Some error occurred!!",
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return await query.answer('Piracy Is Crime')

async def connections_callback_5(client, query):    
    await query.answer()

    userid = query.from_user.id

    groupids = await db.all_connections(str(userid))
    if groupids is None:
        await query.message.edit_text(
            "There are no active connections!! Connect to some groups first.",
        )
        return await query.answer('Piracy Is Crime')
    buttons = []
    for groupid in groupids:
        try:
            ttl = await client.get_chat(int(groupid))
            title = ttl.title
            active = await db.if_active(str(userid), str(groupid))
            act = " - ACTIVE" if active else ""
            kb = [
                [
                    button()
                        (
                            text=f"{title}{act}",
                                callback_data=f"groupcb:{groupid}:{act}"
                        )
                ]
            ]
            buttons.append(kb)              
        except:
            pass
    if buttons:
        await query.message.edit_text(
            "Your connected group details ;\n\n",
            reply_markup=markup()(buttons)
        )
