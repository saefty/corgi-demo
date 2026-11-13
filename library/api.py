"""HTTP handlers (framework-free: each takes a dict and returns status and body)."""
from library.dates import format_day
from library.loans import Loan, LoanStore
from library.reminders import overdue

store = LoanStore()


def borrow(req):
    loan = store.add(Loan(id=req["id"], member=req["member"], book=req["book"], email=req["email"]))
    return 201, {"id": loan.id, "due": format_day(loan.due_on)}


def give_back(req):
    store.give_back(req["id"])
    return 200, {"id": req["id"], "returned": True}


def late(req):
    """The front desk's list of overdue loans."""
    return 200, [{"id": l.id, "member": l.member, "book": l.book, "due": format_day(l.due_on)} for l in overdue(store.open_loans())]
