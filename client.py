import socket
import _thread
import json
import sys
import time

HOST = ""
PORT = 5000
IP_SERVER = "10.0.1.10"
NICKNAME = None
ROOM_ID = None
MSG_ID = 1
HAS_CAME_IN_ROOM = False


def server(udp):
    orig = ("", PORT)
    udp.bind(orig)
    while True:
        msg, client = udp.recvfrom(1024)
        msg_decoded = msg.decode('utf-8')
        string_dict = json.loads(msg_decoded)
        if string_dict["action"] == 1:
            if string_dict["room_id"] == ROOM_ID:
                if string_dict["status"] == 1:
                    HAS_CAME_IN_ROOM = True
        elif string_dict["action"] == 2:
            pass
        elif string_dict["action"] == 3:
            pass
        print(f"-> #{client}# {string_dict}")


def client():
    print(f"Starting UDP Server on port {PORT}")
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    _thread.start_new_thread(server, (udp,))
    message = None
    dest = (IP_SERVER, PORT)
    name = input("Nickname -> ")
    try:
        ROOM_ID = int(input("Room -> "))
        came_in_room_msg = {
            'action': 1,
            'room_id': ROOM_ID,
            'name': name
        }
        string_json = json.dumps(came_in_room_msg)
        udp.sendto(string_json.encode('utf-8'), dest)
    except Exception:
        sys.exit(0)

    count = 0
    print("Waiting the server to accept you in the room")
    while True:
        if not HAS_CAME_IN_ROOM:
            count += 1
        else:
            break
        if count == 10:
            sys.exit(0)
        time.sleep(1)

    print("Type q to exit")
    while message != "q":
        message = input("Message -> ")
        msg = {
            'action': 3,
            'name': NICKNAME,
            'room_id': ROOM_ID,
            'msg_id': MSG_ID,
            'msg': message
        }
        string_json = json.dumps(msg)
        udp.sendto(string_json.encode('utf-8'), dest)
        MSG_ID += 1
    udp.close()


if __name__ == "__main__":
    client()
