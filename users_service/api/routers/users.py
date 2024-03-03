from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from starlette import status

from api.dependencies import users_service_dep
from api.schemas.users import UserRead, UserCreate

router = APIRouter(prefix='/users', tags=['Users'])


@router.post(
    '',
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {
            'description': 'Username already taken'
        }
    }
)
async def create_new_user(new_user: UserCreate, users_service: users_service_dep):
    """
    Creates a new user
    """
    existing_user = await users_service.get_by_username(new_user.username)
    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'User with username "{new_user.username}" already exists')

    return await users_service.add(new_user)


@router.get(
    '/{user_id}',
    response_model=UserRead,
    responses={
        404: {
            'description': 'User not found'
        }
    }
)
async def get_user(user_id: UUID, users_service: users_service_dep):
    """
    Returns the user by his id
    """
    user = await users_service.get_by_id(user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user


@router.get(
    '',
    response_model=list[UserRead]
)
async def get_all_users(
        offset: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=100)] = 50,
        *,
        users_service: users_service_dep
):
    """
    Returns a list of all users
    """
    return await users_service.get_all(offset=offset, limit=limit)


@router.get(
    '/{user_id}/exists',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {
            'description': 'User exists'
        },
        404: {
            'description': 'User does not exist'
        }
    }
)
async def get_user_exists(user_id: UUID, users_service: users_service_dep):
    """
    Checks whether a user with the specified id exists.
    Status 204 if the user exists, otherwise 404
    """
    is_user_exists = await users_service.is_user_exists(user_id)

    if not is_user_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
