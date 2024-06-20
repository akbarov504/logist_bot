import sqlalchemy
from telethon import TelegramClient
from configs.utils import get_client
from models.message_group import MessageGroup
from configs.database_config import Base, engine
from models.message_group_user import MessageGroupUser

class Message(Base):
    __tablename__ = "message"

    id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    message = sqlalchemy.Column(sqlalchemy.Text(), nullable=False)
    timer = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)   
    status = sqlalchemy.Column(sqlalchemy.Boolean(), default=True)
    send_count_in_day = sqlalchemy.Column(sqlalchemy.Integer())
    send_count_all = sqlalchemy.Column(sqlalchemy.BigInteger())
    phone = sqlalchemy.Column(sqlalchemy.String(length=13), nullable=False)

    is_deleted = sqlalchemy.Column(sqlalchemy.Boolean(), default=True)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime())
    created_by = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime())
    updated_by = sqlalchemy.Column(sqlalchemy.Integer())

    @staticmethod
    def create(user_id: int, message: str, timer: int, phone: str) -> int:
        message_table = Message.metadata.tables.get("message")
        ins = message_table.insert().values(user_id = user_id, message = message, timer = timer, status = False, send_count_in_day = 0, send_count_all = 0, created_by = user_id, is_deleted = False, phone = phone).returning(Message.id)
        conn = engine.connect()
        res = conn.execute(ins)
        conn.commit()
        return res.fetchone()

    @staticmethod
    async def change_status(user_id: int, message_id: int, status: bool, mess: str, phone: str) -> None:
        message_table = Message.metadata.tables.get("message")
        message_group_user_table = MessageGroupUser.metadata.tables.get("message_group_user")
        ins = message_table.update().values(status = status).where(Message.id == message_id)
        upd = message_group_user_table.update().values(message_id = message_id).where(MessageGroupUser.user_id == user_id, MessageGroupUser.message_id == None)
        conn = engine.connect()
        conn.execute(ins)
        conn.execute(upd)
        conn.commit()
        message_group_user_list = MessageGroupUser.list_user_id(user_id)
        for msg_group_user in message_group_user_list:
            if msg_group_user[2] == message_id:
                msg_group = MessageGroup.get(msg_group_user[3])
                client: TelegramClient = await get_client(phone)
                await client.connect()
                await client.send_message(msg_group[2], mess)
                await client.disconnect()

    @staticmethod
    def set_status(user_id: int, message_id: int, status: bool) -> None:
        message_table = Message.metadata.tables.get("message")
        upd = message_table.update().values(status = status).where(Message.user_id == user_id, Message.id == message_id, Message.is_deleted == False)
        conn = engine.connect()
        conn.execute(upd)
        conn.commit()

    @staticmethod
    def list() -> list:
        message_table = Message.metadata.tables.get("message")
        sel = message_table.select().where(Message.is_deleted == False)
        conn = engine.connect()
        res = conn.execute(sel)
        return res.fetchall()
    
    @staticmethod
    def list_to_lambda() -> list:
        msg_list = []
        message_table = Message.metadata.tables.get("message")
        sel = message_table.select().where(Message.is_deleted == False)
        conn = engine.connect()
        res = conn.execute(sel)
        l_m = res.fetchall()
        for l in l_m:
            msg_list.append(l[0])
        return msg_list
    
    @staticmethod
    def list_by_user_id(user_id: int) -> list:
        message_table = Message.metadata.tables.get("message")
        sel = message_table.select().where(Message.is_deleted == False, Message.user_id == user_id)
        conn = engine.connect()
        res = conn.execute(sel)
        return res.fetchall()
