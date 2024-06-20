import sqlalchemy
from configs.database_config import Base, engine

class Offer(Base):
    __tablename__ = "offer"

    id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)

    price = sqlalchemy.Column(sqlalchemy.Numeric(10, 2), nullable=False)
    month = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean(), default=True)

    is_deleted = sqlalchemy.Column(sqlalchemy.Boolean(), default=True)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime())
    created_by = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime())
    updated_by = sqlalchemy.Column(sqlalchemy.Integer())

    @staticmethod
    def list() -> list:
        offer = Offer.metadata.tables.get("offer")
        sel = offer.select().where(Offer.is_active == True, Offer.is_deleted == False)
        conn = engine.connect()
        res = conn.execute(sel)
        return res.fetchall()
