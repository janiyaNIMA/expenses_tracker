# Expenses Tracker

A Flask API and Telegram bot for tracking expenses from a PostgreSQL database.

## Features

- Fetch the latest expense records through a REST API
- Send the latest expenses to Telegram via the `/start` command
- Uses environment variables for secure configuration
- Runs as one app process with the bot starting in the background

## Tech Stack

- Python 3.12+
- Flask
- PostgreSQL
- psycopg2
- python-dotenv
- python-telegram-bot
- Matplotlib

## Project Structure

- `main.py` — Flask application, API routes, and bot startup
- `bot.py` — Telegram bot logic and expense table image generator
- `.env` — local environment configuration
- `sample.env` — example environment file
- `pyproject.toml` — project metadata and dependencies
- `test_bot.py` — tests for the bot behavior

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
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   ```

4. Make sure your PostgreSQL database has an `expenses` table.

## Run locally

```bash
python main.py
```

The API will be available at:

```text
http://localhost:5000/api/expenses/latest
```

The Telegram bot will also start automatically in the background when the app runs.

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

## Telegram Bot

Once the app is running, send `/start` to the bot and it will reply with a table image of the latest expenses.

## Deploy on a VPS with PM2

These steps assume you are deploying to a Linux VPS, such as Ubuntu.

### 1) Install PM2

```bash
sudo npm install -g pm2
```

### 2) Clone or upload the project

```bash
cd /opt
git clone <your-repository-url> expenses-tracker
cd expenses-tracker
```

### 3) Create a virtual environment and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

### 4) Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://user:password@host:5432/database_name
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

### 5) Start the app with PM2

Create a PM2 ecosystem file or run directly:

```bash
pm2 start "source .venv/bin/activate && python main.py" --name expenses-tracker
```

To keep it running after reboot:

```bash
pm2 save
pm2 startup
```

### 6) Check status

```bash
pm2 status
pm2 logs expenses-tracker
```

### 7) Restart or stop the app

```bash
pm2 restart expenses-tracker
pm2 stop expenses-tracker
pm2 delete expenses-tracker
```

## Production notes

- `DATABASE_URL` is required.
- `TELEGRAM_BOT_TOKEN` is required for the Telegram bot to start.
- If the database is unavailable or the table does not exist, the API returns a JSON error response with HTTP 500.
- The app is intended for local development and simple deployments, and PM2 is recommended for continuous VPS hosting.
