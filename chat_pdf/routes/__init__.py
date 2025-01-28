from routes.agent_action import agent_action_bp


def register_blueprints(app):
    # Register the blueprints with the Flask app
    app.register_blueprint(agent_action_bp, url_prefix="/agent_actions")
