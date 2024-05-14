import pygame

pygame.init()

#define screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Masks")

#define colours
BG = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

#hide mouse cursor
pygame.mouse.set_visible(False)

#create soldier
player = pygame.image.load("images/right_player.png").convert_alpha()
player_rect = player.get_rect()
player_mask = pygame.mask.from_surface(player)
mask_image = player_mask.to_surface()

#game loop
run = True
while run:

    #update background
    screen.fill(BG)

    screen.blit(mask_image, (0, 0))

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.flip()

pygame.quit()