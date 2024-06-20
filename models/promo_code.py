import sqlalchemy
from datetime import datetime
from configs.database_config import Base, engine

class PromoCode(Base):
    __tablename__ = "promo_code"

    id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)

    name = sqlalchemy.Column(sqlalchemy.String(length=100), nullable=False)
    publish_day = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    expire = sqlalchemy.Column(sqlalchemy.DateTime(), nullable=False)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean(), default=True)

    is_deleted = sqlalchemy.Column(sqlalchemy.Boolean(), default=True)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime())
    created_by = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime())
    updated_by = sqlalchemy.Column(sqlalchemy.Integer())

    @staticmethod
    def get(name: str) -> int:
        promo_code = PromoCode.metadata.tables.get("promo_code")
        sel = promo_code.select().where(PromoCode.name == name, PromoCode.expire > datetime.now(), PromoCode.is_active == True, PromoCode.is_deleted == False)
        conn = engine.connect()
        res = conn.execute(sel)
        f = res.fetchone()
        if f is None:
            return None
        else:
            return f[2]
    
    @staticmethod
    def list() -> list:
        promo_code = PromoCode.metadata.tables.get("promo_code")
        sel = promo_code.select().where(PromoCode.is_active == True, PromoCode.is_deleted == False)
        conn = engine.connect()
        res = conn.execute(sel)
        return res.fetchall()
    
    @staticmethod
    def delete(id: int) -> None:
        promo_code = PromoCode.metadata.tables.get("promo_code")
        upd = promo_code.update().values(is_deleted = True, is_active = False).where(PromoCode.id == id)
        conn = engine.connect()
        conn.execute(upd)
        conn.commit()
