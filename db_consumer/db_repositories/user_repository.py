from sqlalchemy.dialects.postgresql import insert
from models.users import User


class UserRepository:
    def __init__(self, db):
        self.db = db

    def upsert_user(self, email: str, username: str, hashed_password: str):
        stmt = insert(User).values(
            email=email,
            username=username,
            hashed_password=hashed_password
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=[User.email],
            set_={
                "username": username,
                "hashed_password": hashed_password
            }
        )

        self.db.execute(stmt)
        self.db.commit()

    def close(self):
        self.db.close()
