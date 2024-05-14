import threading
from udp import *

from game import Game
from lobby import Lobby

ip = '0.0.0.0'
port = 1234
sock = socket.socket()
sock.bind((ip, port))

lobby = Lobby()

def start():
    
    print("Server up and running")

    threads = []
    server_socket = socket.socket()

    server_socket.bind(('0.0.0.0', 1233))

    server_socket.listen(20)

    while True:

        data, addr = recv_msg(sock)

        if data.split(b'~')[0] == b'GAME':
            lobby.add(addr)
            print(f"Lobby: {lobby}")
            send_msg(sock, b'WAIT', addr)

        if lobby.has_pair:
            pair = lobby.pair()
            game = Game(*pair)

            t = threading.Thread(target=game.start)
            t.start()
            threads.append(t)

if __name__ == "__main__":
    start()
