Picframe is a digital frame that can 
- pull pictures from 
    - any local directory
    - gdrive
    - samba

- Sleep (go dark) during the night
- Adjust brightness automatically
- Turn on and off based on motion
- Work on linux (also Raspberri pi) and Windows
- Run fullscreen or in a window of any chosen size

Simple command:
    python3 picframe.py

Install
-------
    sudo apt-get install python3-tk
    pip3 install pillow
    pip3 install pydrive2


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

