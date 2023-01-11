from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    Text,
    Enum
)
from .schemas.post import ReactionKind
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    date = Column(Date, default=date.today())
    description = Column(Text, nullable=True)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)


class Reaction(Base):
    __tablename__ = 'reaction'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    post_id = Column(Integer, ForeignKey('posts.id'), index=True)
    reaction_kind = Column(Enum(ReactionKind))
