"""
picframe_settings.py holds the user-configurable settings for the 
frame.
"""

import sys
from picframe_env import PFEnv

############################################################
#
# PFSettings
# This class holds user-configurable settings values.
#
class PFSettings:
    """
    This class holds user-configurable settings values.
    """

    fullscreen = False

    #
    log_to_stdout = True
    debug_level = 'DEBUG'
    
    # Options are "Google Drive", "Filesystem"
    image_source = 'Filesystem'
    #image_source = 'Google Drive'

    # image_paths can be a single path, the path to a single file,
    # or a list of comma separated paths.
    #image_paths = ('/mnt/c/tmp/images/IMG_1275.JPG',)
    image_paths = ('/mnt/c/tmp/images/',)
    display_time = 2
    #sleep_hour = None
    sleep_hour = 12
    sleep_minute = 0
    wake_hour = 14
    wake_minute = 0
    log_directory = '/mnt/c/tmp'

    # Settings if for Google Drive (if used)
    # If there is a root level directory to start in, can save a lot of time
    # not traversing the rest.  If the desired directory is at root level,
    # then give both.
    gdrive_root_folder = "PicFrame"

    # The directory the photos are in.  It may be the same as the
    # ROOT_FOLDER_TITLE
    gdrive_photos_folder = "PicFrame"

    @staticmethod
    def get_image_dirs():
        return PFEnv.path_to_platform(PFSettings.image_paths)

