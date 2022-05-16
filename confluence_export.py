# Welcome to Workiva Scripting
import mimetypes
import os
import re
import requests
import time

#HOST = 'api.app.wdesk.com'
HOST = 'api.wk-dev.wdesk.org'
AUTH_API_HOST = 'https://api.wk-dev.wdesk.org/iam/v1/oauth2/token'
EXPORT_DOCUMENT_TEMPLATE = 'https://{}/platform/v1/documents/{}/export'
EXPORT_PROTO_DOCUMENT_TEMPLATE = 'https://{}/prototype/platform/documents/{}/export'
XHTML = True

def main():
    document_id = os.getenv('DOCUMENT_ID')
    if not document_id:
        document_id = '24c9d74575a5412a99d040d66c0cfa7b'

    if XHTML:
        format_data = {'format': 'xhtml', 'xhtmlOptions': {'includeExternalHyperlinks': True}}
        url = EXPORT_PROTO_DOCUMENT_TEMPLATE.format(HOST, document_id)
    else:
        format_data = {'format': 'pdf'}
        url = EXPORT_DOCUMENT_TEMPLATE.format(HOST, document_id)
    headers = rebuild_json_headers()
    response = requests.post(url, json=format_data, headers=headers)

    if response is not None and response.status_code == 401:
        print('401 - refreshing token to retry')
        headers = rebuild_json_headers()
        response = requests.post(url, json=format_data, headers=headers)
    # This response should have a Location header
    job_location = response.headers.get('Location')
    if job_location:
        response = poll_for_completion(job_location, headers)
        if response and response.status_code < 300:
            d = response.headers.get('content-disposition')
            fname = re.findall("filename=(.+)", d)[0].strip(';"')
            print('file {} exported from Wdesk'.format(fname))
            mimetype = mimetypes.guess_type(fname)
            files = {'file': (fname, response.content, mimetype)}
            #print('confluence input: {}'.format(files))
            write_file_to_confluence(files)
            print('wrote {}'.format(fname))
        else:
            print('failed response on job location {}'.format(job_location))
    else:
        print('no job location, failed call')

def rebuild_json_headers():
    token = get_access_token()
    return {'Authorization': 'Bearer ' + token, 'content-type': 'application/vnd.api+json'}

def poll_for_completion(job_location, headers):
    sleep_between = 2
    retries = 0
    while retries < 30:
        response = requests.get(job_location, headers=headers)
        if response is not None and response.status_code == 401:  # try to refresh token and retry once.
            print('401 - refreshing token to retry')
            headers = rebuild_json_headers()
            response = requests.get(job_location, headers=headers)
        if response is not None and response.status_code < 300 and response.json().get('resourceUrl'):
            #print('resource url response {}'.format(response.text))
            final_signed_url = response.json().get('resourceUrl')
            response = requests.get(final_signed_url, headers=headers)
            #print('resource url response {}'.format(response.text))
            if response is not None and response.status_code == 401:  # try to refresh token and retry once.
                print('401 - refreshing token to retry')
                headers = rebuild_json_headers()
                response = requests.get(final_signed_url, headers=headers)
            return response
        elif response is not None and response.status_code < 300 and response.json().get('status') == 'failed':
            print('failed url response {}'.format(response.text))
            break
        time.sleep(sleep_between)
        retries += 1
        if retries == 15: # at 30 seconds of waiting, bump to 5 seconds
            sleep_between = 5
        elif retries == 21: # at 1 minutes of waiting, bump to 10 seconds
            sleep_between = 10
        elif retries == 27:  # at 2 minutes of waiting, bump to 30 seconds
            sleep_between = 60
    return None

def get_access_token():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = 'client_id={}&client_secret={}&grant_type=client_credentials'.format(CLIENT_ID, CLIENT_SECRET)
    result = requests.post(AUTH_API_HOST, data=data, headers=headers)
    auth_response = result.json()
    # print(auth_response.get('access_token'))
    return auth_response.get('access_token')

def write_file_to_confluence(files):
    """accepts files = {'file': ('test.csv', open('test.csv', 'rb'), 'text/csv')}"""
    headers = {'Authorization': 'Bearer {}'.format(confluence_personal_access_token),
               'X-Atlassian-Token': 'nocheck'}
    URL = 'https://wiki.atl.workiva.net/rest/api/content/{}/child/attachment'.format(confluence_page_id)

    #files = {'file': ('test.csv', open('test.csv', 'rb'), 'text/csv')}
    result = requests.post(URL, files=files, headers=headers)
    print('result status {} response {}'.format(result.status_code, result.text))

CLIENT_ID = '<redacted>'
CLIENT_SECRET = '<redacted>'
confluence_page_id = '236359427'
confluence_personal_access_token = '<redacted>'

main()