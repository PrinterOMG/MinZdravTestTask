from fastapi import APIRouter
from starlette import status

from api.dependencies import users_service_dep
from api.schemas.users import UserRead, UserCreate

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('', response_model=UserRead)
async def create_new_user(new_user: UserCreate, users_service: users_service_dep):
    pass


@router.get('/{user_id}', response_model=UserRead)
async def get_user(user_id: int, users_service: users_service_dep):
    pass


@router.get(
    '/{user_id}/exists',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {
            'description': 'User does not exist'
        }
    }
)
async def get_user_exists(user_id: int, users_service: users_service_dep):
    pass
