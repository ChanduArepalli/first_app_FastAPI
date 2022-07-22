from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # Profile details
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    description = Column(String, nullable=True)

    created_at = Column(DateTime, nullable=True)