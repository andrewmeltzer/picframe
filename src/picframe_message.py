"""
picframe_message.py holds and processes the messages passed on the 
picframe queue. It also generates the messages from key events on 
the canvas.

"""

from picframe_messagecontent import PFMessageContent
from picframe_image import PFImage
from picframe_state import PFState, PFStates
from picframe_canvas import PFCanvas
from picframe_env import PFEnv
from picframe_settings import PFSettings


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
    # setup_canvas_messaging
    #
    @staticmethod
    def setup_canvas_messaging():
        """
        Set up the necessary messaging information for a canvas.
        """
        # When a key is pressed on the canvas, send message to keypress
        PFCanvas.canvas.bind("<KeyPress>", PFMessage.keypress)
        
        # Process non-keyboard messages
        PFCanvas.win.after(100, PFMessage.process_message)

        # enque a message to get the first real image on the screen
        PFMessage.queue.put(PFMessage(PFMessageContent.KEYBOARD_NEXT_IMAGE))

    ############################################################
    #
    # keypress
    #
    @staticmethod
    def keypress(evnt):
        """
        Capture and react to a keypress event in the display window.
        """
        key = evnt.char

        if key == 'f':
            PFEnv.logger.info("Sending message: Fullscreen")
            PFMessage.queue.put(PFMessage(PFMessageContent.KEYBOARD_FULLSCREEN))
        if key == 'n':
            PFEnv.logger.info("Sending message: Next Image")
            PFMessage.queue.put(PFMessage(PFMessageContent.KEYBOARD_NEXT_IMAGE))
        if key == 'h':
            PFEnv.logger.info("Sending message: Hold Image")
            PFMessage.queue.put(PFMessage(PFMessageContent.KEYBOARD_HOLD))
        if key == 'b':
            PFEnv.logger.info("Sending message: Blackout Screen")
            PFMessage.queue.put(PFMessage(PFMessageContent.KEYBOARD_BLACKOUT))
        if key == 'm':
            """ ++++
            if PFVideo.use_motion_sensor:
                PFEnv.logger.info("Sending message: Toggle Motion Detector Off")
            else:
                PFEnv.logger.info("Sending message: Toggle Motion Detector On")
            """
            PFMessage.queue.put(PFMessage(PFMessageContent.KEYBOARD_TOGGLE_MOTION_SENSOR))
        if key == 'V':
            PFEnv.logger.info("Sending message: Increase Brightness")
            PFMessage.queue.put(PFMessage(PFMessageContent.KEYBOARD_INCREASE_BRIGHTNESS))
        if key == 'v':
            PFEnv.logger.info("Sending message: Decrease Brightness")
            PFMessage.queue.put(PFMessage(PFMessageContent.KEYBOARD_DECREASE_BRIGHTNESS))

        if key == 'a':
            PFEnv.logger.info("Sending message: Use Default Brightness")
            PFMessage.queue.put(PFMessage(PFMessageContent.KEYBOARD_USE_DEFAULT_BRIGHTNESS))
        if key in ('q', 'x'):
            PFEnv.logger.info("Sending message: Quit")
            PFMessage.queue.put(PFMessage(PFMessageContent.KEYBOARD_QUIT))


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
            PFImage.display_first_image()
            PFMessage.setup_canvas_messaging()

    
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

        # See if the canvas has changed size
        PFMessage.adjust_canvas_geom()

        PFMessage.message = PFMessage.queue.get_nowait()
        message = PFMessage.message
        PFEnv.logger.debug("process_message: %s" % (str(message.message),))

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

        elif message.message == PFMessageContent.KEYBOARD_BLACKOUT:
            if PFState.current_state == PFStates.KEYBOARD_BLACKOUT:
                PFImage.display_next_image()
            else:
                PFImage.display_black_image()

        elif message.message == PFMessageContent.KEYBOARD_INCREASE_BRIGHTNESS:
            PFImage.adjust_brightness('up')
        elif message.message == PFMessageContent.KEYBOARD_DECREASE_BRIGHTNESS:
            PFImage.adjust_brightness('down')
        elif message.message == PFMessageContent.KEYBOARD_USE_DEFAULT_BRIGHTNESS:
            PFImage.brightness = 1
        elif message.message == PFMessageContent.KEYBOARD_TOGGLE_MOTION_SENSOR:
            """ ++++
            if PFVideo.use_motion_sensor:
                PFVideo.use_motion_sensor = False
            else:
                PFVideo.use_motion_sensor = True
            """
            PFImage.display_next_image()
        elif message.message == PFMessageContent.BLACKOUT:
            PFImage.display_black_image()
        elif message.message == PFMessageContent.END_BLACKOUT:
            PFImage.display_current_image()
        elif message.message == PFMessageContent.INCREASE_BRIGHTNESS:
            PFImage.adjust_brightness('up')
        elif message.message == PFMessageContent.DECREASE_BRIGHTNESS:
            PFImage.adjust_brightness('down')
        elif message.message == PFMessageContent.MOTION:
            PFImage.display_current_image()
        elif message.message == PFMessageContent.KEYBOARD_FULLSCREEN:
            PFCanvas.toggle_fullscreen()
            PFMessage.setup_canvas_messaging()
            PFImage.display_first_image()

            # This runs forever until a 'q' or 'x' is entered.
            PFCanvas.win.mainloop()

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
