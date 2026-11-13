"""AWS Lambda entry for the front desk: GET /late and POST /remind, with a bearer token."""
import hmac
import json
import os

from library import api, consumer
from library.dates import today

TOKEN = os.environ.get("FRONT_DESK_TOKEN", "")


def handler(event, context):
    auth = (event.get("headers") or {}).get("authorization", "")
    if not auth.startswith("Bearer "):
        return {"statusCode": 401, "body": "missing token"}
    if not hmac.compare_digest(auth[len("Bearer "):], TOKEN):
        return {"statusCode": 403, "body": "wrong token"}
    if event.get("rawPath") == "/remind":
        # The front desk wants the mail out at once, so skip the queue for this one loan.
        loan_id = json.loads(event.get("body") or "{}")["id"]
        consumer.handle({"type": "loan.reminded", "loan_id": loan_id, "on": today().isoformat()})
        return {"statusCode": 202, "body": json.dumps({"id": loan_id, "reminded": True})}
    if event.get("rawPath") != "/late":
        return {"statusCode": 404, "body": "not found"}
    status, body = api.late({})
    return {"statusCode": status, "body": json.dumps(body)}
