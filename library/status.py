"""A loan's status and the moves allowed between them."""
from enum import Enum


class Status(str, Enum):
    BORROWED = "borrowed"
    REMINDED = "reminded"
    OVERDUE = "overdue"
    RETURNED = "returned"


MOVES = {
    Status.BORROWED: {Status.REMINDED, Status.OVERDUE, Status.RETURNED},
    Status.REMINDED: {Status.OVERDUE, Status.RETURNED},
    Status.OVERDUE: {Status.RETURNED},
    Status.RETURNED: set(),
}


def move(current, new):
    """The new status, if a loan may go there from the current one."""
    if new not in MOVES[current]:
        raise ValueError(f"a loan can't go from {current.value} to {new.value}")
    return new


def status_of(loan, on):
    """Where a loan stands on a given day."""
    if loan.returned_on is not None:
        return Status.RETURNED
    if loan.due_on < on:
        return Status.OVERDUE
    if loan.reminded_on is not None:
        return Status.REMINDED
    return Status.BORROWED
