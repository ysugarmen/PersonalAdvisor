from sqlalchemy import Column, Integer, String
from app.config import Base


class Advice(Base):
    __tablename__ = "advice"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    reccomendation = Column(String)
