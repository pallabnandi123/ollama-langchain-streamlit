from models.business_category import BusinessCategory
from sqlalchemy.orm import Session


def run(db: Session):
    """
    Seeds the database with a single business category if it doesn't exist.

    Args:
        db (Session): The database session used for querying and adding records.

    This function checks if any business category exists in the database. 
    If not, it calls the seeder function to create the necessary categories.
    """
    if not db.query(BusinessCategory).first():
        print("Seeding business category...")
        seeder(db)
        print("Business category seeded successfully.")
    else:
        print("Business category already seeded, skipping...")


def create_business_category(db: Session, name: str, parent_id: int = None):
    """
    Creates a new business category in the database.

    Args:
        db (Session): The database session used for adding the category.
        name (str): The name of the business category to create.
        parent_id (int, optional): The ID of the parent category, if applicable.

    Returns:
        BusinessCategory: The created BusinessCategory object.
    """
    category = BusinessCategory(name=name, parent_id=parent_id)
    db.add(category)
    db.flush()
    print(f"Created business category: {name}")
    return category


def seeder(db: Session):
    """
    Seeds the database with the E-commerce parent category and its child category.

    Args:
        db (Session): The database session used for adding records.

    This function creates an E-commerce category and an Online Food Delivery 
    category linked to it as a child category.
    """
    try:
        # Step 1: Create the parent category (E-commerce)
        parent_category = create_business_category(db, name="E-commerce")

        # Step 2: Create the child category (Online Food Delivery) with parent_id
        create_business_category(db, name="Online Food Delivery", parent_id=parent_category.id)

    except Exception as e:
        print(f"Error seeding business categories: {e}")
