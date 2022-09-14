import socket
import json

PORT = 5000
USER_LIST = []


def add_user(string_dict, client, udp):
    # Add the user to the list
    add_user_list(string_dict, client)
    # Send a response message of accept the user
    response = {
        "action": 1,
        "name": string_dict["name"],
        "room_id": string_dict["room_id"],
        "status": 1
    }
    # Convert the message to a JSON string
    response_json = json.dumps(response)
    # Send the message to the client
    udp.sendto(response_json.encode('utf-8'), client)
    print(f"User {string_dict['name']} with IP {client[0]}, has entered the room {string_dict['room_id']}")


def add_user_list(user, client):
    global USER_LIST
    # Create a new user
    new_user = {
        "name": user["name"],
        "connexion": client,
        "room_id": user["room_id"]
    }
    # Add the user to the list
    USER_LIST.append(new_user)


def withdraw_user(string_dict, client, udp):
    for user in USER_LIST:
        if user["name"] == string_dict["name"] and user["room_id"] == string_dict["room_id"]:
            # Remove the user from the list
            USER_LIST.remove(user)
            # Send a response message of withdraw the user
            response = {
                "action": 2,
                "name": string_dict["name"],
                "room_id": string_dict["room_id"],
                "status": 1
            }
            # Convert the message to a JSON string
            response_json = json.dumps(response)
            # Send the message to the client
            udp.sendto(response_json.encode('utf-8'), client)
            print(f"User {string_dict['name']} with IP {client[0]}, has left the room {string_dict['room_id']}")
            break


def send_message_to_room(string_dict, client, udp):
    send_response_to_sender(string_dict, client, udp)
    # Send the message to all users in the room
    print(f"User {string_dict['name']} with IP {client[0]}, has sent a message to the room {string_dict['room_id']}")
    for user in USER_LIST:
        if user["room_id"] == string_dict["room_id"] and user["name"] != string_dict["name"]:
            # Send the message to the client
            msg_to_send = {
                "action": 3,
                "room_id": string_dict["room_id"],
                "name": string_dict["name"],
                "msg": string_dict["msg"]
            }
            # Convert the message to a JSON string
            msg_json = json.dumps(msg_to_send)
            # Send the message to the client
            udp.sendto(msg_json.encode('utf-8'), user["connexion"])
            print(f"Message sent to {user['name']} with IP {user['connexion'][0]}")


def send_response_to_sender(string_dict, client, udp):
    # Send a response message of accept the user
    response = {
        "action": 3,
        "name": string_dict["name"],
        "room_id": string_dict["room_id"],
        "msg_id": string_dict["msg_id"],
        "status": 1
    }
    # Convert the message to a JSON string
    response_json = json.dumps(response)
    # Send the message to the client
    udp.sendto(response_json.encode('utf-8'), client)


def listener(udp):
    orig = ("", PORT)
    # Bind the socket to the port
    udp.bind(orig)
    while True:
        # Wait for a message
        msg, client = udp.recvfrom(1024)
        # Decode the message
        msg_decoded = msg.decode('utf-8')
        try:
            # Convert the message to a dictionary
            string_dict = json.loads(msg_decoded)
            # If is a request message of client to entry room
            if string_dict["action"] == 1:
                add_user(string_dict, client, udp)
            # If is a request message of client to quit room
            elif string_dict["action"] == 2:
                withdraw_user(string_dict, client, udp)
            # Case is a request message of client to send a message
            elif string_dict["action"] == 3:
                send_message_to_room(string_dict, client, udp)
        except TypeError or InterruptedError:
            print("Message is not a JSON string")
            # If the message is not a JSON string
            udp.close()
            pass


def server():
    print(f"Starting UDP Server on port {PORT}")
    # Create a UDP socket
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Start a thread to listen for incoming messages
    print("Waiting for messages...")
    listener(udp)


if __name__ == "__main__":
    server()
