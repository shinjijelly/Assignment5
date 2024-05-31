import pygame
import sys
import random

# 2048 게임 color 모음
color = {0: (180, 180, 180),
         2: (238, 218, 218),
         4: (235, 225, 205),
         8: (240, 180, 120),
         16: (245, 150, 100),
         32: (246, 125, 95),
         64: (246, 95, 60),
         128: (237, 208, 114),
         256: (240, 225, 100),
         512: (243, 180, 80),
         1024: (200, 220, 230),
         2048: (100, 220, 230),
         'bg': (250, 248, 239),
         'gamebg': (200, 200, 200)}

# 보드 판의 숫자
# board_values = [ [1024 for i in range(4)] for i in range(4)] ]
board_values = [[2, 4, 8, 16], [32, 64, 128, 256], [512, 1024, 2048, 0], [0, 0, 0, 0]]


def game3_page(screen, font, WHITE, BLACK):
    while True:
        screen.fill(color['bg'])

        home_button = create_home_button(screen, font, WHITE, BLACK)

        draw_board(screen)
        draw_block(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if home_button.collidepoint(event.pos):
                    return
            elif event.type == pygame.KEYDOWN:
                pass
            elif event.type == pygame.KEYUP:
                pass

        pygame.display.flip()


# 보드 판을 그린다.
def draw_board(screen):
    pygame.draw.rect(screen, color['gamebg'], [250, 200, 400, 400], 0, 10)
    pass


# 보드 판 안의 블록들을 그린다.
def draw_block(screen):
    for i in range(4):
        for j in range(4):
            value = board_values[i][j]  # 블록의 값
            block_color = color[value]  # 값에 맞는 색깔
            pygame.draw.rect(screen, block_color, [247 + j * 95 + 20, 197 + i * 95 + 20, 80, 80], 0, 10)  # 그리기
            if value > 0:
                font = pygame.font.SysFont('arial', 30)
                value_text = font.render(str(value), True, 'black')
                text_rect = value_text.get_rect(center=(247 + j * 95 + 59, 198 + i * 95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'black', [247 + j * 95 + 20, 197 + i * 95 + 20, 80, 80], 2, 10)  # 검은 색 테두리 입히기


def create_home_button(screen, font, WHITE, BLACK):
    text_surface = font.render("홈", True, BLACK)
    text_rect = text_surface.get_rect(topleft=(10, 10))
    pygame.draw.rect(screen, WHITE, text_rect)
    screen.blit(text_surface, text_rect)
    return text_rect
