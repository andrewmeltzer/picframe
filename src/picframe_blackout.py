#!/mnt/c/tmp/frame/env/bin/python3
"""
Calculate and send a message when in a blackout window (usually meant for
turning the screen off overnight) and when coming out of blackout.

This runs as a separate process in a continual loop, sleeping until it is
next tested.  

"""
import time
import datetime

from picframe_settings import PFSettings
from picframe_message import PFMessage
from picframe_messagecontent import PFMessageContent
from picframe_env import PFEnv

class PFBlackout:
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
    # blackout_main
    #
    @staticmethod
    def blackout_main(canvas_mq):
        """
        Continually loop, checking to see if the blackout status changes
        and if so, send the blackout message.
        Inputs:
            canvas_mq: The canvas message queue
        """
        PFEnv.setup_logger()

        while True:
            blackout_interval = PFBlackout.check_blackout_window()
            if blackout_interval > 0:
                if not PFBlackout.in_blackout:
                    # Send blackout message
                    canvas_mq.put(PFMessage(PFMessageContent.BLACKOUT))
                    PFEnv.logger.info("Going dark for %d seconds." % (blackout_interval,))
                    PFBlackout.in_blackout = True
            else:
                if PFBlackout.in_blackout:
                    # Send end blackout message
                    canvas_mq.put(PFMessage(PFMessageContent.END_BLACKOUT))
                    PFBlackout.in_blackout = False

            # Test every 60 seconds
            time.sleep(60)
