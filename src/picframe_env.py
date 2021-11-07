"""
picframe_env.py gathers information about the environment that the fram
is running in, such as the monitor information, the OS, etc.

"""
import ctypes
import sys
import subprocess

class PFEnv:
    """
    PFEnv supplies information about the environment that the fram
    is running in, such as the monitor information, the OS, etc.
    """
    geometry = None
    screen_width = None
    screen_height = None
    geometry_str = None
    supported_types = None

    ############################################################
    #
    # init_environment
    #
    def init_environment():
        if sys.platform in ("linux", "linux2"):
            # ++++ Find a linux way of doing this
            #PFEnv.geometry = (1920, 1080)
            #PFEnv.screen_width = 1920
            #PFEnv.screen_height = 1080
            #PFEnv.geometry_str = '1920x1080'
            PFEnv.geometry = (, 1080)
            PFEnv.screen_width = 1920
            PFEnv.screen_height = 1080
            PFEnv.geometry_str = '1920x1080'


            # FIX THIS BACK UP ++++
            # PFEnv.supported_types = ('.heic', '.png', '.jpg')
            PFEnv.supported_types = ('.png', '.jpg')
        else:
            user32 = ctypes.windll.user32
            PFEnv.geometry = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
            PFEnv.screen_width = PFEnv.geometry[0]
            PFEnv.screen_height = PFEnv.geometry[1]
            PFEnv.geometry_str = str(PFEnv.screen_width) + "x" + str(PFEnv.screen_height)
            PFEnv.supported_types = ('.png', '.jpg')


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

