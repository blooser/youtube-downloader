from sqlalchemy import Column, Integer, String

from . import Base

class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True)
    url = Column(String(80), unique=True)
    title = Column(String(80))
    uploader = Column(String(80))
    thumbnail = Column(String(80))

