"""Reminder mails: two days before a loan is due, once per loan."""
import datetime as dt

from library.dates import format_day, today

REMIND_DAYS = 2


def due_soon(loans, on=None):
    """Open loans due in exactly REMIND_DAYS days that got no reminder yet."""
    day = (on or today()) + dt.timedelta(days=REMIND_DAYS)
    return [l for l in loans if l.open and l.due_on == day and l.reminded_on is None]


def send_reminders(store, mailer, on=None):
    """Mails each member whose loan is due soon and marks the loan as reminded. Returns how many were sent."""
    sent = 0
    for loan in due_soon(store.open_loans(), on):
        mailer.send(loan.email, f"Please return {loan.book}",
                    f"Hi {loan.member}, {loan.book} is due on {format_day(loan.due_on)}.")
        loan.reminded_on = on or today()
        sent += 1
    return sent


def overdue(loans, on=None):
    """Open loans past their due date, the longest overdue first."""
    day = on or today()
    return sorted((l for l in loans if l.open and l.due_on < day), key=lambda l: l.due_on)
