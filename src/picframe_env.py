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
picframe_env.py holds information about the environment that the frame
is running in, such as the monitor information, the OS, etc.

"""
import logging
import ctypes
import sys
import os
from datetime import datetime
from tkinter import Tk
from picframe_settings import PFSettings

class NoImagesFoundException(Exception):
    """
    Used when the images location yields no usable images.
    """
    def __init__(self):
        self.message = []
        if PFSettings.image_source == "Google Drive":
            self.message = f"No images found on Google Drive in '{PFSettings.gdrive_photos_folder}'"
        elif PFSettings.image_source == "Filesystem":
            self.message = f"No images found on filesystem in '{str(PFSettings.image_paths)}'"
        else:
            self.message = f"Unknown image source: '{PFSettings.image_source}'"

        super().__init__(self.message)

class PFEnv:
    """
    PFEnv supplies information about the environment that the frame
    is running in, such as the monitor information, the OS, etc.
    """
    geometry = []
    screen_width = None
    screen_height = None
    geometry_str = None
    supported_types = []
    logger_initialized = False
    logger = None

    # Location of image used when the system is in sleep mode.
    black_image = '../images/black.png'

    # Format string for hour-minute-second dates
    HMS_FMT_STR = '%Y-%m-%dT%H:%M:%S'

    # Location of the log file.  This is set when the logger is initialized
    logfile = None

    # What is the maximum imagefile size that will be allowed.  Too big
    # have errors or hang.
    max_image_size = 30000000

    ############################################################
    #
    # init_environment
    #
    @staticmethod
    def init_environment():
        """
        Initialize the os environment, the screen dimensions, and the
        supported image types.
        """
        if sys.platform in ("linux", "linux2"):
            PFEnv.supported_types = ('.avif', '.heic', '.png', '.tif', '.gif', '.jpg', '.jpeg')
        else:
            PFEnv.supported_types = ('.png', '.jpg', '.tif', '.gif', '.jpeg')

        PFEnv.set_fullscreen_geom()


    ############################################################
    #
    # setup_logger
    #
    def setup_logger():
        """
        Setup the logger for the application.
        Args:
        Returns:
            none
        """
        if not PFEnv.logger_initialized:
            logfile = None
            logger_handler = None
            PFEnv.logger = logging.getLogger('picframe')
    
            # If the user wants the logfile to go to the default file location
            # with a datestamp
            if not PFSettings.log_to_stdout:
                # If want it in utc
                #timestamp = datetime.now(timezone.utc).strftime(PFEnv.HMS_FMT_STR)
                timestamp = datetime.now().strftime(PFEnv.HMS_FMT_STR)
                fname = "picframe_" + timestamp + ".log"
                path = PFSettings.log_directory
    
                if not os.path.exists(path):
                    os.makedirs(path)
                logfile = os.path.join(path, fname)
    
                logger_handler = logging.FileHandler(logfile)
            else:
                logger_handler = logging.StreamHandler(sys.stdout)
    
            log_formatter = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": %(message)s}')
            # log_formatter.converter = time.gmtime
            PFEnv.logger.setLevel(PFSettings.debug_level)
    
            logger_handler.setLevel(PFSettings.debug_level)
            PFEnv.logger.addHandler(logger_handler)
            logger_handler.setFormatter(log_formatter)
    
            PFEnv.logger_initialized = True

    ############################################################
    #
    # set_fullscreen_geom
    #
    @staticmethod
    def set_fullscreen_geom():
        """
        Set the geometry for a full-screen display.
        """
        if sys.platform in ("linux", "linux2"):
            # This works if there is only one monitor
            if PFSettings.fullscreen_geom_str is None:
                win = Tk()
                PFEnv.screen_width = win.winfo_screenwidth()
                PFEnv.screen_height = win.winfo_screenheight()
                PFEnv.geometry = (PFEnv.screen_width, PFEnv.screen_height)
                PFEnv.geometry_str = str(PFEnv.screen_width) + "x" + str(PFEnv.screen_height)
                win.destroy()
            else:
                wstr, hstr = PFSettings.fullscreen_geom_str.split('x')
                PFEnv.screen_width = int(wstr)
                PFEnv.screen_height = int(hstr)
                PFEnv.geometry = (PFEnv.screen_width, PFEnv.screen_height)
                PFEnv.geometry_str = PFSettings.geometry_str
        else:
            user32 = ctypes.windll.user32
            PFEnv.geometry = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
            PFEnv.screen_width = PFEnv.geometry[0]
            PFEnv.screen_height = PFEnv.geometry[1]
            PFEnv.geometry_str = str(PFEnv.screen_width) + "x" + str(PFEnv.screen_height)

    ############################################################
    #
    # path_to_platform
    #
    @staticmethod
    def path_to_platform(inpath):
        """
        Convert the path passed in to one that is appropriate for the
        platform that the code is running on, Linux vs Windows.
        Args:
            inpath: The path to convert.

        Returns:
            the proper path
        """
        path = inpath
        if sys.platform in ("linux", "linux2"):
            if "C:" in inpath:
                path = inpath[3:]
                path = path.replace("\\", "/")
                path = "/mnt/c/" + path
        elif sys.platform == "win32":
            if "/mnt/c" in inpath:
                path = "C:\\" + inpath[7:]
            path = path.replace("/", "\\")
            if "C:" not in path and path.startswith("\\"):
                path = "C:" + path

        return path

    ############################################################
    #
    # default_temp_file_path
    #
    @staticmethod
    def default_temp_file_path():
        """
        Depending on the OS, return a proper path in which to put
        temporary files.
        """
        if sys.platform in ("linux", "linux2"):
            return '/tmp/PICFRAME__'
        elif sys.platform == "win32":
            return 'C:\\Temp\\PICFRAME__'
        else:
            return ''

    ############################################################
    #
    # get_black_image
    #
    @staticmethod
    def get_black_image():
        """
        Depending on the OS, return a proper path where the black image
        is found.
        """
        return PFEnv.path_to_platform(os.path.dirname(__file__) + '/' + PFEnv.black_image)

    ############################################################
    #
    # is_format_supported
    #
    @staticmethod
    def is_format_supported(image_file):
        """
        Returns whether the image file format is supported by the code on
        this platform.
        Inputs:
            image_file: The file to check.

        Returns
            boolean indicating whether it is supported or not.

        """

        filename, file_extension = os.path.splitext(image_file)
        if file_extension.lower() in PFEnv.supported_types:
            return True

        PFEnv.logger.warning("'%s' format is not supported." % (image_file,))
        return False

    ############################################################
    #
    # get_environment_str
    #
    @staticmethod
    def get_environment_str():
        """
        Get a string of the current settings.
        """

        outstr = \
        ("%-20s: %s" % ("geometry", str(PFEnv.geometry))) + os.linesep + \
        ("%-20s: %s" % ("screen_width", str(PFEnv.screen_width))) + os.linesep + \
        ("%-20s: %s" % ("screen_height", str(PFEnv.screen_height))) + os.linesep + \
        ("%-20s: %s" % ("geometry_str", str(PFEnv.geometry_str))) + os.linesep + \
        ("%-20s: %s" % ("supported_types", str(PFEnv.supported_types))) + os.linesep + \
        ("%-20s: %s" % ("logfile", str(PFEnv.logfile))) + os.linesep
        return outstr

    ############################################################
    #
    # get_settings_str
    #
    @staticmethod
    def get_settings_str():
        """
        Get a string containing the current settings.
        """
        outstr = \
        ("%-20s: %s" % ("log_to_stdout", str(PFSettings.log_to_stdout))) + os.linesep + \
        ("%-20s: %s" % ("log_directory", str(PFSettings.log_directory))) + os.linesep + \
        ("%-20s: %s" % ("debug_level", str(PFSettings.debug_level))) + os.linesep + \
        ("%-20s: %s" % ("fullscreen", str(PFSettings.fullscreen))) + os.linesep + \
        ("%-20s: %s" % ("geometry_str", str(PFSettings.geometry_str))) + os.linesep + \
        ("%-20s: %s" % ("display_time", str(PFSettings.display_time))) + os.linesep + \
        ("%-20s: %s" % ("blackout_hour", str(PFSettings.blackout_hour))) + os.linesep + \
        ("%-20s: %s" % ("blackout_minute", str(PFSettings.blackout_minute))) + os.linesep + \
        ("%-20s: %s" % ("end_blackout_hour", str(PFSettings.end_blackout_hour))) + os.linesep + \
        ("%-20s: %s" % ("end_blackout_minute", str(PFSettings.end_blackout_minute))) + os.linesep + \
        ("%-20s: %s" % ("image_source", str(PFSettings.image_source))) + os.linesep + \
        ("%-20s: %s" % ("image_paths", str(PFSettings.image_paths))) + os.linesep + \
        ("%-20s: %s" % ("gdrive_root_folder", str(PFSettings.gdrive_root_folder))) + os.linesep + \
        ("%-20s: %s" % ("gdrive_photos_folder", str(PFSettings.gdrive_photos_folder))) + os.linesep 

        return outstr

    ############################################################
    #
    # get_help_str
    #
    @staticmethod
    def get_help_str():
        """
        Get a string containing the help commands
        """
        outstr = \
        ("h: Toggle help screen") + os.linesep + \
        ("f: Toggle fullscreen") + os.linesep + \
        ("n: Next picture") + os.linesep + \
        ("c: Toggle hold current picure") + os.linesep + \
        (f"t: Decrease the amount of time an image is shown by {PFSettings.timer_step} seconds") + os.linesep + \
        (f"T: Increase the amount of time an image is shown by {PFSettings.timer_step} seconds") + os.linesep + \
        ("b: Toggle blackout mode") + os.linesep + \
        ("d: Toggle display detailed information") + os.linesep + \
        ("m: Toggle whether to use the motion detector.") + os.linesep + \
        ("V: Increase video brightness") + os.linesep + \
        ("v: Decrease video brightess") + os.linesep + \
        ("a: Set to default video brightness") + os.linesep + \
        ("x or q: Quit")

        return outstr
