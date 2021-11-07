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
    logfile = 'stdfile'
    debuglevel = 'INFO'
    single_image = False
    #image_path = '/mnt/c/tmp/frame/images/IMG_1275.JPG'
    image_path = '/mnt/c/tmp/frame/images/'
    display_time = 5
    sleep_hour = None
    #sleep_hour = 13
    sleep_minute = 0
    wake_hour = 14
    wake_minute = 0

    @staticmethod
    def get_image_dir():
        return PFEnv.path_to_platform(PFSettings.image_path)

