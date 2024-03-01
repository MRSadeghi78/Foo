from sqlalchemy.orm import Session

from database import models
from database.constants import UserRole


def create_user(db: Session):
    db_user = models.User(
        name='Mr. Admin', email="admin@admin.com",
        hashed_password="", role=UserRole.ADMIN
    )
    db_user.save_password("1234")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
