import threading
from udp import *
from game import Game
from lobby import Lobby

ip = '0.0.0.0'
port = 1234

lobby = Lobby()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.1)
sock.bind((ip, port))

def print_lobby():
    print(f"Main Thread: Lobby: {lobby}")


def handle_request(request: bytes, addr):

    try:
        code = request.decode()

        if code == 'GAME':
            lobby.add(addr)
            send_msg(sock, b'WAIT', addr)
            print_lobby()
            
        elif code == 'CNCL':
            lobby.delete(addr)
            print_lobby()

    except:
        pass


def start():
    
    print("Server up and running")

    threads = []

    while True:

        data, addr = recv_msg(sock)

        if data:
            handle_request(data, addr)

        if lobby.has_pair:
            pair = lobby.pair()
            game = Game(*pair)

            t = threading.Thread(target=game.start)
            t.start()
            threads.append(t)

if __name__ == "__main__":
    start()
