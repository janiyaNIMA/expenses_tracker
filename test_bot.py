import unittest

from bot import ExpensesTrackerBot, build_expenses_table


class BuildExpensesTableTests(unittest.TestCase):
    def test_builds_table_with_latest_entries(self):
        rows = [
            {"id": 5, "description": "Groceries", "amount": 42.5, "created_at": "2026-10-12T10:00:00Z"},
            {"id": 6, "description": "Transport", "amount": 15.0, "created_at": "2026-10-12T12:30:00Z"},
        ]

        table = build_expenses_table(rows)

        self.assertIsNotNone(table)
        self.assertTrue(table.getvalue().startswith(b"\x89PNG"))
        self.assertGreater(len(table.getvalue()), 100)

    def test_bot_class_stores_token(self):
        bot = ExpensesTrackerBot(token="test-token")

        self.assertEqual(bot.token, "test-token")


if __name__ == "__main__":
    unittest.main()
