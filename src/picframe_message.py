"""
picframe_message.py holds the messages passed on the picframe queue

"""
import logging
from enum import Enum, auto


class PFMessageContent(Enum):
    """
    What message is being sent.
    """
    NOOP = auto()
    TIMER_NEXT_IMAGE = auto()
    KEYBOARD_NEXT_IMAGE = auto()
    KEYBOARD_HOLD = auto()
    KEYBOARD_END_HOLD = auto()
    KEYBOARD_BLACKOUT= auto()
    KEYBOARD_END_BLACKOUT = auto()
    KEYBOARD_INCREASE_BRIGHTNESS = auto()
    KEYBOARD_DECREASE_BRIGHTNESS = auto()
    KEYBOARD_USE_DEFAULT_BRIGHTNESS = auto()
    KEYBOARD_EMULATE_MOTION = auto()
    KEYBOARD_EMULATE_MOTION_TIMEOUT = auto()

    BLACKOUT = auto()
    END_BLACKOUT = auto()

    INCREASE_BRIGHTNESS = auto()
    DECREASE_BRIGHTNESS = auto()

    MOTION = auto()
    MOTION_TIMEOUT = auto()
    
class PFMessage:
    """
    """
    ############################################################
    #
    # init_environment
    #
    def __init__(self, message):
        self.message = message


