import os
from flask import Flask, jsonify
from flask_cors import CORS
from api import api
from models import setup_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get("SQLALCHEMY_DATABASE_URI")
        setup_db(app, database_path=database_path)
        
    app.register_blueprint(api, url_prefix=f"/")

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/*": {"origins": "*"}})
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Headers", "GET, POST, PATCH, DELETE, OPTIONS"
        )
        return response

    @app.route("/")
    def init():
        return jsonify({"status": 200})

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"status": 404, "message": "Resource not found"}), 404

    @app.errorhandler(422)
    def unprocessable_entity_error(error):
        return (
            jsonify({"status": 422, "message": "Unprocessable entity"}),
            422,
        )

    return app
