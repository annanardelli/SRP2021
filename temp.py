from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
# Rename the downloaded JSON file to client_secrets.json
# The client_secrets.json file needs to be in the same directory as the script.
gauth = GoogleAuth()
drive = GoogleDrive(gauth)
# List files in Google Drive
fileList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file1 in fileList:
  print('title: %s, id: %s' % (file1['title'], file1['id']))