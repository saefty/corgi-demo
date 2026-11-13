import datetime as dt
import unittest

from library.loans import Loan, LoanStore
from library.mailer import Mailer
from library.reminders import overdue, send_reminders

MARCH_1 = dt.date(2026, 3, 1)


class ReminderTest(unittest.TestCase):
    def setUp(self):
        self.store = LoanStore()
        self.store.add(Loan(id=1, member="ada", book="SICP", email="ada@example.com", borrowed_on=MARCH_1))
        self.store.add(Loan(id=2, member="alan", book="TAOCP", email="alan@example.com", borrowed_on=MARCH_1 - dt.timedelta(days=30)))

    def test_reminds_two_days_before_due_once(self):
        mailer = Mailer()
        on = dt.date(2026, 3, 20)  # loan 1 is due on 22 March
        self.assertEqual(send_reminders(self.store, mailer, on), 1)
        self.assertEqual(mailer.outbox[0]["to"], "ada@example.com")
        self.assertEqual(send_reminders(self.store, mailer, on), 0)

    def test_overdue_lists_the_late_loan(self):
        self.assertEqual([l.id for l in overdue(self.store.open_loans(), dt.date(2026, 3, 20))], [2])


if __name__ == "__main__":
    unittest.main()
