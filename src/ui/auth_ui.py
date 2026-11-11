from services import auth_service

def login():
    print("\n=== АВТОРИЗАЦИЯ В СИСТЕМЕ ===")
    name = input("Введите имя пользователя: ").strip()
    password = input("Введите пароль: ").strip()
    
    user = auth_service.authenticate(name, password)
    if not user:
        print("Ошибка: Неверное имя пользователя или пароль.")
        return None
    print(f"Успешный вход! Добро пожаловать, {user.surname} {user.name}")
    return user