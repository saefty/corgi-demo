"""AWS Lambda entry for the front desk: GET /late, with a bearer token."""
import hmac
import json
import os

from library import api

TOKEN = os.environ.get("FRONT_DESK_TOKEN", "")


def handler(event, context):
    auth = (event.get("headers") or {}).get("authorization", "")
    if not auth.startswith("Bearer "):
        return {"statusCode": 401, "body": "missing token"}
    if not hmac.compare_digest(auth[len("Bearer "):], TOKEN):
        return {"statusCode": 403, "body": "wrong token"}
    if event.get("rawPath") != "/late":
        return {"statusCode": 404, "body": "not found"}
    status, body = api.late({})
    return {"statusCode": status, "body": json.dumps(body)}
