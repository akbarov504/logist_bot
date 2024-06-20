import sqlalchemy
from configs.database_config import Base, engine

class MessageGroup(Base):
    __tablename__ = "message_group"

    id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)

    name = sqlalchemy.Column(sqlalchemy.Text(), nullable=False)
    link = sqlalchemy.Column(sqlalchemy.Text(), nullable=False)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean(), default=True)

    is_deleted = sqlalchemy.Column(sqlalchemy.Boolean(), default=True)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime())
    created_by = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime())
    updated_by = sqlalchemy.Column(sqlalchemy.Integer())

    @staticmethod
    def list_with_pagination(page: int) -> list:
        message_group = MessageGroup.metadata.tables.get("message_group")
        sel = message_group.select().where(MessageGroup.is_active == True, MessageGroup.is_deleted == False).limit(5).offset(page*5)
        conn = engine.connect()
        res = conn.execute(sel)
        return res.fetchall()
    
    @staticmethod
    def list() -> list:
        message_group = MessageGroup.metadata.tables.get("message_group")
        sel = message_group.select().where(MessageGroup.is_active == True, MessageGroup.is_deleted == False)
        conn = engine.connect()
        res = conn.execute(sel)
        return res.fetchall()
    
    @staticmethod
    def get_size() -> int:
        message_group = MessageGroup.metadata.tables.get("message_group")
        sel = message_group.select().where(MessageGroup.is_active == True, MessageGroup.is_deleted == False)
        conn = engine.connect()
        res = conn.execute(sel)
        return len(res.fetchall())
    
    @staticmethod
    def get_group_name_list() -> list:
        respose = []
        message_group = MessageGroup.metadata.tables.get("message_group")
        sel = message_group.select().where(MessageGroup.is_active == True, MessageGroup.is_deleted == False)
        conn = engine.connect()
        res = conn.execute(sel)
        r = res.fetchall()
        for i in r:
            respose.append(i[2])
        return respose
    
    @staticmethod
    def get(id: int) -> list:
        message_group = MessageGroup.metadata.tables.get("message_group")
        sel = message_group.select().where(MessageGroup.id == id, MessageGroup.is_active == True, MessageGroup.is_deleted == False)
        conn = engine.connect()
        res = conn.execute(sel)
        return res.fetchone()
    
    @staticmethod
    def get_id_by_link(link: str):
        message_group = MessageGroup.metadata.tables.get("message_group")
        sel = message_group.select().where(MessageGroup.link == link, MessageGroup.is_active == True, MessageGroup.is_deleted == False)
        conn = engine.connect()
        res = conn.execute(sel)
        return res.fetchone()
