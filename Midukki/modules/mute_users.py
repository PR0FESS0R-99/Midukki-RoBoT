from Midukki.midukki import Midukki_RoboT
from Midukki.functions.extract_user import extract_user
from Midukki.functions.extract_time import extract_time
from Midukki.functions.handlers import Mute

@Midukki_RoboT.on_message(Mute.a)
async def mute_user(_, message):
    user_id, user_first_name, _ = extract_user(message)

    try:
        await message.chat.restrict_member(
            user_id=user_id, permissions=ChatPermissions()
        )
    except Exception as error:
        await message.reply_text(str(error))
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "👍🏻 " f"{user_first_name}" " I banned him! 🤐"
            )
        else:
            await message.reply_text(
                "👍🏻 "
                f"<a href='tg://user?id={user_id}'>"
                "Bloody Guy"
                "</a>"
                "I banned him! 🤐"
            )

@Midukki_RoboT.on_message(Mute.b)
async def un_ban_user(_, message):
    user_id, user_first_name, _ = extract_user(message)

    try:
        await message.chat.unban_member(user_id=user_id)
    except Exception as error:
        await message.reply_text(str(error))
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "Ok, I throw him to out"
                f"{user_first_name} "
            )
        else:
            await message.reply_text(
                "Ok, I throw him to out"
                f"<a href='tg://user?id={user_id}'>"
                f"{user_first_name}"
                "</a>!"
            )

@Midukki_RoboT.on_message(Mute.c)
async def temp_mute_user(_, message):
    if not len(message.command) > 1:
        return

    user_id, user_first_name, _ = extract_user(message)

    until_date_val = extract_time(message.command[1])
    if until_date_val is None:
        await message.reply_text(
            (
                "Invalid time type specified. "
                "Expected m, h, or d, Got it: {}"
            ).format(message.command[1][-1])
        )
        return

    try:
        await message.chat.restrict_member(
            user_id=user_id, permissions=ChatPermissions(), until_date=until_date_val
        )
    except Exception as error:
        await message.reply_text(str(error))
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "Be quiet for a while! 😠"
                f"{user_first_name}"
                f" muted for {message.command[1]}!"
            )
        else:
            await message.reply_text(
                "Be quiet for a while! 😠"
                f"<a href='tg://user?id={user_id}'>"
                "Of lavender"
                "</a>"
                " Mouth "
                f" muted for {message.command[1]}!"
            )
