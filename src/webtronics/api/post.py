from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi import Depends, status

from ..schemas.post import (
    Post,
    PostUpdate,
    PostCreate,
    PostList,
    LeaveReaction,
)
from ..schemas.user import User
from ..services.post import PostService
from ..dependencies import get_current_user

router = InferringRouter()


@cbv(router)
class Post:
    @router.post(
        '/',
        response_model=Post,
        status_code=status.HTTP_201_CREATED,
    )
    async def create(
            self,
            post_data: PostCreate,
            post_service: PostService = Depends(),
            user: User = Depends(get_current_user),
    ):
        '''
        - Creates new post of authorized user.
        \f
        :param post_data:
        :param post_service:
        :param user:
        :return:
        '''
        return post_service.create(user_id=user.id, post_data=post_data)

    @router.get(
        '/',
        response_model=PostList,
    )
    async def get(
            post_service: PostService = Depends()
    ):
        '''
        - Returns list of all post.
        \f
        :return:
        '''
        return post_service.get_list()

    @router.get(
        '/{post_id}',
        response_model=Post,
    )
    async def get(
            self,
            post_id: int,
            post_service: PostService = Depends(),
    ):
        '''
        - Returns a post with the specific id.
        \f
        :param post_id:
        :param post_service:
        :return:
        '''
        return post_service.get(post_id=post_id)

    @router.patch(
        '/{post_id}/leave_reaction',
        status_code=status.HTTP_204_NO_CONTENT,

    )
    async def leave_reaction(
            self,
            post_id: int,
            reaction: LeaveReaction,
            post_service: PostService = Depends(),
            user: User = Depends(get_current_user),

    ):
        '''
        - Allows to leave reaction on post of another author.
        - You can set like.
        - You can set dislike.
        - You can change the reaction to the opposite in the same post.
        \f
        :param post_id:
        :param reaction:
        :param post_service:
        :param user:
        :return:
        '''
        return post_service.set_reaction(post_id=post_id, user_id=user.id, reaction=reaction)

    @router.put(
        '/{post_id}',
        status_code=status.HTTP_204_NO_CONTENT
    )
    async def update(
            self,
            post_id: int,
            post_data: PostUpdate,
            post_service: PostService = Depends(),
            user: User = Depends(get_current_user),
    ):
        '''
        - Allows to author update his own post.
        \f
        :param post_id:
        :param post_data:
        :param post_service:
        :param user:
        :return:
        '''
        return post_service.update(user_id=user.id, post_id=post_id, post_data=post_data)

    @router.delete(
        '/{post_id}',
        status_code=status.HTTP_204_NO_CONTENT
    )
    async def delete(
            self,
            post_id: int,
            post_service: PostService = Depends(),
            user: User = Depends(get_current_user),
    ):
        '''
        - Allows to author delete his own post.
        \f
        :param post_id:
        :param post_service:
        :param user:
        :return:
        '''
        return post_service.delete(user_id=user.id, post_id=post_id)
