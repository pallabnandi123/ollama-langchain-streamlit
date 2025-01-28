from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from models import Base

class Company(Base):
    """
    Represents a company within the system. Each company is associated with a 
    specific business type and can have multiple users.

    Relationships:
        - business_type: Many-to-one relationship with the BusinessType model, indicating the 
          business classification of the company.
        - users: One-to-many relationship with the User model, representing the users 
          associated with the company.
    """

    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    business_type_id = Column(Integer, ForeignKey('business_types.id'), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    # Many-to-one relationship to BusinessType
    business_type = relationship("BusinessType", back_populates="companies")
    
    # One-to-many relationship to User
    users = relationship("User", back_populates="company")
    
    # One-to-many relationship to Project
    projects = relationship("Project", back_populates="company")
