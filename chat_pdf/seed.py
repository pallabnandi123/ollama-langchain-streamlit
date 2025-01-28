from database import get_db
from sqlalchemy.orm import Session
from seeders import (
    business_type_seeder,
    business_category_seeder,
    user_seeder,
    template_seeder,
    page_seeder,
)


def run_seeder():
    """
    Run all seeders to populate the database.
    """
    # Get a new database session from the generator
    db_gen = get_db()
    db: Session = next(db_gen)  # Extract session object from generator

    try:
        # Begin transaction
        with db.begin():
            business_type_seeder.run(db)
            user_seeder.run(db)
            business_category_seeder.run(db)
            template_seeder.run(db)
            page_seeder.run(db)

        # Commit the transaction
        db.commit()

    except Exception as e:
        print(f"Error while seeding: {e}")
        db.rollback()

    finally:
        # Close the database session
        db.close()
        next(db_gen, None)  # Ensure the generator is finalized


if __name__ == "__main__":
    run_seeder()
