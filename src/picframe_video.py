#!/mnt/c/tmp/frame/env/bin/python3
"""
picframe_video.py

Send a blackout message if there has been no motion for the configured
number of minutes.

Also adjust the brightness of the image as the room darkens.
"""

import cv2
from datetime import datetime
import time

from picframe_env import PFEnv
from picframe_settings import PFSettings
from picframe_message import PFMessage

class PFVideo:
    """
    Generate a blackout message if there has been no motion for the
    configured (motion_sensor_timeout) amount of time.

    This takes a picture of the initial scene and if any scene differs
    it decides there has been motion.
    """
    camera = None
    use_motion_sensor = True

    ############################################################
    #
    # motion_cleanup
    #
    @staticmethod
    def motion_cleanup():
        """
        Close the video and cleanup.
        """
        if PFVideo.camera is not None:
            # Destroying all the windows
            cv2.destroyAllWindows()
        
    ############################################################
    #
    # motion_main
    #
    @staticmethod
    def motion_main(canvas_mq, video_mq):
        """
        Continually loop, sending a blackout message if no motion has been
        detected.
        Inputs:
            canvas_mq: The canvas message queue
        """

        PFEnv.setup_logger()
        PFVideo.use_motion_sensor = PFSettings.use_motion_sensor

        # Return if nothing to do
        if PFSettings.motion_sensor_timeout is None or PFSettings.motion_sensor_timeout == 0:
            return

        # Keep track of the last time motion was seen so we know when to 
        # timeout
        last_motion = None

        # Is it in a state where no motion has been seen for a while?
        in_motion_timeout = False

        # Delay between two snapshots
        #delay_scanning = 0.2
        #delay_presence = 0.025
        delay_scanning = 0.5
        delay_presence = 0.0

        # How long should it run before the image is stable.
        ramp_frames = 40

        # See if the we have seen motion recently
        last_motion = datetime.now()
        image1 = None

        # Init capture
        PFVideo.camera = cv2.VideoCapture(PFSettings.camera_port)

        # Ramp the camera -  skip while frames while
        # the camera adjusts to light levels
        for frame in range(ramp_frames):
            ret, image1 = PFVideo.camera.read()

        delay = delay_scanning

        while True:
            start = time.time()
            time.sleep(delay)

            # See if any process sent this one a message
            if not video_mq.empty():
                message = video_mq.get_nowait()
                PFEnv.logger.debug("Video message: %s" % (str(message.message),))
                if message.message == PFMessage.KEYBOARD_TOGGLE_MOTION_SENSOR:
                    if PFVideo.use_motion_sensor:
                        PFEnv.logger.info("Disabling motion detector")
                        PFVideo.use_motion_sensor = False
                        canvas_mq.put(PFMessage(PFMessage.MOTION))
                    else:
                        PFEnv.logger.info("Enabling motion detector")
                        PFVideo.use_motion_sensor = True

            # See if the motion sensor is disabled via the settings
            if not PFVideo.use_motion_sensor:
                continue

            # when it fails, it says:
            #   Corrupt JPEG data: premature end of data segment
            ret, image2 = PFVideo.camera.read()

            # Triggers
            brightness_threshold = 50
            mesh = 10
    
            height, width, channels = image2.shape
    
            # cv2.imshow('capture', image2)
    
            # Convert to grayscale and Make diff
            image1_grey = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
            image2_grey = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
            capt_diff_grey = cv2.absdiff(image1_grey, image2_grey)
    
            # Parse image
            changedpixels = 0
            for i_row in range(0, height):
                if not i_row % mesh:
                    for i_col in range(0, width):
                        if not i_col % mesh:
                            if capt_diff_grey[i_row,i_col] > brightness_threshold:
                                changedpixels += 1
    
            if changedpixels > PFSettings.pixel_threshold:
                # change capture range
                delay = delay_presence
                PFEnv.logger.info(f"Motion detected. changedpixels = {changedpixels}")
    
                # Send a message to indicate motion ocurred
                last_motion = datetime.now()
                if in_motion_timeout:
                    in_motion_timeout = False
                    PFEnv.logger.info("Motion timeout disabled.")
                    canvas_mq.put(PFMessage(PFMessage.MOTION))
            else:
                delay = delay_scanning
    
            # See of the motion that was seen was too long ago.
            minutes_diff = (datetime.now() - last_motion).total_seconds()/60.0
            if minutes_diff > PFSettings.motion_sensor_timeout:
                if not in_motion_timeout:
                    in_motion_timeout = True
                    PFEnv.logger.info("Motion timeout occurred.")
                    canvas_mq.put(PFMessage(PFMessage.MOTION_TIMEOUT))
    
    

            image1 = image2
