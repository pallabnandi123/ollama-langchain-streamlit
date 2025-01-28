from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models import Base
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


class ProjectPage(Base):
    """
    Represents a page associated with a project. Each page has a unique UUID and is linked
    to a specific project. Includes timestamps for creation, updates, and soft deletion.

    Attributes:
        - uuid: Unique identifier for the page, generated as a UUID.
        - project_id: Foreign key linking the page to the Project model.
    """

    __tablename__ = "project_pages"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), unique=True, nullable=False, default=generate_uuid)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    deleted_at = Column(DateTime)

    # Many-to-one relationship with the Project model
    project = relationship("Project", back_populates="pages")