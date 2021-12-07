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
picframe_filesystem.py pulls new images from an ordinarily mounted Windows
or linux filesystem.
"""
import os

from pathlib import Path
from picframe_settings import PFSettings
from picframe_env import PFEnv
from picframe_env import NoImagesFoundException
from picframe_message import PFMessage

class PFFilesystem:
    """
    If the user's photos are on the local filesystem, this class gets
    them.
    """
    initialized = False

    ############################################################
    #
    # init
    #
    @staticmethod
    def init():
        """
        Initialize static class variables.
        """

        PFFilesystem.initialized = True

    ############################################################
    #
    # get_image_dirs
    #
    @staticmethod
    def get_image_dirs():
        """
        Get the OS appropriate image directory path.
        """
        result_dirs = []
        for idir in PFSettings.image_paths:
            result_dirs.append(PFEnv.path_to_platform(idir))

        return result_dirs

    ############################################################
    #
    # get_next_file
    #
    @staticmethod
    def get_next_file():
        """
        Get next supported image file from the list of filesystem
        directories given for pictures to display.

        Use a generator so it is compatible with the way the google drive
        version works, yielding a single file at a time.

        Inputs: None

        Returns: List of fully qualified paths in the right
                format for the operating system and image source.
        """

        # Traverse the recursive list of directories.
        PFEnv.logger.debug("Entering get_next_file()")
        while True:
            image_file_count = 0
            for dirname in PFFilesystem.get_image_dirs():
                if Path(dirname).is_file():
                    if PFEnv.is_format_supported(dirname):
                        image_file_count = image_file_count + 1
                        PFEnv.logger.debug("Exiting get_next_file: %s" % (dirname,))
                        yield dirname
                else:
                    for root, dirs, files in os.walk(dirname):
                        path = root.split(os.sep)
                        for file in files:
                            pathdir = '/'.join(path) + '/' + file
                            if PFEnv.is_format_supported(pathdir):
                                image_file_count = image_file_count + 1
                                PFEnv.logger.debug("Exiting get_next_file: %s" % (pathdir,))
                                yield pathdir
            if image_file_count == 0:
                PFEnv.logger.error(f"No images found in {PFFilesystem.get_image_dirs()}, quitting")

                raise NoImagesFoundException()


    ############################################################
    #
    # get_file_list
    #
    @staticmethod
    def get_file_list():
        """
        Get the list of supported image files from the list of filesystem
        directories given for pictures to display.

        Inputs: None

        Returns: List of fully qualified paths in the right
                format for the operating system and image source.
        """
        image_file_list = []

        # Traverse the recursive list of directories.
        for dirname in PFFilesystem.get_image_dirs():
            if Path(dirname).is_file():
                if PFEnv.is_format_supported(dirname):
                    image_file_list.append(dirname)
            else:
                for root, dirs, files in os.walk(dirname):
                    path = root.split(os.sep)
                    for file in files:
                        pathdir = '/'.join(path) + '/' + file
                        if PFEnv.is_format_supported(pathdir):
                            image_file_list.append(pathdir)

        return image_file_list
