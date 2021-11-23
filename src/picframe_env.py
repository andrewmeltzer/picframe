"""
picframe_env.py gathers information about the environment that the fram
is running in, such as the monitor information, the OS, etc.

"""
import logging
import ctypes
import sys
import os
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
    PFEnv supplies information about the environment that the fram
    is running in, such as the monitor information, the OS, etc.
    """
    geometry = []
    screen_width = None
    screen_height = None
    geometry_str = None
    supported_types = []
    logger_initialized = False

    # Location of image used when the system is in sleep mode.
    black_image = '../images/black.png'

    # Format string for hour-minute-second dates
    HMS_FMT_STR = '%Y-%m-%dT%H:%M:%S'

    # Location of the log file.  This is set when the logger is initialized
    logfile = None

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
    # set_fullscreen_geom
    #
    @staticmethod
    def set_fullscreen_geom():
        """
        Set the geometry for a full-screen display.
        """
        if sys.platform in ("linux", "linux2"):
            # ++++ Find a linux way of doing this
            PFEnv.geometry = (1920, 1080)
            PFEnv.screen_width = 1920
            PFEnv.screen_height = 1080
            PFEnv.geometry_str = '1920x1080'
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

        logging.warning("'%s' format is not supported." % (image_file,))
        return False

    ############################################################
    #
    # print_environment
    #
    @staticmethod
    def print_environment():
        """
        Print the current settings.
        """
        print("%-20s: %s" % ("geometry", str(PFEnv.geometry)))
        print("%-20s: %s" % ("screen_width", str(PFEnv.screen_width)))
        print("%-20s: %s" % ("screen_height", str(PFEnv.screen_height)))
        print("%-20s: %s" % ("geometry_str", str(PFEnv.geometry_str)))
        print("%-20s: %s" % ("supported_types", str(PFEnv.supported_types)))
        print("%-20s: %s" % ("logfile", str(PFEnv.logfile)))

