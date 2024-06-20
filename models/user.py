import sqlalchemy
from configs.database_config import Base, engine

class User(Base):
    __tablename__ = "user"

    id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)

    first_name = sqlalchemy.Column(sqlalchemy.String(length=100), nullable=False)
    last_name = sqlalchemy.Column(sqlalchemy.String(length=100), nullable=False)
    phone = sqlalchemy.Column(sqlalchemy.String(length=9), unique=True, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String(length=100), nullable=False)
    chat_id = sqlalchemy.Column(sqlalchemy.BigInteger(), unique=True)
    lang = sqlalchemy.Column(sqlalchemy.String(length=10), nullable=False)
    role = sqlalchemy.Column(sqlalchemy.String(length=10), nullable=False)
    publish_day = sqlalchemy.Column(sqlalchemy.Integer(), default=0)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean(), default=True)

    is_deleted = sqlalchemy.Column(sqlalchemy.Boolean(), default=True)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime())
    created_by = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime())
    updated_by = sqlalchemy.Column(sqlalchemy.Integer())

    @staticmethod
    def login(phone: str, password: str) -> str:
        user = User.metadata.tables.get("user")
        sel = user.select().where(User.phone == phone, User.password == password, User.is_deleted == False)
        conn = engine.connect()
        conn_res = conn.execute(sel)
        res = conn_res.fetchone()
        if res is not None:
            if res[9] == True:
                return res[7]
            else:
                return "NOT_ACTIVE"
        else:
            return "NO"
        
    @staticmethod
    def register(first_name: str, last_name: str, phone: str, password: str, lang: str, chat_id: int) -> bool:
        user = User.metadata.tables.get("user")
        sel = user.select().where(User.phone == phone, User.is_deleted == False)
        conn = engine.connect()
        sel_res = conn.execute(sel)
        if sel_res.fetchone() is None:
            ins = user.insert().values(first_name = first_name, last_name = last_name, phone = phone, password = password, is_deleted = False, lang = lang, role = "STUDENT", chat_id = chat_id, created_by = -1, is_active = False)
            conn.execute(ins)
            conn.commit()
            return True
        else:
            return False
        
    @staticmethod
    def list() -> list:
        user = User.metadata.tables.get("user")
        sel = user.select().where(User.is_deleted == False, User.publish_day > 0)
        conn = engine.connect()
        res = conn.execute(sel)
        return res.fetchall()
    
    @staticmethod
    def set_chat_id_by_phone(chat_id: sqlalchemy.BigInteger, phone: str) -> None:
        user = User.metadata.tables.get("user")
        upd = user.update().values(chat_id = chat_id).where(User.phone == phone, User.is_deleted == False)
        conn = engine.connect()
        conn.execute(upd)
        conn.commit()
        return None
        
    @staticmethod
    def get_id_by_phone(phone: str) -> int:
        user = User.metadata.tables.get("user")
        sel = user.select().where(User.phone == phone, User.is_deleted == False, User.is_active == True)
        conn = engine.connect()
        res = conn.execute(sel)
        return res.fetchone()[0]

    @staticmethod
    def get_phone_by_id(id: int) -> str:
        user = User.metadata.tables.get("user")
        sel = user.select().where(User.id == id, User.is_deleted == False, User.is_active == True)
        conn = engine.connect()
        res = conn.execute(sel)
        return res.fetchone()[3]
    
    @staticmethod
    def get_by_phone(phone: str) -> str:
        user = User.metadata.tables.get("user")
        sel = user.select().where(User.phone == phone, User.is_deleted == False, User.is_active == True)
        conn = engine.connect()
        res = conn.execute(sel)
        return res.fetchone()

    @staticmethod
    def get_publish_day_by_phone(phone: str) -> int:
        user = User.metadata.tables.get("user")
        sel = user.select().where(User.phone == phone, User.is_deleted == False, User.is_active == True)
        conn = engine.connect()
        res = conn.execute(sel)
        return res.fetchone()[8]

    @staticmethod
    def set_publish_day_by_phone(phone: str, publish_day: int) -> None:
        user = User.metadata.tables.get("user")
        upd = user.update().values(publish_day = publish_day).where(User.phone == phone, User.is_deleted == False, User.is_active == True)
        conn = engine.connect()
        conn.execute(upd)
        conn.commit()
    
    @staticmethod
    def change_active(phone: str, chat_id: int) -> None:
        user = User.metadata.tables.get("user")
        upd = user.update().where(User.phone == phone, User.is_deleted == False).values(is_active = True, chat_id = chat_id)
        conn = engine.connect()
        conn.execute(upd)
        conn.commit()
        return None  
