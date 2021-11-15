
import logging
import os
from pathlib import Path
from picframe_settings import PFSettings
from picframe_env import *

class PicframeFilesystem:
    """
    If the user's photos are on the local filesystem, this class gets
    them.
    """
    initialized = False
    
    ############################################################ 
    #
    # init
    #
    @staticmethod
    def init():
        PicframeFilesystem.initialized = True


    ############################################################ 
    #
    # get_next_file
    #
    @staticmethod
    def get_next_file():
        """
        Get next supported image file from the list of filesystem
        directories given for pictures to display.
    
        Use a generator so it is compatible with the way the google drive
        version works, yielding a single file at a time.
    
        Inputs: None 
    
        Returns: List of fully qualified paths in the right 
                format for the operating system and image source.  
        """
    
        # Traverse the recursive list of directories.
        while True:
            image_file_count = 0
            for dirname in PFSettings.get_image_dirs():
                if Path(dirname).is_file():
                    if PFEnv.is_format_supported(dirname):
                        image_file_count = image_file_count + 1
                        yield dirname
                else:
                    for root, dirs, files in os.walk(dirname):
                        path = root.split(os.sep)
                        for file in files:
                            pathdir = '/'.join(path) + '/' + file
                            if PFEnv.is_format_supported(pathdir):
                                image_file_count = image_file_count + 1
                                yield pathdir
            if image_file_count == 0:
                raise NoImagesFoundException()
    
        return None
    
    ############################################################
    #
    # get_file_list
    #
    @staticmethod
    def get_file_list():
        """
        Get the list of supported image files from the list of filesystem
        directories given for pictures to display.
    
        Inputs: None
    
        Returns: List of fully qualified paths in the right
                format for the operating system and image source.
        """
        image_file_list = []
    
        # Traverse the recursive list of directories.
        for dirname in PFSettings.get_image_dirs():
            if Path(dirname).is_file():
                if PFEnv.is_format_supported(dirname):
                    image_file_list.append(dirname)
            else:
                for root, dirs, files in os.walk(dirname):
                    path = root.split(os.sep)
                    for file in files:
                        pathdir = '/'.join(path) + '/' + file
                        if PFEnv.is_format_supported(pathdir):
                            image_file_list.append(pathdir)
    
        return image_file_list
    
