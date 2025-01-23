from sqlalchemy import Column, Integer, BigInteger
from core.database import Base


class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, nullable=False, unique=True)
