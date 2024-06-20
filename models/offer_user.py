import sqlalchemy
from configs.database_config import Base, engine

class OfferUser(Base):
    __tablename__ = "offer_user"

    id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    offer_id = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean(), default=True)

    is_deleted = sqlalchemy.Column(sqlalchemy.Boolean(), default=True)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime())
    created_by = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime())
    updated_by = sqlalchemy.Column(sqlalchemy.Integer())
