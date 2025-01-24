from sqlalchemy import Column, Integer, String, DateTime, func, CheckConstraint
from app.config import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    __table_args__ = (
        CheckConstraint("LENGTH(username) >= 3", name="check_username_length"),
    )

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
