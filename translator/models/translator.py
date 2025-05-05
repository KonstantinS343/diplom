from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Language(Base):
    __tablename__ = "languages"

    language = Column(String, primary_key=True)
    language_name = Column(String, nullable=True)
    iso = Column(String(2), unique=True, nullable=False)
