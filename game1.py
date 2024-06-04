import pygame
import sys
import math

def game1_page(screen, font, WHITE, BLACK):
    pygame.display.set_caption("벽돌깨기 게임")

    collision_sound = pygame.mixer.Sound("resources/pingpong.mp3")
    break_sound = pygame.mixer.Sound("resources/break.mp3")
    next_sound = pygame.mixer.Sound("resources/next.mp3")

    # 색깔 정의
    BLUE = (0, 0, 255)
    YELLOW = (255,255,0)
    GREEN = (0,255,0)

    # 천장을 나타내는 사각형 생성
    ceiling_rect = pygame.Rect(0, 0, screen.get_width(), 50)
    black_line_rect = pygame.Rect(0, 50, screen.get_width(), 2)  # 검은색 줄

    class Paddle(pygame.sprite.Sprite):
        def __init__(self, image_path, width, height):
            super().__init__()
            self.image = pygame.image.load(image_path).convert_alpha()  # 이미지 로드
            self.image = pygame.transform.scale(self.image, (width, height))  # 이미지 크기 조정
            self.rect = self.image.get_rect()
            self.rect.x = (screen.get_width()- width) // 2
            self.rect.y = screen.get_width() - height - 10

        def move(self, pos):
            self.rect.x += pos[0]
            # 패들이 화면 내에 유지되도록 제한
            if self.rect.x < 0:
                self.rect.x = 0
            elif self.rect.x > screen.get_width() - self.rect.width:
                self.rect.x = screen.get_width() - self.rect.width

    class Wall(pygame.sprite.Sprite):
        def __init__(self, color, width, height):
            super().__init__()
            self.image = pygame.Surface([width, height])
            self.image.fill(color)
            self.rect = self.image.get_rect()

    class Brick(pygame.sprite.Sprite):
        def __init__(self, color, width, height):
            super().__init__()
            self.color = color
            self.image = self.create_image(color, width, height)
            self.rect = self.image.get_rect()

        def create_image(self, color, width, height):
            if color == YELLOW:
                image_path = "resources/yellowbrick.png"  # 노란색 벽돌 이미지 파일 경로
            elif color == GREEN:
                image_path = "resources/greenbrick.png"  # 초록색 벽돌 이미지 파일 경로
            else:
                image_path = None

            if image_path:
                image = pygame.image.load(image_path).convert_alpha()
                image = pygame.transform.scale(image, (width, height))
            else:
                # 기본 이미지 생성
                image = pygame.Surface([width, height])
                image.fill(color)
        
            return image

    import random
    class Ball(pygame.sprite.Sprite):
        def __init__(self, image_path, speed):
            super().__init__()
            self.image = pygame.image.load(image_path).convert_alpha()  # 이미지 로드
            self.image = pygame.transform.scale(self.image, (10, 10))  # 이미지 크기 조정
            self.rect = self.image.get_rect()
            self.speed_x = random.choice([-3, 3]) 
            self.speed_y = speed
            self.start()

        def update(self):
            # 공이 아래로 이동
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            # 공이 천장과 충돌하면 수직 속도를 반대로 변경
            if self.rect.top <= ceiling_rect.bottom:
                self.speed_y *= -1

             # 패들과 공의 충돌 여부 확인
            paddle_collided = pygame.sprite.spritecollide(paddle, [ball], False)
            if paddle_collided:
                collision_sound.play()
                # 패들과의 충돌을 수직/수평 충돌로 나눔
                if abs(self.rect.bottom - paddle.rect.top) < 10 and self.speed_y > 0:
                    # 공이 패들의 위쪽 면과 충돌
                    paddle_width = paddle.rect.width
                    paddle_x = paddle.rect.x
                    segment_width = paddle_width // 10
                    ball_x = self.rect.centerx

                    if ball_x < paddle_x + segment_width * 3:  # 3번째 세그먼트 이내에 부딪혔을 때
                        self.speed_x = -6
                    elif ball_x > paddle_x + segment_width * 7:  # 7번째 세그먼트 이상에 부딪혔을 때
                        self.speed_x = 6

                    # 공의 수직 속도를 반대로 변경하여 위로 향하도록 함
                    self.speed_y *= -1
                elif abs(self.rect.right - paddle.rect.left) < 10 and self.speed_x > 0:
                    # 공이 패들의 왼쪽 면과 충돌
                    self.rect.right = paddle.rect.left  # 충돌 후 위치 조정
                    self.speed_x *= -1
                elif abs(self.rect.left - paddle.rect.right) < 10 and self.speed_x < 0:
                    # 공이 패들의 오른쪽 면과 충돌
                    self.rect.left = paddle.rect.right  # 충돌 후 위치 조정
                    self.speed_x *= -1

            
            # 벽과 충돌
            if pygame.sprite.spritecollide(self, [left_wall, right_wall], False):
                self.speed_x *= -1  

            # 벽돌과 충돌
            hit_bricks = pygame.sprite.spritecollide(self, bricks_group, False)
            for brick in hit_bricks:
                break_sound.play()
                # 공이 벽돌의 어느 면과 충돌했는지 확인
                collision_tolerance = 10
                if abs(self.rect.right - brick.rect.left) < collision_tolerance and self.speed_x > 0:
                    self.speed_x *= -1  # 오른쪽 면 충돌
                if abs(self.rect.left - brick.rect.right) < collision_tolerance and self.speed_x < 0:
                    self.speed_x *= -1  # 왼쪽 면 충돌
                if abs(self.rect.bottom - brick.rect.top) < collision_tolerance and self.speed_y > 0:
                    self.speed_y *= -1  # 아래쪽 면 충돌
                if abs(self.rect.top - brick.rect.bottom) < collision_tolerance and self.speed_y < 0:
                    self.speed_y *= -1  # 위쪽 면 충돌

                if(brick.color == YELLOW):
                    brick.image = pygame.image.load("resources/greenbrick.png").convert_alpha()  # 초록색 벽돌 이미지로 변경
                    brick.color = GREEN
                    brick.image = pygame.transform.scale(brick.image, (brick.rect.width, brick.rect.height))
                    # 벽돌 이미지 업데이트
                    brick.rect = brick.image.get_rect(center=brick.rect.center)
                else:
                    bricks_group.remove(brick)

            # 공이 화면 밖으로 벗어나면 게임 오버
            if self.rect.top > screen.get_height():
                pygame.mixer.music.pause()
                pygame.mixer.music.load("resources/Gameover.ogg")
                pygame.mixer.music.play(-1)
                return True

        def start(self):
            # 공의 초기 위치 설정
            self.rect.centerx = paddle.rect.centerx
            self.rect.bottom = paddle.rect.top - 30

    # 벽 생성
    left_wall = Wall(BLACK, 100, screen.get_height() - 50)   # 왼쪽 벽
    right_wall = Wall(BLACK, 100, screen.get_height() - 50)  # 오른쪽 벽

    # 벽 위치 설정
    left_wall.rect.left = 0
    left_wall.rect.top = 50   # 천장 밑부터 시작
    right_wall.rect.right = screen.get_width()
    right_wall.rect.top = 50  # 천장 밑부터 시작  

    #paddle = Paddle(BLUE, 100, 10)
    paddle = Paddle("resources/paddle.png",100,15)

    # 패들의 초기 위치를 조정하여 좌우 벽 밖에 위치하도록 설정
    paddle.rect.centerx = screen.get_width() // 2  # 화면 가로 중앙
    paddle.rect.bottom = screen.get_height() - 10  # 화면 아래쪽에서 일정 거리

    # 게임1 페이지 내에서 공 객체 생성
    #ball = Ball((255, 0, 0), 5, 7)
    ball = Ball("resources/ball.png",7)

    game_start = False
    game_over = False
    
    initial_n = 3
    stage = 1

    bricks_group = pygame.sprite.Group()

    clock = pygame.time.Clock()

    def load_background_image(image_path, screen):
        background_image = pygame.image.load(image_path)
        background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))
        return background_image
    
    background_image = load_background_image("resources/background.jpg", screen)

    reset_text_blink = True  # 텍스트 깜빡임을 제어하기 위한 플래그

    is_muted = False

    while True:
        screen.fill(WHITE)

        screen.blit(background_image,(0,0))

        # 천장 그리기
        pygame.draw.rect(screen, BLACK, ceiling_rect)
        # 천장 경계면 그리기
        pygame.draw.rect(screen, BLACK, black_line_rect)

        # 벽 그리기
        screen.blit(left_wall.image, left_wall.rect)
        screen.blit(right_wall.image, right_wall.rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if home_button.collidepoint(event.pos):
                    pygame.mixer.music.pause()
                    pygame.display.set_caption("미니게임 모음.zip")
                    return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and game_over:  # 게임 오버 상태에서 s키가 눌린 경우
                    bricks_group.empty()
                    ball.start()
                    initial_n = 3
                    stage = 1
                    game_over = False
                    game_start = False
                    pygame.mixer.music.pause()
                    pygame.display.flip()
                if event.key == pygame.K_m:                    # mute all
                    is_muted = not is_muted
                    if(is_muted):
                        pygame.mixer.music.set_volume(0)
                        collision_sound.set_volume(0)
                        break_sound.set_volume(0)
                        next_sound.set_volume(0)
                    else:
                        pygame.mixer.music.set_volume(0.1)
                        collision_sound.set_volume(1)
                        break_sound.set_volume(1)
                        next_sound.set_volume(1)

                
        if len(bricks_group) == 0:
                if(game_start):
                    initial_n += 1
                    ball.start()
                    stage += 1
                    game_start = False
                    next_sound.play()
                    pygame.time.delay(1000)

                n = initial_n

                # 벽돌의 높이를 동적으로 계산
                max_brick_height = (screen.get_height() // 2 - ceiling_rect.height - 100) // n
                brick_width = (screen.get_width() - 200) // n - 10  # 동적으로 벽돌 너비 계산
                brick_height = max_brick_height
                brick_padding = 10

                total_brick_width = n * brick_width + (n - 1) * brick_padding
                start_x = (screen.get_width() - total_brick_width) // 2

                for row in range(n):
                    for column in range(n):
                        is_yellow = random.random() < 0.3  # 30% 확률로 노란색 벽돌 생성
                        if is_yellow:
                            brick_color = YELLOW
                        else:
                            brick_color = GREEN
                        brick = Brick(brick_color, brick_width, brick_height)
                        brick.rect.x = start_x + column * (brick_width + brick_padding)
                        brick.rect.y = row * (max_brick_height + brick_padding) + ceiling_rect.bottom + brick_padding
                        bricks_group.add(brick)

                game_start = True

        # 패들 그리기
        screen.blit(paddle.image, paddle.rect)

        screen.blit(ball.image, ball.rect)

        bricks_group.draw(screen)

        if not game_over:
            # 패들 이동
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle.rect.x -= 6
            if keys[pygame.K_RIGHT]:
                paddle.rect.x += 6

            # 패들이 벽과 충돌
            paddle.rect.x = max(100, min(paddle.rect.x, 800 - paddle.rect.width))

            # 공 업데이트 및 그리기
            if ball.update():
                game_over = True  # 게임 오버 상태로 전환

            # 남은 블럭 개수 + 스테이지
            text_remaining_bricks = font.render(f'남은 벽돌: {len(bricks_group)}', True, WHITE)
            text_remaining_bricks_rect = text_remaining_bricks.get_rect(center=(ceiling_rect.centerx, ceiling_rect.centery))
            screen.blit(text_remaining_bricks, text_remaining_bricks_rect)

            text_stage = font.render(f'스테이지: {stage}', True, WHITE)
            text_stage_rect = text_stage.get_rect(midright=(ceiling_rect.right - 10, ceiling_rect.centery))
            screen.blit(text_stage, text_stage_rect)    

        else:
            # 흐릿하게 보이는 오버레이
            overlay = pygame.Surface((screen.get_width(), screen.get_height()))
            overlay.set_alpha(128)  # 반투명 정도 설정 (0은 완전 투명, 255는 완전 불투명)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))

            # "Game Over" 메시지 표시
            game_over_text = font.render("Game Over", True, WHITE)
            game_over_rect = game_over_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(game_over_text, game_over_rect)

            # "Press spacebar to reset" 텍스트 표시
            if reset_text_blink:  # 깜빡임 플래그가 True일 때만 텍스트 표시
                reset_text = font.render("Press 's' to reset game", True, (255, 0, 0))  # 빨간색으로 렌더링
                reset_rect = reset_text.get_rect(center=(screen.get_width() // 2, game_over_rect.bottom + 20))
                screen.blit(reset_text, reset_rect)

            # 일정 시간마다 텍스트 깜빡임을 제어하는 플래그를 변경
            if pygame.time.get_ticks() % 1000 < 500:
                reset_text_blink = True
            else:
                reset_text_blink = False

        # 홈 버튼 그리기
        home_button = create_home_button(screen, font, WHITE, BLACK)

        pygame.display.flip()
        clock.tick(60)

def create_home_button(screen, font, WHITE, BLACK):
    image = pygame.image.load("resources/HomeButton2.png")
    button_width, button_height = 50,50
    image = pygame.transform.scale(image, (button_width, button_height))
    image_rect = image.get_rect(topleft=(10, 10))
    screen.blit(image, image_rect)

    return image_rect
