from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models import Base


class BusinessType(Base):
    """
    Represents various company business classifications. The table supports
    hierarchical relationships between business types via the `parent_id` field,
    allowing one business type to be the parent of others.

    Relationships:
        - parent: Self-referential relationship to establish a hierarchy of business types.
        - companies: One-to-many relationship with the Company model, representing the companies
          that fall under a specific business type.
    """

    __tablename__ = "business_types"

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("business_types.id"), nullable=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    deleted_at = Column(DateTime, nullable=True)

    # Self-referential relationship to allow for parent-child hierarchy of business types.
    parent = relationship("BusinessType", remote_side=[id], backref="children")

    # Has many relationship with the Company model.
    companies = relationship("Company", back_populates="business_type")
