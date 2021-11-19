#!/mnt/c/tmp/frame/env/bin/python3
import tkinter
from tkinter import *
from PIL import ImageTk, Image, ImageOps
import sys
import os
import time
import datetime
import logging

if sys.platform in ("linux", "linux2"):
    import pyheif

from picframe_settings import PFSettings
from picframe_env import PFEnv
from picframe_env import NoImagesFoundException
from picframe_gdrive import PFGoogleDrive
from picframe_filesystem import PFFilesystem
from picframe_messagecontent import PFMessageContent
from picframe_message import PFMessage

class PFCanvas:
    """
    Get, load, and display images.
    """
    win = None
    canvas = None
    queue = None

    ############################################################
    #
    # init
    #
    @staticmethod
    def init(queue):
        """
        One-time initialization of the class.
        """

        PFCanvas.win = PFCanvas.get_window()
        PFCanvas.canvas = PFCanvas.get_canvas()

        PFCanvas.queue = queue

    ############################################################
    #
    # keypress
    #
    @staticmethod
    def keypress(e):
        """
        Capture and react to a keypress event in the display window.
        """
        print(f"#########################{e} {e.char} pressed")
        key = e.char

        if key == 'f':
            PFCanvas.queue.put(PFMessage(PFMessageContent.KEYBOARD_FULLSCREEN))
        if key == 'n':
            PFCanvas.queue.put(PFMessage(PFMessageContent.KEYBOARD_NEXT_IMAGE))
        if key == 'h':
            PFCanvas.queue.put(PFMessage(PFMessageContent.KEYBOARD_HOLD))
        if key == 'b':
            PFCanvas.queue.put(PFMessage(PFMessageContent.KEYBOARD_BLACKOUT))
        if key == 'M':
            PFCanvas.queue.put(PFMessage(PFMessageContent.KEYBOARD_EMULATE_MOTION))
        if key == 'm':
            PFCanvas.queue.put(PFMessage(PFMessageContent.KEYBOARD_EMULATE_MOTION_TIMEOUT))
        if key == 'V':
            PFCanvas.queue.put(PFMessage(PFMessageContent.KEYBOARD_INCREASE_BRIGHTNESS))
        if key == 'v':
            PFCanvas.queue.put(PFMessage(PFMessageContent.KEYBOARD_DECREASE_BRIGHTNESS))

        if key == 'a':
            PFCanvas.queue.put(PFMessage(PFMessageContent.KEYBOARD_USE_DEFAULT_BRIGHTNESS))
        if key in ('q', 'x'):
            PFCanvas.queue.put(PFMessage(PFMessageContent.KEYBOARD_QUIT))

        PFCanvas.win.quit()

    ############################################################
    #
    # get_window
    #
    @staticmethod
    def get_window():
        """
        Get the window that will be displaying the image and set it up
        appropriately.
        Inputs:
        """
    
        win = Tk(className = "Picframe")
        win.resizable(height = None, width = None)
        win.geometry(PFEnv.geometry_str)
        if PFSettings.fullscreen == True:
            win.attributes('-fullscreen', True)

        return win
    
    
    ############################################################
    #
    # get_canvas
    #
    @staticmethod
    def get_canvas():
        """
        Return the appropriately sized and generated canvas which the picture
        will appear on.
        Inputs:
        """
        canvas = Canvas(PFCanvas.win, width=PFEnv.screen_width,height=PFEnv.screen_height)

        canvas.bind("<KeyPress>", PFCanvas.keypress)
        canvas.pack(fill=tkinter.BOTH, expand=True)
        canvas.grid(row=1, column=1)
        canvas.focus_set()

        return canvas
    
