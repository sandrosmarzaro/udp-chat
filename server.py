import socket
import _thread
import json

HOST = ""
PORT = 5000
userList = []

def adicionar_usuario(usuario, client):
    newUser = {}
    newUser["nome"] = usuario["nome"]
    newUser["ip"] = client[0]
    newUser["porta"] = client[1]
    newUser["grupo"] = usuario["grupo"]
    userList.append(newUser)

def server(udp):
    print(f"Starting UDP Server on port {PORT}")
    orig = ("", PORT)
    udp.bind(orig)
    while True:
        msg, client = udp.recvfrom(1024)
        msg_decoded = msg.decode('utf-8')
        try:
            string_dict = json.loads(msg_decoded)
            if string_dict["acao"] == 0:
                adicionar_usuario(string_dict, client)
        except Exception as ex:
            pass

def client():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    _thread.start_new_thread(server, (udp,))
    print("Type q to exit")
    message = None
    while message != "q":
        ip_dest = input("destino -> ")
        dest = (ip_dest, PORT)
        message = input("-> ")
        msg = {}
        msg['destino'] = ip_dest
        msg['body'] = message
        string_json = json.dumps(msg)
        udp.sendto(string_json.encode('utf-8'), dest)
    udp.close()

if __name__ == "__main__":
    client()