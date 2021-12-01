"""
picframe_message.py holds the messages passed on the picframe queue

"""
from enum import Enum, auto

class PFMessageContent(Enum):
    """
    What message is being sent.
    """
    NOOP = auto()
    TIMER_NEXT_IMAGE = auto()
    KEYBOARD_NEXT_IMAGE = auto()
    KEYBOARD_HOLD = auto()
    KEYBOARD_BLACKOUT = auto()
    KEYBOARD_INCREASE_BRIGHTNESS = auto()
    KEYBOARD_DECREASE_BRIGHTNESS = auto()
    KEYBOARD_USE_DEFAULT_BRIGHTNESS = auto()
    KEYBOARD_TOGGLE_MOTION_SENSOR = auto()
    KEYBOARD_FULLSCREEN = auto()
    KEYBOARD_QUIT = auto()

    BLACKOUT = auto()
    END_BLACKOUT = auto()

    INCREASE_BRIGHTNESS = auto()
    DECREASE_BRIGHTNESS = auto()

    MOTION = auto()
    MOTION_TIMEOUT = auto()
