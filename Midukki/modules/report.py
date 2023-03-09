#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @VysakhTG

from Midukki.midukki import Midukki_RoboT
from Midukki.functions.handlers import Reports
from pyrogram import enums

@Midukki_RoboT.on_message(Reports.a)
async def notify_admin(bot, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    administrators = []
    chat_member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    if (
            chat_member.status == enums.ChatMemberStatus.ADMINISTRATOR
            or chat_member.status == enums.ChatMemberStatus.OWNER
    ):
        return
    async for m in bot.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        administrators.append(m)
    full_name = message.from_user.first_name + " " + message.from_user.last_name if message.from_user.last_name else message.from_user.first_name
    await message.reply_text("`Report sent !")
    for admin in administrators:
        try:
            if admin.user.id != message.from_user.id:
                await bot.send_message(
                    chat_id=admin.user.id, 
                    text=f"**⚠️ ATTENTION!**\n{full_name} [{user_id}] has required an admin action in the group: **{message.chat.title}**\n\n[👉🏻 Go to message]({message.link})",
                    disable_web_page_preview=True
                )
        except:
            pass
