from sqlalchemy.orm import Session

from database import models


def create_user(db: Session):
    """
       Creates a user with admin privileges.

       This function creates a user with predefined admin credentials, including name, email, and password.
       The created user is then added to the database.

       :param db: Database session.
       :return: User object representing the created admin user.
    """
    db_user = models.User(
        name='Mr. Admin', email="admin@admin.com",
        hashed_password=""
    )
    db_user.save_password("1234")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
