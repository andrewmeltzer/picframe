#!/mnt/c/tmp/frame/env/bin/python3

import getopt
import sys
import os
import logging
import time
import multiprocessing as mp

from picframe_settings import PFSettings
from picframe_env import PFEnv
from picframe_timer import PFTimer
from picframe_blackout import PFBlackout
from picframe_keyboard import PFKeyboard
from picframe_messagecontent import PFMessageContent
from picframe_message import PFMessage
from picframe_state import PFState, PFStates

# TODO: ++++
# - Want to support videos (mp4, mov, wmv, mp3, wav).  
# - Add a showhelp screen

############################################################
# print_help
#
def print_help(rval=0):
    """
    Print out the command-line help.
    """

    print("picframe.py ")
    print("    <-h|--help>")
    print("    <-s|--single=<path to single image>")
    print("    <-p|--path=<path to image root directory>")
    print("    <-d|--debug=<debug level (DEBUG, INFO, WARN, ERROR)")
    print("    <-l|--logfile=<path to log file>")
    print("    <-f|--fullscreen")
    print("    <-g|--geom=<a geometry in the form 1920x1080)>")
    sys.exit(rval)

############################################################
# get_args
#
def get_args(argv):
    """
    Get input arguments

    Inputs:
    argv: the input arguments to the program.
    Returns: None
        sets global settings and environmentt settings
    """

    # Start with the geometry from the settings
    if PFSettings.geometry_str != None:
        PFSettings.fullscreen = False
        PFEnv.geometry_str = PFSettings.geometry_str
        wstr, hstr = PFSettings.geometry_str.split('x')
        PFEnv.screen_height = int(hstr)
        PFEnv.screen_width = int(wstr)
        PFEnv.geometry = (PFEnv.screen_width, PFEnv.screen_height)

    try:
        opts, inargs = getopt.getopt(argv, "hfs:d:g:",
                ["help", "fullscreen", "logfile=", "debuglevel=", "single=", "path=", "geom="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_help()
        elif opt in ('-d', '--debuglevel'):
            PFSettings.debug_level = arg.upper()
        elif opt in ('-l', '--logfile'):
            PFSettings.logfile = arg
        elif opt in ('-f', '--fullscreen'):
            PFSettings.fullscreen = True
        elif opt in ('-g', '--geom'):
            PFSettings.fullscreen = False
            PFEnv.geometry_str = arg
            wstr, hstr = arg.split('x')
            PFEnv.screen_height = int(hstr)
            PFEnv.screen_width = int(wstr)
            PFEnv.geometry = (PFEnv.screen_width, PFEnv.screen_height)
        elif opt in ('-s', '--single'):
            PFSettings.single_image = True
            PFSettings.image_dir = arg
        elif opt in ('-p', '--path'):
            PFSettings.single_image = False
            PFSettings.image_dir = arg

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

        # If the user wants the logfile to go to the default file location
        # with a datestamp
        if PFSettings.log_to_stdout == False:
            # If want it in utc
            #timestamp = datetime.now(timezone.utc).strftime(PFEnv.MS_FMT_STR)
            timestamp = datetime.now().strftime(PFEnv.MS_FMT_STR)
            fname = "picframe_" + timestamp + ".log"
            path = PFSettings.log_directory

            if not os.path.exists(path):
                os.makedirs(path)
            logfile = os.path.join(path, fname)

            logger_handler = logging.FileHandler(logfile)
        else:
            logger_handler = logging.StreamHandler(sys.stdout)

        log_formatter = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "info": %(message)s}')
        log_formatter.converter = time.gmtime
        logger_root = logging.getLogger()
        logger_root.setLevel(PFSettings.debug_level)

        logger_handler.setLevel(PFSettings.debug_level)
        logger_root.addHandler(logger_handler)
        logger_handler.setFormatter(log_formatter)

        PFEnv.logger_initialized = True

############################################################
#
# main
#
def main():
    """
    """

    queue = mp.Queue()
    timer_p = mp.Process(target=PFTimer.timer_main, args=(queue,))
    blackout_p = mp.Process(target=PFBlackout.blackout_main, args=(queue,))
    message_p = mp.Process(target=PFMessage.message_main, args=(queue,))
    timer_p.start()
    blackout_p.start()
    message_p.start()

    PFKeyboard.keyboard_main(queue)

    timer_p.terminate()
    blackout_p.terminate()
    message_p.terminate()
    queue.close()

if __name__ == "__main__":
    PFEnv.init_environment()
    get_args(sys.argv[1:])
    setup_logger()

    main()

    sys.exit(0)
