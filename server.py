import socket
import _thread
import json

HOST = ""
PORT = 5000
userList = []


def add_user(user, client):
    new_user = {
        "name": user["name"],
        "ip": client[0],
        "port": client[1],
        "group": user["group"]
    }
    userList.append(new_user)


def server(udp):
    print(f"Starting UDP Server on port {PORT}")
    orig = ("", PORT)
    udp.bind(orig)
    while True:
        msg, client = udp.recvfrom(1024)
        msg_decoded = msg.decode('utf-8')
        try:
            string_dict = json.loads(msg_decoded)
            if string_dict["action"] == 0:
                add_user(string_dict, client)
        except Exception:
            pass


def client():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    _thread.start_new_thread(server, (udp,))
    print("Type q to exit")
    message = None
    while message != "q":
        ip_dest = input("destiny -> ")
        dest = (ip_dest, PORT)
        message = input("-> ")
        msg = {
            'destiny': ip_dest,
            'body': message
        }
        string_json = json.dumps(msg)
        udp.sendto(string_json.encode('utf-8'), dest)
    udp.close()


if __name__ == "__main__":
    client()
