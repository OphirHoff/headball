import pygame, math

IMG = "images/better_ball.png"

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
pygame.init()
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Game")
clock = pygame.time.Clock()
REFRESH_RATE = 60

screen.fill(WHITE)

ball_x_pos = WINDOW_WIDTH/2
ball_y_pos = 200

ball_image = pygame.image.load("images/better_ball.png").convert_alpha()
ball_image = pygame.transform.scale_by(ball_image, 0.5)

r = ball_image.get_width() / 2  # ball radius
c = ball_image.get_width() * math.pi  # ball circumference

speed_x = 0
speed_y = 0
speed_limit = 800
time_delta = 1 / REFRESH_RATE
a_x = 2000
a_y = 2000
jump_velocity = -1000

angle = 0

RIGHT_WALL = WINDOW_WIDTH - ball_image.get_size()[1]
LEFT_WALL = 0


pygame.display.flip()

finish = False
while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        if speed_x < speed_limit:
            speed_x = speed_x + a_x*time_delta
        ball_x_pos = ball_x_pos + speed_x*time_delta + a_x/2*(time_delta**2)
    
    if keys[pygame.K_LEFT]:
        if speed_x > -speed_limit:
            speed_x = speed_x - a_x*time_delta
        ball_x_pos = ball_x_pos + speed_x*time_delta + a_x/2*(time_delta**2)

    if ball_x_pos <= LEFT_WALL or ball_x_pos > RIGHT_WALL:
        speed_x *= -1
    
    if keys[pygame.K_UP] and not speed_y:
       speed_y = jump_velocity
    
    if speed_y:
        if ball_y_pos <= WINDOW_HEIGHT/2:
            speed_y = speed_y + a_y*time_delta
            ball_y_pos = ball_y_pos + speed_y*time_delta + a_y/2*(time_delta**2)
        else:
            jump_velocity += 200
            speed_y = jump_velocity
            ball_y_pos -= 5
            if jump_velocity == 0:
                jump_velocity = -1000
                speed_y = 0
                # ball_y_pos -= 5

    if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
        if abs(speed_x) > 1:
            if speed_x > 0:
                speed_x = speed_x - a_x*time_delta
                ball_x_pos = ball_x_pos + speed_x*time_delta +a_x/2*(time_delta**2)
            elif speed_x < 0:
                speed_x = speed_x + a_x*time_delta
                ball_x_pos = ball_x_pos + speed_x*time_delta +a_x/2*(time_delta**2)
        else:
            speed_x = 0


    angle -= speed_x / r
    angle %= 360

    screen.fill(WHITE)

    rot_image = pygame.transform.rotate(ball_image, angle)
    rot_rect = ball_image.get_rect().copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    screen.blit(rot_image, (ball_x_pos, ball_y_pos))
    # img_copy = pygame.transform.rotate(ball_image, angle)
    # screen.blit(img_copy, [ball_x_pos - int(img_copy.get_width() / 2), ball_y_pos - int(img_copy.get_height() / 2)])

    # rotated = pygame.transform.rotate(ball_image, angle)
    # screen.blit(rotated, (ball_x_pos, ball_y_pos))
    pygame.display.flip()
    clock.tick(REFRESH_RATE)
