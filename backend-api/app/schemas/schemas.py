from marshmallow import Schema, ValidationError as MarshmallowValidationError, fields, validate, validates_schema

from app.errors import ValidationError


class UserSchema(Schema):
    id = fields.Int(required=True)
    username = fields.Str(required=True)


class SignupSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=6))
    password_confirmation = fields.Str(required=True)

    @validates_schema
    def validate_password_confirmation(self, data, **kwargs):
        if data.get("password") != data.get("password_confirmation"):
            raise MarshmallowValidationError("Password confirmation must match password", "password_confirmation")


class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class JournalEntryCreateSchema(Schema):
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    mood = fields.Str(required=False)


class JournalEntryUpdateSchema(Schema):
    title = fields.Str(required=False)
    content = fields.Str(required=False)
    mood = fields.Str(required=False)


class PaginationQuerySchema(Schema):
    page = fields.Int(required=False)
    per_page = fields.Int(required=False)


class JournalEntrySchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    mood = fields.Str(allow_none=True)
    created_at = fields.Str(required=True)
    updated_at = fields.Str(required=True)
    user_id = fields.Int(required=True)


def load_or_raise(schema, payload):
    try:
        return schema.load(payload or {})
    except MarshmallowValidationError as err:
        first_message = next(iter(err.messages.values()))
