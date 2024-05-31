import pygame
import sys
import random
from copy import deepcopy

def game4_page(screen, font, WHITE, BLACK):
    frame_width = 900
    frame_height = 700
    block_size = 30
    dir = 0
    fall = 0
    lr = 0
    score = 0

    pygame.display.set_caption("Tetris")

    game_display = pygame.display.set_mode((frame_width, frame_height))
    clock = pygame.time.Clock()

    game_field_width = 690 # 30 x 30
    game_field_height = 690 # 30 x 23
    game_field_left = (frame_width - game_field_width) // 2
    game_field_top = frame_height - game_field_height

    shapes = [
        [  # Line shape
            [[3, 0], [4, 0], [5, 0], [6, 0]],
            [[5, -1], [5, 0], [5, 1], [5, 2]]
        ],
        [  # L shape
            [[4, 0], [4, 1], [4, 2], [5, 2]],
            [[3, 1], [4, 1], [5, 1], [3, 2]],
            [[4, 0], [5, 0], [5, 1], [5, 2]],
            [[5, 1], [3, 2], [4, 2], [5, 2]]
        ],
        [  # S shape
            [[4, 0], [5, 0], [3, 1], [4, 1]],
            [[4, 0], [4, 1], [5, 1], [5, 2]]
        ],
        [  # T shape
            [[4, 0], [3, 1], [4, 1], [5, 1]],
            [[4, 0], [4, 1], [5, 1], [4, 2]],
            [[3, 1], [4, 1], [5, 1], [4, 2]],
            [[4, 0], [4, 1], [3, 1], [4, 2]]
        ],
        [  # Square shape
            [[4, 0], [5, 0], [4, 1], [5, 1]]
        ]
    ]

    colors = [
        pygame.Color(3, 65, 174),
        pygame.Color(114, 203, 59),
        pygame.Color(255, 213, 0),
        pygame.Color(255, 151, 28),
        pygame.Color(255, 50, 19)
    ]

    field = [[0 for _ in range(game_field_width // block_size)] for _ in range(game_field_height // block_size)]

    def new_shape():
        shape_index = random.randint(0, len(shapes) - 1)
        shape = deepcopy(shapes[shape_index][0])
        color = random.choice(colors)
        return shape, shape_index, color, 0

    def check_collision(shape, field):
        for x, y in shape:
            if x < 0 or x >= game_field_width // block_size or y >= game_field_height // block_size or (y >= 0 and field[y][x]):
                return True
        return False

    def merge_shape(shape, color, field):
        for x, y in shape:
            field[y][x] = color

    def remove_full_lines(field):
        new_field = [row for row in field if any(cell == 0 for cell in row)]
        lines_removed = len(field) - len(new_field)
        new_field = [[0] * (game_field_width // block_size) for _ in range(lines_removed)] + new_field
        return new_field, lines_removed

    current_shape, current_shape_index, current_color, current_rotation = new_shape()
    fall_time = 0

    def draw_grid():
        for i in range(game_field_height // block_size):
            pygame.draw.line(game_display, pygame.Color(20, 20, 20), (game_field_left, game_field_top + i * block_size), (game_field_left + game_field_width, game_field_top + i * block_size))
        for j in range(game_field_width // block_size):
            pygame.draw.line(game_display, pygame.Color(20, 20, 20), (game_field_left + j * block_size, game_field_top), (game_field_left + j * block_size, game_field_top + game_field_height))

    def draw_field():
        for y, row in enumerate(field):
            for x, cell in enumerate(row):
                if cell != 0:
                    pygame.draw.rect(game_display, cell, (game_field_left + x * block_size, game_field_top + y * block_size, block_size, block_size))

    while True:
        game_display.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            moved_shape = [[x - 1, y] for x, y in current_shape]
            if not check_collision(moved_shape, field):
                current_shape = moved_shape
        if keys[pygame.K_RIGHT]:
            moved_shape = [[x + 1, y] for x, y in current_shape]
            if not check_collision(moved_shape, field):
                current_shape = moved_shape
        if keys[pygame.K_DOWN]:
            moved_shape = [[x, y + 1] for x, y in current_shape]
            if not check_collision(moved_shape, field):
                current_shape = moved_shape
        if keys[pygame.K_UP]:
            current_rotation = (current_rotation + 1) % len(shapes[current_shape_index])
            rotated_shape = deepcopy(shapes[current_shape_index][current_rotation])
            rotated_shape = [[x + current_shape[0][0], y + current_shape[0][1]] for x, y in rotated_shape]
            if not check_collision(rotated_shape, field):
                current_shape = rotated_shape

        fall_time += clock.get_rawtime()
        if fall_time >= 500:
            fall_time = 0
            moved_shape = [[x, y + 1] for x, y in current_shape]
            if not check_collision(moved_shape, field):
                current_shape = moved_shape
            else:
                merge_shape(current_shape, current_color, field)
                field, lines_removed = remove_full_lines(field)
                score += lines_removed * 100
                current_shape, current_shape_index, current_color, current_rotation = new_shape()
                if check_collision(current_shape, field):
                    print("Game Over")
                    pygame.quit()
                    sys.exit()

        draw_grid()
        draw_field()

        for x, y in current_shape:
            pygame.draw.rect(game_display, current_color, (game_field_left + x * block_size, game_field_top + y * block_size, block_size, block_size))

        pygame.display.update()
        clock.tick(60)

