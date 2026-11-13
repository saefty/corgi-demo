"""Loans: who borrowed which book, and until when."""
from dataclasses import dataclass, field
import datetime as dt

from library.dates import LOAN_DAYS, today


@dataclass
class Loan:
    id: int
    member: str
    book: str
    email: str
    borrowed_on: dt.date = field(default_factory=today)
    returned_on: dt.date | None = None
    reminded_on: dt.date | None = None

    @property
    def due_on(self):
        return self.borrowed_on + dt.timedelta(days=LOAN_DAYS)

    @property
    def open(self):
        return self.returned_on is None


class LoanStore:
    def __init__(self):
        self._loans = {}

    def add(self, loan):
        self._loans[loan.id] = loan
        return loan

    def get(self, loan_id):
        return self._loans[loan_id]

    def open_loans(self):
        return [l for l in self._loans.values() if l.open]

    def give_back(self, loan_id):
        self._loans[loan_id].returned_on = today()
