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
picframe_canvas.py

The picframe canvas also includes the window in which the image is 
displayed.  It uses the tkinter libraries.
"""
import tkinter
from tkinter import Tk, Canvas

from picframe_settings import PFSettings
from picframe_env import PFEnv

class PFCanvas:
    """
    Set up the canvas and window in which images will be displayed.
    """
    win = None
    canvas = None
    fullscreen = True
    width = None
    height = None
    geometry = None
    geometry_str = None

    ############################################################
    #
    # init
    #
    @staticmethod
    def init():
        """
        One-time initialization of the class.
        """
        if PFSettings.fullscreen:
            PFCanvas.set_fullscreen_geom()
        elif PFSettings.geometry_str is not None:
            PFCanvas.set_settings_geom()

        PFCanvas.fullscreen = PFSettings.fullscreen
        PFCanvas.get_window()
        PFCanvas.get_canvas()
        PFCanvas.canvas.configure(bg='black')
        PFCanvas.win.update()

    ############################################################
    #
    # set_settings_geom
    #
    @staticmethod
    def set_settings_geom():
        """
        Set the geometry based on a geometry string provided in the
        settings file; if none default to 400x400.
        """
        if PFSettings.geometry_str is not None:
            PFCanvas.geometry_str = PFSettings.geometry_str
        else:
            PFCanvas.geometry_str = "400x400"

        wstr, hstr = PFCanvas.geometry_str.split('x')
        PFCanvas.height = int(hstr)
        PFCanvas.width = int(wstr)
        PFCanvas.geometry = (PFEnv.screen_width, PFEnv.screen_height)

    ############################################################
    #
    # set_fullscreen_geom
    #
    @staticmethod
    def set_fullscreen_geom():
        """
        Set the geometry based on  the computed fullscreen geometry in
        PFEnv
        """
        PFCanvas.width = PFEnv.screen_width
        PFCanvas.height = PFEnv.screen_height
        PFCanvas.geometry = PFEnv.geometry
        PFCanvas.geometry_str = PFEnv.geometry_str

    ############################################################
    #
    # adjust_canvas_geom
    #
    @staticmethod
    def adjust_canvas_geom():
        """
        See if the user has adjsuted the canvas geometry.  
        """
        width = PFCanvas.win.winfo_width()
        height = PFCanvas.win.winfo_height()

        if width != PFCanvas.width or height != PFCanvas.height:
            PFCanvas.win.destroy()
            PFCanvas.width = width
            PFCanvas.height = height
            PFCanvas.geometry = (width, height)
            PFCanvas.geometry_str = str(width) + 'x' + str(height)

            PFCanvas.reset_window_size()
            return True
        else:
            return False

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

        PFCanvas.win = Tk(className="Picframe")
        PFCanvas.win.resizable(height=None, width=None)
        PFCanvas.win.geometry(PFCanvas.geometry_str)
        if PFCanvas.fullscreen:
            PFCanvas.win.attributes('-fullscreen', True)

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
        PFCanvas.canvas = Canvas(PFCanvas.win, width=PFCanvas.width, height=PFCanvas.height)

        PFCanvas.canvas.pack(fill=tkinter.BOTH, expand=True)
        PFCanvas.canvas.focus_set()


    ############################################################
    #
    # reset_window_size
    #
    @staticmethod
    def reset_window_size():
        """
        The window size has changed.  Adjust everything.
        """
        PFCanvas.get_window()
        PFCanvas.get_canvas()

        PFCanvas.win.geometry(PFCanvas.geometry_str)
        if PFCanvas.fullscreen:
            PFCanvas.win.attributes('-fullscreen', True)
        else:
            PFCanvas.win.attributes('-fullscreen', False)

        PFCanvas.win.geometry(PFCanvas.geometry_str)
        PFCanvas.canvas.configure(bg='black')
        PFCanvas.win.update()

    ############################################################
    #
    # toggle_fullscreen
    #
    @staticmethod
    def toggle_fullscreen():
        """
        Toggle whether in fullscreen mode or not. 
        """
        PFCanvas.win.destroy()

        if PFCanvas.fullscreen:
            PFCanvas.fullscreen = False
            PFCanvas.set_settings_geom()
        else:
            PFCanvas.fullscreen = True
            PFCanvas.set_fullscreen_geom()

        PFCanvas.reset_window_size()
        PFCanvas.canvas.focus_set()

