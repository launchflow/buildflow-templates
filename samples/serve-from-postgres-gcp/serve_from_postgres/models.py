from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Strings(Base):
    __tablename__ = "strings"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    string = Column(String)
