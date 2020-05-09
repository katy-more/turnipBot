from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
load_dotenv()
SPREADSHEET_ID = os.getenv('TURNIP_SPREADSHEET_ID')
RANGE_NAME = os.getenv('TEST_RANGE')
usernameToRow = None


def api_setup():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values = result.get('values', [])

    return sheet

def username_update(sheet):
    global usernameToRow

    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME
    ).execute()

    # If usernameToRow has data, delete it and start over
    usernameToRow = {}

    # The range starts at 3 to account for blank lines in the
    # spreadsheet. Different spreadsheets may vary
    for row in range(3, len(result.get('values', []))):
        usernameToRow[result.get('values', [])[row][0]] = row+1
        # TODO: This is hard to read! Fix that at some point ^^^

def insert_by_username_date(sheet, username, date, value):
    global usernameToRow

    # create the dict that will align the day of the week to the column
    # Note: These values are specific to the spreadsheet that I'm
    # building this spreadsheet around, and may need to be tweaked
    # for wider use
    dayToColumn = {
        1:{# Monday
            "am":"C",
            "pm":"D"
        },
        2:{# Tuesday
            "am": "E",
            "pm": "F"
        },
        3:{# Wednesday
            "am": "G",
            "pm": "H"
        },
        4:{# Thursday
            "am": "I",
            "pm": "J"
        },
        5:{#Friday
            "am": "K",
            "pm": "L"
        },
        6:{#Saturday
            "am": "M",
            "pm": "N"
        }
    }

    # Create the 'values' object that will be passed to the Google API
    values = [
        [
            value[1]
        ]
    ]

    # Create the body based on the values
    body = {
        'values': values
    }

    # Create the range based on the parameter data
    day = None
    if date.weekday() == 0:  # if the day of the week is Sunday
        day = "B"
    else:
        day = dayToColumn[date.weekday()][value[0]]

    range = "test!" + str(day) + str(usernameToRow[username])

    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range = range,
        valueInputOption = 'RAW',
        body = body
    ).execute()


if __name__ == '__main__':
    api_setup()
