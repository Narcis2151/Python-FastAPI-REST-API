from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text
from datetime import datetime


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default="TRUE")
    created = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()")
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()")
    )

