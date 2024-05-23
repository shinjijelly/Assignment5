import pygame
import sys

def game2_page(screen, font, WHITE, BLACK):
    while True:
        screen.fill(WHITE)
        
        home_button = create_home_button(screen, font, WHITE, BLACK)
        
        # 오목 게임의 시작 화면 추가 (이 부분은 추후 구현 예정)
        draw_text("Omok Game Start Screen", font, BLACK, screen, 450, 350)
        
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
