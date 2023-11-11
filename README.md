# Debugger

## Webpage
### Remote Access
SSH Zugriff gemäss https://code.visualstudio.com/docs/remote/ssh konfigurieren.

Port 8080 (Webserver.HttpPort) und Port 12500 (Websocket.Port) gemäss https://code.visualstudio.com/docs/remote/ssh#_forwarding-a-port-creating-ssh-tunnel forwarden 

Website unter http://localhost:8080/index.html aufrufen.

## Livestream

### Installation

1. Herunterladen: https://github.com/GStreamer/gst-rtsp-server/blob/master/examples/test-launch.c
1. gst_rtsp_media_factory_set_enable_rtcp (factory, !disable_rtcp); löschen (das gibts in der von Jetson Nano verwendeten Version nicht)
1. sudo apt-get install libgstrtspserver-1.0 libgstreamer1.0-dev
1. gcc test-launch.c -o test-launch $(pkg-config --cflags --libs gstreamer-1.0 gstreamer-rtsp-server-1.0)

### RTSP Stream starten

1. launch_server.sh ausführen
1. Im VLC stream öffnen: rtsp://192.168.43.11:8554/test
1. Vielleicht Zwischenspeicherung in VLC heruntersetzen auf z.B. 250ms

Wichtig: Kamera kann nur von einem Prozess gleichzeitig verwendet werden.

Falls Probleme auftreten:

* sudo service nvargus-daemon restart