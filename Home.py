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
font_path = "resources/mainFont.ttf"  # 폰트 파일 경로
font_path2 = "resources/mainFont2.ttf" 
font = pygame.font.Font(font_path, 36)
small_font = pygame.font.Font(font_path2, 22)  # 작은 글씨 폰트 추가

# 배경 이미지 로드 및 크기 조정
background_image = pygame.image.load('resources/mainimage.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

game1_image = pygame.image.load("resources/벽돌깨기.png")
game2_image = pygame.image.load("resources/오목.png")
game3_image = pygame.image.load("resources/2048.png")
game4_image = pygame.image.load("resources/테트리스.png")

# 버튼 생성 함수
def create_button(x, y, text, game_func, highlight=False):
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x, y))

    # 버튼의 크기를 조정
    button_rect = pygame.Rect(0, 0, 200, 50)
    button_rect.center = text_rect.center

    # 텍스트를 버튼의 중앙에 위치시키기 위해 보정
    text_rect.center = button_rect.center

    # If highlight is True, draw a semi-transparent overlay behind the button text
    if highlight:
        overlay = pygame.Surface((200, 50), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 200))  # Semi-transparent white
        screen.blit(overlay, button_rect)

    screen.blit(text_surface, text_rect)

    return text_rect, game_func

def create_button2(x, y, image_path, game_func, highlight=False):
    # Load the image
    image = image_path

    # Resize the image to fit the button size
    button_width, button_height = 200, 200  # Adjust the button size here
    image = pygame.transform.scale(image, (button_width, button_height))
    image_rect = image.get_rect(center=(x, y))

    # Blit the image onto the screen
    screen.blit(image, image_rect)

    return image_rect, game_func

def draw_multiline_text_box(surface, text, font, x, y, box_color, text_color, alpha=255):
    lines = text.split('\n')
    max_width = max(font.size(line)[0] for line in lines)
    total_height = sum(font.size(line)[1] for line in lines)

    text_surface = pygame.Surface((max_width + 20, total_height + 20), pygame.SRCALPHA)
    text_surface.fill((*box_color, alpha))

    y_offset = 10
    for line in lines:
        line_surface = font.render(line, True, text_color)
        text_surface.blit(line_surface, (10, y_offset))
        y_offset += font.size(line)[1]

    surface.blit(text_surface, (x - (max_width + 20) // 2, y - (total_height + 20) // 2))

def Instruction_text(game_type):
    if game_type == "Break":
        Instruction_text = (
                            "1. 좌우 방향키로 패들을 움직입니다.\n"
                            "2. 패들로 공을 부딪혀 벽돌을 모두 부수게 되면 다음 스테이지로 진출합니다.\n"
                            "3. 노란색 벽돌은 모두 두 번 부딪혀야 제거됩니다.\n"
                            "4. 공이 화면 밖으로 나가게 되면 게임이 종료됩니다.\n"
                            "5. 게임 종료 화면에서 스페이스바를 눌러 게임을 다시 시작할 수 있습니다.") 
    if game_type == "Omok":
        Instruction_text = (
                            "1. 두 명의 플레이어가 번갈아 가며 돌을 놓습니다.\n"
                            "2. 흑돌이 먼저 시작합니다.\n"
                            "3. 돌은 빈 칸에만 놓을 수 있습니다.\n"
                            "4. 마우스로 보드 위의 빈 칸을 클릭하여 돌을 놓습니다.\n"
                            "5. 먼저 가로, 세로, 대각선으로 5개의 돌을 연속으로 놓는 플레이어가 이깁니다.")
    if game_type == "Box":
        Instruction_text =  (
                            "1. 방향키로 타일을 이동시킵니다.\n"
                            "2. 같은 숫자의 타일이 충돌하면 합쳐집니다.\n"
                            "3. 방향키 이동 시 새로운 타일이 빈 칸에 나타납니다.\n"
                            "4. 격자가 꽉 차서 더 이상 이동할 수 없으면 게임은 종료됩니다.\n"
                            "5. 게임 종료 시 'S' 키를 눌러 게임을 다시 시작할 수 있습니다.")
    if game_type == "Tetris":
        Instruction_text =  (
                            "1. .\n"
                            "2. .\n"
                            "3. .\n"
                            "4. .\n"
                            "5. .")
    return Instruction_text

# 메인 페이지 루프
def main_page():
    game_started = False
    game_explain = False

    while True:
        # 배경 이미지 그리기
        screen.blit(background_image, (0, 0))

        if game_started:
            home_button = create_home_button(screen, font, WHITE, BLACK)

            # 버튼 생성 및 버튼 영역 및 실행 함수 저장
            B1, game1_func = create_button2(WIDTH // 3, HEIGHT // 4,game1_image, game1_page)
            B2, game2_func = create_button2(WIDTH // 3 + 300, HEIGHT // 4, game2_image, game2_page)
            B3, game3_func = create_button2(WIDTH // 3, HEIGHT // 4 + 300, game3_image, game3_page)
            B4, game4_func = create_button2(WIDTH // 3 + 300, HEIGHT // 4 + 300, game4_image, game4_page)

        else:
            if (game_explain):
                home_button = create_home_button(screen, font, WHITE, BLACK)

                Breakgame_button, Break_func = create_button(WIDTH // 3, HEIGHT // 4, "벽돌 깨기 게임", main_page, highlight=True)
                Omok_button, Omok_func = create_button(WIDTH // 3 + 300, HEIGHT // 4, "오목 게임", main_page, highlight=True)
                Box_button, Box_func = create_button(WIDTH // 3, HEIGHT // 4 + 300, "2048 게임", main_page, highlight=True)
                Tetris_button, Tetris_func = create_button(WIDTH // 3 + 300, HEIGHT // 4 + 300, "테트리스 게임", main_page, highlight=True)

                mouse_x, mouse_y = pygame.mouse.get_pos()
                if Breakgame_button.collidepoint(mouse_x,mouse_y):
                    instruction_text = Instruction_text("Break")
                    draw_multiline_text_box(screen, instruction_text, small_font, screen.get_width() // 2, screen.get_height() // 2, BLACK, WHITE, alpha=220)
                if Omok_button.collidepoint(mouse_x,mouse_y):
                    instruction_text = Instruction_text("Omok")
                    draw_multiline_text_box(screen, instruction_text, small_font, screen.get_width() // 2, screen.get_height() // 2, BLACK, WHITE, alpha=220)
                if Box_button.collidepoint(mouse_x,mouse_y):
                    instruction_text = Instruction_text("Box")
                    draw_multiline_text_box(screen, instruction_text, small_font, screen.get_width() // 2, screen.get_height() // 2, BLACK, WHITE, alpha=220)    
                if Tetris_button.collidepoint(mouse_x,mouse_y):
                    instruction_text = Instruction_text("Tetris")
                    draw_multiline_text_box(screen, instruction_text, small_font, screen.get_width() // 2, screen.get_height() // 2, BLACK, WHITE, alpha=220)

            else:
                # 텍스트 그리기 (크기 조정)
                title_font_size = 100  # Adjust the font size here
                title_font = pygame.font.Font(font_path, title_font_size)
                title_text = title_font.render("미니게임 모음.zip", True, BLACK)
                title_rect = title_text.get_rect(center=(WIDTH // 2, 100))  
                screen.blit(title_text, title_rect)

                start_button, game_func = create_button(WIDTH // 2, HEIGHT // 2 - 30, "게임 선택", main_page, highlight=True)
                explain_button, explain_func = create_button(WIDTH // 2, HEIGHT // 2 + 30, "게임 설명", main_page, highlight=True)

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if game_started:                                            # 게임 선택 버튼 누른 경우
                    if home_button.collidepoint(x,y):
                        game_started = False
                    if B1.collidepoint(x, y):
                        game1_page(screen, font, WHITE, BLACK)
                        game_started = False
                    elif B2.collidepoint(x, y):
                        game2_page(screen, font, small_font, WHITE, BLACK) 
                        game_started = False
                    elif B3.collidepoint(x, y):
                        game3_page(screen, font, WHITE, BLACK)
                        game_started = False
                    elif B4.collidepoint(x, y):
                        game4_page(screen, font, WHITE, BLACK)
                        game_started = False
                else:                                                       # 메인 화면 ( 게임 선택 전 )
                    if(game_explain):
                        if home_button.collidepoint(x,y):
                            game_explain = False
                    else:
                        if start_button.collidepoint(x, y):
                            game_started = True
                    if explain_button.collidepoint(x,y):
                        game_explain = True



        # 화면 업데이트
        pygame.display.flip()

# 화면 생성
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("미니게임 메인 페이지")

def create_home_button(screen, font, WHITE, BLACK):
    image = pygame.image.load("resources/HomeButton2.png")
    button_width, button_height = 50,50
    image = pygame.transform.scale(image, (button_width, button_height))
    image_rect = image.get_rect(topleft=(10, 10))
    screen.blit(image, image_rect)

    return image_rect

# 메인 페이지 실행
main_page()
