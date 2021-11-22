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

class PFCanvas:
    """
    Set up the canvas and window in which images will be displayed.
    """
    win = None
    canvas = None

    ############################################################
    #
    # init
    #
    @staticmethod
    def init():
        """
        One-time initialization of the class.
        """

        PFCanvas.win = PFCanvas.get_window()
        PFCanvas.canvas = PFCanvas.get_canvas()
        PFCanvas.win.geometry(PFEnv.geometry_str)
        PFCanvas.canvas.configure(bg = 'black')
        PFCanvas.win.update()

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

        canvas.pack(fill=tkinter.BOTH, expand=True)
        canvas.grid(row=1, column=1)
        canvas.focus_set()

        return canvas
    
