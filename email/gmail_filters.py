from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.settings.basic']

def get_gmail_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail filters.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def list_filters(service):
    """List all filters for the authenticated user."""
    try:
        results = service.users().settings().filters().list(userId='me').execute()
        filters = results.get('filter', [])
        
        if not filters:
            print('No filters found.')
            return
        
        print('Filters:')
        for filter in filters:
            print(f"Filter ID: {filter['id']}")
            if 'criteria' in filter:
                criteria = filter['criteria']
                print(f"  From: {criteria.get('from', 'Any')}")
                print(f"  To: {criteria.get('to', 'Any')}")
                print(f"  Subject: {criteria.get('subject', 'Any')}")
                print(f"  Has the words: {criteria.get('hasTheWord', 'None')}")
                print(f"  Doesn't have: {criteria.get('doesNotHaveTheWord', 'None')}")
            if 'action' in filter:
                action = filter['action']
                print(f"  Actions:")
                if 'addLabelIds' in action:
                    print(f"    Add labels: {action['addLabelIds']}")
                if 'removeLabelIds' in action:
                    print(f"    Remove labels: {action['removeLabelIds']}")
                if 'forwardTo' in action:
                    print(f"    Forward to: {action['forwardTo']}")
            print('---')
    except Exception as error:
        print(f'An error occurred: {error}')

def create_filter(service, criteria, actions):
    """Create a new filter with the specified criteria and actions."""
    try:
        filter_body = {
            'criteria': criteria,
            'action': actions
        }
        result = service.users().settings().filters().create(
            userId='me', body=filter_body).execute()
        print(f'Filter created: {result["id"]}')
        return result
    except Exception as error:
        print(f'An error occurred: {error}')
        return None

def delete_filter(service, filter_id):
    """Delete a filter with the specified ID."""
    try:
        service.users().settings().filters().delete(
            userId='me', id=filter_id).execute()
        print(f'Filter {filter_id} deleted successfully.')
    except Exception as error:
        print(f'An error occurred: {error}')

def main():
    service = get_gmail_service()
    
    # Example usage:
    # List all filters
    list_filters(service)
    
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

if __name__ == '__main__':
    main() 