#!/mnt/c/tmp/frame/env/bin/python3

import getopt
import tkinter
from tkinter import *
from PIL import ImageTk, Image, ImageOps
import sys
import os
import time
import datetime

if sys.platform in ("linux", "linux2"):
    import pyheif

from picframe_settings import PFSettings
from picframe_env import PFEnv

# TODO: ++++
# - Need a way to kill it when it is sleeping.

############################################################
# get_args
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
        opts, inargs = getopt.getopt(argv, "hfs:d:",
                ["help", "fullscreen", "logfile=", "debuglevel=", "single=", "path="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_help()
        elif opt in ('-d', '--debuglevel'):
            PFSettings.debug = arg.upper()
        elif opt in ('-l', '--logfile'):
            PFSettings.logfile = arg
        elif opt in ('-f', '--fullscreen'):
            PFSettings.fullscreen = True
        elif opt in ('-s', '--single'):
            PFSettings.single_image = True
            PFSettings.image_dir = arg
        elif opt in ('-p', '--path'):
            PFSettings.single_image = False
            PFSettings.image_dir = arg

    

############################################################
#
# do_sleep
#
def do_sleep(canvas, win):
    """
    See if in the sleep window, and if so then sleep for the 
    right number of seconds.
    """
    if PFSettings.sleep_hour is None:
        return

    secs_per_min = 60
    mins_per_hour = 60
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute

    now_time = hour*60 + minute
    sleep_time = (PFSettings.sleep_hour * mins_per_hour) + PFSettings.sleep_minute
    wake_time = (PFSettings.wake_hour * mins_per_hour) + PFSettings.wake_minute
    sleep_interval = 0

    # if it is sleeping across midnight and it is before midnight
    if wake_time < sleep_time and now_time > sleep_time:
        sleep_interval = (wake_time * secs_per_min) \
            + (24 * mins_per_hour) - now_time

    # if it is sleeping across midnight and it is after midnight
    if wake_time < sleep_time and now_time < wake_time:
        sleep_interval = (wake_time - now_time) * secs_per_min

    if now_time > sleep_time and now_time < wake_time:
        sleep_interval = (wake_time - now_time) * secs_per_min
        
    print(f"Going to sleep for {sleep_interval} seconds.")
    display_image(canvas, win, None)
    time.sleep(sleep_interval)
    
    
############################################################
#
# get_window
#
def get_window():
    """
    Get the window that will be displaying the image and set it up
    appropriately.
    Inputs:
    """

    win = Tk(className = PFSettings.image_path)
    win.resizable(height = None, width = None)
    win.geometry(PFEnv.geometry_str)
    if PFSettings.fullscreen == True:
        win.attributes('-fullscreen', True)

    return win

############################################################
#
# get_canvas
#
def get_canvas(win):
    """
    Return the appropriately sized and generated canvas which the picture
    will appear on.
    Inputs:
        win: The Tk window to draw on.
    """
    canvas = Canvas(win, width=PFEnv.screen_width,height=PFEnv.screen_height)
    canvas.pack(fill=tkinter.BOTH, expand=True)
    canvas.grid(row=1, column=1)

    return canvas

############################################################
#
# get_image
#
def get_image(image_file):
    """
    Get the image from an image file, converting whatever needs to be
    converted to get it into PhotoImage format.  Often need to convert formats
    using the PIL library
        - JPG to PNG

    Inputs:
        image_file: The image

    Returns: 
        img
    """
    # Need PIL library to handle JPG files.
    filename, file_extension = os.path.splitext(image_file)

    img = None
    if file_extension.lower() in ('.jpg', '.png'):
        pil_img = Image.open(image_file)

        # Use the exif information to properly orient the image.
        pil_img = ImageOps.exif_transpose(pil_img)

        # Calculate the image width/height ratio and use it 
        # based on the width of the screen 
        height_ratio = PFEnv.screen_height/pil_img.height
        width_ratio = PFEnv.screen_width/pil_img.width

        actual_width = None
        actual_height = None
        if height_ratio > width_ratio:
            actual_width = int(width_ratio * pil_img.width)
            actual_height = int(width_ratio * pil_img.height)
        else:
            actual_height = int(height_ratio * pil_img.height)
            actual_width = int(height_ratio * pil_img.width)

        pil_img = pil_img.resize((actual_width, actual_height), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(pil_img)
    elif file_extension.lower() == '.heic':
        if sys.platform in ("linux", "linux2"):
            pil_img = Image.frombytes(
                image_file.mode, image_file.size, image_file.data,
                "raw", image_file.mode, image_file.stride,)
        else:
            raise TypeError("HEIC files are not supported on Windows.")
        pil_img = ImageTk.PhotoImage(pil_img)


    else: 
        raise TypeError(f"Invalid file: {image_file}. Your file must be a JPG or PNG file.")

    return img

############################################################
#
# display_image
#
def display_image(canvas, win, filepath):
    """
    Display an image file on the screen.
    Inputs:
        filepath:  The full path to the file to display
    """
    #++++++++++++++++++++++
    #    if filepath is None:
    #        canvas_image = canvas.create_image(0,0, anchor=NW, image='')
    #        win.geometry(PFEnv.geometry_str)
    #        canvas.configure(bg = 'black')
    #        return False

    directory = PFSettings.get_image_dir()
    filename, file_extension = os.path.splitext(filepath)
    if file_extension.lower() in PFEnv.supported_types:
        image_path = os.path.join(directory, filepath)

        img = get_image(image_path)

        # Calculate where to put the image in the frame
        top = (PFEnv.screen_height - img.height())/2
        left = (PFEnv.screen_width - img.width())/2
        canvas_image = canvas.create_image(left, top, anchor=NW, image=img)
        win.geometry(PFEnv.geometry_str)
        canvas.configure(bg = 'black')
        win.update()
        #if PFSettings.single_image:
        #    win.mainloop()
        return True
    else:
        print(f"WARNING: File type '{file_extension}' is not supported.")
        return False


############################################################
#
# main
#
#def main(args):
def main():
    """
    """
    win = get_window()
    canvas = get_canvas(win)

    # Need to incorporate the do_sleep stuff for the night and
    # Need a way to shut it down.
    while True:
        do_sleep(canvas, win)
        if PFSettings.single_image:
            display_image(canvas, win, PFSettings.get_image_dir())
            # so that it can go to sleep, test the do_sleep every
            # 15 mins
            if PFSettings.single_image:
                time.sleep(900)

        else:
            # ++++ Need this to recursively walk the directory
            for filepath in os.listdir(PFSettings.get_image_dir()):
                if display_image(canvas, win, filepath):
                    time.sleep(PFSettings.display_time)

if __name__ == "__main__":
    get_args(sys.argv[1:])
    PFEnv.init_environment()
    main()

    sys.exit(0)
