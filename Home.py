import pygame
import sys
from game1 import game1_page
from game2 import game2_page
from game3 import game3_page
from game4 import game4_page

# 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 900, 700

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 폰트 설정 (경로를 시스템에 맞게 조정)
font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows의 경우
font = pygame.font.Font(font_path, 36)
small_font = pygame.font.Font(font_path, 24)  # 작은 글씨 폰트 추가

# 버튼 생성 함수
def create_button(x, y, text, game_func):
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x, y))
    pygame.draw.rect(screen, WHITE, text_rect)
    screen.blit(text_surface, text_rect)
    return text_rect, game_func

# 메인 페이지 루프
def main_page():
    while True:
        # 화면을 흰색으로 채우기
        screen.fill(WHITE)
        
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if B1.collidepoint(x, y):
                    game1_page(screen, font, WHITE, BLACK)
                elif B2.collidepoint(x, y):
                    game2_page(screen, font, small_font, WHITE, BLACK)  # 작은 글씨 폰트 추가
                elif B3.collidepoint(x, y):
                    game3_page(screen, font, WHITE, BLACK)
                elif B4.collidepoint(x, y):
                    game4_page(screen, font, WHITE, BLACK)

        # 버튼 생성 및 버튼 영역 및 실행 함수 저장
        B1, game1_func = create_button(WIDTH // 2, HEIGHT // 4, "게임1", game1_page)
        B2, game2_func = create_button(WIDTH // 2, HEIGHT // 4 + 100, "게임2", game2_page)
        B3, game3_func = create_button(WIDTH // 2, HEIGHT // 4 + 200, "게임3", game3_page)
        B4, game4_func = create_button(WIDTH // 2, HEIGHT // 4 + 300, "게임4", game4_page)

        # 화면 업데이트
        pygame.display.flip()

# 화면 생성
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("미니게임 메인 페이지")

# 메인 페이지 실행
main_page()
