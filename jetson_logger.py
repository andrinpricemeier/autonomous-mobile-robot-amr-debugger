from typing import Dict
from websocket_handler import DebuggerProtocol
import socket
import struct
import logging
import pickle

def un_pickle(data):
    return pickle.loads(data)

def log_payload(record : logging.LogRecord) -> Dict:
    return {"type": "jetson_log", "level": record.levelname, "function" : record.funcName, "message" : record.getMessage(), "asctime": record.asctime}

def jetson_log_server(port: int):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', port))
    serversocket.listen(5)

    print("Start jetson log server on port {} ...".format(port))

    while True:
        (clientsocket, address) = serversocket.accept()
        try:
            print('jetson log server - connection from', address)
            while True:
                chunk = clientsocket.recv(4)
                if len(chunk) < 4:
                    break

                slen = struct.unpack('>L', chunk)[0]
                chunk = clientsocket.recv(slen)
                while len(chunk) < slen:
                    chunk = chunk + clientsocket.recv(slen - len(chunk))

                obj = un_pickle(chunk)
                record = logging.makeLogRecord(obj)

                DebuggerProtocol.broadcast(log_payload(record))

        finally:
            # Clean up the connection
            clientsocket.close()