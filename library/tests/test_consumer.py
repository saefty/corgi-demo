import datetime as dt
import json
import unittest

from library import api, consumer
from library.loans import Loan


class ConsumerTest(unittest.TestCase):
    def setUp(self):
        api.store.add(Loan(id=7, member="ada", book="SICP", email="ada@example.com", borrowed_on=dt.date(2026, 3, 1)))
        consumer.mailer.outbox.clear()

    def test_a_reminded_event_mails_the_member(self):
        body = json.dumps({"type": "loan.reminded", "loan_id": 7, "on": "2026-03-20"})
        self.assertEqual(consumer.handler({"Records": [{"body": body}]}, None), {"handled": 1})
        self.assertEqual(consumer.mailer.outbox[0]["to"], "ada@example.com")


if __name__ == "__main__":
    unittest.main()
