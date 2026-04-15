from faker import Faker

from app import create_app
from app.config import db
from models import JournalEntry, User

fake = Faker()


def seed_data():
    app = create_app()

    with app.app_context():
        JournalEntry.query.delete()
        User.query.delete()

        users = []
        for i in range(3):
            user = User(username=f"user{i + 1}")
            user.password_hash = "password123"
            users.append(user)

        db.session.add_all(users)
        db.session.commit()

        entries = []
        for user in users:
            for _ in range(5):
                entries.append(
                    JournalEntry(
                        title=fake.sentence(nb_words=5),
                        content=fake.paragraph(nb_sentences=3),
                        mood=fake.random_element(elements=("focused", "calm", "stressed", "motivated")),
                        user_id=user.id,
                    )
                )

        db.session.add_all(entries)
        db.session.commit()
        print("Seeding complete")


if __name__ == "__main__":
    seed_data()
