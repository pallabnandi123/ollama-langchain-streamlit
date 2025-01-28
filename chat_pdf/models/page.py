from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models import Base


class Page(Base):
    """
    Represents an internal page with a name and path, 
    containing associated templates.
    """

    __tablename__ = "pages"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    path = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime)

    # Relationship with page_templates
    templates = relationship("PageTemplate", back_populates="pages")
    
    business_categories = relationship("BusinessCategoryPage", back_populates="pages")