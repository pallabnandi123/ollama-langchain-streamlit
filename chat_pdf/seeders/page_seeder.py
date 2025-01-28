from models.page import Page
from models.template import Template
from models.page_template import PageTemplate
from models.business_category import BusinessCategory
from models.business_category_page import BusinessCategoryPage
from sqlalchemy.orm import Session
import os

# Define the path for templates
template_folder_path = "/app/templates/TemplateA"


def run(db: Session):
    """
    Seeds pages based on template files and links them with business categories.

    Args:
        db (Session): The database session used for querying and adding records.

    This function calls the seeder function to create new pages
    and outputs the status of the seeding process to the console.
    """
    print("Seeding pages...")
    seeder(db)
    print("Pages seeded successfully.")


def get_file_names(folder_path: str):
    """
    Retrieve filenames (without extensions) from a specified folder.

    Args:
        folder_path (str): The path to the folder containing template files.

    Returns:
        list: A list of filenames (without extensions) found in the folder.
               Returns an empty list if the folder does not exist or an error occurs.
    """
    try:
        files = [
            os.path.splitext(file)[0]
            for file in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, file))
        ]
        print(f"Found files: {files}")
        return files
    except FileNotFoundError:
        print(f"Error: Folder '{folder_path}' not found.")
        return []
    except Exception as e:
        print(f"Error accessing folder: {e}")
        return []


def create_page(db: Session, page_name: str) -> Page:
    """
    Create a new Page if it does not already exist in the database.

    Args:
        db (Session): The database session used for querying and adding records.
        page_name (str): The name of the page to create.

    Returns:
        Page: The created or existing Page object.
    """
    existing_page = db.query(Page).filter_by(name=page_name).first()

    if existing_page:
        print(f"Page '{page_name}' already exists, fetching existing template.")
        return existing_page

    new_page = Page(name=page_name, path=page_name)
    db.add(new_page)
    db.flush()

    print(f"Created page '{page_name}' with path '{page_name}'.")
    return new_page


def create_page_template(db: Session, template_id: int, page_id: int):
    """
    Create a new PageTemplate association if it does not already exist.

    Args:
        db (Session): The database session used for querying and adding records.
        template_id (int): The ID of the template to associate with the page.
        page_id (int): The ID of the page to link with the template.

    Outputs the status of the PageTemplate creation to the console.
    """
    existing_page_template = (
        db.query(PageTemplate)
        .filter_by(template_id=template_id, page_id=page_id)
        .first()
    )

    if not existing_page_template:
        new_page_template = PageTemplate(template_id=template_id, page_id=page_id)
        db.add(new_page_template)
        db.flush()
        print(f"Associated page ID {page_id} with template ID {template_id}")
    else:
        print(
            f"Association already exists for page ID '{page_id}' and template ID '{template_id}'."
        )


def create_business_category_page(
    db: Session, business_category_id: int, page_id: int
) -> BusinessCategoryPage:
    """
    Creates a new association between a page and a business category if it doesn't exist.

    Args:
        db (Session): The database session used for adding the records.
        page_id (int): The ID of the page to associate.
        business_category_id (int): The ID of the business category to associate with the page.
    """
    existing_category_page = (
        db.query(BusinessCategoryPage)
        .filter_by(business_category_id=business_category_id, page_id=page_id)
        .first()
    )

    if not existing_category_page:
        new_category_page = BusinessCategoryPage(
            business_category_id=business_category_id, page_id=page_id
        )
        db.add(new_category_page)
        db.flush()
        print(
            f"Associated page ID '{page_id}' with business category ID '{business_category_id}'."
        )
    else:
        print(
            f"Association already exists for page ID '{page_id}' and business category ID '{business_category_id}'."
        )


def seeder(db: Session):
    """
    Seeds pages and links them with the first available business category.

    Args:
        db (Session): The database session used for querying and adding records.

    Outputs the status of the seeding process to the console.
    If no template or pages are found, appropriate messages are printed.
    """
    template = db.query(Template).first()

    if not template:
        print("Error: No template found.")
        return

    business_category = db.query(BusinessCategory).first()

    if not business_category:
        print("Error: No business category found.")
        return

    # Fetch page names from the template folder
    pages = get_file_names(template_folder_path)

    if not pages:
        print("No pages found in the folder.")
        return

    for page_name in pages:
        new_page = create_page(db, page_name)
        create_page_template(db, template.id, new_page.id)
        create_business_category_page(db, business_category.id, new_page.id)
