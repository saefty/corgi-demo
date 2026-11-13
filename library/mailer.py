"""Sends mail through the outbox (a list in tests, SMTP in production)."""
import logging

log = logging.getLogger(__name__)


class Mailer:
    def __init__(self, outbox=None):
        self.outbox = outbox if outbox is not None else []

    def send(self, to, subject, body):
        self.outbox.append({"to": to, "subject": subject, "body": body})
        log.info("mail to %s: %s", to, subject)
