from physics import *
import pygame
from graphics import IMGS


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Ball, self).__init__()
        self.image = IMGS['ball']
        self.x_pos = x
        self.y_pos = y
        self.r = 20.5
        self.angle = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.__vx = 0
        self.__vy = 0
        self.is_jumping = False

    def __getstate__(self):
        return (self.x_pos, self.y_pos, self.angle)

    def __setstate__(self, state):
        self.x_pos, self.y_pos, self.angle = state

    def get_pos(self):
        return self.x_pos, self.y_pos
    
    def in_gate(self):
        return self.x_pos + IMGS[f"{self.side} {self.state}"].get_width() >= BALL_RIGHT_GOAL_X or self.x_pos <= BALL_LEFT_GOAL_X

    def get_vx(self):
        return self.__vx
    
    def get_vy(self):
        return self.__vy
    
    def set_vx(self, v):
        self.__vx = v
    
    def set_vy(self, v):
        self.__vy = v

    def increase_v(self):
        new_vx = ball_accelerate_x(self.__vx)
        if new_vx < BALL_SPEED_LIMIT_X:
            self.__vx = new_vx
        else:
            self.__vx = BALL_SPEED_LIMIT_X
        self.__vx = new_vx

    def decrease_v(self):
        new_vx = ball_decelerate_x(self.__vx)
        if new_vx > -BALL_SPEED_LIMIT_X:
            self.__vx = new_vx
        else:
            self.__vx = -BALL_SPEED_LIMIT_X
        self.__vx = new_vx

        self.__vx = ball_decelerate_x(self.__vx)

    def update_loc_x(self):
        self.x_pos = ball_calc_loc_x(self.x_pos, self.__vx)
        self.check_borders()

    def update_loc_y(self, y_axis):
        self.__vy = accelerate_y(self.__vy)

        new_y_pos = ball_calc_loc_y(self.y_pos, self.__vy)
        if self.y_pos >= y_axis:
            self.__vy *= -1
        if new_y_pos <= BALL_UPPER_LIMIT:
            self.y_pos = BALL_UPPER_LIMIT
            self.__vy *= -1
        if new_y_pos >= y_axis:
            self.__vy *= -0.9
            if abs(self.__vy) < 32:
                self.__vy = 0
        else:
            self.y_pos = new_y_pos

    def move(self, y_axis):
        self.update_loc_x()
        if self.__vy:
            self.update_loc_y(y_axis)
    
    def stop(self):
        if abs(self.__vx) > 5:
            if self.__vx > 0:
                self.decrease_v()
            elif self.__vx < 0:
                self.increase_v()
        else:
            self.__vx = 0
    
    def kick_forward(self, player_side):
        if player_side == 'L':
            self.__vx = KICK_VELOCITY_X
        else:
            self.__vx = -KICK_VELOCITY_X
    
    def kick_up(self, player_side):
        self.kick_forward(player_side)
        self.__vy = KICK_VELOCITY_Y


    def update_velocity_impulse(self, vx, vy):
        if vx == 0:
            self.__vx *= -1
        else:
            new_vx = calc_vx_impulse(vx, self.__vx)
            if abs(new_vx) < BALL_SPEED_LIMIT_X:
                self.__vx = new_vx
            else:
                self.__vx = BALL_SPEED_LIMIT_X if new_vx > 0 else -BALL_SPEED_LIMIT_X
        
        new_vy = calc_vx_impulse(vy, self.__vy)
        if abs(new_vy) < BALL_SPEED_LIMIT_Y:
            self.__vy = new_vy
        else:
            self.__vy = BALL_SPEED_LIMIT_Y if new_vy > 0 else -BALL_SPEED_LIMIT_Y

    def update_angle(self):
        self.angle -= self.__vx / self.r

    def spin(self):
        img = IMGS['ball']
        rot_image = pygame.transform.rotate(img, self.angle)
        rot_rect = img.get_rect().copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def rotate(self):
        img = IMGS['ball']
        rot_image = pygame.transform.rotate(img, self.angle)
        rot_rect = img.get_rect().copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
    
    def check_borders(self):
        if self.x_pos <= BALL_LEFT_LIMIT or self.x_pos >= BALL_RIGHT_LIMIT:
            self.__vx *= -1
            self.x_pos = BALL_LEFT_LIMIT if self.x_pos < BALL_LEFT_LIMIT else BALL_RIGHT_LIMIT
            return True
        return False
    