START_TXT = """
Hello 👋 {mention} 

I'm <b>{bot}</b> ✨ an advanced telegram Group management

I'm here to help you manage your groups! Hit /help to find out more about how to use me to my full potential..!

Join <b><a href=http://t.me/Mo_Tech_YT>my news channel</a></b> to get information on all the latest updates
"""

HELP_TXT = """
👋 <b>Hello {mention}!</b>

I Can Guide You Through All Of <b>{bot}</b>'s Cool Features And How To Properly Use Them. Use The Buttons Below To Navigate Through All Of The Modules          

📚 <u><b>HelpFull Commands</b></u>:

- /start : Starts me! You've probably already used this!.
- /help : Sends this message; I'll tell you more about models!
- /about : Sends this message; I'll tell you more about myself!
- /donate : Gives you info on how to support me and my creator!

<b>All commands can be used with the following: [ / ]</b>
"""

ABOUT_TXT = """
[{name}](t.me/{username}) Was created on September 4, 2022
We are currently developing this bot, using only the Pyrogram library.

➾ Developers : Muhammed
➾ Language : Python3
➾ Framework : Pyrogram
➾ Database : Mongo db
"""

DONATE_TXT = """
If you like this project of mine, you can donate by clicking on the given link

Dev : [Muhammed](t.me/Pr0fess0r_99)
Paytm : [Click Here](https://p.paytm.me/xCTH/7yzmtgie)
  or UPI `motech8129@okaxis`
"""

STATUS_TXT = """
**--{bot}'s STATUS--**

📡 __--Server Status--__
◉ Uptime: `{a}`
◉ CPU Usage: `{b}%`
◉ RAM Usage: `{c}%`
◉ Total Disk Space: `{d}`
◉ Used Space: `{e} ({f}%)`
◉ Free Space: `{g}`

🗃️ __--Database Status--__
◉ Tota Files: `{h}`
◉ Tota Users: `{i}`
◉ Tota Chats: `{j}`
◉ Used Storage: `{k}` 
◉ Free Storage: `{l}`
◉ Total Storage: `{m}` 
"""

AUTO_TXT = """
**--MODULE OF AUTOFILTER--**

● I Can Provide Files In Your Group, It Very Easy Way Just Add Me Ro Your Group And Make Me Admin In Your Group, Thats All.. I Will Provide Files From Your Group 
      
🔋 **--Usage & Commands--** :

◉ /autofilter : use to turn on & off
◉ /set_temp : set new result temp
◉ /del_temp : del seted result temp
◉ /settings : use to modify autofilter settings

🔋 **--Supporting Vars--** :

 • `{mention}` : user profile link
 • `{query}` : request text
 • `{group_name}` : group name
"""

MANUAL_TXT = """
**--MODULE OF MANUALFILTER--**

● Filter Is The Feature Were Users Can Set Automated Replies For A Particular Keyword And Bot Will Respond Whenever A Keyword Is Found The Message

🔋 **--Note--** :

1. This bot should have admin privillage.
2. only admins can add filters in a chat.
3. alert buttons have a limit of 64 characters.

🔋 **--Commands and Usage--** :

◉ /add : add a filter in chat
◉ /filters : list all the filters of a chat
◉ /del : delete a specific filter in chat
◉ /delall : delete the whole filters in a chat (chat owner only)
"""

CONNECTION_TXT = """
**--MODULE OF CONNECTIONS**--

● Used to connect bot to PM for managing filters 
● it helps to avoid spamming in groups.

🔋 **--NOTE--** :

1. Only admins an add a connection.
2. Send <code>/connect</code> for connecting me to ur PM

🔋 **--Commands and Usage--** :

◉ /connect : connect a particular chat to your PM
◉ /disconnect : disconnect from a chat
◉ /connections : list all your connections
"""

INFO_TXT = """
**--MODULE OF INFO--**

● Hese are the extra features of this bot

🔋 **--Commands and Usage--** :

◉ /id : get id of a specifed user.
◉ /info : get information about a user.
"""

SPELL_TXT = """
**--MODULE OF SPELLCHECK--**

● Everything Related To The Spell Check Module When No AutoFilter Result Are Found 

🔋 **--Commands & Usage--** :

◉ /set_spell : Set A New SpellCheck Text
◉ /del_spell : restart Spell Check Message

🔋 **--Supporting Vars--** :

 • `{mention}` : user profile link
 • `{query}` : request text 
 • `{title}` : get chat title

> Eg:- /setspell Check Your Spelling {query}
"""

CAP_TXT = """
**--MODULE OF CUSTOM CAPTION--**

● Use This Feature To Add A Custom Caption To File

🔋 **--Commands & Usage--** :

◉ /set_cap : set new file caption 
◉ /del_cap : restart file caption

🔋 **--Supporting Vars--** :

 • {mention} : user profile link
 • {file_name} : file name
 • {size} : file size 
 • {caption} : get original caption
"""

MUTE_TXT = """
**--MODULE OF MUTE--** 🤐

● some people need to be publicly muted: spammers, annkyances, or just trolls...! this module allows you to do that easily by exposing same commo actions, so everyone will see..!

🔋 **--Commands and Usage**-- :

◉ /mute : Mute a user
◉ /unmute : Unmute a user
◉ /tmute : Temporarily mute a user. Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days
"""

BAN_TXT = """
**--MODULE OF BAN--** 🚫

● some people need to be publicly banned: spammers, annkyances, or just trolls...! this module allows you to do that easily by exposing same commo actions, so everyone will see..!

🔋 **--Commands and Usage**-- :

◉ /ban : ban a user 
◉ /unban : unban the user
◉ /tban : Temporarily ban a user. Example time values: 30s = 30 seconds, 4m = 4 minutes, 3h = 3 hours
"""

PIN_TXT = """
**--MODULE OF PIN--** 📌

● all the pin related commands can be found here; keep your chat up to date on the latest news with a simple pinned message!

🔋 **--Commands and Usage**-- :

◉ /pin : Pin the message you replied to message to send a notification to group members
◉ /unpin : Unpin the current pinned message. if used as a reply, unpins the replied to message
"""

ADMIN_PANEL = """
📤 **Admin Only**

- /channel : total channels
- /total : total files
- /delfile : del single files
- /delallfile : del all files
- /skip : skip index file
- /logs : bot logs
- /broadcast : broadcast message
"""

FILE_CAPTION_TXT = """{file_name}"""

SPELLCHECK_TXT = """Hey Mr 
Check Your Spelling 
"""

IMDB_TEMPLATE_TXT = """
🙋‍♂️ Hey {mention} Your Requested {query} is ready 👍
"""

WELCOME_TXT = """
Hai {mention}

Welcome To {chat} ❣️
"""

SEND_LOGS_A = """
#BOT_STARTED"""

class Txt(object):
    START_TXT = START_TXT
    HELP_TXT = HELP_TXT
    ABOUT_TXT = ABOUT_TXT
    STATUS_TXT = STATUS_TXT
    AUTO_TXT = AUTO_TXT
    MANUAL_TXT = MANUAL_TXT
    INFO_TXT = INFO_TXT
    CONNECTION_TXT = CONNECTION_TXT
    CAP_TXT = CAP_TXT
    SPELL_TXT = SPELL_TXT
    MUTE_TXT = MUTE_TXT
    BAN_TXT = BAN_TXT
    PIN_TXT = PIN_TXT
    ADMIN_PANEL = ADMIN_PANEL
