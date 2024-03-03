from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from starlette import status

from api.dependencies import friend_relations_service_dep, users_api_dep
from api.schemas.friends import FriendRelationRead, FriendRelationCreate

router = APIRouter(prefix='/friend_relations', tags=['Friends'])


@router.get(
    '/{friend_relation_id}',
    response_model=FriendRelationRead,
    responses={
        404: {
            'description': 'Friend relation not found'
        }
    }
)
async def get_friend_relation(friend_relation_id: UUID, friend_relations_service: friend_relations_service_dep):
    friend_relation = await friend_relations_service.get_by_id(friend_relation_id)

    if friend_relation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return friend_relation


@router.get(
    '/user/{user_id}',
    response_model=list[FriendRelationRead],
    responses={
        404: {
            'description': 'User not found'
        }
    }
)
async def get_all_user_friends(
        user_id: UUID,
        offset: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=100)] = 50,
        *,
        friend_relations_service: friend_relations_service_dep,
        users_api: users_api_dep
):
    if not await users_api.is_user_exists(user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return await friend_relations_service.get_user_friend_relations(user_id, offset=offset, limit=limit)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=FriendRelationRead,
    responses={
        400: {
            'description': 'Initiator and target cannot be the same'
        },
        404: {
            'description': 'Initiator or target not found'
        },
        409: {
            'description': 'Friend relation already exists'
        }
    }
)
async def create_friend_relation(
        new_friend_relation: FriendRelationCreate,
        friend_relations_service: friend_relations_service_dep,
        users_api: users_api_dep
):
    """
    Creates new friend relation.

    The initiator is the user who creates the friendship.
    The target is the user with whom the friendship is created.
    Tag is additional information about friendship. For example: “Best friend”, “Relative”, etc.

    * There can only be one friend relation between two users
    * The initiator and target cannot be the same user
    """
    if new_friend_relation.initiator_id == new_friend_relation.target_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Initiator and target cannot be the same')

    if not await users_api.is_user_exists(new_friend_relation.initiator_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Initiator user not found')

    if not await users_api.is_user_exists(new_friend_relation.target_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Target user not found')

    existing_friend_relation = await friend_relations_service.get_friend_relation_by_users(
        new_friend_relation.initiator_id, new_friend_relation.target_id
    )

    if existing_friend_relation is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    return await friend_relations_service.create_friend_relation(new_friend_relation)
