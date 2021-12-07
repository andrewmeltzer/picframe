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
picframe_canvas_message.py processes the messages passed on the 
picframe canvas_queue. It also generates the messages from key events on 
the canvas.

"""

from picframe_message import PFMessage
from picframe_image import PFImage
from picframe_state import PFState, PFStates
from picframe_canvas import PFCanvas
from picframe_env import PFEnv
from picframe_settings import PFSettings


class PFCanvasMessage:
    """
    Process canvas-based messages.
    """
    in_blackout = False

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
        PFCanvas.canvas.bind("<KeyPress>", PFCanvasMessage.keypress)
        
        # Process non-keyboard messages
        PFCanvas.win.after(100, PFCanvasMessage.process_canvas_message)

        # enque a message to get the first real image on the screen
        PFMessage.canvas_mq.put(PFMessage(PFMessage.KEYBOARD_NEXT_IMAGE))

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
            PFMessage.canvas_mq.put(PFMessage(PFMessage.KEYBOARD_FULLSCREEN))
        if key == 'n':
            PFEnv.logger.info("Sending message: Next image")
            PFMessage.canvas_mq.put(PFMessage(PFMessage.KEYBOARD_NEXT_IMAGE))
        if key == 'h':
            PFEnv.logger.info("Sending message: Hold image")
            PFMessage.canvas_mq.put(PFMessage(PFMessage.KEYBOARD_HOLD))
        if key == 'b':
            PFEnv.logger.info("Sending message: Blackout screen")
            PFMessage.canvas_mq.put(PFMessage(PFMessage.KEYBOARD_BLACKOUT))
        if key == 'm':
            PFEnv.logger.info("Sending message: Toggle motion detector")
            PFMessage.video_mq.put(PFMessage(PFMessage.KEYBOARD_TOGGLE_MOTION_SENSOR))
        if key == 'V':
            PFEnv.logger.info("Sending message: Increase brightness")
            PFMessage.canvas_mq.put(PFMessage(PFMessage.KEYBOARD_INCREASE_BRIGHTNESS))
        if key == 'v':
            PFEnv.logger.info("Sending message: Decrease brightness")
            PFMessage.canvas_mq.put(PFMessage(PFMessage.KEYBOARD_DECREASE_BRIGHTNESS))

        if key == 'P':
            PFEnv.logger.info("Sending message: Increase image display time")
            PFMessage.timer_mq.put(PFMessage(PFMessage.KEYBOARD_INCREASE_DISPLAY_TIME))
        if key == 'p':
            PFEnv.logger.info("Sending message: Decrease image display time")
            PFMessage.timer_mq.put(PFMessage(PFMessage.KEYBOARD_DECREASE_DISPLAY_TIME))

        if key == 'a':
            PFEnv.logger.info("Sending message: Use Default brightness")
            PFMessage.canvas_mq.put(PFMessage(PFMessage.KEYBOARD_USE_DEFAULT_BRIGHTNESS))
        if key in ('q', 'x'):
            PFEnv.logger.info("Sending message: Quit")
            PFMessage.canvas_mq.put(PFMessage(PFMessage.KEYBOARD_QUIT))

    
    ############################################################
    #
    # process_canvas_message
    #
    @staticmethod
    def process_canvas_message():
        """
        Process the next message from the canvas message queue based 
        on the current state of the system and the message.  
        As a rule of thumb, keyboard actions
        take precedence over everything else.
        """
        if PFMessage.canvas_mq.empty():
            PFCanvas.win.after(100, PFCanvasMessage.process_canvas_message)
            return True

        # See if the canvas has changed size
        adjusted = PFCanvas.adjust_canvas_geom()
        if adjusted:
            PFImage.display_first_image()
            PFCanvasMessage.setup_canvas_messaging()

        PFMessage.message = PFMessage.canvas_mq.get_nowait()
        message = PFMessage.message
        PFEnv.logger.debug("process_canvas_message: %s" % (str(message.message),))

        # Only go to the next message if in the normal state.
        if message.message == PFMessage.TIMER_NEXT_IMAGE:
            if PFState.current_state == PFStates.NORMAL:
                PFImage.display_next_image()

        # If the keyboard says next image, override any holds or blackouts
        elif message.message == PFMessage.KEYBOARD_NEXT_IMAGE:
            PFImage.display_next_image()

        elif message.message == PFMessage.KEYBOARD_HOLD:
            if PFState.current_state == PFStates.KEYBOARD_HOLD:
                PFImage.display_next_image()

        elif message.message == PFMessage.KEYBOARD_BLACKOUT:
            if PFState.current_state == PFStates.KEYBOARD_BLACKOUT:
                PFImage.display_next_image()
            else:
                PFImage.display_black_image()

        elif message.message == PFMessage.KEYBOARD_INCREASE_BRIGHTNESS:
            PFImage.adjust_brightness('up')
        elif message.message == PFMessage.KEYBOARD_DECREASE_BRIGHTNESS:
            PFImage.adjust_brightness('down')
        elif message.message == PFMessage.KEYBOARD_USE_DEFAULT_BRIGHTNESS:
            PFImage.brightness = 1
        elif message.message == PFMessage.BLACKOUT:
            PFCanvasMessage.in_blackout = True
            PFImage.display_black_image()
        elif message.message == PFMessage.END_BLACKOUT:
            PFCanvasMessage.in_blackout = False
            PFImage.display_current_image()
        elif message.message == PFMessage.INCREASE_BRIGHTNESS:
            PFImage.adjust_brightness('up')
        elif message.message == PFMessage.DECREASE_BRIGHTNESS:
            PFImage.adjust_brightness('down')
        elif message.message == PFMessage.MOTION:
            if not PFCanvasMessage.in_blackout:
                PFImage.display_next_image()
        elif message.message == PFMessage.KEYBOARD_FULLSCREEN:
            PFCanvas.toggle_fullscreen()
            PFCanvasMessage.setup_canvas_messaging()
            PFImage.display_first_image()

            # This runs forever until a 'q' or 'x' is entered.
            PFCanvas.win.mainloop()

        elif message.message == PFMessage.MOTION_TIMEOUT:
            if not PFCanvasMessage.in_blackout:
                PFImage.display_black_image()
        elif message.message == PFMessage.KEYBOARD_QUIT:
            PFCanvas.win.quit()
            PFCanvas.canvas.quit()
            PFCanvas.win.destroy()
        else:
            PFImage.display_current_image()

        PFState.new_state(message)
        PFCanvas.win.after(100, PFCanvasMessage.process_canvas_message)

        return True
