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
picframe_settings.py holds the user-configurable settings for the
frame.
"""

############################################################
#
# PFSettings
# This class holds user-configurable settings values.
#
class PFSettings:
    """
    This class holds user-configurable settings values.  All of these
    can also be configured on the command line.
    """

    ##########################################################
    # Where should logging information be sent? If log_to_stdout is set
    # to true, it ignores log_directory and sends logging information to
    # stdout.  Otherwise it creates a logfile and puts it into the log
    # directory.  The logfile name is picframe_<timestamp>.log
    log_to_stdout = True
    log_directory = '/tmp'

    ##########################################################
    # Debug level.  CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
    debug_level = 'INFO'

    ##########################################################
    # Should the images be displayed fullscreen?  You can also specify a
    # default non-fullscreen size by setting the geom.  If it is 
    # set to None, it defaults to 400x400
    fullscreen = False
    geometry_str = "400x400"

    ##########################################################
    # The fullscreen_geom is calculated by the program and is 
    # generally right unless you are on linux and using more than
    # one monitor, in which case it WILL BE WRONG.
    # Put in the form of fullscreen_geom_str = "1920x1080"
    fullscreen_geom_str = "1920x1080"


    ##########################################################
    # How long should an image be displayed (in seconds)?
    display_time = 30

    ##########################################################
    # Should the screen go dark during certain hours?  If not, set the
    # blackout_hour to None.  Otherwise set the values using a 24 hour
    # clock time.
    #blackout_hour = None
    blackout_hour = 23
    blackout_minute = 0
    end_blackout_hour = 7
    end_blackout_minute = 15

    ##########################################################
    # How long (minutes) should the motion sensor wait to see motion before
    # blacking out the screen.  Setting to None or 0 disables the motion
    # detector.
    # You can also disable the motion detector by setting
    #   use_motion_detector = False
    # If you set motion_sensor_timeout to a usable number, you can toggle
    # the motion sensor on and off using the keyboard.
    motion_sensor_timeout = 15
    use_motion_sensor = True


    ##########################################################
    # Where should images be sourced from?
    #   Options are "Google Drive", "Filesystem"
    image_source = 'Filesystem'
    #image_source = 'Google Drive'

    # Settings if for Filesystem
    # image_paths can be a single path, the path to a single file,
    # or a list of comma separated paths.
    #image_paths = ('/mnt/c/tmp/images/IMG_1275.JPG',)
    image_paths = ('/mnt/pibackup/',)
    #image_paths = ('../images/black.png',)
    #image_paths = ('/mnt/c/Users/andym/Pictures/',)

    # Settings if for Google Drive (if used)
    # If there is a root level directory to start in, can save a lot of time
    # not traversing the rest.  If the desired directory is at root level,
    # then give both.
    gdrive_root_folder = "PicFrame"

    # The directory the photos are in.  It may be the same as the
    # ROOT_FOLDER_TITLE
    gdrive_photos_folder = "PicFrame"

    ############################################################
    ############################################################
    #
    # Advanced settings.  Adjust these carefully
    #

    ############################################################
    #
    # Video settings:
    #
    # camera_port is useful if you have two video cameras and the
    # wrong one is being selected.  If that is the case, first try
    # to set it to 1, then -1.
    # default:
    #   camera_port = 0
    camera_port = 0

    # pixel_threshold identifies how many pixels need to change 
    # before a difference is tagged as motion.  If the camera is
    # lousy, light flickers, or small movements are common, this
    # can be increased.
    # default:
    #   pixel_threshold = 10
    pixel_threshold = 15

    ############################################################
    ############################################################
    ############################################################
    ############################################################
    #
    # print_settings
    #
    @staticmethod
    def print_settings():
        """
        Print the current settings.
        """
        print("%-20s: %s" % ("log_to_stdout", str(PFSettings.log_to_stdout)))
        print("%-20s: %s" % ("log_directory", str(PFSettings.log_directory)))
        print("%-20s: %s" % ("debug_level", str(PFSettings.debug_level)))
        print("%-20s: %s" % ("fullscreen", str(PFSettings.fullscreen)))
        print("%-20s: %s" % ("geometry_str", str(PFSettings.geometry_str)))
        print("%-20s: %s" % ("display_time", str(PFSettings.display_time)))
        print("%-20s: %s" % ("blackout_hour", str(PFSettings.blackout_hour)))
        print("%-20s: %s" % ("blackout_minute", str(PFSettings.blackout_minute)))
        print("%-20s: %s" % ("end_blackout_hour", str(PFSettings.end_blackout_hour)))
        print("%-20s: %s" % ("end_blackout_minute", str(PFSettings.end_blackout_minute)))
        print("%-20s: %s" % ("image_source", str(PFSettings.image_source)))
        print("%-20s: %s" % ("image_paths", str(PFSettings.image_paths)))
        print("%-20s: %s" % ("gdrive_root_folder", str(PFSettings.gdrive_root_folder)))
        print("%-20s: %s" % ("gdrive_photos_folder", str(PFSettings.gdrive_photos_folder)))

