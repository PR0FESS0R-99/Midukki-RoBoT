from pyrogram import filters
from .commands import command
from Midukki.midukki import Midukki_RoboT
from Midukki.functions.cust_p_filters import admin_fliter
from Midukki import Configs

class Command(object):
    a = command(["start"]) & (filters.private | filters.group)                                                    
    b = command(["help"]) & (filters.private | filters.group)
    c = command(["about"]) & (filters.private | filters.group)
    d = command(["donate"]) & (filters.private | filters.group)

class Manual(object):
    a = command(["add", "filter"]) & (filters.private | filters.group)                                                       
    b = command(["filters", "all_filters"]) & (filters.private | filters.group)
    c = command(["del", "del_filter"]) & (filters.private | filters.group)
    d = command(["delall", "del_all", "delall_filter"]) & (filters.private | filters.group)

class Connection(object):
    a = command(["connect"]) & (filters.private | filters.group)                                                       
    b = command(["disconnect"]) & (filters.private | filters.group)
    c = command(["connectios"]) & (filters.private | filters.group)

class AutoFilter(object):
    a = command(["autofilter"]) & (filters.private | filters.group)
    b = command(["set_temp"]) & (filters.private | filters.group)
    c = command(["del_temp"]) & (filters.private | filters.group)
    d = command(["set_cap"]) & (filters.private | filters.group)
    e = command(["del_cap"]) & (filters.private | filters.group)
    f = command(["set_spell"]) & (filters.private | filters.group)
    g = command(["del_spell"]) & (filters.private | filters.group)
    h = command(["set_autodelete"]) & (filters.private | filters.group)               

class Ban(object):
    a = command(["ban"]) & admin_fliter & filters.group                                                     
    b = command(["unban"]) & admin_fliter & filters.group
    c = command(["tban"]) & admin_fliter & filters.group

class Mute(object):
    a = command(["mute"]) & admin_fliter & filters.group                                                      
    b = command(["unmute"]) & admin_fliter & filters.group
    c = command(["tmute"]) & admin_fliter & filters.group

class Info_Id(object):
    a = command(["id"]) & (filters.private | filters.group)
    b = command(["info"]) & (filters.private | filters.group)

class Pin(object):
    a = command(["pin"]) & admin_fliter & filters.group
    b = command(["unpin"]) & admin_fliter & filters.group
    
class Admins(object):
    a = command(["channel"]) & filters.user(Configs.ADMINS_ID) & filters.private
    b = command(["total"]) & filters.user(Configs.ADMINS_ID) & filters.private
    c = command(["delfile"]) & filters.user(Configs.ADMINS_ID) & filters.private
    d = command(["delallfile"]) & filters.user(Configs.ADMINS_ID) & filters.private
    e = command(["skip"]) & filters.user(Configs.ADMINS_ID) & filters.private
    f = command(["logs"]) & filters.user(Configs.ADMINS_ID) & filters.private
    g = command(["broadcast"]) & filters.user(Configs.ADMINS_ID) & filters.private
