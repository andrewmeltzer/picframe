"""
picframe_keyboard.py provides a keyboard interface to the picframe app.

"""
import sys
import logging
import curses
import os

from picframe_settings import PFSettings
from picframe_messagecontent import PFMessageContent
from picframe_message import PFMessage

class PFKeyboard():
    """
    Add a keyboard interface to the picframe app.
    """

    help_added = False
    queue = None

    ############################################################
    #
    # getkey
    #
    @staticmethod
    def getkey(stdscr):
        """
        Wait for keyboard input and when it arrives return it to the
        caller
        """

        key = chr(stdscr.getch())

        return key

    ############################################################
    #
    # keyboard_action
    #
    @staticmethod
    def keyboard_action(stdscr):
        """
        Wait for keyboard input and when it arrives queue it up.
            queue: The message queue
        """
        if not PFKeyboard.help_added:
            stdscr.addstr("f: Toggle fullscreen" + os.linesep)
            stdscr.addstr("n: Next picture" + os.linesep)
            stdscr.addstr("h: Toggle hold current picure" + os.linesep)
            stdscr.addstr("b: Toggle blackout mode" + os.linesep)
            stdscr.addstr("M: Motion start as if the motion detector went off" + os.linesep)
            stdscr.addstr("m: Motion stop as if the motion detector timed out" + os.linesep)
            stdscr.addstr("V: Increase video brightness" + os.linesep)
            stdscr.addstr("v: Decrease video brightess" + os.linesep)
            stdscr.addstr("a: Return to automatic video mode" + os.linesep)
            stdscr.addstr("x or q: Quit" + os.linesep)
            PFKeyboard.help_added = True
        
        queue = PFKeyboard.queue
        status = True
        while status:
            key = PFKeyboard.getkey(stdscr)
    
            if key == 'f':
                queue.put(PFMessage(PFMessageContent.KEYBOARD_FULLSCREEN))
            if key == 'n':
                queue.put(PFMessage(PFMessageContent.KEYBOARD_NEXT_IMAGE))
            if key == 'h':
                queue.put(PFMessage(PFMessageContent.KEYBOARD_HOLD))
            if key == 'b':
                queue.put(PFMessage(PFMessageContent.KEYBOARD_BLACKOUT))
            if key == 'M':
                queue.put(PFMessage(PFMessageContent.KEYBOARD_EMULATE_MOTION))
            if key == 'm':
                queue.put(PFMessage(PFMessageContent.KEYBOARD_EMULATE_MOTION_TIMEOUT))
            if key == 'V':
                queue.put(PFMessage(PFMessageContent.KEYBOARD_INCREASE_BRIGHTNESS))
            if key == 'v':
                queue.put(PFMessage(PFMessageContent.KEYBOARD_DECREASE_BRIGHTNESS))
    
            if key == 'a':
                queue.put(PFMessage(PFMessageContent.KEYBOARD_USE_DEFAULT_BRIGHTNESS))
            if key in ('q', 'x'):
                status = False
    

    
    ############################################################
    #
    # keyboard_main
    #
    @staticmethod
    def keyboard_main(queue):
        """
        Loop, waiting for keyboard input and when it arrives queue it up.
            queue: The message queue
        """
        PFKeyboard.queue = queue
        curses.wrapper(PFKeyboard.keyboard_action)
