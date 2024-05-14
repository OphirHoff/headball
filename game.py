from udp import *
import pygame
import pickle
from ball import Ball 
from player import Player
from graphics import *
import time


class Game:
    def __init__(self, p1, p2) -> None:
        pygame.init()

        self.p1_addr = p1
        self.p2_addr = p2
        self.p1 = Player('R', R_START_X, Y_AXIS)
        self.p2 = Player('L', R_START_X+L_START_X-self.p1.x_pos, Y_AXIS)
        self.sock = None
        self.port = None
        self.ball = Ball(BALL_START_X, BALL_AXIS)
        self.p1_score = 0
        self.p2_score = 0
        self.timer = GAME_DURATION
        pygame.time.set_timer(pygame.USEREVENT, 1000)

        self.p1_last_keep_alive = time.time()
        self.p2_last_keep_alive = time.time()

        self.timeout_cnt1 = 0
        self.timeout_cnt2 = 0

        self.error_during_game = False  # turns on if a player disconnected during game
        
    
    def __notify_start(self):
        # first player on the right, second on the left
        send_msg(self.sock, 'STRT~R'.encode(), self.p1_addr)
        send_msg(self.sock, 'STRT~L'.encode(), self.p2_addr)

    def __initialize_connection(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', 0))
        self.sock.settimeout(0.1)
        self.port = self.sock.getsockname()[1]

    def __forward_msg(self, msg, addr):
        
        try:
            dest = None

            if addr == self.p1_addr:
                dest = self.p2_addr
            elif addr == self.p2_addr:
                dest = self.p1_addr
            else:
                pass

            send_msg(self.sock, msg, dest)
        except:
            pass
    
    def __send_msg_to_all(self, msg):
        """send a msg to both players."""
        send_msg(self.sock, msg, self.p1_addr)
        send_msg(self.sock, msg, self.p2_addr)

    def __send_ball_state(self):
        data = pickle.dumps(self.ball)
        msg = b"BALL~" + data
        self.__send_msg_to_all(msg)

    def update_timer(self):
        self.timer -= 1
    
    def notify_time(self):
        send_msg(self.sock, f"TIME~{str(self.timer)}".encode(), self.p1_addr)
        send_msg(self.sock, f"TIME~{str(self.timer)}".encode(), self.p2_addr)

    def __ball_infront_player(self, player_x_pos, player_side):
        if player_side == 'R':
            return self.ball.x_pos < player_x_pos
        else:
            return self.ball.x_pos > player_x_pos
        
    def __ball_behind_player(self, player_x_pos, player_side):
        if player_side == 'R':
            return self.ball.x_pos > player_x_pos
        else:
            return self.ball.x_pos < player_x_pos
        
    def __ball_below_player(self, player_y_pos, player_image):

        pHeight = player_y_pos + IMGS[player_image].get_height()
        return pHeight >= self.ball.y_pos and pHeight <= self.ball.y_pos + 37
    
    def __ball_above_player(self, player_y_pos):
        return self.ball.y_pos < player_y_pos
    
    def is_player_move_ball(self, player_state, player_x_pos, player_side):
        if player_state == 'still':
            return True
        return (player_state == 'forward' and self.__ball_infront_player(player_x_pos, player_side)) or (player_state == 'backward' and self.__ball_behind_player(player_x_pos, player_side))

    def __is_ball_collided(self, player: Player):
        """return True if ball has "collided" with player."""
        return MASKS[player.mask].overlap(pygame.mask.from_surface(self.ball.spin()), (self.ball.x_pos - player.x_pos, self.ball.y_pos - player.y_pos))

    def __ball_collision(self, player: Player):

        if self.__is_ball_collided(player):

            if self.__ball_below_player(player.y_pos, player.image) and not player.is_kick:
                self.ball.set_vy(-500)
            
            elif self.__ball_above_player(player.y_pos):
                self.ball.y_pos -= (self.ball.y_pos + IMGS['ball'].get_height()) - player.y_pos
                self.ball.set_vy(self.ball.get_vy() * -0.5)
                
            elif self.is_player_move_ball(player.state, player.x_pos, player.side):
                self.ball.update_velocity_impulse(player.get_vx(), player.get_vy())

            if player.is_kick and self.__ball_infront_player(player.x_pos, player.side):
                if player.kick_type == 'side':
                    self.ball.kick_forward(player.side)
                else:
                    self.ball.kick_up(player.side)
    
    def __check_goal(self):
        if self.ball.x_pos <= BALL_LEFT_GOAL_X:
            self.p1_score += 1
            return True
        if self.ball.x_pos + IMGS['ball'].get_width() >= BALL_RIGHT_GOAL_X:
            self.p2_score += 1
            return True
        return False
    
    def reset_ball(self):
        self.ball = Ball(BALL_START_X, BALL_AXIS)

    def update_keep_alive(self, player_side):
        if player_side == b'R':
            self.p1_last_keep_alive = time.time()
        else:
            self.p2_last_keep_alive = time.time()


    def check_connection(self):
        curr_time = time.time()
        return curr_time - self.p1_last_keep_alive < 6 and curr_time - self.p2_last_keep_alive < 6
    
    def notify_goal(self):
        msg = f"GOAL~{self.p2_score}~{self.p1_score}".encode()
        self.__send_msg_to_all(msg)

    def notify_game_cont(self):
        msg = b'PLAY'
        self.__send_msg_to_all(msg)

    def notify_game_over(self):
        send_msg(self.sock, f"OVER~{self.p2_score}~{self.p1_score}", self.p1_addr)
        send_msg(self.sock, f"OVER~{self.p2_score}~{self.p1_score}", self.p2_addr)

    def notify_player_disconnected(self, player_side):

        if player_side == b'L':
            send_msg(self.sock, b'ERRR', self.p1_addr)
        else:
            send_msg(self.sock, b'ERRR', self.p2_addr)

    def transfer_player_state(self, msg):
        
        try:
            fields = msg.split(b'~')
            side = fields[1]
            player_obj = pickle.loads(fields[2])

            # update player info in server & forward msg to other player
            if side == b'R':
                self.p1 = player_obj
                self.__forward_msg(msg, self.p1_addr)  # to fix - might make slower
            else:
                self.p2 = player_obj
                self.__forward_msg(msg, self.p2_addr)
        except:
            pass

    def handle_client_msg(self, msg):

        try:
            fields = msg.split(b'~')
            code = fields[0]

            if code == b'MOVE':
                self.transfer_player_state(msg)
            
            elif code == b'KEEP':
                self.update_keep_alive(fields[1])
            
            elif code == b'EXIT':
                self.notify_player_disconnected(fields[1])
                return 'exit'
        except:
            pass

    def start(self):

        self.__initialize_connection()
        self.__notify_start()
        time.sleep(2)

        print(f'''
            |  GAME STARTED:
            |   player1 = {self.p1_addr}
            |   player2 = {self.p2_addr}
            ''')

        finish = False

        while not finish:

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    self.update_timer()
                    self.notify_time()
                    if self.timer <= 0:
                        finish = True
                        self.notify_game_over()
                        break
                    break
            
            for i in range(2):
                client_msg, _ = recv_msg(self.sock)
                if self.handle_client_msg(client_msg) == 'exit':
                    self.error_during_game = True
                    finish = True
                    continue

            if not self.check_connection():
                self.notify_player_disconnected('R' if self.p1_last_keep_alive >= 6 else 'L')  # to fix
                self.error_during_game = True
                break

            self.__ball_collision(self.p1)
            self.__ball_collision(self.p2)

            # ball movement
            self.ball.update_angle()

            if self.ball.get_vx() or self.ball.get_vy():
                self.ball.move(BALL_AXIS)
            self.ball.stop()

            if self.__check_goal():
                self.notify_goal()
                self.reset_ball()
                time.sleep(2)
                self.notify_game_cont()
            
            self.__send_ball_state()
            self.__send_ball_state()
        
        if not self.error_during_game:

            print(f'''
            |  GAME FINISHED ({self.p2_score}, {self.p1_score}):
            |   player1 = {self.p1_addr}
            |   player2 = {self.p2_addr}
            ''')
        
        else:
            
            print(f'''
            |  GAME STOPPED (Connection Error) ({self.p2_score}, {self.p1_score}):
            |   player1 = {self.p1_addr}
            |   player2 = {self.p2_addr}
            ''')


            