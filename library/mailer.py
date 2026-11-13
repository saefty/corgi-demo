"""Sends mail through the outbox (a list in tests, SMTP in production)."""
import logging
import time

log = logging.getLogger(__name__)
RETRIES = 3


class Mailer:
    def __init__(self, outbox=None):
        self.outbox = outbox if outbox is not None else []

    def send(self, to, subject, body):
        for attempt in range(RETRIES):
            try:
                self.outbox.append({"to": to, "subject": subject, "body": body})
                log.debug("mail to %s: %s", to, subject)
                return
            except OSError:
                time.sleep(2 ** attempt)
