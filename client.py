import socket
import _thread
import json
import sys
import time

PORT = 5000
SERVER_IP = "10.0.1.10"
NICKNAME = None
ROOM_ID = None
MSG_ID = 1


# Object to store the confirmation of the server
class Flag:
    flags = None

    def __init__(self):
        self.flags = {
            "1": False,  # To enter a room
            "2": False,  # To leave a room
            "3": False  # To send a message
        }


# Create a flag object
flag = Flag()


def listener(udp):
    global flag
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
            if string_dict["name"] == NICKNAME:
                # Case your actual room be the response of server
                if string_dict["room_id"] == ROOM_ID:
                    # If you are accept to room, change the confirmation variable
                    if string_dict["status"] == 1:
                        flag.flags["1"] = True
        # If you want to leave the room
        elif string_dict["action"] == 2:
            if string_dict["name"] == NICKNAME:
                if string_dict["room_id"] == ROOM_ID:
                    if string_dict["status"] == 1:
                        # If you are withdraw to room, change the confirmation variable
                        flag.flags["2"] = True
        # If you want to send a message
        elif string_dict["action"] == 3:
            # Cause for the confirmation response about your message sent
            if string_dict["room_id"] == ROOM_ID:
                if string_dict["name"] == NICKNAME:
                    flag.flags["3"] = True
            # Cause for the message sent by other user
            if string_dict["room_id"] == ROOM_ID:
                if string_dict["name"] != NICKNAME:
                    # Print the message received
                    print(f"\n{string_dict['name']} -> {string_dict['msg']}\n[APP] Message -> ", end="")


def request_to_entry_room(udp, dest):
    global NICKNAME
    global ROOM_ID

    NICKNAME = input("[APP] Nickname -> ")
    try:
        ROOM_ID = int(input("[APP] Room -> "))
        # Send a message to enter a room
        came_in_room_msg = {
            'action': 1,
            'room_id': ROOM_ID,
            'name': NICKNAME
        }
        # Convert the message to a JSON string
        string_json = json.dumps(came_in_room_msg)
        # Send the encoded message to the server
        udp.sendto(string_json.encode('utf-8'), dest)
        # Waiting the server to accept you in the room
        waiting_server_acceptance(1)
    except TypeError or InterruptedError:
        print("[APP] -> Error sending message!")
        sys.exit(0)


def waiting_server_acceptance(action):
    global flag
    count = 0

    print("[APP] -> Waiting the server to accept your request", end="")
    while True:
        if not flag.flags[str(action)]:
            count += 1
        # If the server accepted you in the room, you can send messages
        else:
            break
        # If the server doesn't accept you in the room in 10 seconds, exit
        if count == 10 and action != 3:
            print()
            print("[APP] -> The server didn't accept your request")
            sys.exit(0)
        print(".", end="")
        # If the server doesn't accept you in the room in 10 seconds and you are sending messages
        if count == 10 and action == 3:
            print("[APP] -> Your message was not sent")
        time.sleep(1)
    print()


def send_messages(udp, dest):
    global MSG_ID
    message = None

    print("[APP] -> Type q to exit")
    while message != "q":
        message = input("[APP] Message -> ")
        if message == "q":
            request_to_leave_room(udp, dest)
        else:
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
            # Waiting the server to confirm the message
            waiting_server_acceptance(3)
            print("[APP] -> Your message was sent")
            # Increment the message id
            MSG_ID += 1


def request_to_leave_room(udp, dest):
    # Create a leave room message
    leave_room_msg = {
        'action': 2,
        'name': NICKNAME,
        'room_id': ROOM_ID
    }
    # Convert the message to a JSON string
    string_json = json.dumps(leave_room_msg)
    # Send the encoded message request to the server
    udp.sendto(string_json.encode('utf-8'), dest)
    # Waiting the server to withdraw you in the room
    waiting_server_acceptance(2)
    print("[APP] -> You left the room!")


def client():
    print(f"[APP] -> Starting UDP Client on port {PORT}")
    # Create a UDP socket
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Start a thread to listen for incoming messages
    _thread.start_new_thread(listener, (udp,))
    dest = (SERVER_IP, PORT)

    request_to_entry_room(udp, dest)

    send_messages(udp, dest)

    # Close the socket
    udp.close()


if __name__ == "__main__":
    client()
