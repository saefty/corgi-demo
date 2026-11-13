"""HTTP handlers (framework-free: each takes a dict and returns status and body)."""
from library.dates import fmt_date
from library.loans import Loan, LoanStore

store = LoanStore()


def borrow(req):
    loan = store.add(Loan(id=req["id"], member=req["member"], book=req["book"], email=req["email"]))
    return 201, {"id": loan.id, "due": fmt_date(loan.due_on)}


def give_back(req):
    store.give_back(req["id"])
    return 200, {"id": req["id"], "returned": True}
