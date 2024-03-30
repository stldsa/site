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


def edit(action_network_href, put_data, api_token):
    return requests.put(
        action_network_href, headers={"OSDI-API-Token": api_token}, data=put_data
    )


def schedule(endpoint, scheduled_start_date, api_token):
    return requests.post(
        endpoint,
        headers={"OSDI-API-Token": api_token},
        data={"scheduled_start_date": scheduled_start_date},
    )
