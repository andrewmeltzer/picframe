from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import picframe_settings
import picframe_env

class GoogleDriveAccess:
    """
    If the user's photos are on google drive, this class finds them,
    downloads them, and makes them available.
    """

def gdrive_authorize():
    # client_secrets.json needs to be in the same directory as the script
    gauth = GoogleAuth()

    # Try to load saved client credentials
    gauth.LoadCredentialsFile("credentials.json")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.CommandLineAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("credentials.json")
    
    drive = GoogleDrive(gauth)
    fileList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

    print("If the root directory contents show below properly, your authorization has worked.")
    for file in fileList:
        title = file['title']
        file_id = file['id']
        print('title: %s, id: %s' % (file['title'], file['id']))

def main():
    drive = gdrive_authorize()

if __name__ == "__main__":
    main()

