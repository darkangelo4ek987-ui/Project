from repositories import user_repository
from models.user import User

def authenticate(name: str, password_hash: str) -> User | None:
    users = user_repository.get_all()
    for user in users:
        if user.name.lower() == name.lower() and user.password_hash == password_hash:
            return user
    return None