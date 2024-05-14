import socket
import pygame
import pickle
from player import Player
from ball import Ball
import physics
from graphics import *

# connection
# ip = '127.0.0.1'
# port = 1234
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.sendto(b'GAME', (ip, port))
# data, addr = sock.recvfrom(1024)
# side = data.decode().split('~')[1]
# game_port = addr[1]

WINDOW_WIDTH = 1281
WINDOW_HEIGHT = 810

BACKGROUND = 'images/stadium.png'
GATE = 'images/gate_front.png'
BALL = 'images/ball.png'

background_image = pygame.image.load(BACKGROUND)
L_GATE = pygame.image.load(GATE)
R_GATE = pygame.transform.flip(L_GATE, True, False)

clock = pygame.time.Clock()
REFRESH_RATE = 60
y_axis = 472
ball_axis = 540

R_POS = 900, y_axis
L_POS = 230, y_axis

# Set screen
pygame.init()
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Game")

def setup_background():
    # Load background
    screen.blit(background_image, (0,0))

def setup_gate():
    # load front of gate
    screen.blit(L_GATE, (100, 332))
    screen.blit(R_GATE, (1033, 332))

# setup_background()

side = 'R'
# Load player
# player = Player(side, 970 if side == 'R' else 213, y_axis)
player = Player(side, 970 if side == 'R' else 213, y_axis)
player_image = player.image

# Load Opponent
# opponent = Player('R' if side == 'L' else 'L', 970+213-player.get_pos()[0], y_axis)
# screen.blit(pygame.image.load(opponent.image), opponent.get_pos())

# Load ball
ball = Ball(WINDOW_WIDTH / 2, ball_axis)
ball_image = ball.image
ball_mask = pygame.mask.from_surface(ball_image)



setup_gate()
pygame.display.flip()
    

# def handle_message(msg: str):

#     code = msg [:4]
#     data = msg[5:]

#     if code == b'MOVE':
#         return pickle.loads(data)

# def send_player_state():
#     data = pickle.dumps(player)
#     msg = b"MOVE~" + data
#     sock.sendto(msg, (ip, game_port))

# def receive_opponent_state():
#     msg, addr = sock.recvfrom(1024)
#     print(len(msg))
#     data = handle_message(msg)
#     return data


def ball_infront_player(player_x_pos, player_side):
    if player_side == 'R':
        return ball.x_pos < player_x_pos
    else:
        return ball.x_pos > player_x_pos
    
def ball_behind_player(player_x_pos, player_side):
    if player_side == 'R':
        return ball.x_pos > player_x_pos
    else:
        return ball.x_pos < player_x_pos
    
def is_player_move_ball(player_x_pos, player_side):
    if player.state == 'still':
        return True
    return (player.state == 'forward' and ball_infront_player(player_x_pos, player_side)) or (player.state == 'backward' and ball_behind_player(player_x_pos, player_side))

def ball_below_player(player_side, player_x_pos, player_y_pos):

    pHeight = player_y_pos + IMGS[player.mask].get_height()
    return pHeight >= ball.y_pos and pHeight <= ball.y_pos + 37

def ball_above_player(player_y_pos):
    return ball.y_pos < player_y_pos
    

def main():

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
            player.jump(y_axis)

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

        collision = MASKS[player.image].overlap(pygame.mask.from_surface(ball.spin()), (ball.x_pos - player.x_pos, ball.y_pos - player.y_pos))
        # Check collision
        if collision:# and not player.is_kick:# and not player.in_gate():
            if ball_below_player(player.side, player.x_pos, player.y_pos) and not player.is_kick:
                player.y_pos -= (player.y_pos + IMGS[player.image].get_height()) - ball.y_pos
                player.set_jump_vy(-500)
                player.is_jumping = True
                ball.set_vy(-500)

            elif ball_above_player(player.y_pos):
                ball.y_pos -= (ball.y_pos + IMGS['ball'].get_height()) - player.y_pos
                ball.set_vy(ball.get_vy() * -0.5)
                

            elif is_player_move_ball(player.x_pos, player.side):
                ball.update_velocity_impulse(player.get_vx(), player.get_vy())

            if player.is_kick and ball_infront_player(player.x_pos, player.side):
                if player.kick_type == 'side':
                    ball.kick_forward(player.side)
                else:
                    ball.kick_up(player.side)

        # send_player_state()
        # opponent = receive_opponent_state()

        if ball.get_vx() or ball.get_vy():
            ball.move(ball_axis)
        ball.stop()

        setup_background()

        screen.blit(IMGS[player.image], player.get_pos())
        # screen.blit(pygame.image.load(opponent.image), opponent.get_pos())
        ball.update_angle()
        screen.blit(ball.spin(), ball.get_pos())
        setup_gate()

        pygame.display.flip()
        clock.tick(REFRESH_RATE)

    pygame.quit()


if __name__ == "__main__":
    main()
