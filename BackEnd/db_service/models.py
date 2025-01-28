from sqlalchemy import Column, Integer, String # type: ignore
from database import Base
from sqlalchemy import DateTime # type: ignore



class blacklist(Base):
    __tablename__ = "blacklist"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(50), index=True, nullable=False)
    categorie = Column(String(200))
    Date_inscription = Column(DateTime)

class reliability(Base):
    __tablename__ = "reliability"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255), index=True, nullable=False)
    confidence = Column(Integer, default=0)
    prediction = Column(String(255))
    nb_visited = Column(Integer, default=0)
