# Calendar

## Google calendar

### Install packages
```shell
pip install -r packages.lst
```

### Setup credentials
  - Go to the Google Cloud Console (https://console.cloud.google.com/)
  - Create a new project or select an existing one
  - Enable the `Google Calendar API` for your project
  - Create OAuth 2.0 credentials `Desktop application`
  - Download the credentials and save them as credentials.json
  - Add user in Google Auth Platform → Audience → Test users

### Execute
```shell
python google_calendar_import.py
```