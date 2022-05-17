import requests
import json
import os

AUTH_URL = "https://api.wk-dev.wdesk.org/iam/v1/oauth2/token"
SS_API_URL = 'https://api.wk-dev.wdesk.org/platform/v1/spreadsheets/'

'''Copy a Sheet within a Spreadsheet to another Spreadsheet.  
Copies only the sheets's content — not any labels, comments, tasks, or formatting 
from a style guide. Unless otherwise specified, the copy appears at the top level of 
its destination spreadsheet, with an index of 0, and with the same name as the original 
sheet

Environment variables:
    DESTINATION_SPREADSHEET_ID - The destination spread sheet id
    DESTINATION_SHEET_NAME - Optionally provide a Destination sheet name
    CLIENT_ID
    CLIENT_SECRET
    SOURCE_SPREADSHEET_ID the source spreadsheet
    SOURCE_SHEET_ID  the sheet to paste into another workbook      
'''

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
SOURCE_SPREADSHEET_ID = os.getenv('SOURCE_SPREADSHEET_ID')
SOURCE_SHEET_ID = os.getenv('SOURCE_SHEET_ID')

## Spreadsheet Destination Parameters
DESTINATION_SPREADSHEET_ID = os.getenv('DESTINATION_SPREADSHEET_ID')
DESTINATION_SHEET_NAME = os.getenv("DESTINATION_SHEET_NAME")

class ApiAuth:
    def __init__(self):
        self._headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
    def getAuthToken(self):
        tokenRes = requests.post(AUTH_URL, data = 'client_id=' + CLIENT_ID + '&client_secret=' + CLIENT_SECRET + '&grant_type=client_credentials', headers = self._headers)
        tokenResponse = json.loads(tokenRes.text)
        return tokenResponse['access_token']

class SSApi:

    def __init__(self, accessToken):
        self._accessToken = 'Bearer ' + accessToken
        self._ssApiUrl = SS_API_URL + SOURCE_SPREADSHEET_ID + "/sheets/" + SOURCE_SHEET_ID + "/copy"
        self._headers = {'Authorization': self._accessToken, 'Content-Type': 'application/json'}

    def copy_sheet(self, sheetId, values):
        url = SS_API_URL + SOURCE_SPREADSHEET_ID + "/sheets/" + sheetId + "/copy"
        print("Copying Sheet: ", url)
        print("Payload values: ", values)
        dataRes = requests.post(url, headers=self._headers, data=json.dumps(values))
        print("Response: ", dataRes.status_code, ' Response Text: ', dataRes.text, ' Request: ', dataRes.request.body, ' Headers: ', dataRes.request.headers)

def copy_sheet(ssApi: SSApi):
    ssApi.copy_sheet(SOURCE_SHEET_ID, {
        "spreadsheet": DESTINATION_SPREADSHEET_ID,
        "sheetName": DESTINATION_SHEET_NAME if DESTINATION_SHEET_NAME is not None else 'Newly Copied Sheet',
        "sheetIndex": -1 # place the at the end of the spreadsheet by default
    })

def main():
    authToken = ApiAuth().getAuthToken()
    ssApi = SSApi(authToken)
    copy_sheet(ssApi)

print('Calling main')
main()