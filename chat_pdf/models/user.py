from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey,
    Enum,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models import Base
from enum import Enum as PyEnum
import uuid
import hashlib


def generate_uuid():
    """
    Generates a SHA-256 hash from a UUID.
    This provides a unique 64-character hexadecimal token for email verification.
    """
    # Generate a standard UUID (36 characters including hyphens)
    generated_uuid = str(uuid.uuid4())
    # Hash the UUID using SHA-256 to get a 64-character hexadecimal string
    return hashlib.sha256(generated_uuid.encode("utf-8")).hexdigest()


class UserStatusEnum(PyEnum):
    """
    Enumeration for the possible statuses of a user:
    - active: User is currently active.
    - inactive: User is currently inactive.
    - blocked: User is blocked from accessing the platform.
    """

    active = "active"
    inactive = "inactive"
    blocked = "blocked"


class User(Base):
    """
    Represents a user within the system. Users are associated with a company
    and can have different statuses. This model also includes fields for email
    and phone verification, password, and other personal information.

    Attributes:
        - email_verify_token: Unique token for email verification, generated using SHA-256.
        - status: Enum indicating whether the user is active, inactive, or blocked.

    Relationships:
        - company: Many-to-one relationship with the Company model, indicating the company
          the user belongs to.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    email = Column(String(320), unique=True, nullable=False)
    phone_no = Column(String(15))
    dial_code = Column(String(5))
    name = Column(String(200), nullable=False)
    email_verified_at = Column(DateTime)
    email_verify_token = Column(String, unique=True, default=generate_uuid, nullable=False)
    phone_verified_at = Column(DateTime)
    password = Column(String, nullable=False)
    status = Column(Enum(UserStatusEnum), default=UserStatusEnum.active, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    deleted_at = Column(DateTime)

    # Many-to-one relationship with the Company model
    company = relationship("Company", back_populates="users")
    
    # One-to-many relationship with the Project model
    projects = relationship("Project", back_populates="user")

    # Unique constraint on the combination of phone_no and dial_code
    __table_args__ = (
        UniqueConstraint("phone_no", "dial_code", name="uq_phone_no_dial_code"),
    )
