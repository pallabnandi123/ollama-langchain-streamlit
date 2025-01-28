from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models import Base


class BusinessCategoryPage(Base):
    """
    Junction table linking business categories to pages, 
    allowing each business category to be associated with multiple pages.
    """

    __tablename__ = "business_category_pages"

    business_category_id = Column(Integer, ForeignKey("business_categories.id"), primary_key=True, nullable=False)
    page_id = Column(Integer, ForeignKey("pages.id"), primary_key=True, nullable=False)

    # Relationships
    business_categories = relationship("BusinessCategory", back_populates="pages")
    pages = relationship("Page", back_populates="business_categories")
