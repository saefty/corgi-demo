"""A loan's status, the moves allowed between them, and the event each move publishes."""
from enum import Enum

from library.events import LoanEvent


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


EVENTS = {Status.REMINDED: "loan.reminded", Status.OVERDUE: "loan.overdue", Status.RETURNED: "loan.returned"}


def transition(loan, new, queue, on):
    """Moves a loan to a new status and publishes the event for it. The only place a status changes."""
    move(status_of(loan, on), new)
    if new is Status.REMINDED:
        loan.reminded_on = on
    if new is Status.RETURNED:
        loan.returned_on = on
    queue.publish(LoanEvent(EVENTS[new], loan.id, on.isoformat()))
    return new
