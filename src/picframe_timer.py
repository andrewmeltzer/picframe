#!/mnt/c/tmp/frame/env/bin/python3
"""
picframe_timer.py

Send a new image message on the settings-requested time schedule.
"""

import time
import logging
import sys

from picframe_settings import PFSettings
from picframe_env import PFEnv
from picframe_message import PFMessage

class PFTimer:
    """
    Generate the timer messages for picframe for the between-frame
    timing.
    """

    # TIMER_STEP is the amount of time to increase or decrease the 
    # display time by when the value is changed.
    TIMER_STEP = 10

    ############################################################
    #
    # timer_main
    #
    @staticmethod
    def timer_main(canvas_mq, timer_mq):
        """
        Continually loop, sending a next-image message every sleep interval
        Inputs:
            canvas_mq: The canvas message queue
        """
        PFEnv.setup_logger()
        display_time = PFSettings.display_time

        while True:
            PFEnv.logger.debug("Putting next timer message.")
            
            # See if any process sent this one a message
            if not timer_mq.empty():
                message = timer_mq.get_nowait()
                PFEnv.logger.debug("timer message: %s" % (str(message.message),))
                if message.message == PFMessage.KEYBOARD_INCREASE_DISPLAY_TIME:
                    display_time = display_time + PFTimer.TIMER_STEP
                if message.message == PFMessage.KEYBOARD_DECREASE_DISPLAY_TIME:
                    if display_time > PFTimer.TIMER_STEP:
                        display_time = display_time - PFTimer.TIMER_STEP

            canvas_mq.put(PFMessage(PFMessage.TIMER_NEXT_IMAGE))
            time.sleep(display_time)
