from models import JournalEntry
from app.config import db


class JournalEntryRepository:
    def paginate_for_user(self, user_id, page, per_page):
        return (
            JournalEntry.query.filter_by(user_id=user_id)
            .order_by(JournalEntry.created_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )

    def get_by_id_for_user(self, entry_id, user_id):
        return JournalEntry.query.filter_by(id=entry_id, user_id=user_id).first()

    def add(self, entry):
        db.session.add(entry)

    def delete(self, entry):
        db.session.delete(entry)

    def commit(self):
        db.session.commit()

    def rollback(self):
        db.session.rollback()
