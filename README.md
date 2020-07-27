# flask-robocar
 To auto-start Flask program add following code into "/etc/system/system/flask.service" file.

pi@raspberrypi:/etc/systemd/system $ cat flask.service
[Unit]
Description=Flask web server
After=network.target
[Install]
WantedBy=multi-user.target
[Service]
User=pi
WorkingDirectory=/home/pi/robocar/code
ExecStart=/home/pi/robocar/code/app.py
TimeoutSec=600
Restart=always
