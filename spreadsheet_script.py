import requests
import json
import os

AUTH_URL = "https://api.wk-dev.wdesk.org/iam/v1/oauth2/token"
SS_API_URL = 'https://api.wk-dev.wdesk.org/platform/v1/spreadsheets/'


CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
SPREADSHET_ID = os.getenv('SPREADSHET_ID')
SHEET_ID = os.getenv('SHEET_ID')
HELLO_WORLD = os.getenv('HELLO_WORLD')

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
        self._ssApiUrl = SS_API_URL + SPREADSHET_ID + "/sheets/" + SHEET_ID + "/values/A2:H"
        self._headers = {'Authorization': self._accessToken}

    def getRawData(self):
        dataRes = requests.get(self._ssApiUrl, headers = self._headers)
        # print(dataRes)
        rawData = json.loads(dataRes.text)
        #todo handle pagination
        # print("---", rawData['data'][0]['values'][0])
        return rawData['data'][0]['values']

    def updateRange(self, sheetId, range, values):
        url = SS_API_URL + SPREADSHET_ID + "/sheets/" + sheetId + "/values/" + range
        print("Update Range: ", url)
        print("Values: ", values)
        dataRes = requests.put(url, headers = self._headers, data=json.dumps(values))
        print("Response: ", dataRes.status_code, ' Response Text: ', dataRes.text, ' Request: ', dataRes.request.body, ' Headers: ', dataRes.request.headers)

def write_tier_data(ssApi: SSApi):
    values = []
    values.append([HELLO_WORLD])
    ssApi.updateRange(SHEET_ID, 'A1:ZZZZ99', {"values": values})

def main():
    authToken = ApiAuth().getAuthToken()
    ssApi = SSApi(authToken)
    # rawData = ssApi.getRawData()
    write_tier_data(ssApi)

print('Calling main')
main()