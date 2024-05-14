from udp import *
import pygame
import pickle
from player import Player
from ball import Ball
from graphics import *
from constants import *

ip = '127.0.0.1'
port = 1234
sock = None
side = None
game_port = None

score = [0, 0]

# initialize connection
def initialize_connection():
    global sock, side, game_port
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock.settimeout(5)  # to fix
    sock.sendto(b'GAME', (ip, port))
    data, addr = sock.recvfrom(1024)
    side = data.decode().split('~')[1]
    game_port = addr[1]

initialize_connection()

background_image = pygame.image.load(BACKGROUND)
background_image = IMGS['background']
clock = pygame.time.Clock()

# Set screen
pygame.init()
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Headball by OPHIR")

def setup_background():
    # Load background
    screen.blit(background_image, (0,0))

def setup_gate():
    # load front of gate
    screen.blit(IMGS['L gate'], LEFT_GATE_POS)
    screen.blit(IMGS['R gate'], RIGHT_GATE_POS)

# Load player
player = Player(side, R_START_X if side == 'R' else L_START_X, Y_AXIS)
screen.blit(IMGS[player.image], player.get_pos())

# Load Opponent
opponent = Player('R' if side == 'L' else 'L', R_START_X+L_START_X-player.get_pos()[0], Y_AXIS)
screen.blit(IMGS[opponent.image], opponent.get_pos())

# Load ball
ball = Ball(BALL_START_X, BALL_AXIS)
screen.blit(ball.image, ball.get_pos())


fontObj = pygame.font.Font('images/fonts/open24dismay.ttf', 65)
left_score = fontObj.render(str(score[0]), False, (181, 208, 53))
screen.blit(left_score, (530, 50))

def update_score():
    left_score = fontObj.render(str(score[0]), False, (181, 208, 53))
    screen.blit(left_score, (540, 35))
    right_score = fontObj.render(str(score[1]), False, (181, 208, 53))
    screen.blit(right_score, (710, 35))


def ball_infront_player(player_x_pos, player_side):
    if player_side == 'R':
        return ball.x_pos < player_x_pos
    else:
        return player_x_pos > ball.get_pos()[0]

setup_gate()
pygame.display.flip()

def handle_message(msg: str):

    code: bytes = msg [:4]
    # data: bytes = msg[5:]

    if code == b'MOVE':
        return pickle.loads(msg[7:])

    if code == b'BALL':
        return pickle.loads(msg[7:])
    
    if code == b'GOAL':
        return msg[5:].decode().split('~')

def send_player_state():
    data = pickle.dumps(player)
    msg = b"MOVE~" + player.side.encode() + b"~" + data
    send_msg(sock, msg, (ip, game_port))

def receive_opponent_state():
    msg, addr = recv_msg(sock)
    data = handle_message(msg)
    return data

def receive_ball_state():
    msg, addr = recv_msg(sock)
    data = handle_message(msg)
    return data  # to fix - ball might not be sent before opponent from server

def recieve_server_data():
    msg, addr = recv_msg(sock)
    data = handle_message(msg)

    if type(data) == Ball:
        return data
    else:
        score[0] = data[0]
        score[1] = data[1]
        update_score()
        return False
    
# def network_handler(sock):

#     while True:

#         msg, addr = recv_msg(sock)

#         data =





def wait_for_game():
    while True:
        if recv_msg(sock)[0] == b'PLAY':
            return


def ball_below_player(player_side, player_x_pos, player_y_pos):

    pHeight = player_y_pos + IMGS[player.image].get_height()
    y = ball.y_pos
    return pHeight >= ball.y_pos and pHeight <= ball.y_pos + 37


def handle_ball_collision():
    if ball_below_player(player.side, player.x_pos, player.y_pos) and not player.is_kick:
        player.y_pos -= (player.y_pos + IMGS[player.image].get_height()) - ball.y_pos
        player.set_jump_vy(-500)
        player.is_jumping = True


def main():

    global ball

    finish = False
    while not finish:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
        
        keys = pygame.key.get_pressed()

        # Left-right movment
        if keys[pygame.K_d]:
            player.move_right()
        elif keys[pygame.K_a]:
            player.move_left()

        # jump
        if keys[pygame.K_w] and not player.is_jumping:
            player.set_jump_vy()
        if player.is_jumping:
            player.jump(Y_AXIS)

        # slow down & stop
        if not keys[pygame.K_d] and not keys[pygame.K_a]:
            player.stop()
        
        # player kick
        if player.is_kick:
            player.kick(player.kick_type)
        elif keys[pygame.K_LEFT]:
            player.kick('side')
        elif keys[pygame.K_UP]:
            player.kick('up')
        if player.kick_timer:
            player.update_kick_timer()


        # Send & Recieve data
        send_player_state()
        opponent: Player = receive_opponent_state()
        server_data = recieve_server_data()
        if server_data:
            ball = server_data
        else:
            player.x_pos = R_START_X if player.side == 'R' else L_START_X
            wait_for_game()
            continue

        # check collision with ball
        collision = MASKS[player.mask].overlap(pygame.mask.from_surface(ball.spin()), (ball.x_pos - player.x_pos, ball.y_pos - player.y_pos))
        if collision:
            handle_ball_collision()
        
        # update graphics
        setup_background()
        screen.blit(IMGS[player.image], player.get_pos())
        screen.blit(IMGS[opponent.image], opponent.get_pos())
        screen.blit(ball.spin(), ball.get_pos())
        update_score()
        setup_gate()
        pygame.display.flip()
        clock.tick(REFRESH_RATE)


    pygame.quit()


if __name__ == "__main__":
    main()
