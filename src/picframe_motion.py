#!/mnt/c/tmp/frame/env/bin/python3
"""
picframe_motion.py

Send a blackout message if there has been no motion for the configured
number of minutes.
"""

import cv2
import logging
from datetime import datetime

from picframe_settings import PFSettings
from picframe_message import PFMessage
from picframe_messagecontent import PFMessageContent

class PFMotion:
    """
    Generate a blackout message if there has been no motion for the
    configured (motion_sensor_timeout) amount of time.
    """

    # The video stream
    video = None

    ############################################################
    #
    # motion_cleanup
    #
    @staticmethod
    def motion_cleanup():
        """
        Close the video and cleanup.
        """
        if PFMotion.video is not None:
            PFMotion.video.release()
        
            # Destroying all the windows
            cv2.destroyAllWindows()
        
    ############################################################
    #
    # motion_main
    #
    @staticmethod
    def motion_main(queue):
        """
        Continually loop, sending a blackout message if no motion has been
        detected.
        Inputs:
            queue: The message queue
        """

        # Assigning our static_back to None
        static_back = None

        # Return if nothing to do
        if PFSettings.motion_sensor_timeout is None or PFSettings.motion_sensor_timeout == 0:
            return

        # List when any moving object appear
        motion_list = [ None, None ]
    
        in_motion_timeout = False

        # Capturing video
        PFMotion.video = cv2.VideoCapture(0)

        last_motion = datetime.now()
        
        # Infinite while loop to treat stack of image as video
        while True:
            # Reading frame(image) from video
            check, frame = PFMotion.video.read()
        
            # Initializing motion = 0(no motion)
            motion = 0
        
            # Converting color image to gray_scale image
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
            # Converting gray scale image to GaussianBlur
            # so that change can be find easily
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
            # In first iteration we assign the value
            # of static_back to our first frame
            if static_back is None:
                static_back = gray
                continue
        
            # Difference between static background
            # and current frame(which is GaussianBlur)
            diff_frame = cv2.absdiff(static_back, gray)
        
            # If change in between static background and
            # current frame is greater than 30 it will show white color(255)
            thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
            thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
        
            # Finding contour of moving object
            cnts,_ = cv2.findContours(thresh_frame.copy(),
                            cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
            for contour in cnts:
                if cv2.contourArea(contour) < 10000:
                    continue
                motion = 1
        
                (x, y, w, h) = cv2.boundingRect(contour)
                # making green rectangle around the moving object
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        
            # Appending status of motion
            motion_list.append(motion)
        
            motion_list = motion_list[-2:]
        
            # Identify start time of motion
            if motion_list[-1] == 1 and motion_list[-2] == 0:
                logging.info("Motion detected")
                last_motion = datetime.now()
                if in_motion_timeout:
                    in_motion_timeout = False
                    queue.put(PFMessage(PFMessageContent.MOTION))
        
            # Identify end time of motion
            if motion_list[-1] == 0 and motion_list[-2] == 1:
                logging.info("Motion stopped")
                last_motion = datetime.now()
        
            minutes_diff = (datetime.now() - last_motion).total_seconds()/60.0
            if minutes_diff > PFSettings.motion_sensor_timeout:
                if not in_motion_timeout:
                    in_motion_timeout = True
                    queue.put(PFMessage(PFMessageContent.MOTION_TIMEOUT))
            

            # Display image in gray_scale
            # cv2.imshow("Gray Frame", gray)
        
            # Display the difference in currentframe to
            # the staticframe(very first_frame)
            # cv2.imshow("Difference Frame", diff_frame)
        
            # Display the black and white image in which if
            # intensity difference greater than 30 it will appear white
            # cv2.imshow("Threshold Frame", thresh_frame)
        
            # Display color frame with contour of motion of object
            # cv2.imshow("Color Frame", frame)
        
