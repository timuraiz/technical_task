from fastapi import (
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from .. import (
    schemas,
    tables,
)
from ..database import get_session
from typing import Optional, List


class PostService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create(
            self,
            user_id: int,
            post_data: schemas.PostCreate,
    ) -> tables.Post:
        post = tables.Post(
            **post_data.dict(),
            user_id=user_id,
        )
        self.session.add(post)
        self.session.commit()
        return post

    def get(
            self,
            post_id: int,
            user_id: Optional[int] = None
    ) -> tables.Post:
        post = self._get(user_id=user_id, post_id=post_id)
        return post

    def _get_list(self) -> Optional[List[tables.Post]]:
        posts = (
            self.session
            .query(tables.Post)
            .all()
        )
        if not posts:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='No posts yet')
        return posts

    def get_list(self) -> schemas.PostList:
        posts = self._get_list()
        return schemas.PostList(posts=posts)

    def _get(self, post_id: int, user_id: Optional[int] = None) -> Optional[tables.Post]:
        if user_id:
            post = (
                self.session
                .query(tables.Post)
                .filter(
                    tables.Post.user_id == user_id,
                    tables.Post.id == post_id,
                )
                .first()
            )
        else:
            post = (
                self.session
                .query(tables.Post)
                .filter(
                    tables.Post.id == post_id,
                )
                .first()
            )
        if not post:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return post

    def _get_reaction(self, user_id: int, post_id: int) -> Optional[tables.Reaction]:
        reaction = (
            self.session
            .query(tables.Reaction)
            .filter(
                tables.Reaction.user_id == user_id,
                tables.Reaction.post_id == post_id,
            )
            .first()
        )
        if reaction:
            return reaction

    def update(
            self,
            user_id: int,
            post_id: int,
            post_data: schemas.PostUpdate,
    ) -> tables.Post:
        post = self._get(user_id=user_id, post_id=post_id)
        for field, value in post_data:
            setattr(post, field, value)
        self.session.commit()
        return post

    def delete(
            self,
            user_id: int,
            post_id: int,
    ):
        post = self._get(user_id=user_id, post_id=post_id)
        self.session.delete(post)
        self.session.commit()

    def set_reaction(
            self,
            post_id: int,
            user_id: int,
            reaction: schemas.LeaveReaction
    ):
        post = self._get(post_id=post_id)
        if post.user_id == user_id:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail='Client is not allowed to leave reaction on his own post'
            )
        reaction_obj = self._get_reaction(user_id=user_id, post_id=post_id)
        if reaction_obj:
            if reaction_obj.reaction_kind != reaction.reaction_kind:
                if reaction_obj.reaction_kind == schemas.ReactionKind.LIKE:
                    post.likes -= 1
                    post.dislikes += 1
                else:
                    post.likes += 1
                    post.dislikes -= 1
                reaction_obj.reaction_kind = reaction.reaction_kind
        else:
            if reaction.reaction_kind == schemas.ReactionKind.LIKE:
                post.likes += 1
            else:
                post.dislikes += 1
            reaction_obj = tables.Reaction(**reaction.dict(), user_id=user_id, post_id=post_id)
            self.session.add(reaction_obj)

        self.session.commit()
