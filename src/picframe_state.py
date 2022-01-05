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
picframe_state.py manages the state transitions based on the message
received and the current state.

"""
from enum import Enum, auto
from picframe_message import PFMessage

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
        PFMessage.KEYBOARD_HOLD: PFStates.KEYBOARD_HOLD,
        PFMessage.KEYBOARD_BLACKOUT: PFStates.KEYBOARD_BLACKOUT,
        PFMessage.BLACKOUT: PFStates.BLACKOUT,
        PFMessage.MOTION_TIMEOUT: PFStates.MOTION_BLACKOUT,
        PFMessage.KEYBOARD_HELP_INFO: PFStates.KEYBOARD_HOLD,
        PFMessage.KEYBOARD_DETAILS_INFO: PFStates.KEYBOARD_HOLD,
    }
    blackout_state_map = {
        PFMessage.KEYBOARD_HOLD: PFStates.KEYBOARD_HOLD,
        PFMessage.KEYBOARD_BLACKOUT: PFStates.NORMAL,
        PFMessage.END_BLACKOUT: PFStates.NORMAL,
    }
    motion_blackout_state_map = {
        PFMessage.KEYBOARD_HOLD: PFStates.KEYBOARD_HOLD,
        PFMessage.MOTION: PFStates.NORMAL,
        PFMessage.BLACKOUT: PFStates.BLACKOUT,
        PFMessage.KEYBOARD_TOGGLE_MOTION_SENSOR: PFStates.NORMAL,
    }
    keyboard_blackout_state_map = {
        PFMessage.KEYBOARD_HOLD: PFStates.KEYBOARD_HOLD,
        PFMessage.KEYBOARD_BLACKOUT: PFStates.NORMAL,
    }
    keyboard_hold_state_map = {
        PFMessage.KEYBOARD_HOLD: PFStates.NORMAL,
        PFMessage.KEYBOARD_HELP_INFO: PFStates.NORMAL,
        PFMessage.KEYBOARD_DETAILS_INFO: PFStates.NORMAL,
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
