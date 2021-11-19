#!/mnt/c/tmp/frame/env/bin/python3

import sys
import os
import time
import datetime
import logging
import multiprocessing

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
    def get_sleep_interval():
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


    
