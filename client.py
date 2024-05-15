from udp import *
import pygame
import pickle
from player import Player
from ball import Ball
from graphics import *
import threading, time

LEFT = 1
SCROLL = 2
RIGHT = 3

ip = '192.168.1.151'
server_port = 1234

die = False
connection_lost = False
exit = False
goal = False

class Client:

    def __init__(self) -> None:
        self.sock = None
        self.side = None
        self.game_port = None
        self.score = [0, 0]
        self.timer = GAME_DURATION
        self.online = None  # online (True) or offline (False) (free play)

        self.player: Player = None
        self.opponent: Player = None
        self.ball: Ball = None

        self.last_keep_alive = time.time()

        self.timeout_cnt = 0

        # graphics
        pygame.init()
        self.size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Headball by OPHIR")
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        self.score_font = pygame.font.Font('images/fonts/open24dismay.ttf', 65)
        self.timer_font = pygame.font.Font('images/fonts/open24dismay.ttf', 45)
        self.result_font = pygame.font.Font('images/fonts/riffic-bold.ttf', 200)
        self.background_image = pygame.image.load(BACKGROUND)
        self.background_image = IMGS['background']
        self.clock = pygame.time.Clock()


    def start(self):

        global die

        while not exit:

            die = False
            self.timer = GAME_DURATION
            self.score = [0, 0]   # to fix - make a function to reset variables

            self.online = self.show_choose_page()
            if self.online is None:  # exit on choose page
                die = True
                return
            if self.online:
                connected = self.initialize_connection()

                if connected == 'close':
                    return 'close'
                
                if connected:
                    t = threading.Thread(target=self.network_handler)
                    t.start()
                
                else:
                    continue
                
            self.initialize_gui()
            self.mainloop()
            die = True
            if self.online:
                t.join()
    
    def show_open_page(self):
        self.screen.blit(IMGS['open'], (0, 0))
        pygame.display.flip()
        time.sleep(1)

    def show_choose_page(self):
        self.screen.blit(IMGS['choose'], (0, 0))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    if pygame.mouse.get_pos()[1] < GAME_CHOOSE_LINE:
                        return True  # online
                    else:
                        return False  # offline
            pygame.display.flip()

    def notify_exit(self):
        send_msg(self.sock, f"EXIT~{self.side}".encode(), (ip, self.game_port))
    
    def notify_lobby_exit(self):
        send_msg(self.sock, b'CNCL', (ip, server_port))

    def connect(self):

        cnt = 0

        while True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'close', False

            data, addr = recv_msg(self.sock)
            if not data:
                cnt += 1
                if cnt > GAMESTART_TIMEOUT:
                    return False, False
            elif data.split(b'~')[0] == b'STRT':
                return data, addr
            
    def ask_for_game(self):
        
        cnt = 0
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

            send_msg(self.sock, b'GAME', (ip, server_port))
            response, addr = recv_msg(self.sock)
            if not response:
                cnt += 1
                if cnt >= CONNECTION_TRIES:
                    return False
            elif response == b'WAIT':
                return True

    def initialize_connection(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(0.1)

        succeed = self.ask_for_game()
        if succeed:
            data, addr = self.connect()
        else:
            self.notify_lobby_exit()
            return False

        if data == 'close':
            self.notify_lobby_exit()
            return 'close'

        if not data:
            self.notify_lobby_exit()
            return False
        
        else:
            self.side = data.decode().split('~')[1]
            self.game_port = addr[1]
            return True
    
    def send_player_state(self):
        data = pickle.dumps(self.player)
        msg = b"MOVE~" + self.player.side.encode() + b"~" + data
        send_msg(self.sock, msg, (ip, self.game_port))

    def update_ball(self, new: Ball):
        self.ball = new
    
    def update_opponent(self, new: Player):
        self.opponent = new

    def update_score(self, r_score, l_score):
        self.score[0] = int(r_score)
        self.score[1] = int(l_score)

    def handle_message(self, msg):
        try:
            fields = msg.split(b'~')
            code: bytes = fields[0]

            if code == b'MOVE':
                self.update_opponent(pickle.loads(fields[2]))

            elif code == b'BALL':
                self.update_ball(pickle.loads(fields[1]))
            
            elif code == b'GOAL':
                r_score, l_score = msg[5:].decode().split('~')
                self.update_score(r_score, l_score)
                return 'goal'
            
            elif code == b'TIME':
                self.update_timer(int(fields[1]))

            elif code == b'PLAY':
                return True
            
            elif code == b'OVER':
                return 'finish'
            
            elif code == b'ERRR':
                print("recieved error msg")
                return 'error'

            else:
                return False

        except:
            pass

    def check_connection(self):
        return self.timeout_cnt >= 20

    def keep_alive(self):
        
        if time.time() - self.last_keep_alive  >= 5:
            send_msg(self.sock, f'KEEP~{self.side}'.encode(), (ip, self.game_port))
            self.last_keep_alive = time.time()

    def network_handler(self):

        global die, connection_lost, goal

        while not die:
            msg, addr = recv_msg(self.sock)
            if not msg:  # if didn't recieve msg in time (or empty msg)
                self.timeout_cnt += 1
                if self.check_connection():
                    connection_lost = True
                    return
                continue
            elif self.timeout_cnt:
                self.timeout_cnt = 0
            _state = self.handle_message(msg)
            if _state == 'goal':
                goal = True
                if not self.wait_for_game():
                    connection_lost = True
                goal = False
            elif _state == 'error':
                connection_lost = True
            elif _state == 'finish':
                die = True

            self.keep_alive()

    
    def wait_for_game(self):
        cnt = 0
        while True:
            if recv_msg(self.sock)[0] == b'PLAY':
                return True
            cnt += 1
            if cnt > GAMESTART_TIMEOUT:
                return False
            
    def reset_player_pos(self):
        self.player.x_pos = R_START_X if self.player.side == 'R' else L_START_X
    
    def reset_opponent_pos(self):
        self.opponent.x_pos = R_START_X if self.opponent.side == 'R' else L_START_X

    def reset_ball_pos(self):
        self.ball.x_pos = BALL_START_X
        self.ball.y_pos = BALL_AXIS
        self.ball.angle = 0

    def setup_background(self):
        # Load background
        self.screen.blit(self.background_image, (0,0))

    def setup_gate(self):
        # load front of gate
        self.screen.blit(IMGS['L gate'], LEFT_GATE_POS)
        self.screen.blit(IMGS['R gate'], RIGHT_GATE_POS)

    def initialize_gui(self):
        
        # Load player
        self.player = Player('L' if not self.side else self.side, R_START_X if self.side == 'R' else L_START_X, Y_AXIS)

        # Load Opponent
        if self.online:
            self.opponent = Player('R' if self.side == 'L' else 'L', R_START_X+L_START_X-self.player.get_pos()[0], Y_AXIS)

        # Load ball
        self.ball = Ball(BALL_START_X, BALL_AXIS)

    def update_timer(self, time):
        self.timer = time
    
    def time_up(self):
        return self.timer <= 0

    def show_timer(self):
        t = self.timer_font.render(str(self.timer).zfill(2), False, (255, 255, 255))
        self.screen.blit(t, (TIMER_X_POS, TIMER_Y_POS))

    def show_score(self):
        left_score = self.score_font.render(str(self.score[0]), False, (181, 208, 53))
        self.screen.blit(left_score, (540, 35))
        right_score = self.score_font.render(str(self.score[1]), False, (181, 208, 53))
        self.screen.blit(right_score, (710, 35))
    
    def show_count_down(self, num):
        self.screen.blit(IMGS[f'counter{num}'], (COUNT_X_POS, COUNT_Y_POS))

    def count_down(self):

        count = 3

        self.setup_graphics()
        self.show_count_down(count)
        pygame.display.flip()

        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.USEREVENT:
                    count -= 1
                    if count == 0:
                        return True
                    
                    self.setup_graphics()
                    self.show_count_down(count)
                    pygame.display.flip()
                    break
                    

    def setup_graphics(self):
        self.setup_background()
        self.show_timer()
        self.screen.blit(IMGS[self.player.image], self.player.get_pos())
        if self.online:
            self.screen.blit(IMGS[self.opponent.image], self.opponent.get_pos())
        else:
            self.ball.update_angle()
        self.screen.blit(self.ball.spin(), self.ball.get_pos())
        self.show_score()
        self.setup_gate()


    def show_connection_lost(self):
        
        self.screen.blit(IMGS['wifi'], (181, 53))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
        
    def end_title(self):

        res = ''

        if self.player.side == 'L':
            if self.score[0] > self.score[1]:
                res = WIN_TITLE
            elif self.score[0] < self.score[1]:
                res = LOSE_TITLE
            else:
                res = TIE_TITLE
        
        else:
            if self.score[1] > self.score[0]:
                res = WIN_TITLE
            elif self.score[1] < self.score[0]:
                res = LOSE_TITLE
            else:
                res = TIE_TITLE
        
        return res
        

    def show_gameover_page(self):

        # load background
        self.screen.blit(IMGS['result'], (0, 0))

        # load title
        title = self.end_title()
        ending_title = self.result_font.render(title, False, (255, 255, 255))  # to fix - add colors as constants
        self.screen.blit(ending_title, (TIE_TITLE_X if title == TIE_TITLE else WINLOSE_TITLE_X, END_TITLE_Y))

        # load score
        left_score = self.result_font.render(str(self.score[0]), False, (255, 255, 255))
        right_score = self.result_font.render(str(self.score[1]), False, (255, 255, 255))
        dash = self.result_font.render('-', False, (255, 255, 255))
        self.screen.blit(left_score, (END_SCORE1_X, END_SCORE_Y))
        self.screen.blit(dash, (END_RESULT_DASH_X, END_SCORE_Y))
        self.screen.blit(right_score, (END_SCORE2_X, END_SCORE_Y))
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return True
    
    def game_over(self):
        return self.timer <= 0

    def end_game(self):

        self.pause_music()

        if self.online:
            self.notify_exit()  # to fix - add confirm in server side
            return self.show_gameover_page()


    def ball_infront_player(self, player_x_pos, player_side):
        if player_side == 'R':
            return self.ball.x_pos < player_x_pos
        else:
            return self.ball.x_pos > player_x_pos
    
    def ball_behind_player(self, player_x_pos, player_side):
        if player_side == 'R':
            return self.ball.x_pos > player_x_pos
        else:
            return self.ball.x_pos < player_x_pos
    
    def is_player_move_ball(self, player_x_pos, player_side):
        if self.player.state == 'still':
            return True
        return (self.player.state == 'forward' and self.ball_infront_player(player_x_pos, player_side)) or (self.player.state == 'backward' and self.ball_behind_player(player_x_pos, player_side))
    
    def ball_below_player(self, player_side, player_x_pos, player_y_pos):

        pHeight = player_y_pos + IMGS[self.player.image].get_height()
        return pHeight >= self.ball.y_pos and pHeight <= self.ball.y_pos + 37

    def ball_above_player(self, player_y_pos):
        return self.ball.y_pos < player_y_pos
    
    def adjust_player(self):
        if self.player.get_vx() > 0:
            self.player.x_pos -= self.player.x_pos + IMGS[self.player.image].get_width() - self.ball.x_pos - 1
        elif self.player.get_vx() < 0:
            self.player.x_pos += self.ball.x_pos + self.ball.spin().get_width() - self.player.x_pos - 1
    
    def handle_ball_collision(self):
        if self.online:
            if self.ball_below_player(self.player.side, self.player.x_pos, self.player.y_pos) and not self.player.is_kick:
                self.player.y_pos -= (self.player.y_pos + IMGS[self.player.image].get_height()) - self.ball.y_pos
                self.player.set_jump_vy(-500)
                self.player.is_jumping = True

            if self.is_player_move_ball(self.player.x_pos, self.player.side) and self.player.get_vy() == 0 and not self.player.is_kick:
                self.adjust_player()
            
        else:
            if self.ball_below_player(self.player.side, self.player.x_pos, self.player.y_pos) and not self.player.is_kick:
                self.player.y_pos -= (self.player.y_pos + IMGS[self.player.image].get_height()) - self.ball.y_pos
                self.player.set_jump_vy(-500)
                self.player.is_jumping = True
                self.ball.set_vy(-500)

            elif self.ball_above_player(self.player.y_pos):
                self.ball.y_pos -= (self.ball.y_pos + IMGS['ball'].get_height()) - self.player.y_pos
                self.ball.set_vy(self.ball.get_vy() * -0.5)
                

            elif self.is_player_move_ball(self.player.x_pos, self.player.side):
                self.ball.update_velocity_impulse(self.player.get_vx(), self.player.get_vy())

            if self.player.is_kick and self.ball_infront_player(self.player.x_pos, self.player.side):
                if self.player.kick_type == 'side':
                    self.ball.kick_forward(self.player.side)
                else:
                    self.ball.kick_up(self.player.side)

    def start_music(self):
        pygame.mixer.music.load(SONG_FILE)
        pygame.mixer.music.play()

    def pause_music(self):
        pygame.mixer.music.pause()

    def mainloop(self):

        self.start_music()
        finish = not self.count_down()

        global die, connection_lost, exit, goal

        while not finish and not die:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finish = True
                    exit = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.notify_exit()
                    die = True
                    finish = True
                    self.pause_music()
                    return
            
            if self.game_over():
                finish = True

            keys = pygame.key.get_pressed()

            # Left-right movment
            if keys[pygame.K_d]:
                self.player.move_right()
            elif keys[pygame.K_a]:
                self.player.move_left()

            # jump
            if keys[pygame.K_w] and not self.player.is_jumping:
                self.player.set_jump_vy()
            if self.player.is_jumping:
                self.player.jump(Y_AXIS)

            # slow down & stop
            if not keys[pygame.K_d] and not keys[pygame.K_a]:
                self.player.stop()
            
            # player kick
            if self.player.is_kick:
                self.player.kick(self.player.kick_type)
            elif keys[pygame.K_LEFT]:
                self.player.kick('side')
            elif keys[pygame.K_UP]:
                self.player.kick('up')
            if self.player.kick_timer:
                self.player.update_kick_timer()

            if self.online:
                self.send_player_state()

            # check collision with ball
            collision = MASKS[self.player.mask].overlap(pygame.mask.from_surface(self.ball.spin()), (self.ball.x_pos - self.player.x_pos, self.ball.y_pos - self.player.y_pos))
            if collision:
                self.handle_ball_collision()

            if not self.online:
                if self.ball.get_vx() or self.ball.get_vy():
                    self.ball.move(BALL_AXIS)
                self.ball.stop()

            # update graphics
            self.setup_graphics()
            pygame.display.flip()
            self.clock.tick(REFRESH_RATE)

            if connection_lost:
                finish = True
                die = True
            
            if goal:
                self.reset_player_pos()
                self.reset_ball_pos()
                self.reset_opponent_pos()
                pygame.display.flip()
                self.count_down()
                while goal:
                    pass

        if connection_lost:
            self.pause_music()
            self.show_connection_lost()
            connection_lost = False
        else:
            self.end_game()

        
def main():

    client = Client()
    client.show_open_page()
    client.start()
    pygame.quit()


if __name__ == "__main__":
    main()
