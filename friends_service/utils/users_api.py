from aiohttp import ClientSession


class UsersAPI:
    exists_endpoint = '/api/v1/users/{user_id}/exists'

    def __init__(self, host: str, session: ClientSession):
        self.host = host
        self.session = session

    async def is_user_exists(self, user_id):
        async with self.session.get(self.host + self.exists_endpoint.format(user_id=user_id)) as resp:
            return resp.status == 204
