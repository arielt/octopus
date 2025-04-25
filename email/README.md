# Gmail Connector

This Python script allows you to connect to and retrieve emails from your Gmail account using the Gmail API.

## Setup Instructions

1. First, install the required dependencies:
```shell
pip install -r packages.lst
```

2. Set up Gmail API credentials:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Gmail API for your project
   - Go to "Credentials" and create an OAuth 2.0 Client ID
   - Download the credentials and save them as `credentials.json` in the same directory as the script

3. Run the script:
```shell
python gmail_connector.py
```

## Features

- Authenticates with Gmail using OAuth 2.0
- Lists recent emails from your inbox
- Retrieves full message details
- Handles token refresh automatically

## Security Note

- The `token.pickle` file stores your access and refresh tokens. Keep this file secure and do not share it.
- The `credentials.json` file contains your OAuth 2.0 client credentials. Keep this file secure and do not share it.

## Customization

You can modify the `SCOPES` variable in the script to request different permissions:
- `https://www.googleapis.com/auth/gmail.readonly` - Read-only access
- `https://www.googleapis.com/auth/gmail.modify` - Read and modify access
- `https://www.googleapis.com/auth/gmail.compose` - Compose and send emails
- `https://www.googleapis.com/auth/gmail.send` - Send emails only 