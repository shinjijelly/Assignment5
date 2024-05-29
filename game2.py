import pygame
import pygame.gfxdraw
import sys

# 보드 크기와 셀 크기 정의
BOARD_SIZE = 19
CELL_SIZE = 30
BOARD_WIDTH = BOARD_SIZE * CELL_SIZE
BOARD_HEIGHT = BOARD_SIZE * CELL_SIZE

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (109, 41, 50)  # 빨간색
BACKGROUND_COLOR = (199, 183, 163)
BOARD_COLOR = (228, 197, 158)

# 보드 상태 초기화 (0: 빈칸, 1: 흑돌, 2: 백돌)
board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
turn = 1  # 1: 흑돌, 2: 백돌

# 그라데이션 배경 생성 함수
def draw_gradient_background(screen, start_color, end_color):
    for y in range(screen.get_height()):
        r = start_color[0] + (end_color[0] - start_color[0]) * y // screen.get_height()
        g = start_color[1] + (end_color[1] - start_color[1]) * y // screen.get_height()
        b = start_color[2] + (end_color[2] - start_color[2]) * y // screen.get_height()
        pygame.draw.line(screen, (r, g, b), (0, y), (screen.get_width(), y))

def draw_board(screen):
    offset_x = (screen.get_width() - BOARD_WIDTH) // 2
    offset_y = (screen.get_height() - BOARD_HEIGHT) // 2 + 30  # 보드를 조금 아래로 내림

    # 보드 색상 채우기
    pygame.draw.rect(screen, BOARD_COLOR, (offset_x, offset_y, BOARD_WIDTH, BOARD_HEIGHT))

    # 오른쪽과 아래쪽의 한 줄을 배경색으로 칠하기
    pygame.draw.rect(screen, BACKGROUND_COLOR, (offset_x + (BOARD_SIZE - 1) * CELL_SIZE, offset_y, CELL_SIZE, BOARD_HEIGHT))
    pygame.draw.rect(screen, BACKGROUND_COLOR, (offset_x, offset_y + (BOARD_SIZE - 1) * CELL_SIZE, BOARD_WIDTH, CELL_SIZE))

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
                draw_stone(screen, offset_x + col * CELL_SIZE, offset_y + row * CELL_SIZE, CELL_SIZE // 2 - 2, BLACK)
            elif board[row][col] == 2:
                draw_stone(screen, offset_x + col * CELL_SIZE, offset_y + row * CELL_SIZE, CELL_SIZE // 2 - 2, WHITE)

    # 마지막 가로 및 세로 선 그리기
    pygame.draw.line(screen, BLACK, (offset_x, offset_y + (BOARD_SIZE - 1) * CELL_SIZE), (offset_x + (BOARD_SIZE - 1) * CELL_SIZE, offset_y + (BOARD_SIZE - 1) * CELL_SIZE))
    pygame.draw.line(screen, BLACK, (offset_x + (BOARD_SIZE - 1) * CELL_SIZE, offset_y), (offset_x + (BOARD_SIZE - 1) * CELL_SIZE, offset_y + (BOARD_SIZE - 1) * CELL_SIZE))

def draw_stone(screen, x, y, radius, color):
    # 입체감을 주기 위해 돌에 음영 효과를 추가
    if color == BLACK:
        shadow_color = (50, 50, 50)
    else:
        shadow_color = (200, 200, 200)
    
    # 돌의 아래쪽에 음영을 추가
    pygame.gfxdraw.filled_circle(screen, x + 2, y + 2, radius, shadow_color)
    pygame.gfxdraw.aacircle(screen, x + 2, y + 2, radius, shadow_color)
    
    # 실제 돌 그리기
    pygame.gfxdraw.filled_circle(screen, x, y, radius, color)
    pygame.gfxdraw.aacircle(screen, x, y, radius, color)

def check_winner(board):
    # 승리 조건을 검사합니다.
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] != 0 and (
                check_line(board, row, col, 1, 0) or
                check_line(board, row, col, 0, 1) or
                check_line(board, row, col, 1, 1) or
                check_line(board, row, col, 1, -1)
            ):
                return board[row][col]
    return 0

def check_line(board, row, col, d_row, d_col):
    # 주어진 방향으로 5개의 돌이 일렬로 놓여 있는지 확인합니다.
    player = board[row][col]
    count = 0
    for i in range(5):
        r = row + i * d_row
        c = col + i * d_col
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
            count += 1
        else:
            break
    return count == 5

def game2_page(screen, font, WHITE, BLACK):
    global turn, board
    winner = 0
    while True:
        draw_gradient_background(screen, (255, 255, 255), BACKGROUND_COLOR)
        
        home_button = create_home_button(screen, font, WHITE, BLACK)
        
        draw_board(screen)
        
        if not winner:
            draw_text(f"Player {turn}'s Turn", font, BLACK, screen, screen.get_width() // 2, 50)
            winner = check_winner(board)
        
        if winner:
            draw_rounded_text_box(screen, f"Player {winner} Wins!", font, screen.get_width() // 2, screen.get_height() // 2, RED, WHITE)
            pygame.display.flip()
            waiting_for_restart = True
            while waiting_for_restart:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if home_button.collidepoint(event.pos):
                            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if home_button.collidepoint(event.pos):
                    return
                if not winner:
                    mouse_x, mouse_y = event.pos
                    offset_x = (screen.get_width() - BOARD_WIDTH) // 2
                    offset_y = (screen.get_height() - BOARD_HEIGHT) // 2 + 30
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
    pygame.draw.rect(screen, BLACK, text_rect, 2)  # 검정색 테두리 추가
    screen.blit(text_surface, text_rect)
    return text_rect

def draw_rounded_rect(surface, color, rect, radius):
    pygame.gfxdraw.aacircle(surface, rect.left + radius, rect.top + radius, radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.left + radius, rect.top + radius, radius, color)

    pygame.gfxdraw.aacircle(surface, rect.right - radius - 1, rect.top + radius, radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right - radius - 1, rect.top + radius, radius, color)

    pygame.gfxdraw.aacircle(surface, rect.left + radius, rect.bottom - radius - 1, radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.left + radius, rect.bottom - radius - 1, radius, color)

    pygame.gfxdraw.aacircle(surface, rect.right - radius - 1, rect.bottom - radius - 1, radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right - radius - 1, rect.bottom - radius - 1, radius, color)

    pygame.draw.rect(surface, color, (rect.left + radius, rect.top, rect.width - 2 * radius, rect.height))
    pygame.draw.rect(surface, color, (rect.left, rect.top + radius, rect.width, rect.height - 2 * radius))

def draw_rounded_text_box(surface, text, font, x, y, box_color, text_color):
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x, y))
    background_rect = text_rect.inflate(40, 20)
    draw_rounded_rect(surface, box_color, background_rect, 20)
    pygame.draw.rect(surface, BLACK, background_rect, 2, border_radius=20)
    surface.blit(text_surface, text_rect)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

# 메인 페이지 실행
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((900, 700))
    pygame.display.set_caption("오목 게임")
    font_path = "C:/Windows/Fonts/arial.ttf"  # Windows의 경우
    font = pygame.font.Font(font_path, 36)
    game2_page(screen, font, WHITE, BLACK)
