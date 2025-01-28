from datetime import datetime, timezone
from models.user import User, UserStatusEnum
from models.company import Company
from models.project import Project
from models.business_type import BusinessType
from sqlalchemy.orm import Session
from passlib.context import CryptContext


def run(db: Session):
    """
    Seeds the database with a single user if one does not already exist.

    Args:
        db (Session): The database session used for querying and adding records.

    This function checks if any users exist in the database. If not,
    it calls the seeder function to create the necessary user and
    associated company.
    """
    if not db.query(User).first():
        print("Seeding users...")
        seeder(db)
        print("User seeded successfully.")
    else:
        print("User already seeded, skipping...")


# Initialize CryptContext with bcrypt hashing scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hashes a plain text password using bcrypt.

    Args:
        password (str): The plain text password to be hashed.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def create_company(db: Session, name: str, business_type_id: int) -> Company:
    """
    Creates a new company in the database.

    Args:
        db (Session): The database session used for adding the company.
        name (str): The name of the company.
        business_type_id (int): The ID of the business type associated with the company.

    Returns:
        Company: The created Company object.
    """
    new_company = Company(name=name, business_type_id=business_type_id)
    db.add(new_company)
    db.flush()  # Ensure the company ID is generated
    print(f"Created company: {name}")
    return new_company


def create_project(db: Session, name: str, company_id: int, user_id: int) -> Project:
    """
    Creates a new project in the database.

    Args:
        db (Session): The database session used for adding the project.
        name (str): The name of the project.
        company_id (int): The ID of the company associated with the project.
        user_id (int): The ID of the user associated with the project.

    Returns:
        Project: The created Project object.
    """
    new_project = Project(
        name=name,
        company_id=company_id,
        user_id=user_id,
        description="Project Description",
    )
    db.add(new_project)
    db.flush()
    print(f"Created project: {name}")
    return new_project


def create_user(db: Session, company_id: int) -> User:
    """
    Creates a new user in the database.

    Args:
        db (Session): The database session used for adding the user.
        company_id (int): The ID of the company associated with the user.

    Returns:
        User: The created User object.
    """
    new_user = User(
        company_id=company_id,
        email="master@magicminds.io",
        phone_no="1234567890",
        dial_code="+19",
        name="Magicminds",
        email_verified_at=datetime.now(timezone.utc),
        phone_verified_at=datetime.now(timezone.utc),
        password=hash_password("password123"),
        status=UserStatusEnum.active,
    )
    db.add(new_user)
    db.flush()  # Commit the changes to the database
    print(f"Created user: {new_user.email}")
    return new_user


def seeder(db: Session):
    """
    Seeds the database with a company and a user.

    Args:
        db (Session): The database session used for adding records.

    This function retrieves the first business type from the database and
    creates a new company and a user associated with it.
    """
    business_type = db.query(BusinessType).first()

    if not business_type:
        print("Error: No business type found.")
        return

    try:
        new_company = create_company(
            db, name="Master Company", business_type_id=business_type.id
        )
        new_user = create_user(db, company_id=new_company.id)
        create_project(
            db, name="Project 1", company_id=new_company.id, user_id=new_user.id
        )
    except Exception as e:
        print(f"Error while seeding: {e}")
