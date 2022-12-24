from pyrogram import enums 
from Midukki.midukki import Midukki_RoboT
from Midukki.functions.commands import button, markup, message
from Midukki.functions.settings import get_settings, save_group_settings, setting_command, reload_command          
from Midukki.database import db
from Midukki import Configs

@Midukki_RoboT.on_message(reload_command)
async def reloaddbchat(client: Midukki_RoboT, message):
    userid = message.from_user.id if message.from_user else None

    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    
    if message.chat.type == enums.ChatType.PRIVATE:
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

    elif message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (st.status != enums.ChatMemberStatus.OWNER and str(userid) not in Configs.ADMINS_ID ):
        return

    await db.delete_chat(int(grp_id))
    await message.reply(f"Successfully reloaded Database")

@Midukki_RoboT.on_message(setting_command)
async def settings(client: Midukki_RoboT, message):
    userid = message.from_user.id if message.from_user else None

    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    
    if message.chat.type == enums.ChatType.PRIVATE:
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

    elif message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (st.status != enums.ChatMemberStatus.ADMINISTRATOR and st.status != enums.ChatMemberStatus.OWNER and str(userid) not in Configs.ADMINS_ID ):
        return

    settings = await get_settings(grp_id)
    if settings is not None:
        keyboard = await settings_keyboard(settings, grp_id)
        await message.reply_text(text=f"<b>Change Your Settings for {title}</b>", reply_markup=markup()(keyboard), disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML, reply_to_message_id=message.id)                     
        
async def setting_cb(client: Midukki_RoboT, query):
    ident, set_type, status, grp_id = query.data.split("#")
    grpid = await db.active_connection(str(query.from_user.id))

    if str(grp_id) != str(grpid):
        await query.message.edit("Your Active Connection Has Been Changed. Go To /settings.")
        return await query.answer('Piracy Is Crime')

    if status == "True":
        await save_group_settings(grpid, set_type, False)
    else:
        await save_group_settings(grpid, set_type, True)

    settings = await get_settings(grpid)
    if settings is not None:
        keyboard = await settings_keyboard(settings, grpid)
        await query.message.edit_reply_markup(reply_markup=markup()(keyboard))

async def settings_keyboard(settings, grp_id):
    buttons = [
        [           
            button()
                (
                    'Filter Button',
                        callback_data=f'settings#buttons#{settings["buttons"]}#{grp_id}'
                ),             
            button()
                (
                    'Single' if settings["buttons"] else 'Double',
                        callback_data=f'settings#buttons#{settings["buttons"]}#{grp_id}'
                )              
        ],
        [  
            button()
                (
                    'AutoFilter ',
                        callback_data=f'settings#autofilter#{settings["autofilter"]}#{grp_id}'
                ),             
            button()
                (
                    '✅ Yes' if settings["autofilter"] else '❌ No',
                        callback_data=f'settings#autofilter#{settings["autofilter"]}#{grp_id}'
                )              
        ],
        [ 
            button()
                (
                    'Spell Check',                    
                        callback_data=f'settings#spell_check#{settings["spell_check"]}#{grp_id}'
                ),             
            button()
                (
                    '✅ Yes' if settings["spell_check"] else '❌ No',
                        callback_data=f'settings#spell_check#{settings["spell_check"]}#{grp_id}'
                )              
        ]
    ]
    return buttons
