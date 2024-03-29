
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
import traceback

from picframe_settings import PFSettings
from picframe_env import PFEnv, NoImagesFoundException
from picframe_timer import PFTimer
from picframe_blackout import PFBlackout
from picframe_message import PFMessage
from picframe_canvas_message import PFCanvasMessage
from picframe_image import PFImage
from picframe_canvas import PFCanvas
from picframe_video import PFVideo


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
    print(PFEnv.get_help_str())

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
    PFCanvasMessage.setup_canvas_messaging()

    # Queue up a black image as the first image to set it up
    try:
        PFImage.display_first_image()
        PFCanvas.win.update()

        # This runs forever until a 'q' or 'x' is entered.
        PFCanvas.win.mainloop()

    except NoImagesFoundException as exc:
        PFMessage.canvas_mq.put(PFMessage(PFMessage.KEYBOARD_QUIT))
        raise(exc)
    except MemoryError as exc:
        PFMessage.canvas_mq.put(PFMessage(PFMessage.KEYBOARD_QUIT))
        print("ERROR: Out of Memory!")
        traceback.print_stack()
        raise(exc)
        
    except Exception as exc:
        print(PFEnv.get_settings_str())
        print(PFEnv.get_environment_str())
        PFImage.print_image_state()
        raise(exc)

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
