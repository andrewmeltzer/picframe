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
                    display_time = display_time + PFSettings.timer_step
                if message.message == PFMessage.KEYBOARD_DECREASE_DISPLAY_TIME:
                    if display_time > PFSettings.timer_step:
                        display_time = display_time - PFSettings.timer_step

            canvas_mq.put(PFMessage(PFMessage.TIMER_NEXT_IMAGE))
            time.sleep(display_time)
