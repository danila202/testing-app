from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime
status_code = Column(Integer)
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

metadata = MetaData()
Base = declarative_base()


class EntryLog(Base):
    __tablename__ = 'entries_log'

    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime, default=datetime.utcnow)
    ip = Column(String)
    method = Column(String)
    uri = Column(String)
    status_code = Column(Integer)

class LogCreated(BaseModel):
    log: str
