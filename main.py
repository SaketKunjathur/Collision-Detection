import pygame
import sys
import math

# constants
SCREEN_HEIGHT = 480
SCREEN_WIDTH = SCREEN_HEIGHT * 2
MAP_SIZE = 8
TILE_SIZE = ((SCREEN_WIDTH / 2) / MAP_SIZE)
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
FOV = math.pi / 3
HALF_FOV = FOV / 2
CASTED_RAYS = 120
STEP_ANGLE = FOV / CASTED_RAYS
SCALE = (SCREEN_WIDTH / 2) / CASTED_RAYS

# global variables
player_x = (SCREEN_WIDTH / 2) // 2
player_y = SCREEN_HEIGHT // 2
player_angle = math.pi

MAP = (
    '########'
    '# #    #'
    '# #  ###'
    '#      #'
    '#      #'
    '#  ##  #'
    '#   #  #'
    '########'
)

pygame.init()

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RAYCASTING")
clock = pygame.time.Clock()

def draw_map():
    for row in range(8):
        for col in range(8):
            square  = row * MAP_SIZE + col
            pygame.draw.rect(
                win,
                (200, 200, 200) if MAP[square] == '#' else (100, 100, 100),
                (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
            )

            pygame.draw.circle(win, (255, 0, 0), (player_x, player_y), 8)

            # draw player directions
            pygame.draw.line(win, (0, 255, 0), (player_x, player_y),
                                               (player_x - math.sin(player_angle) * 50,
                                                player_y + math.cos(player_angle) * 50), 3)

            # draw player FOV
            pygame.draw.line(win, (0, 255, 0), (player_x, player_y),
                                               (player_x - math.sin(player_angle - HALF_FOV) * 50,
                                                player_y + math.cos(player_angle - HALF_FOV) * 50), 3)

            pygame.draw.line(win, (0, 255, 0), (player_x, player_y),
                                               (player_x - math.sin(player_angle + HALF_FOV) * 50,
                                               player_y + math.cos(player_angle + HALF_FOV) * 50), 3)

# raycasting algorithm
def cast_rays():
    # define leftmost angle of FOV
    start_angle = player_angle - HALF_FOV

    # loop over casted rays
    for ray in range(CASTED_RAYS):
        # cast ray step by step
        for depth in range(MAX_DEPTH):
            # get ray target coordinates
            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y + math.cos(start_angle) * depth

            # convert target Y coordinate to map row
            col = int(target_x / TILE_SIZE)
            row = int(target_y / TILE_SIZE)

            # calculate map square index
            square = row * MAP_SIZE + col
            if MAP[square] == '#':
                pygame.draw.rect(win, (0, 255, 0), (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2))

                # draw casted ray
                pygame.draw.line(win, (255, 255, 0), (player_x, player_y), (target_x, target_y))

                # wall shading
                color = 255 / (1 + depth * depth * 0.0001)

                # fixing fish eye effect
                depth *= math.cos(player_angle - start_angle)

                # calculate wall height
                wall_height = 21000 / (depth + 0.0001)

                # fix stuck at wall
                if wall_height > SCREEN_HEIGHT: wall_height = SCREEN_HEIGHT

                # draw 3d projection rectangle by recatnagle
                pygame.draw.rect(win, (color, color, color), (
                    SCREEN_HEIGHT + ray * SCALE,
                    SCREEN_HEIGHT / 2 - wall_height / 2,
                    SCALE, wall_height))

                break

            # draw casted rays
            # pygame.draw.line(win, (255, 255, 0), (player_x, player_y), (target_x, target_y), 3)

        # increment angle by a single step
        start_angle += STEP_ANGLE

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)

    pygame.draw.rect(win, (0, 0, 0), (0, 0, SCREEN_HEIGHT, SCREEN_HEIGHT))

    # updateing 3d background
    pygame.draw.rect(win, (100, 100, 100), (480, SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))
    pygame.draw.rect(win, (200, 200, 200), (480, -SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))

    draw_map()

    # apply raycasting
    cast_rays()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player_angle -= 0.1
    if keys[pygame.K_RIGHT]: player_angle += 0.1
    if keys[pygame.K_UP]:
        player_x += -math.sin(player_angle) * 5
        player_y += math.cos(player_angle) * 5
    if keys[pygame.K_DOWN]:
        player_x -= -math.sin(player_angle) * 5
        player_y -= math.cos(player_angle) * 5

    pygame.display.update()
    clock.tick(30)
