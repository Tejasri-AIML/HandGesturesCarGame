import cv2
import mediapipe as mp
import pygame
import random
import sys


# ============================================================
# INITIALIZATION
# ============================================================

pygame.init()

WIDTH = 600
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hand Gesture Car Game")

clock = pygame.time.Clock()


# ============================================================
# COLORS
# ============================================================

GREEN = (40, 150, 60)
GRAY = (70, 70, 70)
WHITE = (255, 255, 255)
RED = (220, 40, 40)
YELLOW = (255, 200, 0)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
BLUE = (50, 150, 255)


# ============================================================
# ROAD SETTINGS
# ============================================================

ROAD_WIDTH = 400

ROAD_LEFT = (WIDTH - ROAD_WIDTH) // 2
ROAD_RIGHT = ROAD_LEFT + ROAD_WIDTH


# ============================================================
# PLAYER CAR
# ============================================================

CAR_WIDTH = 50
CAR_HEIGHT = 80

car_x = WIDTH // 2 - CAR_WIDTH // 2
car_y = HEIGHT - 150


# Horizontal movement
HORIZONTAL_SPEED = 8


# Forward / Backward movement
FORWARD_SPEED = 7
BACKWARD_SPEED = 5


# ============================================================
# ENEMY CAR
# ============================================================

enemy_width = 50
enemy_height = 80

enemy_x = random.randint(
    ROAD_LEFT,
    ROAD_RIGHT - enemy_width
)

enemy_y = -100

enemy_speed = 5


# ============================================================
# COIN
# ============================================================

COIN_RADIUS = 14

coin_x = random.randint(
    ROAD_LEFT + COIN_RADIUS,
    ROAD_RIGHT - COIN_RADIUS
)

coin_y = -50

coin_speed = 5


# ============================================================
# SCORE
# ============================================================

score = 0


# ============================================================
# FONTS
# ============================================================

font = pygame.font.Font(None, 34)

game_over_font = pygame.font.Font(None, 70)

instruction_font = pygame.font.Font(None, 30)


# ============================================================
# GAME STATE
# ============================================================

game_over = False


# ============================================================
# MEDIAPIPE HAND SETUP
# ============================================================

mp_hands = mp.solutions.hands

mp_drawing = mp.solutions.drawing_utils


hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)


# ============================================================
# CAMERA
# ============================================================

camera = cv2.VideoCapture(0)


if not camera.isOpened():

    print("Could not access camera.")

    print("Try changing VideoCapture(0) to VideoCapture(1).")

    pygame.quit()

    sys.exit()


# ============================================================
# GESTURE VARIABLES
# ============================================================

direction = "CENTER"

movement = "STOP"


# ============================================================
# GET PALM POSITION
# ============================================================

def get_palm_position(hand_landmarks):

    """
    Calculate the center position of the palm.

    We use landmarks:
    0  = Wrist
    5  = Index finger base
    9  = Middle finger base
    13 = Ring finger base
    17 = Little finger base
    """

    palm_points = [0, 5, 9, 13, 17]

    x = 0
    y = 0

    for point in palm_points:

        x += hand_landmarks.landmark[point].x
        y += hand_landmarks.landmark[point].y

    x = x / len(palm_points)
    y = y / len(palm_points)

    return x, y


# ============================================================
# GET FINGER STATUS
# ============================================================

def get_finger_status(hand_landmarks):

    landmarks = hand_landmarks.landmark

    index_up = landmarks[8].y < landmarks[6].y

    middle_up = landmarks[12].y < landmarks[10].y

    ring_up = landmarks[16].y < landmarks[14].y

    little_up = landmarks[20].y < landmarks[18].y

    return [
        index_up,
        middle_up,
        ring_up,
        little_up
    ]


# ============================================================
# GET MOVEMENT
# ============================================================

def get_movement(hand_landmarks):

    """
    Determine forward/backward using PALM POSITION.

    Camera coordinates:
        y close to 0 = top
        y close to 1 = bottom

    Therefore:

        Hand UP   -> FORWARD
        Hand DOWN -> BACKWARD
        Center    -> STOP
    """

    palm_x, palm_y = get_palm_position(hand_landmarks)


    # --------------------------------------------------------
    # VERTICAL ZONES
    # --------------------------------------------------------

    if palm_y < 0.35:

        return "FORWARD"


    elif palm_y > 0.65:

        return "BACKWARD"


    else:

        return "STOP"


# ============================================================
# GET HORIZONTAL DIRECTION
# ============================================================

def get_direction(hand_landmarks):

    """
    Determine LEFT / CENTER / RIGHT using palm X position.
    """

    palm_x, palm_y = get_palm_position(hand_landmarks)


    if palm_x < 0.35:

        return "LEFT"


    elif palm_x > 0.65:

        return "RIGHT"


    else:

        return "CENTER"


# ============================================================
# RESET GAME
# ============================================================

def reset_game():

    global car_x
    global car_y

    global enemy_x
    global enemy_y

    global coin_x
    global coin_y

    global score

    global game_over


    # Reset player
    car_x = WIDTH // 2 - CAR_WIDTH // 2

    car_y = HEIGHT - 150


    # Reset enemy
    enemy_x = random.randint(
        ROAD_LEFT,
        ROAD_RIGHT - enemy_width
    )

    enemy_y = -100


    # Reset coin
    coin_x = random.randint(
        ROAD_LEFT + COIN_RADIUS,
        ROAD_RIGHT - COIN_RADIUS
    )

    coin_y = -50


    # Reset score
    score = 0


    # Reset game
    game_over = False


# ============================================================
# MAIN GAME LOOP
# ============================================================

running = True


while running:

    # ========================================================
    # PYGAME EVENTS
    # ========================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False


        if event.type == pygame.KEYDOWN:

            # Restart
            if event.key == pygame.K_r and game_over:

                reset_game()


            # Quit
            if event.key == pygame.K_q:

                running = False


    # ========================================================
    # CAMERA
    # ========================================================

    success, frame = camera.read()


    if not success:

        print("Could not read camera frame.")

        break


    # Mirror camera
    frame = cv2.flip(frame, 1)


    # Convert BGR -> RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    # Process hand
    results = hands.process(rgb_frame)


    # Default values
    direction = "CENTER"

    movement = "STOP"


    # ========================================================
    # HAND DETECTION
    # ========================================================

    if results.multi_hand_landmarks:

        hand_landmarks = results.multi_hand_landmarks[0]


        # Draw hand landmarks
        mp_drawing.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS
        )


        # Get horizontal direction
        direction = get_direction(
            hand_landmarks
        )


        # Get vertical movement
        movement = get_movement(
            hand_landmarks
        )


        # ----------------------------------------------------
        # CHECK FOR FIST
        # ----------------------------------------------------

        fingers = get_finger_status(
            hand_landmarks
        )


        # If all fingers are down = fist
        if not any(fingers):

            movement = "BRAKE"


    # ========================================================
    # GAME LOGIC
    # ========================================================

    if not game_over:


        # ====================================================
        # LEFT / RIGHT CAR MOVEMENT
        # ====================================================

        if direction == "LEFT":

            car_x -= HORIZONTAL_SPEED


        elif direction == "RIGHT":

            car_x += HORIZONTAL_SPEED


        # Keep car inside road
        if car_x < ROAD_LEFT:

            car_x = ROAD_LEFT


        if car_x > ROAD_RIGHT - CAR_WIDTH:

            car_x = ROAD_RIGHT - CAR_WIDTH


        # ====================================================
        # FORWARD MOVEMENT
        # ====================================================

        if movement == "FORWARD":

            car_y -= FORWARD_SPEED


        # ====================================================
        # BACKWARD MOVEMENT
        # ====================================================

        elif movement == "BACKWARD":

            car_y += BACKWARD_SPEED


        # ====================================================
        # BRAKE
        # ====================================================

        elif movement == "BRAKE":

            # Car stays in position
            car_y = car_y


        # ====================================================
        # KEEP CAR INSIDE SCREEN
        # ====================================================

        if car_y < 100:

            car_y = 100


        if car_y > HEIGHT - CAR_HEIGHT:

            car_y = HEIGHT - CAR_HEIGHT


        # ====================================================
        # ENEMY MOVEMENT
        # ====================================================

        enemy_y += enemy_speed


        if enemy_y > HEIGHT:

            enemy_y = -100

            enemy_x = random.randint(
                ROAD_LEFT,
                ROAD_RIGHT - enemy_width
            )


        # ====================================================
        # COIN MOVEMENT
        # ====================================================

        coin_y += coin_speed


        if coin_y > HEIGHT:

            coin_y = -50

            coin_x = random.randint(
                ROAD_LEFT + COIN_RADIUS,
                ROAD_RIGHT - COIN_RADIUS
            )


        # ====================================================
        # CREATE PLAYER RECTANGLE
        # ====================================================

        player_rect = pygame.Rect(
            car_x,
            car_y,
            CAR_WIDTH,
            CAR_HEIGHT
        )


        # ====================================================
        # CREATE ENEMY RECTANGLE
        # ====================================================

        enemy_rect = pygame.Rect(
            enemy_x,
            enemy_y,
            enemy_width,
            enemy_height
        )


        # ====================================================
        # CREATE COIN RECTANGLE
        # ====================================================

        coin_rect = pygame.Rect(
            coin_x - COIN_RADIUS,
            coin_y - COIN_RADIUS,
            COIN_RADIUS * 2,
            COIN_RADIUS * 2
        )


        # ====================================================
        # ENEMY COLLISION
        # ====================================================

        if player_rect.colliderect(enemy_rect):

            game_over = True


        # ====================================================
        # COIN COLLECTION
        # ====================================================

        if player_rect.colliderect(coin_rect):

            score += 10


            # New coin
            coin_y = -50

            coin_x = random.randint(
                ROAD_LEFT + COIN_RADIUS,
                ROAD_RIGHT - COIN_RADIUS
            )


    # ========================================================
    # DRAW BACKGROUND
    # ========================================================

    screen.fill(GREEN)


    # ========================================================
    # DRAW ROAD
    # ========================================================

    pygame.draw.rect(
        screen,
        GRAY,
        (
            ROAD_LEFT,
            0,
            ROAD_WIDTH,
            HEIGHT
        )
    )


    # ========================================================
    # DRAW CENTER LINE
    # ========================================================

    pygame.draw.rect(
        screen,
        WHITE,
        (
            WIDTH // 2 - 5,
            0,
            10,
            HEIGHT
        )
    )


    # ========================================================
    # DRAW PLAYER CAR
    # ========================================================

    pygame.draw.rect(
        screen,
        RED,
        (
            car_x,
            car_y,
            CAR_WIDTH,
            CAR_HEIGHT
        )
    )


    # ========================================================
    # DRAW ENEMY
    # ========================================================

    pygame.draw.rect(
        screen,
        YELLOW,
        (
            enemy_x,
            enemy_y,
            enemy_width,
            enemy_height
        )
    )


    # ========================================================
    # DRAW COIN
    # ========================================================

    pygame.draw.circle(
        screen,
        GOLD,
        (
            int(coin_x),
            int(coin_y)
        ),
        COIN_RADIUS
    )


    pygame.draw.circle(
        screen,
        YELLOW,
        (
            int(coin_x),
            int(coin_y)
        ),
        COIN_RADIUS - 4
    )


    # ========================================================
    # SCORE
    # ========================================================

    score_text = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    screen.blit(
        score_text,
        (20, 20)
    )


    # ========================================================
    # DIRECTION
    # ========================================================

    direction_text = font.render(
        f"Direction: {direction}",
        True,
        WHITE
    )

    screen.blit(
        direction_text,
        (20, 55)
    )


    # ========================================================
    # MOVEMENT
    # ========================================================

    movement_text = font.render(
        f"Movement: {movement}",
        True,
        WHITE
    )

    screen.blit(
        movement_text,
        (20, 90)
    )


    # ========================================================
    # CAMERA DISPLAY TEXT
    # ========================================================

    cv2.putText(
        frame,
        f"Direction: {direction}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )


    cv2.putText(
        frame,
        f"Movement: {movement}",
        (20, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )


    # ========================================================
    # CAMERA WINDOW
    # ========================================================

    cv2.imshow(
        "Hand Gesture Camera",
        frame
    )


    # ========================================================
    # GAME OVER SCREEN
    # ========================================================

    if game_over:

        overlay = pygame.Surface(
            (WIDTH, HEIGHT)
        )

        overlay.set_alpha(170)

        overlay.fill(BLACK)

        screen.blit(
            overlay,
            (0, 0)
        )


        game_over_text = game_over_font.render(
            "GAME OVER",
            True,
            RED
        )

        screen.blit(
            game_over_text,
            (
                WIDTH // 2 -
                game_over_text.get_width() // 2,
                HEIGHT // 2 - 120
            )
        )


        final_score_text = font.render(
            f"Final Score: {score}",
            True,
            WHITE
        )

        screen.blit(
            final_score_text,
            (
                WIDTH // 2 -
                final_score_text.get_width() // 2,
                HEIGHT // 2 - 20
            )
        )


        restart_text = instruction_font.render(
            "Press R to Restart",
            True,
            WHITE
        )

        screen.blit(
            restart_text,
            (
                WIDTH // 2 -
                restart_text.get_width() // 2,
                HEIGHT // 2 + 40
            )
        )


        quit_text = instruction_font.render(
            "Press Q to Quit",
            True,
            WHITE
        )

        screen.blit(
            quit_text,
            (
                WIDTH // 2 -
                quit_text.get_width() // 2,
                HEIGHT // 2 + 80
            )
        )


    # ========================================================
    # UPDATE DISPLAY
    # ========================================================

    pygame.display.update()

    clock.tick(60)


    # ========================================================
    # QUIT USING CAMERA WINDOW
    # ========================================================

    if cv2.waitKey(1) & 0xFF == ord("q"):

        running = False


# ============================================================
# CLEANUP
# ============================================================

camera.release()

cv2.destroyAllWindows()

hands.close()

pygame.quit()

sys.exit()