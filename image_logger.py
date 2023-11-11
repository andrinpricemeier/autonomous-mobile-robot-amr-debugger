from typing import Dict
from websocket_handler import DebuggerProtocol
import socket

def image_payload(image_name: str) -> Dict:
    return {"type": "image", "uri" : image_name}

def image_log_server(port: int):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', port))
    serversocket.listen(5)

    print("Start image log server on port {} ...".format(port))


    while True:
        (clientsocket, address) = serversocket.accept()
        try:
            print('WebSocket DebuggerProtocol -  - connection from', address)

            while True:
                data = clientsocket.recv(1024)
                print('WebSocket DebuggerProtocol - received mesage "%s"' % data.decode())
                if not data:
                    break
                DebuggerProtocol.broadcast(image_payload(data.decode()))
        finally:
            # Clean up the connection
            clientsocket.close()
