# Project Picframe
# Copyright 2021, Alef Solutions, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

"""
picframe_gdrive.py

This file implements the code necessary to pull files from google drive. 
It uses a generator so only one file (rather than all at once) can be
pulled.

"""

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from picframe_settings import PFSettings
from picframe_env import PFEnv, NoImagesFoundException
from picframe_message import PFMessage


class PFGoogleDrive:
    """
    If the user's photos are on google drive, this class finds them,
    downloads them, and makes them available.
    """
    initialized = False
    drive = None
    full_id_list_style = False
    id_list = []
    image_file_count = 0

    ############################################################
    #
    # init
    #
    @staticmethod
    def init():
        """
        Initialize the static variables for this class.
        """

        if not PFGoogleDrive.initialized:
            PFGoogleDrive.drive = PFGoogleDrive.gdrive_authorize()

        PFGoogleDrive.initialized = True

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

        c_str = "\'" + parent_id + "\'" + " in parents and trashed=false"
        children = PFGoogleDrive.drive.ListFile({'q': c_str}).GetList()
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
        children = PFGoogleDrive.get_children(parent_id)

        # If there are no children, then at a leaf, so see if it should
        # be added to the list
        if len(children) <= 0:
            if PFEnv.is_format_supported(parent_name) and in_desired_folder:
                PFEnv.logger.debug("Returning %s" % (parent_name,))
                if PFGoogleDrive.full_id_list_style:
                    PFGoogleDrive.id_list.append(parent_name)
                else:
                    # Here download the file and put it into the right
                    # location as stored in PFEnv (/tmp/ for linux,
                    # C:\temp for windows, then return the full path.
                    filepath = PFEnv.default_temp_file_path() + parent_name
                    new_file = PFGoogleDrive.drive.CreateFile({'id': parent_id})
                    new_file.GetContentFile(filepath)
                    PFGoogleDrive.image_file_count = PFGoogleDrive.image_file_count + 1
                    yield filepath


        # Otherwise go through the list of subdirectories of this directory
        for child in children:
            child_name = child['title']
            child_id = child['id']
            PFEnv.logger.debug('title: %s, id: %s' % (child_name, child_id))

            if child_name == PFSettings.gdrive_photos_folder or in_desired_folder:
                yield from PFGoogleDrive.process_children(True, child_name, child_id)
            else:
                yield from PFGoogleDrive.process_children(False, child_name, child_id)


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
        while True:
            PFGoogleDrive.image_file_count = 0
            file_list = PFGoogleDrive.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
            for file in file_list:
                title = file['title']
                file_id = file['id']
                if title == PFSettings.gdrive_root_folder:
                    if title == PFSettings.gdrive_photos_folder:
                        in_desired_folder = True
                    yield from PFGoogleDrive.process_children(in_desired_folder, title, file_id)
            if PFGoogleDrive.image_file_count == 0:
                PFEnv.logger.error(f"No images found in {file_list}, quitting")

                raise NoImagesFoundException()
