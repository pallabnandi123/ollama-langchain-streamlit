from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models import Base


class PageTemplate(Base):
    """
    Junction table between Page and Template models, 
    linking pages to templates.
    """

    __tablename__ = "page_templates"

    template_id = Column(Integer, ForeignKey("templates.id"), primary_key=True, nullable=False)
    page_id = Column(Integer, ForeignKey("pages.id"), primary_key=True, nullable=False)

    # Relationships
    templates = relationship("Template", back_populates="pages")
    pages = relationship("Page", back_populates="templates")
