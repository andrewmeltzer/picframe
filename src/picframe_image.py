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
from picframe_canvas import PFCanvas
from picframe_state import PFState, PFStates
from picframe_messagecontent import PFMessageContent

class PFImage:
    """
    Get, load, and display images.
    """

    image_file_gen = None
    current_image = None
    previous_image = None
    message = None
    queue = None
    image_id = None
    displayed_img = None

    ############################################################
    #
    # init
    #
    @staticmethod
    def init(queue):
        """
        One-time initialization of the class.
        """

        # Initialize the data source
        if PFSettings.image_source == "Filesystem": 
            PFFilesystem.init() 
        elif PFSettings.image_source == "Google Drive": 
            PFGoogleDrive.init() 
        else: 
            raise Exception(f"Image source from settings file: '{PFSettings.image_source}' is not supported.")

        PFImage.image_file_gen = PFImage.get_next_image_file()
        PFImage.queue = queue

    ############################################################
    #
    # process_message
    #
    @staticmethod
    def process_message():
        """
        Process the next message from the queue based on the current state
        of the system and the message.  As a rule of thumb, keyboard actions
        take precedence over everything else.
        """
        if PFImage.queue.empty():
            PFCanvas.win.after(100, PFImage.process_message)
            return

        PFImage.message = PFImage.queue.get_nowait()
        message = PFImage.message
    
        # Only go to the next message if in the normal state.
        if message.message == PFMessageContent.TIMER_NEXT_IMAGE:
            if PFState.current_state == PFStates.NORMAL:
                PFImage.display_next_image()
            else:
                PFImage.display_current_image()
    
        # If the keyboard says next image, override any holds or blackouts
        elif message.message == PFMessageContent.KEYBOARD_NEXT_IMAGE:
            PFImage.display_next_image()
    
        elif message.message == PFMessageContent.KEYBOARD_HOLD:
            if PFState.current_state == PFStates.KEYBOARD_HOLD:
                PFImage.display_next_image()
            else:
                PFImage.display_previous_image()
    
        elif message.message == PFMessageContent.KEYBOARD_BLACKOUT:
            if PFState.current_state == PFStates.KEYBOARD_BLACKOUT:
                PFImage.display_next_image()
            else:
                PFImage.display_black_image()
    
        elif message.message == PFMessageContent.KEYBOARD_INCREASE_BRIGHTNESS:
            PFState.keyboard_brightness = True
        elif message.message == PFMessageContent.KEYBOARD_DECREASE_BRIGHTNESS:
            PFState.keyboard_brightness = True
        elif message.message == PFMessageContent.KEYBOARD_USE_DEFAULT_BRIGHTNESS:
            PFState.keyboard_brightness = False
        elif message.message == PFMessageContent.KEYBOARD_EMULATE_MOTION:
            PFImage.display_next_image()
        elif message.message == PFMessageContent.KEYBOARD_EMULATE_MOTION_TIMEOUT:
            PFImage.display_black_image()
        elif message.message == PFMessageContent.BLACKOUT:
            PFImage.display_black_image()
        elif message.message == PFMessageContent.END_BLACKOUT:
            PFImage.display_current_image()
        elif message.message == PFMessageContent.INCREASE_BRIGHTNESS:
            PFImage.display_current_image()
        elif message.message == PFMessageContent.DECREASE_BRIGHTNESS:
            PFImage.display_current_image()
        elif message.message == PFMessageContent.MOTION:
            PFImage.display_current_image()
        elif message.message == PFMessageContent.KEYBOARD_FULLSCREEN:
            logging.warn("Fullscreen toggling is not yet implemented.")
            raise NotImplementedError("Fullscreen toggling is not yet implemented.")
        elif message.message == PFMessageContent.MOTION_TIMEOUT:
            PFImage.display_black_image()
        elif message.message == PFMessageContent.KEYBOARD_QUIT:
            PFCanvas.win.quit()
            PFCanvas.canvas.quit()
            PFCanvas.win.destroy()
        else:
            PFImage.display_current_image()
    
        PFState.new_state(message)
        PFCanvas.win.after(100, PFImage.process_message)
    
        return True
    
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
            pfilesystem = PFFilesystem()
            return pfilesystem.get_file_list()
        else:
            gdrive = PFGoogleDrive()
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
            yield from PFFilesystem.get_next_file() 
        else: 
            yield from PFGoogleDrive.get_next_photo()
    
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
        if file_extension.lower() in ('.tif', '.gif', '.jpg', '.png'):
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

        if filepath is None:
            PFImage.displayed_img = PFImage.get_image(PFEnv.black_image)
        else:
            PFImage.displayed_img = PFImage.get_image(filepath)

        top = (PFEnv.screen_height - PFImage.displayed_img.height())/2
        left = (PFEnv.screen_width - PFImage.displayed_img.width())/2
        PFCanvas.canvas.itemconfig(PFImage.image_id, image=PFImage.displayed_img)
        PFCanvas.canvas.coords(PFImage.image_id, (left, top))

    ############################################################
    #
    # display_first_image
    #
    @staticmethod
    def display_first_image():
        """
        Create and display an initial image.  This is just the black image
        to get the canvas set up properly.
        Inputs:
        """

        img = PFImage.get_image(PFEnv.black_image)

        # Calculate where to put the image in the frame
        top = (PFEnv.screen_height - img.height())/2
        left = (PFEnv.screen_width - img.width())/2
        PFImage.image_id = PFCanvas.canvas.create_image(left, top, anchor=NW, image=img)

    ############################################################
    #
    # display_next_image
    #
    @staticmethod
    def display_next_image():
        """
        Get and display the next image as returned.  This is the external
        interface to this class.
        """
        image_file = next(PFImage.image_file_gen)

        PFImage.previous_image = PFImage.current_image
        PFImage.current_image = image_file

        filename, file_extension = os.path.splitext(image_file)
        while file_extension.lower() not in PFEnv.supported_types:
            print(f"WARNING: File type '{file_extension}' is not supported.")
            image_file = next(PFImage.image_file_gen)
            filename, file_extension = os.path.splitext(image_file)

        PFImage.display_image(image_file)

    ############################################################
    #
    # display_previous_image
    #
    @staticmethod
    def display_previous_image():
        """
        Get and display the previous image over again.
        """
        image_file = PFImage.previous_image
        PFImage.display_image(image_file)

    ############################################################
    #
    # display_current_image
    #
    @staticmethod
    def display_current_image():
        """
        Get and display the current image over again.
        """
        image_file = PFImage.current_image
        PFImage.display_image(image_file)

    ############################################################
    #
    # display_black_image
    #
    @staticmethod
    def display_black_image():
        """
        Get and display the blank-screen (black) image
        """
        PFImage.previous_image = PFImage.current_image
        PFImage.current_image = None
        PFImage.display_image(None)
