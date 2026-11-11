from database.database import get_connection
from models.user import User

def _map(row) -> User:
    return User(
        user_id=row[0],
        name=row[1],
        surname=row[2],
        patronymic=row[3],
        password_hash=row[4],
        user_role=row[5]
    )

def get_all() -> list[User]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT user_id, name, surname, patronymic, password_hash, user_role
        FROM "User"
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]