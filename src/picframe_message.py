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
picframe_message.py holds and processes the messages passed on the 
picframe queues. It also generates the messages from key events on 
the canvas.

"""

from enum import Enum, auto

class PFMessage:
    """
    This class holds the messages that get put onto the message queues.
    """

    """
    What message is being sent.
    """
    NOOP = "NOOP"
    TIMER_NEXT_IMAGE = "TIMER_NEXT_MESSAGE"
    KEYBOARD_NEXT_IMAGE = "KEYBOARD_NEXT_IMAGE"
    KEYBOARD_HOLD = "KEYBOARD_HOLD"
    KEYBOARD_BLACKOUT = "KEYBOARD_BLACKOUT"
    KEYBOARD_INCREASE_BRIGHTNESS = "KEYBOARD_INCREASE_BRIGHTNESS"
    KEYBOARD_DECREASE_BRIGHTNESS = "KEYBOARD_DECREASE_BRIGHTNESS"
    KEYBOARD_INCREASE_DISPLAY_TIME = "KEYBOARD_INCREASE_DISPLAY_TIME"
    KEYBOARD_DECREASE_DISPLAY_TIME = "KEYBOARD_DECREASE_DISPLAY_TIME"
    KEYBOARD_USE_DEFAULT_BRIGHTNESS = "KEYBOARD_USE_DEFAULT_BRIGHTNESS"
    KEYBOARD_TOGGLE_MOTION_SENSOR = "KEYBOARD_TOGGLE_MOTION_SENSOR"
    KEYBOARD_FULLSCREEN = "KEYBOARD_FULLSCREEN"

    BLACKOUT = "BLACKOUT"
    END_BLACKOUT = "END_BLACKOUT"

    INCREASE_BRIGHTNESS = "INCREASE_BRIGHTNESS"
    DECREASE_BRIGHTNESS = "DECREASE_BRIGHTNESS"

    MOTION = "MOTION"
    MOTION_TIMEOUT = "MOTION_TIMEOUT"

    KEYBOARD_QUIT = "KEYBOARD_QUIT"

    canvas_mq = None
    video_mq = None
    timer_mq = None
    message = None

    ############################################################
    #
    # __init__
    #
    def __init__(self, message):
        self.message = message


