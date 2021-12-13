# Project Picframe 
# Copyright 2021, Alef Solutions, Inc.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.


What is picframe
----------------
Picframe is a digital picture frame that can 
	- pull pictures from 
    		- any local directory
    		- gdrive
    		- samba
            - USB drive
	- Sleep (go dark) during the night
	- Allows you to dim the screen for a dark room.
	- Turn on and off based on motion detected from a webcam
    - Runs on:
        - Linux
        - Raspberry pi
        - Windows
        - MacOS
	- Runs in fullscreen mode or in a window of any chosen size.
    - Can be controlled from a smartphone via bluetooth.

License
-------
Picframe is licensed under the MIT License.  Please see LICENSE.txt.

Todo
----
Picframe performs all of the above tasks.  However there are a few
additional features that would be nice:
  - Print status and settings on the screen
  - Save settings in a different file; allow the user to save screen-modified
    settings
  - Properly identify the size of the primary screen on linux when there
    is more than one monitor connected
  - Easier installation process
  - Detect ambient light and dim the screen automatically in darker rooms.
  - Support videos (mp4, mov, wmv, mp3, wav).
  - Create a smartphone app to control it over bluetooth or wifi.

Notes
------
- The motion sensor will not work in WSL2 (Windows Linux).
- The motion sensor uses a webcam, so doesn't sense motion in the dark

Getting picframe
----------------
    git clone https://github.com/andrewmeltzer/picframe.git

Install
----------------
    cd picframe
    Create a virtual environment:
        python3 -m venv env
    . env/bin/activate

    sudo apt-get install python3-tk
    pip3 install pillow
    pip3 install pydrive2
    pip3 install pyheif  (linux only, this isn't supported on Windows)
    pip3 install opencv-python

Note on installing opencv-python on raspberry pi
------------------------------------------------
It can be very challenging.  What worked for me:
    pip3 install --no-use-pep517 opencv-python

Note that on the raspberry pi, the opencv library seems to fail occasionally with the error message:
    Corrupt JPEG data: premature end of data segment
This can generally be ignored; the motion sensor is written to handle occasional bad frame reads.

Configure picframe
--------------------
    Edit src/picframe_settings.py.  There are comments in the file.


Simple command:
--------------
    cd picframe/src
    python3 picframe.py

To Install pyheif on a raspberry pi
------------------------------------
    sudo apt-get remove libde265-0 -y 
    sudo apt-get remove libheif1 -y 
    sudo apt-get remove libheif-dev -y 
    sudo apt-get remove libde265-dev -y 
    sudo apt install autotools-dev automake libtool texinfo x265 -y 
    git clone https://github.com/strukturag/libde265.git 
    cd libde265 
    ./autogen.sh 
    ./configure --disable-dec265 --disable-sherlock265 --prefix /usr 
    make 
    sudo make install 
    cd .. 
    git clone https://github.com/strukturag/libheif.git 
    cd libheif 
    ./autogen.sh 
    ./configure --prefix /usr 
    make 
    sudo make install 
    cd .. 
    git clone https://github.com/libffi/libffi.git 
    cd libffi 
    ./autogen.sh 
    ./configure --prefix /usr 
    make 
    sudo make install 
    cd .. 
    pip install git+https://github.com/carsales/pyheif.git 
    pip install pyheif
    
WSL2 Setup
----------
    To use this in WSL2 you'll need to install an xwindow manager like vcXsrv.
        - When you run XLaunch, remember to "disable access control"
        - export DISPLAY=$(grep -m 1 nameserver /etc/resolv.conf | awk '{print $2}'):0
    
    
Google Drive setup:
------------------
    -You may need to create a Google Cloud Platform project to get CLI 
        credentials to create a client_secrets.json file.
        - Download the client_secrets.json file 
    - Either download a client_secrets.json or edit the client_secrets.sample.json
    - Once you have a client_secrets.json file, 
        run picframe_initgdrive.py to set up access to your data.

To mount a remote linux filesystem
----------------------------------
    sudo mkdir /mnt/<your-favorite-mount-point-name>
    sudo sshfs -o allow_other <username>@<ip-address>:<remote-dir> /mnt/<your-favorite-mount-point-name>
    add the following line to the bottom of /etc/fstab
    sshfs#<username>@<ip-address>:<remote-dir> /mnt/<your-favorite-mount-point-name> fuse.sshfs defaults 0 0
    example:
        sudo sshfs -o allow_other myname@pibackup:/sharedata/backup/myname/Pictures/ /mnt/pibackup
    
To unmount a remote linux filesystem:
------------------------------------
    umount /mnt/<your-favorite-mount-point>


To control picframe from your smartphone
----------------------------------------
The is actually a bit of a hack, and a nice project someone could do is to create a nicer bluetooth app for it.

Picframe response to keyboard commands to do almost everything.  All you need to do is download a bluetooth keyboard (I use something called "Bluetooth Keyboard & Mouse").

Once you have the keyboard connected to your device, just use the keyboard commands.


