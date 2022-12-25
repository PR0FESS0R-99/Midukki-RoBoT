import re
from struct import pack
from datetime import date
from pyrogram import enums
from pymongo import MongoClient
from logging import getLogger, ERROR
from pymongo.errors import DuplicateKeyError
from marshmallow.exceptions import ValidationError
from motor.motor_asyncio import AsyncIOMotorClient
from Midukki import Configs, Customize
from Midukki.functions.unpack_file_id import unpack_new_file_id
from umongo import Instance, Document, fields

logger = getLogger(__name__)
logger.setLevel(ERROR)

class Database:
    def __init__(self):
        self.pymongo_client = MongoClient(Configs.DATABASE_URL)
        self.motor_client = AsyncIOMotorClient(Configs.DATABASE_URL)
        self.db = self.motor_client[Configs.DATABASE_NAME]
        self.pydb = self.pymongo_client[Configs.DATABASE_NAME]
        self.connections = self.pydb.connections
        self.filters = self.pymongo_client[Configs.DATABASE_NAME]
        self.users = self.db.users
        self.groups = self.db.groups

    def new_user(self, id, name):
        return dict(id=id, name=name, join_date=date.today().isoformat())

    async def add_user(self, name, id):
        user = self.new_user(name, id)
        await self.users.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.users.find_one({'id':int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.users.count_documents({})
        return count

    async def get_all_users(self):
        return self.users.find({})

    async def delete_user(self, user_id):
        await self.users.delete_many({'id': int(user_id)})

    def new_group(self, id, title):
        return dict(id=id, title=title, chat_status=dict(is_disabled=False, reason=""))
        
    async def add_chat(self, chat, title):
        chat = self.new_group(chat, title)
        await self.groups.insert_one(chat)
    
    async def get_chat(self, chat):
        chat = await self.groups.find_one({'id':int(chat)})
        if not chat:
            return False
        else:
            return chat.get('chat_status')
    
    async def re_enable_chat(self, id):
        chat_status=dict(is_disabled=False, reason="")
        await self.groups.update_one({'id': int(id)}, {'$set': {'chat_status': chat_status}})
    
    async def disable_chat(self, chat, reason="No Reason"):
        chat_status=dict(is_disabled=True, reason=reason)
        await self.groups.update_one({'id': int(chat)}, {'$set': {'chat_status': chat_status}})
   
    async def total_chat_count(self):
        count = await self.groups.count_documents({})
        return count    

    async def get_all_chats(self):
        return self.groups.find({})

    async def get_db_size(self):
        return (await self.db.command("dbstats"))['dataSize']

    async def update_settings(self, id, settings):
        await self.groups.update_one({'id': int(id)}, {'$set': {'settings': settings}})
           
    async def get_settings(self, id):
        default = {
            'buttons': True,
            'autofilter': True,
            'file_mode': False,
            'poster': True,
            'spell_check': True,
            'welcome': True,
            'protect_files': False,
            'force_sub': Configs.AUTH_CHANNEL,
            'template': Customize.IMDB_TEMPLATE,
            'caption': Customize.FILE_CAPTION,
            'spell_caption': Customize.SPELLCHECK_CAPTION,
            'new_user': Customize.WELCOME_CAPTION,
            'auto_del': Customize.AUTO_DEL_TIME  
        }
        chat = await self.groups.find_one({'id':int(id)})
        if chat:
            return chat.get('settings', default)
        return default

    async def delete_chat(self, id):
        await self.groups.delete_many({'id': id})

    # : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : #

    async def add_filter(self, grp_id, text, reply_text, btn, file, alert):
        mycol = self.filters[str(grp_id)]
        # mycol.create_index([('text', 'text')])

        data = {
            'text':str(text),
            'reply':str(reply_text),
            'btn':str(btn),
            'file':str(file),
            'alert':str(alert)
        }

        try:
            mycol.update_one({'text': str(text)},  {"$set": data}, upsert=True)
        except:
            logger.exception('Some error occured!', exc_info=True)
                  
    async def find_filter(self, group_id, name):
        mycol = self.filters[str(group_id)]
    
        query = mycol.find( {"text":name})
        # query = mycol.find( { "$text": {"$search": name}})
        try:
            for file in query:
                reply_text = file['reply']
                btn = file['btn']
                fileid = file['file']
                try:
                    alert = file['alert']
                except:
                    alert = None
            return reply_text, btn, alert, fileid
        except:
            return None, None, None, None

    async def get_filters(self, group_id):
        mycol = self.filters[str(group_id)]

        texts = []
        query = mycol.find()
        try:
            for file in query:
                text = file['text']
                texts.append(text)
        except:
            pass
        return texts

    async def delete_filter(self, message, text, group_id):
        mycol = self.filters[str(group_id)]
    
        myquery = {'text':text }
        query = mycol.count_documents(myquery)
        if query == 1:
            mycol.delete_one(myquery)
            await message.reply_text(
                f"'`{text}`'  deleted. I'll not respond to that filter anymore.",
                quote=True,
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await message.reply_text("Couldn't find that filter!", quote=True)


    async def del_all(self, message, group_id, title):
        if str(group_id) not in self.filters.list_collection_names():
            await message.edit_text(f"Nothing to remove in {title}!")
            return

        mycol = self.filters[str(group_id)]
        try:
            mycol.drop()
            await message.edit_text(f"All filters from {title} has been removed")
        except:
            await message.edit_text("Couldn't remove all filters from group!")
            return

    async def count_filters(self, group_id):
        mycol = self.filters[str(group_id)]

        count = mycol.count()
        return False if count == 0 else count


    async def filter_stats(self):
        collections = self.filters.list_collection_names()

        if "CONNECTION" in collections:
            collections.remove("CONNECTION")

        totalcount = 0
        for collection in collections:
            mycol = self.filters[collection]
            count = mycol.count()
            totalcount += count

        totalcollections = len(collections)
        return totalcollections, totalcount

    # : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : #

    async def add_connection(self, group_id, user_id):
        query = self.connections.find_one(
            { "_id": user_id },
            { "_id": 0, "active_group": 0 }
        )
        if query is not None:
            group_ids = [x["group_id"] for x in query["group_details"]]
            if group_id in group_ids:
                return False

        group_details = {
            "group_id" : group_id
        }

        data = {
            '_id': user_id,
            'group_details' : [group_details],
            'active_group' : group_id,
        }

        if self.connections.count_documents( {"_id": user_id} ) == 0:
            try:
                self.connections.insert_one(data)
                return True
            except:
                logger.exception('Some error occurred!', exc_info=True)

        else:
            try:
                self.connections.update_one(
                    {'_id': user_id},
                        {
                        "$push": {"group_details": group_details},
                        "$set": {"active_group" : group_id}
                    }
                )
                return True
            except:
                logger.exception('Some error occurred!', exc_info=True)

    async def active_connection(self, user_id):

        query = self.connections.find_one(
            { "_id": user_id },
            { "_id": 0, "group_details": 0 }
        )
        if not query:
            return None

        group_id = query['active_group']
        return int(group_id) if group_id != None else None

    async def all_connections(self, user_id):
        query = self.connections.find_one(
            { "_id": user_id },
            { "_id": 0, "active_group": 0 }
        )
        if query is not None:
            return [x["group_id"] for x in query["group_details"]]
        else:
            return None

    async def if_active(self, user_id, group_id):
        query = self.connections.find_one(
            { "_id": user_id },
            { "_id": 0, "group_details": 0 }
        )
        return query is not None and query['active_group'] == group_id

    async def make_active(self, user_id, group_id):
        update = self.connections.update_one(
            {'_id': user_id},
            {"$set": {"active_group" : group_id}}
        )
        return update.modified_count != 0

    async def make_inactive(self, user_id):
        update = self.connections.update_one(
            {'_id': user_id},
            {"$set": {"active_group" : None}}
        )
        return update.modified_count != 0

    async def delete_connection(self, user_id, group_id):

        try:
            update = self.connections.update_one(
                {"_id": user_id},
                {"$pull" : { "group_details" : {"group_id":group_id} } }
            )
            if update.modified_count == 0:
                return False
            query = self.connections.find_one(
                { "_id": user_id },
                { "_id": 0 }
            )
            if len(query["group_details"]) >= 1:
                if query['active_group'] == group_id:
                    prvs_group_id = query["group_details"][len(query["group_details"]) - 1]["group_id"]

                    self.connections.update_one(
                        {'_id': user_id},
                        {"$set": {"active_group" : prvs_group_id}}
                    )
            else:
                self.connections.update_one(
                    {'_id': user_id},
                    {"$set": {"active_group" : None}}
                )
            return True
        except Exception as e:
            logger.exception(f'Some error occurred! {e}', exc_info=True)
            return False

client = AsyncIOMotorClient(Configs.DATABASE_URL)
db = client[Configs.DATABASE_NAME]
instance = Instance.from_db(db)

@instance.register
class Media(Document):
    file_id = fields.StrField(attribute='_id')
    file_ref = fields.StrField(allow_none=True)
    file_name = fields.StrField(required=True)
    file_size = fields.IntField(required=True)
    file_type = fields.StrField(allow_none=True)
    mime_type = fields.StrField(allow_none=True)
    caption = fields.StrField(allow_none=True)

    class Meta:
        indexes = ('$file_name', )
        collection_name = Configs.COLLECTION_NAME

async def save_file(media):
    """Save file in database"""

    # TODO: Find better way to get same file_id for same media to avoid duplicates
    file_id, file_ref = unpack_new_file_id(media.file_id)
    file_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
    try:
        file = Media(
            file_id=file_id,
            file_ref=file_ref,
            file_name=file_name,
            file_size=media.file_size,
            file_type=media.file_type,
            mime_type=media.mime_type,
            caption=media.caption.html if media.caption else None,
        )
    except ValidationError:
        logger.exception('Error occurred while saving file in database')
        return False, 2
    else:
        try:
            await file.commit()
        except DuplicateKeyError:      
            logger.warning(
                f'{getattr(media, "file_name", "NO_FILE")} is already saved in database'
            )

            return False, 0
        else:
            logger.info(f'{getattr(media, "file_name", "NO_FILE")} is saved to database')
            return True, 1

async def get_search_results(query, file_type=None, max_results=1000, offset=0, filter=False):
    """For given query return (results, next_offset)"""

    query = query.strip()
    #if filter:
        #better ?
        #query = query.replace(' ', r'(\s|\.|\+|\-|_)')
        #raw_pattern = r'(\s|_|\-|\.|\+)' + query + r'(\s|_|\-|\.|\+)'
    if not query:
        raw_pattern = '.'
    elif ' ' not in query:
        raw_pattern = r'(\b|[\.\+\-_])' + query + r'(\b|[\.\+\-_])'
    else:
        raw_pattern = query.replace(' ', r'.*[\s\.\+\-_]')
    
    try:
        regex = re.compile(raw_pattern, flags=re.IGNORECASE)
    except:
        return []

    if Configs.USE_CAPTION_FILTER:
        filter = {'$or': [{'file_name': regex}, {'caption': regex}]}
    else:
        filter = {'file_name': regex}

    if file_type:
        filter['file_type'] = file_type

    total_results = await Media.count_documents(filter)
    next_offset = offset + max_results

    if next_offset > total_results:
        next_offset = ''

    cursor = Media.find(filter)
    # Sort by recent
    cursor.sort('$natural', -1)
    # Slice files according to offset and max results
    cursor.skip(offset).limit(max_results)
    # Get list of files
    files = await cursor.to_list(length=max_results)

    return files, next_offset, total_results

async def get_file_details(query):
    filter = {'file_id': query}
    cursor = Media.find(filter)
    filedetails = await cursor.to_list(length=1)
    return filedetails
