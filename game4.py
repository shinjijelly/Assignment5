import pygame
import sys
import random

def game4_page(screen, font, WHITE, BLACK):
    frame_width = 900
    frame_height = 700
    block_size = 20  # 블록 크기 조정
    score = 0
    level = 1

    pygame.display.set_caption("테트리스")

    game_display = pygame.display.set_mode((frame_width, frame_height))
    clock = pygame.time.Clock()

    # 게임 필드 크기 설정
    game_field_width = block_size * 25  # 25 x block_size
    game_field_height = block_size * 35  # 35 x block_size
    game_field_left = (frame_width - game_field_width) // 2
    game_field_top = (frame_height - game_field_height) // 2

    # 블록 모양 구성
    shapes = [
        [  # I 모양
            [[3, 0], [4, 0], [5, 0], [6, 0]],
            [[5, -1], [5, 0], [5, 1], [5, 2]]
        ],
        [  # L 모양
            [[4, 0], [4, 1], [4, 2], [5, 2]],
            [[3, 1], [4, 1], [5, 1], [3, 2]],
            [[4, 0], [5, 0], [5, 1], [5, 2]],
            [[5, 1], [3, 2], [4, 2], [5, 2]]
        ],
        [  # S 모양
            [[4, 0], [5, 0], [3, 1], [4, 1]],
            [[4, 0], [4, 1], [5, 1], [5, 2]]
        ],
        [  # T 모양
            [[4, 0], [3, 1], [4, 1], [5, 1]],
            [[4, 0], [4, 1], [5, 1], [4, 2]],
            [[3, 1], [4, 1], [5, 1], [4, 2]],
            [[4, 0], [4, 1], [3, 1], [4, 2]]
        ],
        [  # 정사각형 모양
            [[4, 0], [5, 0], [4, 1], [5, 1]]
        ]
    ]

    # 블럭 색깔 구성
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
        shape = [block[:] for block in shapes[shape_index][0]]
        color = random.choice(colors)
        # 블록의 초기 위치를 조정
        initial_x = (game_field_width // block_size - len(shape[0])) // 3
        shape = [[x + initial_x, y] for x, y in shape]
        return shape, shape_index, color, 0

    # 바닥과의 충돌 감지
    def check_collision(shape, field):
        for x, y in shape:
            if x < 0 or x >= game_field_width // block_size or y >= game_field_height // block_size or (y >= 0 and field[y][x]):
                return True
        return False

    def merge_shape(shape, color, field):
        for x, y in shape:
            field[y][x] = color

    def drop_block():
        moved_shape = current_shape[:]
        while not check_collision([[x, y + 1] for x, y in moved_shape], field):
            moved_shape = [[x, y + 1] for x, y in moved_shape]
        return moved_shape        

    # 한줄이 다 차면 줄 삭제
    def remove_full_lines(field):
        new_field = [row for row in field if any(cell == 0 for cell in row)]
        lines_removed = len(field) - len(new_field)
        new_field = [[0] * (game_field_width // block_size) for _ in range(lines_removed)] + new_field
        return new_field, lines_removed

    current_shape, current_shape_index, current_color, current_rotation = new_shape()
    fall_time = 0

    def draw_block(x, y, color):
        pygame.draw.rect(game_display, color, (game_field_left + x * block_size, game_field_top + y * block_size, block_size, block_size))
        pygame.draw.rect(game_display, (246, 246, 246), (game_field_left + x * block_size, game_field_top + y * block_size, block_size, block_size), 1)

    def draw_field():
        for y, row in enumerate(field):
            for x, cell in enumerate(row):
                if cell != 0:
                    draw_block(x, y, cell)

    def draw_background():
        game_display.fill(BLACK)
        pygame.draw.rect(game_display, WHITE, (game_field_left, game_field_top, game_field_width, game_field_height))

    # 게임 필드 내 눈금 표시
    def draw_grid():
        for x in range(game_field_left, game_field_left + game_field_width, block_size):
            pygame.draw.line(game_display, (246, 246, 246), (x, game_field_top), (x, game_field_top + game_field_height))
        for y in range(game_field_top, game_field_top + game_field_height, block_size):
            pygame.draw.line(game_display, (246, 246, 246), (game_field_left, y), (game_field_left + game_field_width, y))

    def draw_text(text, size, color, x, y):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        game_display.blit(text_surface, text_rect)

    def create_home_button(screen, font, WHITE, BLACK):
        image = pygame.image.load("resources/HomeButton2.png")
        button_width, button_height = 50,50
        image = pygame.transform.scale(image, (button_width, button_height))
        image_rect = image.get_rect(topleft=(10, 10))
        screen.blit(image, image_rect)

        return image_rect

    def game_over():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if home_button.collidepoint(event.pos):
                        return "home"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        return "restart"

            # 홈 버튼 그리기
            home_button = create_home_button(screen, font, WHITE, BLACK)

            draw_text("GAME OVER", 64, (255,0,0), frame_width // 2 - 130, frame_height // 2 - 50)

            restart_button = pygame.Rect(frame_width // 2 - 160, frame_height // 2 + 50, 200, 50)
            pygame.draw.rect(game_display, WHITE, restart_button)
            draw_text("PRESS 'S' TO RESET GAME", 36, BLACK, restart_button.x, restart_button.y + 5)

            pygame.display.update()

    def reset_game():
        nonlocal field, score, level, current_shape, current_shape_index, current_color, current_rotation, fall_time
        field = [[0 for _ in range(game_field_width // block_size)] for _ in range(game_field_height // block_size)]
        score = 0
        level = 1
        current_shape, current_shape_index, current_color, current_rotation = new_shape()
        fall_time = 0

    def increase_score(lines_removed):
        nonlocal score, level
        score += lines_removed * 100
        level = score // 1000 + 1  # 점수 1000점 당 1 레벨 증가

    move_delay = 0

    while True:
        draw_background()  # 게임 필드 외부를 검은색으로 채움
        draw_grid()  # 그리드 그리기

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if home_button.collidepoint(event.pos):
                    pygame.display.set_caption("미니게임 모음.zip")
                    return

        # 키 입력 이벤트 설정
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and move_delay <= 0:
            moved_shape = [[x - 1, y] for x, y in current_shape]
            if not check_collision(moved_shape, field):
                current_shape = moved_shape
            move_delay = 10
        if keys[pygame.K_RIGHT] and move_delay <= 0:
            moved_shape = [[x + 1, y] for x, y in current_shape]
            if not check_collision(moved_shape, field):
                current_shape = moved_shape
            move_delay = 10
        if keys[pygame.K_DOWN] and move_delay <= 0:
            moved_shape = [[x, y + 1] for x, y in current_shape]
            if not check_collision(moved_shape, field):
                current_shape = moved_shape
            move_delay = 5
        if keys[pygame.K_UP] and move_delay <= 0:
            current_rotation = (current_rotation + 1) % len(shapes[current_shape_index])
            rotated_shape = [block[:] for block in shapes[current_shape_index][current_rotation]]
            rotated_shape = [[x + current_shape[0][0], y + current_shape[0][1]] for x, y in rotated_shape]
            if not check_collision(rotated_shape, field):
                current_shape = rotated_shape
            move_delay = 10
        if keys[pygame.K_SPACE]:
            current_shape = drop_block()

        move_delay -= 1

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
                    action = game_over()
                    if action == "home":
                        pygame.display.set_caption("미니게임 모음.zip")
                        return
                    elif action == "restart":
                        reset_game()

        draw_field()

        for x, y in current_shape:
            draw_block(x, y, current_color)

        draw_text(f"Score: {score}", 36, WHITE, frame_width - 150, 50)
        draw_text(f"Level: {level}", 36, WHITE, frame_width - 150, 100)

        # 홈 버튼 그리기
        home_button = create_home_button(screen, font, WHITE, BLACK)

        pygame.display.update()
        clock.tick(60)