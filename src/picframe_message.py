"""
picframe_message.py holds the messages passed on the picframe queue

"""
import logging
from enum import Enum, auto
from picframe_state import PFState, PFStates
from picframe_messagecontent import PFMessageContent
from picframe_image import PFImage

class PFMessage:
    """
    """
    ############################################################
    #
    # init_environment
    #
    def __init__(self, message):
        self.message = message


    ############################################################
    #
    # process_message
    #
    @staticmethod
    def process_message(message):
        """
        Process the next message from the queue based on the current state
        of the system and the message.  As a rule of thumb, keyboard actions
        take precedence over everything else.
        """
    
        # Only go to the next message if in the normal state.
        if message.message == PFMessageContent.TIMER_NEXT_IMAGE:
            if PFState.current_state == PFStates.NORMAL:
                PFImage.display_next_image()
    
        # If the keyboard says next image, override any holds or blackouts
        elif message.message == PFMessageContent.KEYBOARD_NEXT_IMAGE:
            PFImage.display_next_image()
    
        elif message.message == PFMessageContent.KEYBOARD_HOLD:
            if PFState.current_state == PFStates.KEYBOARD_HOLD:
                PFImage.display_next_image()
            else:
                pass
    
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
            pass
        elif message.message == PFMessageContent.INCREASE_BRIGHTNESS:
            pass
        elif message.message == PFMessageContent.DECREASE_BRIGHTNESS:
            pass
        elif message.message == PFMessageContent.MOTION:
            pass
        elif message.message == PFMessageContent.TOGGLE_FULLSCREEN:
            logging.warn("Fullscreen toggling is not yet implemented.")
            raise NotImplementedError("Fullscreen toggling is not yet implemented.")
        elif message.message == PFMessageContent.MOTION_TIMEOUT:
            PFImage.display_black_image()
        elif message.message == PFMessageContent.KEYBOARD_QUIT:
            return False
    
        PFState.new_state(message)
    
        return True


    ############################################################
    #
    # message_main
    #
    @staticmethod
    def message_main(queue):
        """
        Continually loop, receiving and processing messages
        Inputs: 
            queue: The message queue
        """

        status = True
        while status:
            message = queue.get()
            status = PFMessage.process_message(message)

    
