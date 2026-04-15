from app.errors import NotFoundError, ValidationError
from app.repositories.journal_entry_repository import JournalEntryRepository
from models import JournalEntry


class JournalService:
    def __init__(self, journal_repository=None):
        self.journal_repository = journal_repository or JournalEntryRepository()

    def list_entries(self, user_id, page, per_page):
        pagination = self.journal_repository.paginate_for_user(user_id, page, per_page)
        return {
            "items": pagination.items,
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": pagination.total,
                "pages": pagination.pages,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev,
            },
        }

    def create_entry(self, user_id, payload):
        try:
            entry = JournalEntry(
                title=payload["title"],
                content=payload["content"],
                mood=payload.get("mood"),
                user_id=user_id,
            )
            self.journal_repository.add(entry)
            self.journal_repository.commit()
            return entry
        except ValueError as err:
            self.journal_repository.rollback()
            raise ValidationError(str(err))

    def update_entry(self, entry_id, user_id, payload):
        entry = self.journal_repository.get_by_id_for_user(entry_id, user_id)
        if not entry:
            raise NotFoundError("Journal entry not found")

        if not payload:
            raise ValidationError("No valid fields provided")

        try:
            for field, value in payload.items():
                setattr(entry, field, value)
            self.journal_repository.commit()
            return entry
        except ValueError as err:
            self.journal_repository.rollback()
            raise ValidationError(str(err))

    def delete_entry(self, entry_id, user_id):
        entry = self.journal_repository.get_by_id_for_user(entry_id, user_id)
        if not entry:
            raise NotFoundError("Journal entry not found")

        self.journal_repository.delete(entry)
        self.journal_repository.commit()
