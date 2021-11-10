Picframe is a digital frame that will eventually be able to
- pull pictures from 
    - any local directory
    - gdrive
    - samba

- Sleep (go dark) during the night
- Adjust brightness automatically
- Turn on based on motion
- Work on linux (also Raspberri pi) and Windows

Simple command:
    python3 picframe.py --geom=200x200

WSL2
To use this in WSL2 you'll need to install an xwindow manager like vcXsrv.
    - When you run XLaunch, remember to "disable access control"



Google Drive setup:
------------------
-You may need to create a Google Cloud Platform project to get CLI 
    credentials to create a client_secrets.json file.
    - Download the client_secrets.json file 
- Either download a client_secrets.json or edit the client_secrets.sample.json
- Once you have a client_secrets.json file, 
    run firstauth.py to set up access to your data.

