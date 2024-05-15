from sqlalchemy import create_engine, Column, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func, sqltypes

SQLALCHEMY_DATABASE_URL = "sqlite:///database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class BaseModel(Base):
    """
        Base class for database models.

        This class defines common attributes for all database models, such as id, created_at, and updated_at.

        :ivar id: Primary key identifier.
        :ivar created_at: Date and time when the record was created.
        :ivar updated_at: Date and time when the record was last updated.
    """
    __abstract__ = True
    id = Column(sqltypes.Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


def get_db():
    """
        Provides a database session for the application.

        This function yields a database session using the SessionLocal context manager.
        It ensures that the session is closed properly after its use.

        :yield: Database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
