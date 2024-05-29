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
LIGHT_GRAY = (211, 211, 211)

# 화면 크기 정의
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700

# 게임 초기화
pygame.init()
font = pygame.font.SysFont(None, 36)

def draw_board(screen):
    offset_x = (SCREEN_WIDTH - BOARD_WIDTH) // 2
    offset_y = (SCREEN_HEIGHT - BOARD_HEIGHT) // 2
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            rect = pygame.Rect(offset_x + col * CELL_SIZE, offset_y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, LIGHT_GRAY, rect, 1)

def game2_page(screen, font, WHITE, BLACK):
    while True:
        screen.fill(WHITE)
        
        home_button = create_home_button(screen, font, WHITE, BLACK)
        
    
        draw_board(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if home_button.collidepoint(event.pos):
                    return

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
