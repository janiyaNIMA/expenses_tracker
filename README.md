# Expenses Tracker

A simple Flask API for retrieving the latest expenses from a PostgreSQL database.

## Features

- Fetch the last 10 expense records
- Uses environment variables for database configuration
- Built with Flask and PostgreSQL

## Tech Stack

- Python 3.12+
- Flask
- PostgreSQL
- psycopg2
- python-dotenv

## Project Structure

- `main.py` — Flask application and API route
- `.env` — local environment configuration
- `sample.env` — example environment file
- `pyproject.toml` — project metadata and dependencies

## Setup

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -e .
   ```

3. Create a `.env` file based on `sample.env`:

   ```env
   DATABASE_URL=postgresql://username:password@host:5432/database_name
   ```

4. Make sure your PostgreSQL database has an `expenses` table.

## Run the app

```bash
python main.py
```

The API will be available at:

```text
http://localhost:5000/api/expenses/latest
```

## API Endpoint

### GET /api/expenses/latest

Returns the latest 10 expenses from the `expenses` table, ordered by `id` descending.

Example response:

```json
[
  {
    "id": 15,
    "amount": 49.99,
    "description": "Groceries",
    "created_at": "2026-10-11T12:34:56Z"
  }
]
```

## Notes

- `DATABASE_URL` is required.
- If the database is unavailable or the table does not exist, the API returns a JSON error response with HTTP 500.
- The app is intended for local development and simple API usage.
