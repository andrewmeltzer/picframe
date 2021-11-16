#!/mnt/c/tmp/frame/env/bin/python3

import sys
import os
import time
import datetime
import logging

from picframe_settings import PFSettings
from picframe_env import PFEnv

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
    def timer_main():
        """
        Continually loop, sending a next-image message every sleep interval
        """

        while True:
            # ++++ Send next-image message
            sleep(PFSettings.display_time)
            pass


    
