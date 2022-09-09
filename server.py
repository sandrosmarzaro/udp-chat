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
                pass
            # Case is a request message of client to send a message
            elif string_dict["action"] == 3:
                pass
        except Exception:
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
