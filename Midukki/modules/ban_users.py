from pyrogram import Client, filters
from Midukki.midukki import Midukki_RoboT 
from Midukki.functions.extract_user import extract_user
from Midukki.functions.extract_time import extract_time
from Midukki.functions.handlers import Ban

@Midukki_RoboT.on_message(Ban.a)
async def ban_user(_, message):
    user_id, user_first_name, _ = extract_user(message)

    try:
        await message.chat.ban_member(user_id=user_id)
    except Exception as error:
        await message.reply_text(str(error))
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "വേറെ ഒരാളും പൊടി പാറിപ്പിക്കുന്നു..! "
                f"{user_first_name}"
                " നെ വിലക്കിയിരിക്കുന്നു."
            )
        else:
            await message.reply_text(
                "വേറെ ഒരാളും പൊടി പാറിപ്പിക്കുന്നു..! "
                f"<a href='tg://user?id={user_id}'>"
                f"{user_first_name}"
                "</a>"
                " നെ വിലക്കിയിരിക്കുന്നു."
            )

@Client.on_message(Ban.b)
async def un_ban_user(_, message):
    user_id, user_first_name, _ = extract_user(message)

    try:
        await message.chat.unban_member(user_id=user_id)
    except Exception as error:
        await message.reply_text(str(error))
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "ശരി, മാറ്റിയിട്ടുണ്ട്... ഇനി "
                f"{user_first_name} ക്ക് "
                " ഗ്രൂപ്പിൽ ചേരാൻ കഴിയും!"
            )
        else:
            await message.reply_text(
                "ശരി, മാറ്റിയിട്ടുണ്ട്... ഇനി "
                f"<a href='tg://user?id={user_id}'>"
                f"{user_first_name}"
                "</a> ക്ക് "
                " ഗ്രൂപ്പിൽ ചേരാൻ കഴിയും!"
            )

@Midukki_RoboT.on_message(Ban.c)
async def temp_ban_user(_, message):
    if not len(message.command) > 1:
        return

    user_id, user_first_name, _ = extract_user(message)

    until_date_val = extract_time(message.command[1])
    if until_date_val is None:
        await message.reply_text(
            (
                "അസാധുവായ സമയ തരം വ്യക്തമാക്കി. "
                "പ്രതീക്ഷിച്ചതു m, h, or d, കിട്ടിയത്: {}"
            ).format(message.command[1][-1])
        )
        return

    try:
        await message.chat.ban_member(user_id=user_id, until_date=until_date_val)
    except Exception as error:
        await message.reply_text(str(error))
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "വേറെ ഒരാളും പൊടി പാറിപ്പിക്കുന്നു..! "
                f"{user_first_name}"
                f" banned for {message.command[1]}!"
            )
        else:
            await message.reply_text(
                "വേറെ ഒരാളും പൊടി പാറിപ്പിക്കുന്നു..! "
                f"<a href='tg://user?id={user_id}'>"
                "ലവനെ"
                "</a>"
                f" banned for {message.command[1]}!"
            )
