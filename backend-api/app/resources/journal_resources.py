from flask import request
from flask_restful import Resource

from app.schemas.schemas import (
    JournalEntryCreateSchema,
    JournalEntrySchema,
    JournalEntryUpdateSchema,
    PaginationQuerySchema,
    load_or_raise,
)
from app.services.journal_service import JournalService
from app.validator.authenticator import SessionAuthenticator


class JournalEntriesResource(Resource):
    def __init__(self):
        self.authenticator = SessionAuthenticator()
        self.journal_service = JournalService()
        self.pagination_schema = PaginationQuerySchema()
        self.entry_create_schema = JournalEntryCreateSchema()
        self.entry_schema = JournalEntrySchema()

    def get(self):
        user = self.authenticator.require_user()
        query = load_or_raise(self.pagination_schema, request.args.to_dict())

        result = self.journal_service.list_entries(
            user_id=user.id,
            page=query["page"],
            per_page=query["per_page"],
        )
        return {
            "data": self.entry_schema.dump(result["items"], many=True),
            "pagination": result["pagination"],
        }, 200

    def post(self):
        user = self.authenticator.require_user()
        payload = load_or_raise(self.entry_create_schema, request.get_json())

        entry = self.journal_service.create_entry(user_id=user.id, payload=payload)
        return self.entry_schema.dump(entry), 201


class JournalEntryByIdResource(Resource):
    def __init__(self):
        self.authenticator = SessionAuthenticator()
        self.journal_service = JournalService()
        self.entry_update_schema = JournalEntryUpdateSchema()
        self.entry_schema = JournalEntrySchema()

    def patch(self, id):
        user = self.authenticator.require_user()
        payload = load_or_raise(self.entry_update_schema, request.get_json())

        entry = self.journal_service.update_entry(entry_id=id, user_id=user.id, payload=payload)
        return self.entry_schema.dump(entry), 200

    def delete(self, id):
        user = self.authenticator.require_user()
        self.journal_service.delete_entry(entry_id=id, user_id=user.id)
        return {}, 204
