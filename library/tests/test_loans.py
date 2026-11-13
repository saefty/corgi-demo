import datetime as dt
import unittest

from library.loans import Loan, LoanStore


class LoanTest(unittest.TestCase):
    def test_due_after_21_days(self):
        loan = Loan(id=1, member="ada", book="SICP", email="ada@example.com", borrowed_on=dt.date(2026, 3, 1))
        self.assertEqual(loan.due_on, dt.date(2026, 3, 22))

    def test_give_back_closes_the_loan(self):
        store = LoanStore()
        store.add(Loan(id=1, member="ada", book="SICP", email="ada@example.com"))
        store.give_back(1)
        self.assertEqual(store.open_loans(), [])


if __name__ == "__main__":
    unittest.main()
