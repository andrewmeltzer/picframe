"""
picframe_state.py manages the state transitions based on the message
received and the current state.

"""
from enum import Enum, auto
from picframe_messagecontent import PFMessageContent



class PFStates(Enum):
    """
    What state can the system be in?
    """
    NORMAL = auto()
    BLACKOUT = auto()
    MOTION_BLACKOUT = auto()
    KEYBOARD_HOLD = auto()
    KEYBOARD_BLACKOUT = auto()

class PFState:
    """
    Define the states and the state transitions for the picframe.
    """
    current_state = PFStates.NORMAL
    previous_state = PFStates.NORMAL

    normal_state_map = {
        PFMessageContent.KEYBOARD_HOLD: PFStates.KEYBOARD_HOLD,
        PFMessageContent.KEYBOARD_BLACKOUT: PFStates.KEYBOARD_BLACKOUT,
        PFMessageContent.BLACKOUT: PFStates.BLACKOUT,
        PFMessageContent.MOTION_TIMEOUT: PFStates.MOTION_BLACKOUT,
    }
    blackout_state_map = {
        PFMessageContent.KEYBOARD_HOLD: PFStates.KEYBOARD_HOLD,
        PFMessageContent.KEYBOARD_BLACKOUT: PFStates.NORMAL,
        PFMessageContent.END_BLACKOUT: PFStates.NORMAL,
    }
    motion_blackout_state_map = {
        PFMessageContent.KEYBOARD_HOLD: PFStates.KEYBOARD_HOLD,
        PFMessageContent.MOTION: PFStates.NORMAL,
        PFMessageContent.KEYBOARD_TOGGLE_MOTION_SENSOR: PFStates.NORMAL,
    }
    keyboard_blackout_state_map = {
        PFMessageContent.KEYBOARD_HOLD: PFStates.KEYBOARD_HOLD,
        PFMessageContent.KEYBOARD_BLACKOUT: PFStates.NORMAL,
    }
    keyboard_hold_state_map = {
        PFMessageContent.KEYBOARD_HOLD: PFStates.NORMAL,
    }


    ############################################################
    #
    # new_state
    #
    @staticmethod
    def new_state(message):
        """
        Given a state and a message, set the new state.
        """

        state_map = PFState.normal_state_map
        if PFState.current_state == PFStates.NORMAL:
            state_map = PFState.normal_state_map
        elif PFState.current_state == PFStates.BLACKOUT:
            state_map = PFState.blackout_state_map
        elif PFState.current_state == PFStates.MOTION_BLACKOUT:
            state_map = PFState.motion_blackout_state_map
        elif PFState.current_state == PFStates.KEYBOARD_HOLD:
            state_map = PFState.keyboard_hold_state_map
        elif PFState.current_state == PFStates.KEYBOARD_BLACKOUT:
            state_map = PFState.keyboard_blackout_state_map

        if message.message in state_map:
            PFState.previous_state = PFState.current_state
            PFState.current_state = state_map[message.message]
