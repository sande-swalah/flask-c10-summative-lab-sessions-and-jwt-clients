from flask import jsonify
from flask_restful import Api

from app.errors import AppError
from app.resources import (
    CheckSessionResource,
    JournalEntriesResource,
    JournalEntryByIdResource,
    LoginResource,
    LogoutResource,
    SignupResource,
)


def register_routes(app):
    """Register all API routes and error handlers."""
    api = Api(app)

    @app.get("/")
    def index():
        return jsonify({"message": "Productivity API is running"})

    @app.errorhandler(AppError)
    def handle_app_error(err):
        return {"errors": [err.message]}, err.status_code

    api.add_resource(SignupResource, "/signup")
    api.add_resource(LoginResource, "/login")
    api.add_resource(CheckSessionResource, "/check_session")
    api.add_resource(LogoutResource, "/logout")
    api.add_resource(JournalEntriesResource, "/journal_entries")
    api.add_resource(JournalEntryByIdResource, "/journal_entries/<int:id>")
