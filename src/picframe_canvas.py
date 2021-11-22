#!/mnt/c/tmp/frame/env/bin/python3
"""
picframe_canvas.py
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

    ############################################################
    #
    # init
    #
    @staticmethod
    def init():
        """
        One-time initialization of the class.
        """

        PFCanvas.fullscreen = PFSettings.fullscreen
        PFCanvas.get_window()
        PFCanvas.get_canvas()
        PFCanvas.win.geometry(PFEnv.geometry_str)
        PFCanvas.canvas.configure(bg='black')
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

        PFCanvas.win = Tk(className="Picframe")
        PFCanvas.win.resizable(height=None, width=None)
        PFCanvas.win.geometry(PFEnv.geometry_str)
        if PFCanvas.fullscreen:
            PFCanvas.win.attributes('-fullscreen', True)
            PFCanvas.win.attributes('-type', 'dock')


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
        PFCanvas.canvas = Canvas(PFCanvas.win, width=PFEnv.screen_width, height=PFEnv.screen_height)

        PFCanvas.canvas.pack(fill=tkinter.BOTH, expand=True)
        PFCanvas.canvas.grid(row=1, column=1)
        PFCanvas.canvas.focus_set()


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
            PFEnv.set_settings_geom()
        else:
            PFCanvas.fullscreen = True
            PFEnv.set_fullscreen_geom()

        PFCanvas.get_window()
        PFCanvas.get_canvas()

        PFCanvas.win.geometry(PFEnv.geometry_str)
        if PFCanvas.fullscreen:
            PFCanvas.win.attributes('-type', 'dock')
            PFCanvas.win.attributes('-fullscreen', True)
        PFCanvas.canvas.configure(bg='black')
        PFCanvas.win.update()
