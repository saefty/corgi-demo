import datetime as dt
import json
import unittest

from library.events import Queue
from library.loans import Loan
from library.status import Status, transition

MARCH_1 = dt.date(2026, 3, 1)


class EventTest(unittest.TestCase):
    def setUp(self):
        self.loan = Loan(id=1, member="ada", book="SICP", email="ada@example.com", borrowed_on=MARCH_1)
        self.queue = Queue()

    def test_a_reminded_loan_publishes_one_event(self):
        transition(self.loan, Status.REMINDED, self.queue, dt.date(2026, 3, 20))
        self.assertEqual([json.loads(m) for m in self.queue.messages],
                         [{"type": "loan.reminded", "loan_id": 1, "on": "2026-03-20"}])

    def test_a_returned_loan_publishes_nothing_more(self):
        transition(self.loan, Status.RETURNED, self.queue, dt.date(2026, 3, 10))
        with self.assertRaises(ValueError):
            transition(self.loan, Status.REMINDED, self.queue, dt.date(2026, 3, 20))
        self.assertEqual(len(self.queue.messages), 1)


if __name__ == "__main__":
    unittest.main()
