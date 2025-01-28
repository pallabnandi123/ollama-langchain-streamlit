from models.business_type import BusinessType
from sqlalchemy.orm import Session


def run(db: Session):
    """
    Seeds the database with business types if they don't already exist.

    Args:
        db (Session): The database session used for querying and adding records.

    This function checks if any business types exist in the database. If not, 
    it calls the seeder function to create the necessary business types.
    """
    if not db.query(BusinessType).first():
        print("Seeding business types...")
        seeder(db)
        print("Business types seeded successfully.")
    else:
        print("Business types already seeded, skipping...")


def create_business_type(db: Session, name: str):
    """
    Creates a new business type in the database.

    Args:
        db (Session): The database session used for adding the business type.
        name (str): The name of the business type to create.

    Returns:
        BusinessType: The created BusinessType object.
    """
    business_type = BusinessType(name=name)
    db.add(business_type)
    print(f"Created business type: {name}")
    return business_type


def seeder(db: Session):
    """
    Seeds the database with a predefined list of business types.

    Args:
        db (Session): The database session used for adding records.

    This function iterates through a list of business types and adds each 
    type to the database.
    """
    # List of all business types to seed
    business_types = [
        "Information Technology",
        "Healthcare and Medical Services",
        "Finance and Banking",
        "Retail and E-commerce",
        "Manufacturing",
        "Real Estate",
        "Education and Training",
        "Construction and Engineering",
        "Marketing and Advertising",
        "Hospitality and Tourism",
        "Food and Beverage",
        "Transportation and Logistics",
        "Telecommunications",
        "Energy and Utilities",
        "Entertainment and Media",
        "Non-Profit Organizations",
        "Consulting and Professional Services",
        "Pharmaceuticals and Biotechnology",
        "Agriculture and Farming",
        "Automotive and Transportation Services"
    ]

    try:
        # Step 1: Create and add each business type to the session
        for business_name in business_types:
            create_business_type(db, business_name)

        db.flush()  # Commit the changes to the database
    except Exception as e:
        print(f"Error seeding business types: {e}")
