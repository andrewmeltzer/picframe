"""
picframe_message.py holds the messages passed on the picframe queue

"""
import logging

from picframe_messagecontent import PFMessageContent
from picframe_image import PFImage
from picframe_state import PFState, PFStates
from picframe_canvas import PFCanvas


class PFMessage:
    """
    Create and react to messages.
    """
    queue = None
    message = None

    ############################################################
    #
    # __message__
    #
    def __init__(self, message):
        self.message = message


    ############################################################
    #
    # keypress
    #
    @staticmethod
    def keypress(evnt):
        """
        Capture and react to a keypress event in the display window.
        """
        print(f"#########################{evnt} {evnt.char} pressed")
        key = evnt.char

        if key == 'f':
            PFMessage.queue.put(PFMessage(PFMessageContent.KEYBOARD_FULLSCREEN))
        if key == 'n':
            PFMessage.queue.put(PFMessage(PFMessageContent.KEYBOARD_NEXT_IMAGE))
        if key == 'h':
            PFMessage.queue.put(PFMessage(PFMessageContent.KEYBOARD_HOLD))
        if key == 'b':
            PFMessage.queue.put(PFMessage(PFMessageContent.KEYBOARD_BLACKOUT))
        if key == 'M':
            PFMessage.queue.put(PFMessage(PFMessageContent.KEYBOARD_EMULATE_MOTION))
        if key == 'm':
            PFMessage.queue.put(PFMessage(PFMessageContent.KEYBOARD_EMULATE_MOTION_TIMEOUT))
        if key == 'V':
            PFMessage.queue.put(PFMessage(PFMessageContent.KEYBOARD_INCREASE_BRIGHTNESS))
        if key == 'v':
            PFMessage.queue.put(PFMessage(PFMessageContent.KEYBOARD_DECREASE_BRIGHTNESS))

        if key == 'a':
            PFMessage.queue.put(PFMessage(PFMessageContent.KEYBOARD_USE_DEFAULT_BRIGHTNESS))
        if key in ('q', 'x'):
            PFMessage.queue.put(PFMessage(PFMessageContent.KEYBOARD_QUIT))

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
        if PFMessage.queue.empty():
            PFCanvas.win.after(100, PFMessage.process_message)
            return True

        PFMessage.message = PFMessage.queue.get_nowait()
        message = PFMessage.message

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
        PFCanvas.win.after(100, PFMessage.process_message)

        return True
