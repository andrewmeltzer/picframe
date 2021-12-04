What is picframe
----------------
Picframe is a digital frame that can 
	- pull pictures from 
    		- any local directory
    		- gdrive
    		- samba
            - USB drive
	- Sleep (go dark) during the night
	- Adjust brightness automatically based on the brightness of the room
	- Turn on and off based on motion
    - Turn off if the room is dark
	- Work on linux (also Raspberri pi) and Windows
	- Run fullscreen or in a window of any chosen size

- The motion sensor will not work in WSL2 (Windows Linux).
- The motion sensor is based on light, so it also will disable itself in a dark room.

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
This can generally be ignored.

Configure picframe
--------------------
    Edit src/picframe_settings.py


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
        run firstauth.py to set up access to your data.

To mount a remote linux filesystem
----------------------------------
    sudo mkdir /mnt/<your-favorite-mount-point-name>
    sudo sshfs -o allow_other <username>@<ip-address>:<remote-dir> /mnt/<your-favorite-mount-point-name>
    add the following line to the bottom of /etc/fstab
    sshfs#<username>@<ip-address>:<remote-dir> /mnt/<your-favorite-mount-point-name> fuse.sshfs defaults 0 0
    example:
        sudo sshfs -o allow_other ameltzer@pibackup:/sharedata/backup/ameltzer/Windows/Pictures/ /mnt/pibackup
    
To unmount a remote linux filesystem:
------------------------------------
    umount /mnt/<your-favorite-mount-point>




