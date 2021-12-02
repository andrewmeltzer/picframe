#!/mnt/c/tmp/frame/env/bin/python3
"""
Picframe is a digital frame that can
- pull pictures from
    - any local directory
    - gdrive
    - samba

- Sleep (go dark) during the night
- Adjust brightness automatically
- Turn on and off based on motion
- Work on linux (also Raspberri pi) and Windows
- Run fullscreen or in a window of any chosen size
"""

import getopt
import sys
import os
import time
from datetime import datetime
import multiprocessing as mp

from picframe_settings import PFSettings
from picframe_env import PFEnv
from picframe_timer import PFTimer
from picframe_blackout import PFBlackout
from picframe_messagecontent import PFMessageContent
from picframe_message import PFMessage
from picframe_image import PFImage
from picframe_canvas import PFCanvas
from picframe_video import PFVideo


# TODO: ++++
# - Print status and settings on the screen
# - Save settings in a different file; allow the user to save screen-modified
#   settings
# - Properly identify the size of the screen on linux
# - Test with usb drive and document how to do it
# - Better installation process
# - Detect ambient light and dim the screen if it is darker.
# - Someday support videos (mp4, mov, wmv, mp3, wav).
# - Someday create a smartphone app to control it over bluetooth or wifi
# BUGS:

############################################################
# print_help
#
def print_help(rval=0):
    """
    Print out the command-line help.
    """

    print("picframe.py ")
    print("    <-h|--help>")
    print("    <-p|--path=<path to image root directory (local filesytem only)>")
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

    try:
        opts, inargs = getopt.getopt(argv, "hfs:d:g:",
                ["help", "fullscreen", "logfile=", "debuglevel=",
                 "path=", "geom="])
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
            PFSettings.geometry_str = arg
        elif opt in ('-p', '--path'):
            PFSettings.image_source = 'Filesystem'
            PFSettings.single_image = False
            PFSettings.image_dir = arg

############################################################
#
# show_command_help
#
def show_command_help():
    """
    Display the keyboard commands.
    """
    print("f: Toggle fullscreen")
    print("n: Next picture")
    print("h: Toggle hold current picure")
    print(f"p: Decrease the amount of time an image is shown by {PFTimer.TIMER_STEP} seconds")
    print(f"P: Increase the amount of time an image is shown by {PFTimer.TIMER_STEP} seconds")
    print("b: Toggle blackout mode")
    print("m: Toggle whether to use the motion detector.")
    print("V: Increase video brightness")
    print("v: Decrease video brightess")
    print("a: Set to default video brightness")
    print("x or q: Quit")


############################################################
#
# main
#
def main():
    """
    Execute the program.
    """

    PFEnv.setup_logger()

    show_command_help()

    PFMessage.canvas_mq = mp.Queue()
    PFMessage.video_mq = mp.Queue()
    PFMessage.timer_mq = mp.Queue()
    PFCanvas.init()
    PFImage.init()


    timer_p = mp.Process(target=PFTimer.timer_main, args=(PFMessage.canvas_mq,PFMessage.timer_mq))
    blackout_p = mp.Process(target=PFBlackout.blackout_main, args=(PFMessage.canvas_mq,))
    motion_p = mp.Process(target=PFVideo.motion_main, args=(PFMessage.canvas_mq, PFMessage.video_mq))

    timer_p.start()
    blackout_p.start()
    if PFSettings.motion_sensor_timeout is not None and PFSettings.motion_sensor_timeout > 0:
        motion_p.start()

    # Add the messaging pieces (keyboard events and other events) to
    # the canvas
    PFMessage.setup_canvas_messaging()

    # Queue up a black image as the first image to set it up
    try:
        PFImage.display_first_image()
        PFCanvas.win.update()

        # This runs forever until a 'q' or 'x' is entered.
        PFCanvas.win.mainloop()

    except Exception as e:
        PFSettings.print_settings()
        PFEnv.print_environment()
        PFImage.print_image_state()
        raise(e)

    if PFSettings.motion_sensor_timeout is not None and PFSettings.motion_sensor_timeout > 0:
        PFVideo.motion_cleanup()
        motion_p.terminate()
    timer_p.terminate()
    blackout_p.terminate()
    PFMessage.canvas_mq.close()

if __name__ == "__main__":
    PFEnv.init_environment()
    get_args(sys.argv[1:])

    main()

    sys.exit(0)
