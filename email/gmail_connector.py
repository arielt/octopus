from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_gmail_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
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

    # Build the Gmail service
    service = build("gmail", "v1", credentials=creds)
    return service


def list_messages(service, user_id="me", max_results=10):
    """List all Messages of the user's mailbox matching the query."""
    try:
        response = (
            service.users()
            .messages()
            .list(userId=user_id, maxResults=max_results)
            .execute()
        )

        messages = []
        print('xxx got response')
        print(len(response['messages']))
        print(response)
        if "messages" in response:
            print('extending')
            messages.extend(response["messages"])

        print(response)
        
        # while "nextPageToken" in response:
        #     page_token = response["nextPageToken"]
        #     response = (
        #         service.users()
        #         .messages()
        #         .list(userId=user_id, maxResults=max_results, pageToken=page_token)
        #         .execute()
        #     )
        #     messages.extend(response["messages"])
        
        print('xxx return')
        return messages
    except Exception as error:
        print(f"An error occurred: {error}")
        return None


def get_message(service, user_id, msg_id):
    """Get a Message with given ID."""
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        return message
    except Exception as error:
        print(f"An error occurred: {error}")
        return None


if __name__ == "__main__":
    # Get the Gmail service
    service = get_gmail_service()
    print('xxx built service')

    # List messages
    messages = list_messages(service)
    print('xxx got messages')
    if messages:
        print(f"Found {len(messages)} messages")
        for message in messages:
            msg = get_message(service, "me", message["id"])
            print(f"Message ID: {message['id']}")
            print(f"Subject: {msg['snippet']}")
            print("-" * 50)
