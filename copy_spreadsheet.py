import requests
import json
import os

AUTH_URL = "https://api.wk-dev.wdesk.org/iam/v1/oauth2/token"
SS_API_URL = 'https://api.wk-dev.wdesk.org/platform/v1/spreadsheets/'

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
SHEET_ID = os.getenv('SHEET_ID')

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
        self._ssApiUrl = SS_API_URL + SPREADSHEET_ID + "/sheets/" + SHEET_ID + "/copy/"
        self._headers = {'Authorization': self._accessToken}

    def copySheet(self, sheetId):
        url = SS_API_URL + SPREADSHEET_ID + "/sheets/" + sheetId + "/values/" + range
        # print("Update Cell: ", url)
        # print("Values: ", values)
        dataRes = requests.put(url, headers = self._headers, data=json.dumps(values))
        print("Response: ", dataRes.status_code, ' Response Text: ', dataRes.text, ' Request: ', dataRes.request.body, ' Headers: ', dataRes.request.headers)

def copy_sheet(ssApi: SSApi):
    ssApi.copySheet(SHEET_ID)

def main():
    authToken = ApiAuth().getAuthToken()
    ssApi = SSApi(authToken)
    # rawData = ssApi.getRawData()

print('Calling main')
main()