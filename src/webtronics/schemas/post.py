from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from enum import Enum


class BasePost(BaseModel):
    title: str
    description: str
    date: Optional[date]


class PostCreate(BasePost):
    pass


class PostUpdate(BasePost):
    pass


class Post(BasePost):
    id: int
    user_id: int
    likes: int
    dislikes: int

    class Config:
        orm_mode = True


class PostList(BaseModel):
    posts: List[Post]

    class Config:
        orm_mode = True


class ReactionKind(str, Enum):
    LIKE = 'like'
    DISLIKE = 'dislike'


class LeaveReaction(BaseModel):
    reaction_kind: ReactionKind
