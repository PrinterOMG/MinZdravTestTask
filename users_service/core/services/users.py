from core.repositories.users import BaseUsersRepository


class UserService:
    def __init__(self, users_repository: BaseUsersRepository):
        self.users_repository = users_repository
