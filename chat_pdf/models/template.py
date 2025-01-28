from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models import Base


class Template(Base):
    """
    Represents a template file used within the system, 
    identified by its name and path.
    """

    __tablename__ = "templates"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    path = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime)

    # Relationships with other models
    pages = relationship("PageTemplate", back_populates="templates")
