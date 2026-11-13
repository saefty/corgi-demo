import datetime as dt
import unittest

from library.loans import Loan
from library.status import Status, move, status_of

MARCH_1 = dt.date(2026, 3, 1)


class StatusTest(unittest.TestCase):
    def test_a_returned_loan_stays_returned(self):
        with self.assertRaises(ValueError):
            move(Status.RETURNED, Status.BORROWED)

    def test_status_of_a_late_loan(self):
        loan = Loan(id=1, member="ada", book="SICP", email="ada@example.com", borrowed_on=MARCH_1)
        self.assertEqual(status_of(loan, dt.date(2026, 3, 30)), Status.OVERDUE)


if __name__ == "__main__":
    unittest.main()
