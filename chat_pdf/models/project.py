from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models import Base


class Project(Base):
    """
    Represents a project within the system. A project is associated with both a company
    and a user. Each project can have a description and timestamps for creation, updates, 
    and soft deletion.

    Attributes:
        - company_id: Foreign key linking the project to the Company model.
        - user_id: Foreign key linking the project to the User model.
        - name: The name of the project.
        - description: A text field for project details.
    
    Relationships:
        - company: Many-to-one relationship with the Company model.
        - user: Many-to-one relationship with the User model.
    """

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)  # Corrected ForeignKey to match 'companies' table
    business_category_id = Column(Integer, ForeignKey("business_categories.id"), nullable=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime)

    # Many-to-one relationship with the Company model
    company = relationship("Company", back_populates="projects")
    
    # Many-to-one relationship with the User model
    user = relationship("User", back_populates="projects")
    
    # One-to-many relationship with the ProjectPage model
    pages = relationship("ProjectPage", back_populates="project")
    
    # Many-to-one relationship with the Company model
    business_category = relationship("BusinessCategory", back_populates="projects")