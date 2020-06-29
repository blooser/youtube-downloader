from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql.expression import func

from . import Base

class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True)
    url = Column(String(80), unique=True)
    title = Column(String(80))
    uploader = Column(String(80))
    uploader_url = Column(String(80))
    thumbnail = Column(String(80))
    date = Column(DateTime(), server_default=func.now())


