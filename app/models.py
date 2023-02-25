from flask_login import UserMixin
from .services import get_user_by_username

class UserModel(UserMixin):
    """ Model User - login. """
    def __init__(self, user_data):
        self.id = user_data.email
        self.password = user_data.password

    @staticmethod
    def get(email):
        """ Método para obtener el usuario a partir del username. """
        print(f' get en load_user :: {email}')
        user_data = get_user_by_username(email)
        print(f' user_data :: {user_data}')
        return UserModel(user_data)