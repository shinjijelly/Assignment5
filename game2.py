import pygame
import sys

# 보드 크기와 셀 크기 정의
BOARD_SIZE = 19
CELL_SIZE = 30
BOARD_WIDTH = BOARD_SIZE * CELL_SIZE
BOARD_HEIGHT = BOARD_SIZE * CELL_SIZE

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (200, 200, 200)  # 연한 회색

# 화면 크기 정의
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700

# 게임 초기화
pygame.init()
font = pygame.font.SysFont(None, 36)

# 보드 상태 초기화 (0: 빈칸, 1: 흑돌, 2: 백돌)
board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
turn = 1  # 1: 흑돌, 2: 백돌

def draw_board(screen):
    offset_x = (SCREEN_WIDTH - BOARD_WIDTH) // 2
    offset_y = (SCREEN_HEIGHT - BOARD_HEIGHT) // 2

    # 보드의 모든 가로 선 그리기
    for row in range(BOARD_SIZE):
        start_pos = (offset_x, offset_y + row * CELL_SIZE)
        end_pos = (offset_x + (BOARD_SIZE - 1) * CELL_SIZE, offset_y + row * CELL_SIZE)
        pygame.draw.line(screen, BLACK, start_pos, end_pos)
    
    # 보드의 모든 세로 선 그리기
    for col in range(BOARD_SIZE):
        start_pos = (offset_x + col * CELL_SIZE, offset_y)
        end_pos = (offset_x + col * CELL_SIZE, offset_y + (BOARD_SIZE - 1) * CELL_SIZE)
        pygame.draw.line(screen, BLACK, start_pos, end_pos)

    # 돌 그리기
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 1:
                pygame.draw.circle(screen, BLACK, (offset_x + col * CELL_SIZE, offset_y + row * CELL_SIZE), CELL_SIZE // 2 - 2)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, WHITE, (offset_x + col * CELL_SIZE, offset_y + row * CELL_SIZE), CELL_SIZE // 2 - 2)

    # 마지막 가로 및 세로 선 그리기
    pygame.draw.line(screen, BLACK, (offset_x, offset_y + (BOARD_SIZE - 1) * CELL_SIZE), (offset_x + (BOARD_SIZE - 1) * CELL_SIZE, offset_y + (BOARD_SIZE - 1) * CELL_SIZE))
    pygame.draw.line(screen, BLACK, (offset_x + (BOARD_SIZE - 1) * CELL_SIZE, offset_y), (offset_x + (BOARD_SIZE - 1) * CELL_SIZE, offset_y + (BOARD_SIZE - 1) * CELL_SIZE))

def game2_page(screen, font, WHITE, BLACK):
    global turn
    while True:
        screen.fill(BACKGROUND_COLOR)
        
        home_button = create_home_button(screen, font, WHITE, BLACK)
        
        draw_board(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if home_button.collidepoint(event.pos):
                    return
                # 클릭한 위치에 돌 놓기
                mouse_x, mouse_y = event.pos
                offset_x = (SCREEN_WIDTH - BOARD_WIDTH) // 2
                offset_y = (SCREEN_HEIGHT - BOARD_HEIGHT) // 2
                if offset_x <= mouse_x < offset_x + BOARD_WIDTH and offset_y <= mouse_y < offset_y + BOARD_HEIGHT:
                    col = (mouse_x - offset_x + CELL_SIZE // 2) // CELL_SIZE
                    row = (mouse_y - offset_y + CELL_SIZE // 2) // CELL_SIZE
                    if board[row][col] == 0:
                        board[row][col] = turn
                        turn = 3 - turn  # 턴 변경 (1 <-> 2)

        pygame.display.flip()

def create_home_button(screen, font, WHITE, BLACK):
    text_surface = font.render("홈", True, BLACK)
    text_rect = text_surface.get_rect(topleft=(10, 10))
    pygame.draw.rect(screen, WHITE, text_rect)
    screen.blit(text_surface, text_rect)
    return text_rect

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)
