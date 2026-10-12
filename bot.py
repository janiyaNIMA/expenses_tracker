import logging
import os
from io import BytesIO

import matplotlib
from dotenv import load_dotenv
from matplotlib import pyplot as plt
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

matplotlib.use("Agg")

# Load environment variables from the .env file
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def build_expenses_table(expenses):
    """Create a PNG image of the latest expenses for Telegram."""
    if not expenses:
        return None

    rows = [
        ["ID", "Description", "Amount", "Date"],
    ]

    for item in expenses:
        rows.append(
            [
                str(item.get("id", "-")),
                str(item.get("description", "-")),
                f"Rs. {float(item.get('amount', 0)):.2f}",
                str(item.get("created_at", "-")),
            ]
        )

    fig, ax = plt.subplots(figsize=(12, max(2.5, 0.7 * len(rows))))
    fig.patch.set_facecolor("white")
    ax.axis("off")

    table = ax.table(
        cellText=rows[1:],
        colLabels=rows[0],
        loc="center",
        cellLoc="center",
        colColours=["#f0f0f0"] * 4,
        fontsize=10,
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.5)

    for (row, col), cell in table.get_celld().items():
        if col == 0:
            cell.set_width(0.12)
        elif col == 1:
            cell.set_width(0.38)
        elif col == 2:
            cell.set_width(0.20)
        elif col == 3:
            cell.set_width(0.30)

    buffer = BytesIO()
    fig.savefig(buffer, format="PNG", bbox_inches="tight", dpi=150)
    plt.close(fig)
    buffer.seek(0)
    return buffer


class ExpensesTrackerBot:
    """Telegram bot entry point for the expense tracker."""

    def __init__(self, token: str | None = None):
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.application = None

    def build(self):
        if not self.token:
            raise RuntimeError("TELEGRAM_BOT_TOKEN is not set.")

        self.application = ApplicationBuilder().token(self.token).build()
        self.application.add_handler(CommandHandler("start", self.start))
        return self.application

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send the latest 10 expenses as an image when the user sends /start."""
        try:
            from main import get_latest_expenses

            expenses = get_latest_expenses(limit=10)
            image = build_expenses_table(expenses)

            if image is None:
                await update.message.reply_text("No expenses found yet.")
                return

            await update.message.reply_photo(photo=image)
        except Exception as exc:
            logging.exception("Failed to send latest expenses image")
            await update.message.reply_text(f"Something went wrong: {exc}")

    def run(self) -> None:
        if not self.token:
            raise RuntimeError("TELEGRAM_BOT_TOKEN is not set.")

        self.application = self.build()
        logging.info("Bot started. Polling for updates...")
        self.application.run_polling()


Bot = ExpensesTrackerBot
