
## Features
- Session-based authentication
- User signup, login, check session, logout
- Password hashing with Flask-Bcrypt
- Journal entries resource with ownership-based authorization
- Paginated index endpoint
- Seed script for sample users and journal entries

## Installation Instructions
1. Move into the backend directory:
   - `cd backend-api`
2. Install dependencies:
   - `pipenv install`
3. Activate virtual environment:
   - `pipenv shell`

## Database Setup (Migrations + Seed)
1. Set Flask app environment variable:
   - `export FLASK_APP=app.py`
2. Initialize migrations (first time only):
   - `flask db init`
3. Generate migration:
   - `flask db migrate -m "initial migration"`
4. Apply migration:
   - `flask db upgrade`
5. Seed sample data:
   - `python seed.py`

## Run Instructions
- Start development server:
  - `flask run --port 5555`

## API Endpoints
- `POST /signup`
  - Creates a user and starts a session.
  - Body: `{ "username": "string", "password": "string", "password_confirmation": "string" }`
- `POST /login`
  - Logs in an existing user and starts a session.
  - Body: `{ "username": "string", "password": "string" }`
- `DELETE /logout`
  - Clears active user session.

- `GET /journal_entries?page=1&per_page=5`
  - Returns paginated journal entries for the current user only.
- `POST /journal_entries`
  - Creates a journal entry for the current user.
  - Body: `{ "title": "string", "content": "string", "mood": "string" }`
- `PATCH /journal_entries/<id>`
  - Updates one of the current user's journal entries.
  - Body can include one or more: `title`, `content`, `mood`
- `DELETE /journal_entries/<id>`
  - Deletes one of the current user's journal entries.

## Status Codes
- `200` successful read/update/login/check session
- `201` successful creation
- `204` successful delete/logout
- `401` unauthorized
- `404` resource not found for current user
- `422` validation errors
