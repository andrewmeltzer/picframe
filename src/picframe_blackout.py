#!/mnt/c/tmp/frame/env/bin/python3

import sys
import os
import time
import datetime
import logging

from picframe_settings import PFSettings
from picframe_env import PFEnv

class PicframeBlackout:
    """
    See if we are in a nightly blackout window, and if so, send a message
    to black out the screen.

    If emerging from the blackout window, send a message indicating that.
    """
    in_blackout = False
    
    ############################################################
    #
    # check_blackout_window
    #
    @staticmethod
    def check_blackout_window():
        """
        Check for a change in blackout status.
        
        """
        if PFSettings.blackout_hour is None:
            return 0
    
        secs_per_min = 60
        mins_per_hour = 60
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
    
        now_time = hour*60 + minute
        blackout_time = (PFSettings.blackout_hour * mins_per_hour) + PFSettings.blackout_minute
        end_blackout_time = (PFSettings.end_blackout_hour * mins_per_hour) + PFSettings.end_blackout_minute
        blackout_length = 0
    
        # if it is blacked out across midnight and it is before midnight
        # but in the blackout period
        if end_blackout_time < blackout_time and now_time > blackout_time:
            blackout_length = (end_blackout_time * secs_per_min) \
                + (24 * mins_per_hour) - now_time
    
        # if it is blacked out across midnight and it is after midnight
        # but in the blackout period
        if end_blackout_time < blackout_time and now_time < end_blackout_time:
            blackout_length = (end_blackout_time - now_time) * secs_per_min
    
        # if it is not blacked out across midnight, but in the blackout period
        if now_time > blackout_time and now_time < end_blackout_time:
            blackout_length = (end_blackout_time - now_time) * secs_per_min
    
        return blackout_length
        

    ############################################################
    #
    # get_blackout_length
    #
    @staticmethod
    def get_blackout_length():
        """
        Determine the current blackout interval
        """

        blackout_interval = PicframeBlackout.check_blackout_window()
        return blackout_interval


    ############################################################
    #
    # blackout_main
    #
    @staticmethod
    def blackout_main():
        """
        Continually loop, checking to see if the blackout status changes
        and if so, send the blackout message.
        """
        while True:
            blackout_interval = PicframeBlackout.check_blackout_window()
            if blackout_interval > 0:
                if PicframeBlackout.in_blackout == False:
                    # ++++ Send blackout message
                    logging.info(f"Going dark for {blackout_interval} seconds.")
                    PicframeBlackout.in_blackout = True
                    pass
            else:
                if PicframeBlackout.in_blackout == True:
                    # ++++ Send end blackout message
                    PicframeBlackout.in_blackout = False
                    pass

            # Test every 60 seconds
            sleep(60)

    
