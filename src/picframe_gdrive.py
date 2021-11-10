from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from picframe_settings import PFSettings
from picframe_env import PFEnv

class PicframeGoogleDrive:
    """
    If the user's photos are on google drive, this class finds them,
    downloads them, and makes them available.
    """

    ############################################################
    #
    # __init__
    #
    def __init__(self):
        self.drive = self.gdrive_authorize()
        self.id_list = []
        self.get_photo_list()

        # ++++ Turn this into debug logging
        print(self.id_list)

    ############################################################
    #
    # gdrive_authorize
    #
    def gdrive_authorize(self):
        """
        Connect to google to authorize the user.
        Note: client_secrets.json needs to be in the same directory as the script
        Returns: the google drive handle
        """
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
        return drive
    
    
    
    ############################################################
    #
    # get_children
    #
    def get_children(self,parent_id):
        """
        Get the list of children from a parent node.
        Inputs:
            parent_id: The parent folder to look at to get the children.

        Returns:
            List of children.
        """

        str = "\'" + parent_id + "\'" + " in parents and trashed=false"
        file_list = self.drive.ListFile({'q': str}).GetList()
        return file_list
    
    ############################################################
    #
    # add_children
    #
    def add_children(self, in_desired_folder, file_list, parent_id):
        """
        Add children to the id_list if they are of the right format.
        Input:
            in_desired_folder:
            file_list:
            parent_id:
        """

        for file in file_list:
            # Save the desired files in the id_list if they are not 
            # directories
            # ++++ Check to see if the extension is a supported one
            if in_desired_folder:
                self.id_list.append(file['title'])
    
            # ++++ Turn this into a DEBUG logging thing.
            print('parent: %s, title: %s, id: %s' % (parent_id, file['title'], file['id']))
    
    ############################################################
    #
    # process_children
    #
    def process_children(self, in_desired_folder, parent_id):
        """
        Go down the tree until you reach a leaf 
        """
        children = self.get_children(parent_id)
        self.add_children(in_desired_folder, children, parent_id)
        if(len(children) > 0):
            for child in children:
                if child['title'] == PFSettings.gdrive_photos_folder or in_desired_folder == True:
                    self.process_children(True, child['id'])
                else:
                    self.process_children(False, child['id'])
    
    
    ############################################################
    #
    # Get the full list of photos from gdrive
    # ++++ Maybe set it up so it only does a directory at a time?
    #
    def get_photo_list(self):
        """
        Get the list of photos from a google drive folder hierarchy.
        """

        in_desired_folder = False
    
        # List files in Google Drive
        fileList = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file in fileList:
            title = file['title']
            file_id = file['id']
            if title == PFSettings.gdrive_root_folder:
                self.process_children(in_desired_folder, file_id)
    
