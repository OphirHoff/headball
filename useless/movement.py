import pygame

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
pygame.display.flip()

ball_x_pos = 10
ball_y_pos = WINDOW_HEIGHT/2
pygame.draw.circle(screen, BLACK, [ball_x_pos, ball_y_pos], 10)
pygame.display.flip()

speed_limit = 800
a_x = 2000  # acceleration x
a_y = 2000  # acceleration y
speed_x = 0
speed_y = 0
jump_velocity = -800
time_delta = 1 / REFRESH_RATE

finish = False

while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
    
    if ball_x_pos > WINDOW_WIDTH or ball_x_pos < 0:
        speed_x = 0

    # if ball_x_pos <= WINDOW_WIDTH/2:# and ball_x_pos >= 0:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:# and ball_x_pos < WINDOW_WIDTH:
        if speed_x < speed_limit:
            speed_x = speed_x + a_x*time_delta
        ball_x_pos = ball_x_pos + speed_x*time_delta + a_x/2*(time_delta**2)
    
    # elif ball_x_pos >= WINDOW_WIDTH/2:# and ball_x_pos <= WINDOW_WIDTH-20:
    if keys[pygame.K_LEFT]:# and ball_x_pos > 0:
        if speed_x > -speed_limit:
            speed_x = speed_x - a_x*time_delta
        ball_x_pos = ball_x_pos + speed_x*time_delta + a_x/2*(time_delta**2)
    
    if keys[pygame.K_UP] and not speed_y:
       speed_y = jump_velocity
    
    if speed_y:
        if ball_y_pos <= WINDOW_HEIGHT/2:
            speed_y = speed_y + a_y*time_delta
            ball_y_pos = ball_y_pos + speed_y*time_delta + a_y/2*(time_delta**2)
        else:
            speed_y = 0
            ball_y_pos -= 5

    if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
        if abs(speed_x) > 1:
            if speed_x > 0:
                speed_x = speed_x - a_x*time_delta
                ball_x_pos = ball_x_pos + speed_x*time_delta +a_x/2*(time_delta**2)
            elif speed_x < 0:
                speed_x = speed_x + a_x*time_delta
                ball_x_pos = ball_x_pos + speed_x*time_delta + a_x/2*(time_delta**2)

    screen.fill(WHITE)
    pygame.draw.circle(screen, BLACK, [ball_x_pos, ball_y_pos], 10)
    pygame.display.flip()
    clock.tick(REFRESH_RATE)
    # print(speed_y)  
    
    


pygame.quit()