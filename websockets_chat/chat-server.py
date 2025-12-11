# SERVER USING RAW SOCKETS #
# import socket

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind(('127.0.0.1', 55555))
# s.listen()

# listening = True
# while listening:
#     client, address = s.accept()
#     print("Connected to {}".format(address))
#     client.send("You are connected".encode())
#     client.close()

# ----------------------- #
# SERVER USING WEBSOCKETS #
# ----------------------- #

# MESSAGE STRUCTURE (JSON):
# {
#     "Sender": "Sender nickname"
#     "Message": "Message"
#     "Type": "server-msg" / "user-msg"
# }

import asyncio
import json
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosedOK


host = "localhost"
port = 55555
clients = []
nicknames = []

# async def send_to_websocket(message, websocket):
#     msg_packed = {"Message": message}
#     await websocket.send(json.dumps(msg_packed))

async def broadcast(message): # Takes JSON as the message parameter
    print("Broadcasting", message)
    for client in clients:
        await client.send(json.dumps(message))


def pack_message(message, sender=None, type="user-msg"):
    msg_packed = {"Sender": sender, "Message": message, "Type": type}
    return msg_packed

async def new_connection(websocket):
    message = await websocket.recv()
    message_data = json.loads(message)
    print("-->", message_data["Nick"], "was connected with IP {}".format(websocket.remote_address[0]))
    nicknames.append(message_data["Nick"])
    clients.append(websocket)
    
    new_connection_msg = pack_message("{} has joined the chat".format(message_data["Nick"]), None, "server-msg")
    await broadcast(new_connection_msg)


async def disconnect(websocket):
    index = clients.index(websocket)
    print("<--", nicknames[index], "was disconnected.", "server-msg")
    del clients[index]
    del nicknames[index]

    
async def handle_message(message, websocket):
    index = clients.index(websocket)
    msg = pack_message(message, nicknames[index])
    await broadcast(msg)


async def handler(websocket):
    await new_connection(websocket)
    async for message in websocket:
        await handle_message(message, websocket)
    await disconnect(websocket)


async def main():
    async with serve(handler, host, port) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())