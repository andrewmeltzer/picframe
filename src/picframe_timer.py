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
from picframe_messagecontent import PFMessageContent

class PFTimer:
    """
    Generate the timer messages for picframe for the between-frame
    timing.
    """

    ############################################################
    #
    # get_sleep_interval
    #
    @staticmethod
    def get_sleep_interval():
        """
        How long is it set to sleep for between pictures.
        """
        return PFSettings.display_time

    ############################################################
    #
    # timer_main
    #
    @staticmethod
    def timer_main(canvas_mq):
        """
        Continually loop, sending a next-image message every sleep interval
        Inputs:
            canvas_mq: The canvas message queue
        """
        PFEnv.setup_logger()
        while True:
            PFEnv.logger.debug("Putting next timer message.")
            canvas_mq.put(PFMessage(PFMessageContent.TIMER_NEXT_IMAGE))
            time.sleep(PFSettings.display_time)
