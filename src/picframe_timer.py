#!/mnt/c/tmp/frame/env/bin/python3

import sys
import os
import time
import datetime
import logging

from picframe_settings import PFSettings
from picframe_env import PFEnv

class PicframeTimer:
    """
    Generate the timer messages for picframe, including the between-frame
    timing and the (optional) nightly shutoff timing.
    """
    
    ############################################################
    #
    # check_blackout_window
    #
    @staticmethod
    def check_blackout_window():
        """
        See if in the sleep window, and if so then sleep for the 
        right number of seconds.
        """
        if PFSettings.sleep_hour is None:
            return 0
    
        secs_per_min = 60
        mins_per_hour = 60
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
    
        now_time = hour*60 + minute
        sleep_time = (PFSettings.sleep_hour * mins_per_hour) + PFSettings.sleep_minute
        wake_time = (PFSettings.wake_hour * mins_per_hour) + PFSettings.wake_minute
        sleep_interval = 0
    
        # if it is sleeping across midnight and it is before midnight
        if wake_time < sleep_time and now_time > sleep_time:
            sleep_interval = (wake_time * secs_per_min) \
                + (24 * mins_per_hour) - now_time
    
        # if it is sleeping across midnight and it is after midnight
        if wake_time < sleep_time and now_time < wake_time:
            sleep_interval = (wake_time - now_time) * secs_per_min
    
        if now_time > sleep_time and now_time < wake_time:
            sleep_interval = (wake_time - now_time) * secs_per_min
    
        if sleep_interval == 0:
            return 0
            
        logging.info(f"Going dark for {sleep_interval} seconds.")

        # ++++ When fully event driven, this needs to move to main loop
        PicframeImage.display_image(None)

        return sleep_interval
        

    ############################################################
    #
    # get_sleep_interval
    #
    @staticmethod
    def get_sleep_interval():
        """
        Determine the current sleep interval, either the (short) interval
        between images, or a long period for optionally nightly blackout.
        """

        blackout_interval = PicframeTimer.check_blackout_window()
        sleep_interval = max(blackout_interval, PFSettings.display_time)

        return sleep_interval


    
