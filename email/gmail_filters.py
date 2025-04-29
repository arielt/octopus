"""
Script to manipulate Gmail filters.
"""

from collections import defaultdict
import os.path
import pickle
from datetime import datetime
import tldextract

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

import pandas as pd

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/gmail.settings.basic"]


def get_gmail_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail filters.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("gmail", "v1", credentials=creds)
    return service


def get_filters(service):
    """Get all filters for the authenticated user."""
    results = service.users().settings().filters().list(userId="me").execute()
    filters = results.get("filter", [])
    return filters


def print_filters(filters):
    """Print labels."""
    df = pd.DataFrame(filters)
    print_df(df)


def list_filters(service):
    """List all filters for the authenticated user."""
    results = service.users().settings().filters().list(userId="me").execute()
    filters = results.get("filter", [])

    if not filters:
        print("No filters found.")
        return

    print("Filters:")
    for fltr in filters:
        print(f"Filter ID: {fltr['id']}")
        if "criteria" in fltr:
            criteria = fltr["criteria"]
            print(f"  From: {criteria.get('from', 'Any')}")
            print(f"  To: {criteria.get('to', 'Any')}")
            print(f"  Subject: {criteria.get('subject', 'Any')}")
            print(f"  Has the words: {criteria.get('hasTheWord', 'None')}")
            print(f"  Doesn't have: {criteria.get('doesNotHaveTheWord', 'None')}")
        if "action" in fltr:
            action = fltr["action"]
            print("  Actions:")
            if "addLabelIds" in action:
                print(f"    Add labels: {action['addLabelIds']}")
            if "removeLabelIds" in action:
                print(f"    Remove labels: {action['removeLabelIds']}")
            if "forwardTo" in action:
                print(f"    Forward to: {action['forwardTo']}")
        print("---")


def print_df(df):
    """Print dataframe."""
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_colwidth", None)
    print(df)
    print(f"Total entries: {len(df)}")


def print_dd(dd):
    """Print defaultdict."""
    df = pd.DataFrame.from_dict(dd, orient="index")
    print_df(df)


def analyze_filters(service, filters, labels):
    """Analyze filters."""
    print("Analyzing filters ...")
    label_ids = {label["id"] for label in labels}
    tlds = defaultdict(lambda: {"counter": 0, "criteria": set(), "latest": []})

    for fltr in filters:
        if "criteria" in fltr:
            tld = tldextract.extract(fltr["criteria"]["from"])
            tlds[tld.domain]["counter"] += 1
            from_email = fltr["criteria"]["from"]
            tlds[tld.domain]["criteria"].add(from_email)
            latest = (
                service.users()
                .messages()
                .list(userId="me", q=f"from:{from_email}", maxResults=1)
                .execute()
            )
            if "messages" in latest:
                msg = (
                    service.users()
                    .messages()
                    .get(userId="me", id=latest["messages"][0]["id"])
                    .execute()
                )
                tlds[tld.domain]["latest"].append(
                    datetime.fromtimestamp(int(msg["internalDate"]) / 1000).date()
                )
        if "action" in fltr:
            action = fltr["action"]
            if "addLabelIds" in action:
                for lbl in action["addLabelIds"]:
                    if lbl not in label_ids:
                        print(f"inactive label {lbl}")
            if "removeLabelIds" in action:
                for lbl in action["removeLabelIds"]:
                    if lbl not in label_ids:
                        print(f"inactive label {lbl}")
            if "forwardTo" in action:
                print(f"    Forward to: {action['forwardTo']}")

    print_dd(tlds)
    print("Done analyzing filters.")


def create_filter(service, criteria, actions):
    """Create a new filter with the specified criteria and actions."""

    filter_body = {"criteria": criteria, "action": actions}
    result = (
        service.users()
        .settings()
        .filters()
        .create(userId="me", body=filter_body)
        .execute()
    )
    print(f'Filter created: {result["id"]}')
    return result


def delete_filter(service, filter_id):
    """Delete a filter with the specified ID."""
    service.users().settings().filters().delete(userId="me", id=filter_id).execute()
    print(f"Filter {filter_id} deleted successfully.")


def get_labels(service):
    """Get all labels for the authenticated user."""
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])
    return labels


def print_labels(labels):
    """Print labels."""
    print(f"Labels: {len(labels)} found")
    print("----------------------------------------------------")
    df = pd.DataFrame(labels)
    print_df(df)


def analyze_labels(service, labels):
    """Analyze labels."""
    print("Analyzing labels ...")

    user_labels = list(filter(lambda l: l["type"] == "user", labels))

    for label in user_labels:
        sample_messages = (
            service.users()
            .messages()
            .list(userId="me", labelIds=[label["id"]], maxResults=1)
            .execute()
        )
        if "messages" in sample_messages:
            label["empty"] = ""
            msg = (
                service.users()
                .messages()
                .get(userId="me", id=sample_messages["messages"][0]["id"])
                .execute()
            )
            label["dt"] = datetime.fromtimestamp(int(msg["internalDate"]) / 1000)
        else:
            label["empty"] = "Empty"
            label["dt"] = ""

    potentially_idle_lables = list(
        filter(
            lambda l: l["empty"] or (datetime.now() - l["dt"]).days > 365, user_labels
        )
    )
    if not potentially_idle_lables:
        return

    print("\033[1;31mPotentially idle labels:\033[0m")

    for label in potentially_idle_lables:
        if label["empty"] or (datetime.now() - label["dt"]).days > 365:
            print(
                f"\033[31m{label['name']:<20} {label['empty']:<20} Latest: {label['dt']}\033[0m"
            )
    print("Done analyzing labels.")


def main():
    """
    Script driver.
    """
    service = get_gmail_service()

    labels = get_labels(service)
    print_labels(labels)
    print("\n")
    analyze_labels(service, labels)
    print("\n")

    filters = get_filters(service)
    print_filters(filters)
    print("\n")
    analyze_filters(service, filters, labels)
    # Example of creating a new filter
    # criteria = {
    #     'from': 'example@example.com',
    #     'subject': 'Important'
    # }
    # actions = {
    #     'addLabelIds': ['IMPORTANT'],
    #     'removeLabelIds': ['INBOX']
    # }
    # create_filter(service, criteria, actions)

    # Example of deleting a filter
    # delete_filter(service, 'filter_id_here')


if __name__ == "__main__":
    main()
