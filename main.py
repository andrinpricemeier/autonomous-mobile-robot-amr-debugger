from jetson_logger import jetson_log_server
from webserver import webserver
from websocket_handler import DebuggerProtocol, websocket_server
from image_logger import image_log_server
import threading
import asyncio
import configparser

def __read_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read("debugger.conf")
    return config

def main():
    loop = asyncio.get_event_loop()
    config = __read_config()    

    image_log_port = int(config["ImageLogger"]["TcpPort"])
    tcp_images_thread = threading.Thread(target=image_log_server, args=(image_log_port,))
    tcp_images_thread.start()

    jetson_log_port = int(config["JetsonLogger"]["TcpPort"])
    tcp_logs_thread = threading.Thread(target=jetson_log_server, args=(jetson_log_port,))
    tcp_logs_thread.start()

    image_webserver_path = config["Webserver"]["ImagePath"]
    image_webserver_port = int(config["Webserver"]["HttpPort"])

    websocket_port = int(config["Websocket"]["Port"])

    websocket_server(websocket_port)

    loop.run_until_complete(asyncio.gather(
        webserver(image_webserver_port, image_webserver_path)
    ))

if __name__ == '__main__':
    main()
