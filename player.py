from physics import *
import pygame
from graphics import *

def velocity_change(func):
        
        def inner1(self):

            func(self)
            self.update_image()
        return inner1


class Player(pygame.sprite.Sprite):

    def __init__(self, side, x, y):
        super(Player, self).__init__()
        self.side = side
        self.state = 'still'  # 'still', 'forward' or 'backward'
        self.image = f"{self.side} {self.state}"
        self.mask = f"{self.side} {self.state}"
        self.x_pos = x
        self.y_pos = y
        self.__vx = 0
        self.__vy = 0
        self.is_jumping = False
        self.is_kick = 0
        self.move_kick = False
        self.kick_type = None
        self.kick_timer = 0  # after kick counts down before player can kick again
        self.kick_done = False

    def __getstate__(self):
        """Return state values to be pickled."""
        return (self.image, self.mask, self.side, self.state, self.move_kick, self.x_pos, self.y_pos, self.__vx, self.__vy, self.is_kick, self.kick_type)

    def __setstate__(self, state):
        """Restore state from the unpickled state values."""
        self.image, self.mask, self.side, self.state, self.move_kick, self.x_pos, self.y_pos, self.__vx, self.__vy, self.is_kick, self.kick_type = state

    def update_image(self):

        if self.is_kick:
            return

        if self.side == 'R':
            if self.__vx > 0 and self.state != 'backward':
                self.state = 'backward'
                self.image = f"{self.side} {self.state}"
                self.mask = f"{self.side} {self.state}"
                if not self.kick_done:
                    self.y_pos += 10
            elif self.__vx < 0 and self.state != 'forward':
                self.state = 'forward'
                self.image = f"{self.side} {self.state}"
                self.mask = f"{self.side} {self.state}"
                if not self.kick_done:
                    self.y_pos += 10
            elif self.__vx == 0 and self.state != 'still' and not self.is_kick:
                self.state = 'still'
                self.image = f"{self.side} {self.state}"
                self.mask = f"{self.side} {self.state}"
                if not self.move_kick:
                    self.y_pos -= 10
        else:
            if self.__vx > 0 and self.state != 'forward':
                self.state = 'forward'
                self.image = f"{self.side} {self.state}"
                self.mask = f"{self.side} {self.state}"
                if not self.kick_done:
                    self.y_pos += 10
            elif self.__vx < 0 and self.state != 'backward':
                self.state = 'backward'
                self.image = f"{self.side} {self.state}"
                self.mask = f"{self.side} {self.state}"
                if not self.kick_done:
                    self.y_pos += 10
            elif self.__vx == 0 and self.state != 'still':
                self.state = 'still'
                self.image = f"{self.side} {self.state}"
                self.mask = f"{self.side} {self.state}"
                if not self.move_kick:
                    self.y_pos -= 10

    def get_pos(self):
        return self.x_pos, self.y_pos
    
    def in_gate(self):
        d= self.x_pos + IMGS[f"{self.side} {self.state}"].get_width() >= BALL_RIGHT_GOAL_X or self.x_pos <= BALL_LEFT_GOAL_X
        return d
    
    def get_vx(self):
        return self.__vx
    
    def get_vy(self):
        return self.__vy

    @velocity_change
    def increase_v(self):
        self.__vx = accelerate_x(self.__vx)

    @velocity_change
    def decrease_v(self):
        self.__vx = decelerate_x(self.__vx)

    def set_vy(self, vy):
        self.__vy = vy

    def update_loc(self):
        self.x_pos = calc_loc_x(self.x_pos, self.__vx)

    def move_right(self):
        if self.__vx < SPEED_LIMIT:
            self.increase_v()
        if self.x_pos < PLAYER_RIGHT_LIMIT:
            self.update_loc()

    def move_left(self):
        if self.__vx > -SPEED_LIMIT:
            self.decrease_v()
        if self.x_pos > PLAYER_LEFT_LIMIT:
            self.update_loc()

    def stop(self):
        if abs(self.__vx) > 1:
            if self.__vx > 0:
                self.decrease_v()
            elif self.__vx < 0:
                self.increase_v()
            if self.x_pos < PLAYER_RIGHT_LIMIT and self.x_pos > PLAYER_LEFT_LIMIT:
                self.update_loc()
    
    def set_jump_vy(self, v=JUMP_VELOCITY):
        self.__vy = v
        self.is_jumping = True
    
    def jump(self, y_axis):
        self.__vy = accelerate_y(self.__vy)
        new_y_pos = calc_loc_y(self.y_pos, self.__vy)
        if new_y_pos <= y_axis:
            self.y_pos = new_y_pos
        else:
            self.__vy = 0
            self.is_jumping = False
            if self.state == 'still':
                self.y_pos = y_axis
            else:
                self.y_pos = y_axis + 10

    def kick(self, kick_type):
        if self.kick_timer:
            return
        if not self.is_kick:
            self.kick_type = kick_type
            self.image = f"{self.side} kick"
            self.is_kick = KICK_DURATION  # kick lasts 10 frames -> 1/6 sec.
            if self.state == 'still':
                self.y_pos += 10
            else:
                self.move_kick = True
                # self.y_pos -= 10
        else:
            self.is_kick -= 1
            if self.is_kick == 0:
                self.stop_kick()
        
    def stop_kick(self):
        self.kick_timer = KICK_PAUSE
        self.state = ''
        self.kick_done = True
        self.update_image()
        self.kick_done = False
        self.move_kick = False


    def update_kick_timer(self):
        if self.kick_timer > 0:
            self.kick_timer -= 1