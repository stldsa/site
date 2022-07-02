import requests


def create(subject, body, from_, reply_to, api_token):
    return requests.post(
        "https://actionnetwork.org/api/v2/messages",
        headers={"OSDI-API-Token": api_token},
        data={
            "subject": subject,
            "body": body,
            "from": from_,
            "reply_to": reply_to,
        },
    )
