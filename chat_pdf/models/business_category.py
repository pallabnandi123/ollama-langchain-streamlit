from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models import Base


class BusinessCategory(Base):
    """
    Represents a hierarchical structure of business categories, 
    where each category can have a parent category.
    """

    __tablename__ = "business_categories"

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("business_categories.id"), nullable=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime)

    # Self-referential relationship to support category hierarchy
    parent = relationship("BusinessCategory", remote_side=[id], backref="children")

    # Relationship with business_category_pages
    pages = relationship("BusinessCategoryPage", back_populates="business_categories")
    
    # One-to-many relationship to Project
    projects = relationship("Project", back_populates="business_category")
