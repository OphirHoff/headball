import threading
from udp import *
from game import Game
from lobby import Lobby
from graphics import MAX_ACTIVE_GAMES
import global_vars
import keyboard

ip = '0.0.0.0'
port = 1234

lobby = Lobby()
global_vars.init()

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
    
    # global all_to_die, active_games

    print("Server up and running")

    threads = []
    
    while True:

        data, addr = recv_msg(sock)

        if data:
            handle_request(data, addr)

        if lobby.has_pair and global_vars.active_games < MAX_ACTIVE_GAMES:
            pair = lobby.pair()
            game = Game(*pair)

            t = threading.Thread(target=game.start)
            t.start()
            threads.append(t)
        
        if keyboard.is_pressed('esc'):
            break
    
    global_vars.all_to_die = True
    print("Main thread: waiting for all clients to die")
    for t in threads:
        t.join()
    sock.close()
    print("Server Down")


if __name__ == "__main__":
    start()
