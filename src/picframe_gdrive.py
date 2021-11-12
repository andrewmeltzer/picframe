
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
    initialized = False
    drive = None
    full_id_list_style = False
    id_list = []

    ############################################################
    #
    # init
    #
    @staticmethod
    def init():

        if not PicframeGoogleDrive.initialized:
            PicframeGoogleDrive.drive = PicframeGoogleDrive.gdrive_authorize()

        if PicframeGoogleDrive.full_id_list_style == True:
            PicframeGoogleDrive.get_photo_list()
        
        PicframeGoogleDrive.initialized = True

    ############################################################
    #
    # gdrive_authorize
    #
    @staticmethod
    def gdrive_authorize():
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
    @staticmethod
    def get_children(parent_id):
        """
        Get the list of children from a parent node.
        Inputs:
            parent_id: The parent folder to look at to get the children.

        Returns:
            List of children.
        """

        str = "\'" + parent_id + "\'" + " in parents and trashed=false"
        children = PicframeGoogleDrive.drive.ListFile({'q': str}).GetList()
        return children
    
    ############################################################
    #
    # process_children
    #
    @staticmethod
    def process_children(in_desired_folder, parent_name, parent_id):
        """
        Recursively walk the directory hierarchy to get the next photo
        Use a generator (yield and yield from) to return files as they
        are found, otherwise very large google drives will be way too
        slow and unwieldy.
        """
        children = PicframeGoogleDrive.get_children(parent_id)

        # If there are no children, then at a leaf, so see if it should
        # be added to the list
        if len(children) <= 0:
            if PFEnv.is_format_supported(parent_name) and in_desired_folder:
                if PicframeGoogleDrive.full_id_list_style:
                    PicframeGoogleDrive.id_list.append(parent_name)
                else:
                    # Here download the file and put it into the right
                    # location as stored in PFEnv (/tmp/blah for linux, 
                    # C:\temp? for windows, then return the full path.
                    yield parent_name

                logging.info(f"Returning {parent_name}")
            
        # Otherwise go through the list of subdirectories of this directory
        for child in children:
            child_name = child['title']
            child_id = child['id']
            logging.debug('title: %s, id: %s' % (child_name, child_id))

            if child_name == PFSettings.gdrive_photos_folder or in_desired_folder == True:
                yield from PicframeGoogleDrive.process_children(True, child_name, child_id)
            else:
                yield from PicframeGoogleDrive.process_children(False, child_name, child_id)
    
        return None
    
    ############################################################
    #
    # get_next_photo
    #
    @staticmethod
    def get_next_photo():
        """
        Get the list of photos from a google drive folder hierarchy.
        """

        in_desired_folder = False
    
        # List files in Google Drive
        file_list = PicframeGoogleDrive.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file in file_list:
            title = file['title']
            file_id = file['id']
            if title == PFSettings.gdrive_root_folder:
                if title == PFSettings.gdrive_photos_folder:
                    in_desired_folder = True
                yield from PicframeGoogleDrive.process_children(in_desired_folder, title, file_id)
        return None
    
