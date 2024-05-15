import pygame

#  ----------- graphics constants -----------

REFRESH_RATE = 60
WINDOW_WIDTH = 1281
WINDOW_HEIGHT = 810

GAME_DURATION = 90  # seconds

Y_AXIS = 472
R_START_X = 970
L_START_X = 213
BALL_START_X = 615
BALL_AXIS = 540
BALL_OFFSET = 53

GAME_CHOOSE_LINE = 440

ARROW_LEFT_X = 230
ARROW_RIGHT_X = 970
ARROW_Y = 390

END_SCORE1_X = 360
END_SCORE2_X = 720
END_RESULT_DASH_X = 560
END_SCORE_Y = 300

WIN_TITLE = "YOU WON!"
LOSE_TITLE = "YOU LOST"
TIE_TITLE = "TIE"

TIE_TITLE_X = 430
WINLOSE_TITLE_X = 60
END_TITLE_Y = 20

TIMER_X_POS = 620
TIMER_Y_POS = 52

COUNT_X_POS = 300
COUNT_Y_POS = 200

LEFT_GATE_POS = (100, 332)
RIGHT_GATE_POS = (1033, 332)

COUNTER_1_IMAGE = 'images/counter1.png'
COUNTER_2_IMAGE = 'images/counter2.png'
COUNTER_3_IMAGE = 'images/counter3.png'
SONG_FILE = 'sounds/song2.mp3'
ARROW_IMAGE = 'images/arrow.png'
WIFI_IMAGE = 'images/wifi.png'
OPENING_IMAGE = 'images/open_page.png'
CHOOSE_IMAGE = 'images/choose_page.png'
RESULT_BG_IMAGE = 'images/score_page.jpg'
BACKGROUND = 'images/stadium.png'
BALL_IMAGE = 'images/ball.png'
GATE = 'images/gate_front.png'
RIGHT_PLAYER_IMAGE = 'images/right_player.png'
LEFT_PLAYER_IMAGE = 'images/left_player.png'
RIGHT_PLAYER_FORWARD_IMAGE = 'images/right_player_forward.png'
LEFT_PLAYER_FORWARD_IMAGE = 'images/left_player_forward.png'
RIGHT_PLAYER_BACKWARD_IMAGE = 'images/right_player_backwards.png'
LEFT_PLAYER_BACKWARD_IMAGE = 'images/left_player_backwards.png'
RIGHT_PLAYER_KICK = 'images/right_player_kick.png'
LEFT_PLAYER_KICK = 'images/left_player_kick.png'
IMGS = {
    'counter1'   :  pygame.image.load(COUNTER_1_IMAGE),
    'counter2'   :  pygame.image.load(COUNTER_2_IMAGE),
    'counter3'   :  pygame.image.load(COUNTER_3_IMAGE),
    'arrow'      :  pygame.image.load(ARROW_IMAGE),
    'wifi'       :  pygame.image.load(WIFI_IMAGE),
    'open'       :  pygame.image.load(OPENING_IMAGE),
    'choose'     :  pygame.image.load(CHOOSE_IMAGE),
    'result'     :  pygame.image.load(RESULT_BG_IMAGE),
    'ball'       :  pygame.image.load(BALL_IMAGE),
    'background' :  pygame.image.load(BACKGROUND),
    'L gate'     :  pygame.image.load(GATE),
    'R gate'     :  pygame.transform.flip(pygame.image.load(GATE), True, False),
    'R still'    :  pygame.image.load(RIGHT_PLAYER_IMAGE),
    'L still'    :  pygame.image.load(LEFT_PLAYER_IMAGE),
    'R forward'  :  pygame.image.load(RIGHT_PLAYER_FORWARD_IMAGE),
    'L forward'  :  pygame.image.load(LEFT_PLAYER_FORWARD_IMAGE),
    'R backward' :  pygame.image.load(RIGHT_PLAYER_BACKWARD_IMAGE),
    'L backward' :  pygame.image.load(LEFT_PLAYER_BACKWARD_IMAGE),
    'R kick'     :  pygame.image.load(RIGHT_PLAYER_KICK),
    'L kick'     :  pygame.image.load(LEFT_PLAYER_KICK)
}
MASKS = {
    'ball'       :  pygame.mask.from_surface(IMGS['ball']),
    'R still'    :  pygame.mask.from_surface(IMGS['R still']),
    'L still'    :  pygame.mask.from_surface(IMGS['L still']),
    'R forward'  :  pygame.mask.from_surface(IMGS['R forward']),
    'L forward'  :  pygame.mask.from_surface(IMGS['L forward']),
    'R backward' :  pygame.mask.from_surface(IMGS['R backward']),
    'L backward' :  pygame.mask.from_surface(IMGS['L backward']),
    'R kick'     :  pygame.mask.from_surface(IMGS['R kick']),
    'L kick'     :  pygame.mask.from_surface(IMGS['L kick'])
}

#  ------------- game constants -------------

### player ###
SPEED_LIMIT = 500
JUMP_VELOCITY = -1000
PLAYER_RIGHT_LIMIT = 1035
PLAYER_LEFT_LIMIT = 141
BALL_LEFT_GOAL_X =  200
BALL_RIGHT_GOAL_X = 1100
KICK_DURATION = 10
KICK_PAUSE = 10

### ball ###
BALL_RIGHT_LIMIT = 1090
BALL_LEFT_LIMIT = 141
BALL_UPPER_LIMIT = 300
BALL_SPEED_LIMIT_X = 500
BALL_SPEED_LIMIT_Y = 1200
KICK_VELOCITY_X = 1200
KICK_VELOCITY_Y = -1200
BALL_LEFT_GOAL_X =  190
BALL_RIGHT_GOAL_X = 1100

#  ----------- phyisics constants -----------
PLAYER_A_X = 3000  # acceleration x
PLAYER_A_Y = 4000  # acceleration y
BALL_A_X =  400
BALL_A_Y = 2000
PLAYER_MASS = 1680
BALL_MASS = 1200
TIME_DELTA = 1 / REFRESH_RATE

#  ----------- network constants ------------

MAX_ACTIVE_GAMES = 5
CONNECTION_TRIES = 2000
GAMESTART_TIMEOUT = 100