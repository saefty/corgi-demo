"""Date helpers shared by the service."""
import datetime as dt

LOAN_DAYS = 21


def today():
    return dt.date.today()


def format_day(day):
    """A date as members see it, e.g. 'Mon 12 Mar'."""
    return day.strftime("%a %d %b")
