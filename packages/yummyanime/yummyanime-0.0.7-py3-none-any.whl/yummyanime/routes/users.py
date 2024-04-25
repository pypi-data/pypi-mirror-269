from ._abs import IApiMethods
from ..structs.user import IUser


class Users(IApiMethods):
    def get(self, user_id: int):
        return self.method(f'/users/id{user_id}', 'GET', type=IUser)
