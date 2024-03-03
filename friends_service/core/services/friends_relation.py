from core.repositories.friend_relations import BaseFriendRelationRepository


class FriendRelationsService:
    def __init__(self, friends_repository: BaseFriendRelationRepository):
        self._friends_repository = friends_repository

    async def get_by_id(self, friend_relation_id):
        return await self._friends_repository.get_by_id(friend_relation_id)

    async def get_user_friend_relations(self, user_id, offset, limit):
        return await self._friends_repository.get_by_user_id(user_id)

    async def create_friend_relation(self, friend_relation):
        return await self._friends_repository.add(friend_relation)

    async def get_friend_relation_by_users(self, first_user_id, second_user_id):
        return await self._friends_repository.get_friend_relation_by_users(first_user_id, second_user_id)
