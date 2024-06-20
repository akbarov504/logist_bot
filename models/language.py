import sqlalchemy
from configs.database_config import Base, engine

class Language(Base):
    __tablename__ = "language"

    id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)

    lang = sqlalchemy.Column(sqlalchemy.String(length=10), nullable=False)
    code = sqlalchemy.Column(sqlalchemy.Text(), nullable=False)
    message = sqlalchemy.Column(sqlalchemy.Text(), nullable=False)

    is_deleted = sqlalchemy.Column(sqlalchemy.Boolean(), default=True)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime())
    created_by = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime())
    updated_by = sqlalchemy.Column(sqlalchemy.Integer())

    @staticmethod
    def get(lang: str, code: str) -> str:
        language = Language.metadata.tables.get("language")
        sel = language.select().where(Language.lang == lang, Language.code == code, Language.is_deleted == False)
        conn = engine.connect()
        res = conn.execute(sel)
        return res.fetchone()[3]
