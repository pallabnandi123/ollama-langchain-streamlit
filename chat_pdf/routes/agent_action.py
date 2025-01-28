from flask import Blueprint, jsonify, request
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas.project import ProjectResponse
from models.project import Project
from models.business_category import BusinessCategory

# Define the blueprint for project-related routes
agent_action_bp = Blueprint("agent_action", __name__)

# Get a new database session from the generator
db_gen = get_db()
db: Session = next(db_gen)


def find_category_id_by_name(response):
    # Check if 'Subcategory:' is in the response and extract the subcategory
    if "Subcategory:" in response:
        subcategory_part = response.split("Subcategory:")[-1].strip()

        # Query the database to find the business category by name
        business_category = (
            db.query(BusinessCategory)
            .filter(BusinessCategory.name == subcategory_part)
            .first()
        )

        # Return the business category ID if found, otherwise return None
        return business_category.id if business_category else None

    # Return None if 'Subcategory:' is not in the response
    return None


# Update an existing project route
@agent_action_bp.route("/business_category/<int:id>", methods=["POST"])
def business_category(id):
    try:
        # Get the project from the database
        project = db.query(Project).filter(Project.id == id).first()
        if not project:
            return jsonify({"error": "Project not found."}), 404

        # Validate the incoming JSON payload
        payload = request.get_json()
        business_category_id = find_category_id_by_name(payload.get("response"))

        # Update project fields
        project.business_category_id = business_category_id

        # Save the updated project to the database
        db.commit()

        return (
            jsonify(
                {
                    "message": "Project business category updated successfully",
                    "project": ProjectResponse.model_validate(project).dict(),
                }
            ),
            200,
        )

    except IntegrityError as e:
        db.rollback()
        print(f"Integrity error: {str(e.orig)}")
        return {"error": f"Integrity error: {str(e.orig)}"}, 400
    except SQLAlchemyError as e:
        db.rollback()
        print("A database error occurred.")
        return {"error": "A database error occurred."}, 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": f"Error: {str(e)}"}, 500


# Update an existing project route
@agent_action_bp.route("/target_customer/<int:id>", methods=["POST"])
def target_customer(id):
    try:
        # Get the project from the database
        project = db.query(Project).filter(Project.id == id).first()
        if not project:
            return jsonify({"error": "Project not found."}), 404

        # Validate the incoming JSON payload
        payload = request.get_json()

        # Update project description
        project.description = payload.get("response")

        # Save the updated project to the database
        db.commit()

        return (
            jsonify(
                {
                    "message": "Project description updated successfully",
                    "project": ProjectResponse.model_validate(project).dict(),
                }
            ),
            200,
        )

    except IntegrityError as e:
        db.rollback()
        print(f"Integrity error: {str(e.orig)}")
        return {"error": f"Integrity error: {str(e.orig)}"}, 400
    except SQLAlchemyError as e:
        db.rollback()
        print("A database error occurred.")
        return {"error": "A database error occurred."}, 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": f"Error: {str(e)}"}, 500


# Update an existing project route
@agent_action_bp.route("/save_template/<int:id>", methods=["POST"])
def save_template(id):
    try:
        # Get the project from the database
        project = db.query(Project).filter(Project.id == id).first()
        if not project:
            return jsonify({"error": "Project not found."}), 404

        # Validate the incoming JSON payload
        payload = request.get_json()

        # # Update project description
        # project.description = payload.get("response")

        # # Save the updated project to the database
        # db.commit()
        
        print(payload)

        return (
            jsonify(
                {
                    "message": "Project description updated successfully",
                    "project": ProjectResponse.model_validate(project).dict(),
                }
            ),
            200,
        )

    except IntegrityError as e:
        db.rollback()
        print(f"Integrity error: {str(e.orig)}")
        return {"error": f"Integrity error: {str(e.orig)}"}, 400
    except SQLAlchemyError as e:
        db.rollback()
        print("A database error occurred.")
        return {"error": "A database error occurred."}, 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": f"Error: {str(e)}"}, 500
