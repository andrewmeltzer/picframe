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
    log_directory = '/mnt/c/tmp'

    ##########################################################
    # Debug level.  CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
    debug_level = 'INFO'

    ##########################################################
    # Should the images be displayed fullscreen?  You can also specify a
    # size by setting the geom.  If it is set to None, it defaults to the
    # screen size.
    fullscreen = False
    geometry_str = "200x200"

    ##########################################################
    # How long should an image be displayed?
    display_time = 5

    ##########################################################
    # Should the screen go dark during certain hours?  If not, set the
    # blackout_hour to None.  Otherwise set the values using a 24 hour
    # clock time.
    #blackout_hour = None
    blackout_hour = 15
    blackout_minute = 0
    end_blackout_hour = 15
    end_blackout_minute = 14


    ##########################################################
    # Where should images be sourced from?
    #   Options are "Google Drive", "Filesystem"
    image_source = 'Filesystem'
    #image_source = 'Google Drive'

    # Settings if for Filesystem
    # image_paths can be a single path, the path to a single file,
    # or a list of comma separated paths.
    #image_paths = ('/mnt/c/tmp/images/IMG_1275.JPG',)
    image_paths = ('/mnt/c/tmp/images/',)
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

