"""Loan events: what happened to a loan, for anything that reacts to it."""
from dataclasses import asdict, dataclass
import json


@dataclass(frozen=True)
class LoanEvent:
    type: str  # "loan.reminded", "loan.overdue" or "loan.returned"
    loan_id: int
    on: str  # the day it happened, as an ISO date


class Queue:
    """The loan-events queue (a list in tests, SQS in production)."""

    def __init__(self, messages=None):
        self.messages = messages if messages is not None else []

    def publish(self, event):
        self.messages.append(json.dumps(asdict(event)))
