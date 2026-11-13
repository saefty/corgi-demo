"""Reminder consumer Lambda: reads loan events from the queue and mails the member."""
import json

from library import api
from library.dates import format_day, today
from library.mailer import Mailer

mailer = Mailer()


def handler(event, context):
    records = event.get("Records", [])
    for record in records:
        handle(json.loads(record["body"]))
    return {"handled": len(records)}


def handle(message):
    loan = api.store.get(message["loan_id"])
    if message["type"] == "loan.reminded":
        mailer.send(loan.email, f"Please return {loan.book}",
                    f"Hi {loan.member}, {loan.book} is due on {format_day(loan.due_on)}.")
        loan.reminded_on = today()
    elif message["type"] == "loan.overdue":
        mailer.send(loan.email, f"{loan.book} is overdue",
                    f"Hi {loan.member}, {loan.book} was due on {format_day(loan.due_on)}.")
