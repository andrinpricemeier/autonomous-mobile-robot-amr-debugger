from typing import Dict
from autobahn.asyncio.websocket import WebSocketServerProtocol, WebSocketServerFactory

import json
import asyncio

class DebuggerProtocol(WebSocketServerProtocol):
    connections = []

    def onConnect(self, request):
        print("WebSocket DebuggerProtocol - Client connecting: {0}".format(request.peer))
        DebuggerProtocol.connections.append(self)
        print(DebuggerProtocol.connections)

    def onOpen(self):
        print("WebSocket DebuggerProtocol - connection open.")

    def onMessage(self, payload, isBinary):
        ## echo back message verbatim
        self.sendMessage(payload, isBinary)
        obj = json.loads(payload.decode('utf8'))
        payload = json.dumps(obj, ensure_ascii = False).encode('utf8')
        print(payload)        

    def onClose(self, was_clean, code, reason):
        DebuggerProtocol.connections.remove(self)
        print("WebSocket DebuggerProtocol - connection closed: {0}".format(reason))

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)

    @staticmethod
    def broadcast(data: Dict):
        for web_socket_client in DebuggerProtocol.connections:
            web_socket_client.sendMessage(json.dumps(data).encode(), False) 


def websocket_server(port):
    loop = asyncio.get_event_loop()
    factory = WebSocketServerFactory()

    factory.protocol = DebuggerProtocol
    coro = loop.create_server(factory, '0.0.0.0', port)

    print("Start websocket_server on port {} ...".format(port))
    loop.run_until_complete(coro)