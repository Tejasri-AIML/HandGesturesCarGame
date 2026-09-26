import pygame
import sys
import random

# ==================================================
# PHASE 6
# CAR GAME + COLLISION DETECTION
# ==================================================

# --------------------------------------------------
# 1. Initialize Pygame
# --------------------------------------------------

pygame.init()


# --------------------------------------------------
# 2. Create Game Window
# --------------------------------------------------

WIDTH = 600
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Hand Gesture Car Game")

clock = pygame.time.Clock()


# --------------------------------------------------
# 3. Colors
# --------------------------------------------------

GREEN = (30, 120, 30)
GRAY = (80, 80, 80)
WHITE = (255, 255, 255)
RED = (220, 50, 50)
YELLOW = (255, 220, 0)
BLUE = (50, 100, 220)
BLACK = (0, 0, 0)


# --------------------------------------------------
# 4. Road Settings
# --------------------------------------------------

ROAD_WIDTH = 400

ROAD_LEFT = (WIDTH - ROAD_WIDTH) // 2
ROAD_RIGHT = ROAD_LEFT + ROAD_WIDTH


# --------------------------------------------------
# 5. Player Car Settings
# --------------------------------------------------

CAR_WIDTH = 50
CAR_HEIGHT = 90

car_x = WIDTH // 2 - CAR_WIDTH // 2
car_y = HEIGHT - 150

CAR_SPEED = 6


# --------------------------------------------------
# 6. Enemy Car Settings
# --------------------------------------------------

enemy_width = 50
enemy_height = 90

enemy_x = random.randint(
    ROAD_LEFT,
    ROAD_RIGHT - enemy_width
)

enemy_y = -enemy_height

enemy_speed = 5


# --------------------------------------------------
# 7. Game Variables
# --------------------------------------------------

running = True

game_over = False


# --------------------------------------------------
# 8. Fonts
# --------------------------------------------------

font = pygame.font.Font(None, 40)

game_over_font = pygame.font.Font(None, 70)


# ==================================================
# MAIN GAME LOOP
# ==================================================

while running:

    # --------------------------------------------------
    # 9. Handle Events
    # --------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


    # ==================================================
    # 10. NORMAL GAME
    # ==================================================

    if not game_over:

        # --------------------------------------------------
        # Keyboard Controls
        # --------------------------------------------------

        keys = pygame.key.get_pressed()

        # Move LEFT
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            car_x -= CAR_SPEED

        # Move RIGHT
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            car_x += CAR_SPEED


        # --------------------------------------------------
        # Keep Player Inside Road
        # --------------------------------------------------

        if car_x < ROAD_LEFT:
            car_x = ROAD_LEFT

        if car_x + CAR_WIDTH > ROAD_RIGHT:
            car_x = ROAD_RIGHT - CAR_WIDTH


        # --------------------------------------------------
        # Move Enemy Car
        # --------------------------------------------------

        enemy_y += enemy_speed


        # --------------------------------------------------
        # Reset Enemy When It Leaves Screen
        # --------------------------------------------------

        if enemy_y > HEIGHT:

            enemy_y = -enemy_height

            enemy_x = random.randint(
                ROAD_LEFT,
                ROAD_RIGHT - enemy_width
            )


        # --------------------------------------------------
        # Create Player Rectangle
        # --------------------------------------------------

        player_rect = pygame.Rect(
            car_x,
            car_y,
            CAR_WIDTH,
            CAR_HEIGHT
        )


        # --------------------------------------------------
        # Create Enemy Rectangle
        # --------------------------------------------------

        enemy_rect = pygame.Rect(
            enemy_x,
            enemy_y,
            enemy_width,
            enemy_height
        )


        # --------------------------------------------------
        # COLLISION DETECTION
        # --------------------------------------------------

        if player_rect.colliderect(enemy_rect):

            game_over = True


    # ==================================================
    # RESTART / QUIT AFTER GAME OVER
    # ==================================================

    else:

        keys = pygame.key.get_pressed()

        # Press R to restart
        if keys[pygame.K_r]:

            car_x = WIDTH // 2 - CAR_WIDTH // 2

            enemy_y = -enemy_height

            enemy_x = random.randint(
                ROAD_LEFT,
                ROAD_RIGHT - enemy_width
            )

            game_over = False


        # Press Q to quit
        if keys[pygame.K_q]:

            running = False


    # ==================================================
    # DRAWING
    # ==================================================

    # --------------------------------------------------
    # 11. Background
    # --------------------------------------------------

    screen.fill(GREEN)


    # --------------------------------------------------
    # 12. Draw Road
    # --------------------------------------------------

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


    # --------------------------------------------------
    # 13. Draw Road Lane
    # --------------------------------------------------

    lane_x = WIDTH // 2

    for y in range(0, HEIGHT, 80):

        pygame.draw.rect(
            screen,
            WHITE,
            (
                lane_x - 5,
                y,
                10,
                40
            )
        )


    # --------------------------------------------------
    # 14. Draw Player Car
    # --------------------------------------------------

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


    # --------------------------------------------------
    # 15. Player Car Window
    # --------------------------------------------------

    pygame.draw.rect(
        screen,
        BLUE,
        (
            car_x + 10,
            car_y + 10,
            CAR_WIDTH - 20,
            25
        )
    )


    # --------------------------------------------------
    # 16. Draw Enemy Car
    # --------------------------------------------------

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


    # --------------------------------------------------
    # 17. Enemy Car Window
    # --------------------------------------------------

    pygame.draw.rect(
        screen,
        BLUE,
        (
            enemy_x + 10,
            enemy_y + 10,
            enemy_width - 20,
            25
        )
    )


    # ==================================================
    # GAME OVER SCREEN
    # ==================================================

    if game_over:

        # Dark transparent effect
        overlay = pygame.Surface(
            (WIDTH, HEIGHT)
        )

        overlay.set_alpha(150)

        overlay.fill(BLACK)

        screen.blit(
            overlay,
            (0, 0)
        )


        # GAME OVER text

        game_over_text = game_over_font.render(
            "GAME OVER",
            True,
            WHITE
        )

        screen.blit(
            game_over_text,
            (
                WIDTH // 2 -
                game_over_text.get_width() // 2,
                HEIGHT // 2 - 80
            )
        )


        # Restart message

        restart_text = font.render(
            "Press R to Restart",
            True,
            WHITE
        )

        screen.blit(
            restart_text,
            (
                WIDTH // 2 -
                restart_text.get_width() // 2,
                HEIGHT // 2 + 10
            )
        )


        # Quit message

        quit_text = font.render(
            "Press Q to Quit",
            True,
            WHITE
        )

        screen.blit(
            quit_text,
            (
                WIDTH // 2 -
                quit_text.get_width() // 2,
                HEIGHT // 2 + 60
            )
        )


    # --------------------------------------------------
    # 18. Update Screen
    # --------------------------------------------------

    pygame.display.flip()


    # --------------------------------------------------
    # 19. FPS
    # --------------------------------------------------

    clock.tick(60)


# ==================================================
# 20. Quit Pygame
# ==================================================

pygame.quit()

sys.exit()