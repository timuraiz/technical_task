from fastapi import FastAPI
from .api import (
    auth,
    post
)
tags_metadata = [
    {
        'name': 'auth',
        'description': 'User authorization and registration'
    },
    {
        'name': 'post',
        'description': 'All crud operations applying to posts'
    },

]

app = FastAPI(
    title='Social Networking Application (technical task)',
    description='This service provides an opportunity:\n'
                '- To create/read/update/delete posts\n'
                '- Singing in/up as a user\n'
                '- Leave reactions (like/dislike) posts of other authors',
    version='1.0.0',
    openapi_tags=tags_metadata
)

app.include_router(auth.router, prefix='/auth', tags=['auth'])
app.include_router(post.router, prefix='/post', tags=['post'])
