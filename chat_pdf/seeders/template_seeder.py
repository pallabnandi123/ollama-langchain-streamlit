from sqlalchemy.orm import Session
from models.template import Template


def run(db: Session):
    """
    Seeds the database with a template.

    Args:
        db (Session): The database session used for querying and adding records.
    """
    print("Seeding template...")
    seeder(db)
    print("Template seeding process completed.")


def create_template(db: Session, template_name: str, template_path: str) -> Template:
    """
    Creates a new template or fetches an existing one.

    Args:
        db (Session): The database session used for adding the records.
        template_name (str): The name of the template to create or fetch.
        template_path (str): The path of the template.

    Returns:
        Template: The created or fetched template object.
    """
    existing_template = db.query(Template).filter_by(name=template_name).first()

    if existing_template:
        print(f"Template '{template_name}' already exists, fetching existing template.")
        return existing_template

    new_template = Template(name=template_name, path=template_path)
    db.add(new_template)
    db.flush()

    print(f"Created template '{template_name}' with path '{template_path}'.")
    return new_template


def seeder(db: Session):
    """
    Seeds the database with a template.

    Args:
        db (Session): The database session used for adding records.
    """
    

    try:
        create_template(db, template_name="TemplateA", template_path="TemplateA")
    except Exception as e:
        print(f"Error while creating or fetching template: {e}")
