#!/mnt/c/tmp/frame/env/bin/python3
"""
picframe_timer.py
"""

import time
import logging

from picframe_settings import PFSettings
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
    def timer_main(queue):
        """
        Continually loop, sending a next-image message every sleep interval
        Inputs:
            queue: The message queue
        """

        while True:
            logging.debug("Putting next timer message.")
            queue.put(PFMessage(PFMessageContent.TIMER_NEXT_IMAGE))
            time.sleep(PFSettings.display_time)
