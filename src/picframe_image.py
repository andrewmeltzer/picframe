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
from picframe_gdrive import PicframeGoogleDrive
from picframe_filesystem import PicframeFilesystem

class PicframeImage:
    """
    Get, load, and display images.
    """

    initialized = False
    win = None
    canvas = None
    image_file = None

    ############################################################
    #
    # init
    #
    @staticmethod
    def init():
        """
        One-time initialization of the class.
        """

        PicframeImage.win = PicframeImage.get_window()
        PicframeImage.canvas = PicframeImage.get_canvas(PicframeImage.win)

        # Initialize the data source
        if PFSettings.image_source == "Filesystem": 
            PicframeFilesystem.init() 
        elif PFSettings.image_source == "Google Drive": 
            PicframeGoogleDrive.init() 
        else: 
            raise Exception(f"Image source from settings file: '{PFSettings.image_source}' is not supported.")

        PicframeImage.image_file = PicframeImage.get_next_image_file()
        PicframeImage.initialized = True

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
    
        win = Tk(className = str(PFSettings.get_image_dirs()))
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
    # get_image_file_list
    #
    @staticmethod
    def get_image_file_list():
        """
        Get the list of supported image files from the list of directories
        given for pictures to display.
    
        Inputs: None
    
        Returns: List of fully qualified paths in the right
                format for the operating system and image source.
        """
    
        if PFSettings.image_source == "Filesystem":
            pfilesystem = PicframeFilesystem()
            return pfilesystem.get_file_list()
        else:
            gdrive = PicframeGoogleDrive()
            return gdrive.id_list
    
    ############################################################
    #
    # get_next_image_file
    #
    @staticmethod
    def get_next_image_file():
        """
        Get the next supported image files from the list of directories
        given for pictures to display.
    
        Inputs: None 
    
        Returns: List of fully qualified paths in the right 
                format for the operating system and image source.  
        """ 
    
        if PFSettings.image_source == "Filesystem": 
            yield from PicframeFilesystem.get_next_file() 
        else: 
            yield from PicframeGoogleDrive.get_next_photo()
    
    ############################################################
    #
    # get_image
    #
    @staticmethod
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
    
    
        elif file_extension.lower() in ('.heic', '.avif'):
            if sys.platform not in ("linux", "linux2"):
                raise TypeError("HEIC files are not supported on Windows.")
    
            heif_img = pyheif.read_heif(image_file) 
            pil_img = Image.frombytes(
                heif_img.mode, heif_img.size, heif_img.data,
                "raw", heif_img.mode, heif_img.stride,)
    
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
    
    
        return img
    
    ############################################################
    #
    # display_image
    #
    @staticmethod
    def display_image(filepath):
        """
        Display an image file on the screen.
        Inputs:
            filepath:  The full path to the file to display
        """

        img = None
        if filepath is None:
            img = get_image(PFEnv.black_image)
        else:
            img = PicframeImage.get_image(filepath)

        # Calculate where to put the image in the frame
        top = (PFEnv.screen_height - img.height())/2
        left = (PFEnv.screen_width - img.width())/2
        canvas_image = PicframeImage.canvas.create_image(left, top, anchor=NW, image=img)
        PicframeImage.win.geometry(PFEnv.geometry_str)
        PicframeImage.canvas.configure(bg = 'black')
        PicframeImage.win.update()
    
    ############################################################
    #
    # display_next_image
    #
    @staticmethod
    def display_next_image():
        """
        Get and display the next image as returned.  This is the external
        interface to this class.
        Inputs:
            filepath:  The full path to the file to display
        """
        if PicframeImage.initialized == False:
            PicframeImage.init()

        image_file = next(PicframeImage.image_file)
        filename, file_extension = os.path.splitext(image_file)
        while file_extension.lower() not in PFEnv.supported_types:
            print(f"WARNING: File type '{file_extension}' is not supported.")
            image_file = next(PicframeImage.image_file)
            filename, file_extension = os.path.splitext(image_file)

        PicframeImage.display_image(image_file)

