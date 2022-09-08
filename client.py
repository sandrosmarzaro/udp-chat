import socket
import _thread
import json
import sys
import time

HOST = ""
PORT = 5000
SERVER_IP = "10.0.1.10"
NICKNAME = None
ROOM_ID = None
MSG_ID = 1
HAS_CAME_IN_ROOM = False


def listener(udp):
    global HAS_CAME_IN_ROOM
    orig = ("", PORT)
    # Bind the socket to the port
    udp.bind(orig)
    while True:
        # Wait for a message
        msg, client = udp.recvfrom(1024)
        # Decode the message
        msg_decoded = msg.decode('utf-8')
        # Convert the message to a dictionary
        string_dict = json.loads(msg_decoded)
        # If is a response message of server of request to entry room
        if string_dict["action"] == 1:
            # Case your actual room be the response of server
            if string_dict["room_id"] == ROOM_ID:
                # If you are accept to room, change the confirmation variable
                if string_dict["status"] == 1:
                    HAS_CAME_IN_ROOM = True
        elif string_dict["action"] == 2:
            pass
        elif string_dict["action"] == 3:
            pass


def client():
    global ROOM_ID
    global MSG_ID
    print(f"Starting UDP Server on port {PORT}")
    # Create a UDP socket
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Start a thread to listen for incoming messages
    _thread.start_new_thread(listener, (udp,))
    message = None
    dest = (SERVER_IP, PORT)
    name = input("Nickname -> ")
    try:
        ROOM_ID = int(input("Room -> "))
        # Send a message to enter a room
        came_in_room_msg = {
            'action': 1,
            'room_id': ROOM_ID,
            'name': name
        }
        # Convert the message to a JSON string
        string_json = json.dumps(came_in_room_msg)
        # Send the encoded message to the server
        udp.sendto(string_json.encode('utf-8'), dest)
    except Exception:
        print("Error sending message!")
        sys.exit(0)

    count = 0
    print("Waiting the server to accept you in the room")
    while True:
        if not HAS_CAME_IN_ROOM:
            count += 1
        # If the server accepted you in the room, you can send messages
        else:
            break
        # If the server doesn't accept you in the room in 10 seconds, exit
        if count == 10:
            print("The server didn't accept you in the room")
            sys.exit(0)
        print(".", end="")
        time.sleep(1)

    print("Type q to exit")
    while message != "q":
        message = input("Message -> ")
        # Send a message to the server
        msg = {
            'action': 3,
            'name': NICKNAME,
            'room_id': ROOM_ID,
            'msg_id': MSG_ID,
            'msg': message
        }
        # Convert the message to a JSON string
        string_json = json.dumps(msg)
        # Send the encoded message to the server
        udp.sendto(string_json.encode('utf-8'), dest)
        # Increment the message id
        MSG_ID += 1
    # Close the socket
    udp.close()


if __name__ == "__main__":
    client()
