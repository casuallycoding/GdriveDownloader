from __future__ import print_function
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import io
from io import StringIO
from googleapiclient.http import MediaIoBaseDownload




# If modifying these scopes, delete the file token.json. # Scopes https://developers.google.com/drive/api/v2/about-auth
SCOPES = ['https://www.googleapis.com/auth/documents.readonly','https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/drive.readonly']

# The ID of a sample document.
DOCUMENT_ID = '1H2VA9MvMdh96DwSGjN_ecEbxlgCm0STdK_KPxigx8Ag' 

def main():
    """Shows basic usage of the drive API. Downloads a document based on the DocumentID above and iterates through all of the metadata in the share.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

  
    
    downloadService = build('drive', 'v3', credentials=creds)
    results = downloadService.files().list(
        pageSize=10, includeItemsFromAllDrives=True, supportsAllDrives=True, fields="nextPageToken, files(id, name,mimeType,createdTime,name)").execute()
    items = results.get('files', [])
    

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})({2} - {3} - {4})'.format(item['name'], item['id'], item['mimeType'],item['createdTime'],item['name'])) #Metadata formats https://developers.google.com/drive/api/v3/reference/files

    request = downloadService.files().export_media(fileId=DOCUMENT_ID, mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document') # Export formats : https://developers.google.com/drive/api/v3/ref-export-formats
    fh = io.FileIO("test", mode='w')
    
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))


if __name__ == '__main__':
    main()
