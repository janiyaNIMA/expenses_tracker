import unittest

from bot import build_expenses_table


class BuildExpensesTableTests(unittest.TestCase):
    def test_builds_table_with_latest_entries(self):
        rows = [
            {"id": 5, "description": "Groceries", "amount": 42.5, "created_at": "2026-10-12T10:00:00Z"},
            {"id": 6, "description": "Transport", "amount": 15.0, "created_at": "2026-10-12T12:30:00Z"},
        ]

        table = build_expenses_table(rows)

        self.assertIn("ID", table)
        self.assertIn("Groceries", table)
        self.assertIn("42.50", table)
        self.assertIn("Transport", table)
        self.assertIn("15.00", table)


if __name__ == "__main__":
    unittest.main()
