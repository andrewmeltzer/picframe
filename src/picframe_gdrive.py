
import logging
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
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
        
        logging.debug(self.id_list)

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
        children = self.drive.ListFile({'q': str}).GetList()
        return children
    
    ############################################################
    #
    # process_children
    #
    def process_children(self, in_desired_folder, parent_name, parent_id):
        """
        Go down the tree until you reach a leaf 
        """
        children = self.get_children(parent_id)

        # If there are no children, then at a leaf, so see if it should
        # be added to the list
        if len(children) <= 0:
            if PFEnv.is_format_supported(parent_name) and in_desired_folder:
                self.id_list.append(parent_name)
            
        # Otherwise go through the list of subdirectories of this directory
        for child in children:
            child_name = child['title']
            child_id = child['id']
            logging.debug('title: %s, id: %s' % (child_name, child_id))

            if child_name == PFSettings.gdrive_photos_folder or in_desired_folder == True:
                self.process_children(True, child_name, child_id)
            else:
                self.process_children(False, child_name, child_id)
    
    
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
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file in file_list:
            title = file['title']
            file_id = file['id']
            if title == PFSettings.gdrive_root_folder:
                if title == PFSettings.gdrive_photos_folder:
                    in_desired_folder = True
                self.process_children(in_desired_folder, title, file_id)
    
