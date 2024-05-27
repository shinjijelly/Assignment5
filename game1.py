import pygame
import sys

def game1_page(screen, font, WHITE, BLACK):
    # 색깔 정의
    BLUE = (0, 0, 255)
    YELLOW = (255,255,0)
    GREEN = (0,255,0)

    # 천장을 나타내는 사각형 생성
    ceiling_rect = pygame.Rect(0, 0, screen.get_width(), 50)
    black_line_rect = pygame.Rect(0, 50, screen.get_width(), 2)  # 검은색 줄

    class Paddle(pygame.sprite.Sprite):
        def __init__(self, color, width, height):
            super().__init__()
            self.image = pygame.Surface([width, height])
            self.image.fill(WHITE)
            pygame.draw.rect(self.image, color, [0, 0, width, height])
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
            self.image = pygame.Surface([width, height])
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.color = color

    import random
    class Ball(pygame.sprite.Sprite):
        def __init__(self, color, radius, speed):
            super().__init__()
            self.image = pygame.Surface([2 * radius, 2 * radius], pygame.SRCALPHA)
            pygame.draw.circle(self.image, color, (radius, radius), radius)
            self.rect = self.image.get_rect()
            self.radius = radius
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
                # 패들의 너비를 10개의 영역으로 나누고, 공이 부딪힌 위치에 따라 수평 속도 조절
                paddle_width = paddle.rect.width
                paddle_x = paddle.rect.x
                segment_width = paddle_width // 10
                ball_x = self.rect.centerx

                if ball_x < paddle_x + segment_width * 3:  # 3번째 세그먼트 이내에 부딪혔을 때
                    self.speed_x = -5
                elif ball_x > paddle_x + segment_width * 7:  # 7번째 세그먼트 이상에 부딪혔을 때
                    self.speed_x = 5

                # 공의 수직 속도를 반대로 변경하여 위로 향하도록 함
                self.speed_y *= -1

            # 벽과 충돌
            if pygame.sprite.spritecollide(self, [left_wall, right_wall], False):
                self.speed_x *= -1  

            # 벽돌과 충돌
            hit_bricks = pygame.sprite.spritecollide(self, bricks_group, False)
            for brick in hit_bricks:
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
                    brick.image.fill(GREEN)
                    brick.color = GREEN
                    continue
                
                bricks_group.remove(brick)

            # 공이 화면 밖으로 벗어나면 게임 오버
            if self.rect.top > screen.get_height():
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

    paddle = Paddle(BLUE, 100, 10)
    # 패들의 초기 위치를 조정하여 좌우 벽 밖에 위치하도록 설정
    paddle.rect.centerx = screen.get_width() // 2  # 화면 가로 중앙
    paddle.rect.bottom = screen.get_height() - 10  # 화면 아래쪽에서 일정 거리

    # 게임1 페이지 내에서 공 객체 생성
    ball = Ball((255, 0, 0), 5, 7)

    game_start = False
    
    initial_n = 3
    stage = 1
    #hit_limit = 1

    bricks_group = pygame.sprite.Group()

    clock = pygame.time.Clock()

    while True:
        screen.fill(WHITE)

        # 천장 그리기
        pygame.draw.rect(screen, WHITE, ceiling_rect)
        # 천장 경계면 그리기
        pygame.draw.rect(screen, BLACK, black_line_rect)

        # 벽 그리기
        screen.blit(left_wall.image, left_wall.rect)
        screen.blit(right_wall.image, right_wall.rect)

        # 패들 이동
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.rect.x -= 6  
        if keys[pygame.K_RIGHT]:
            paddle.rect.x += 6  

        # 패들이 벽과 충돌
        paddle.rect.x = max(100, min(paddle.rect.x, 800 - paddle.rect.width))

        # 패들 그리기
        screen.blit(paddle.image, paddle.rect)

        # 공 업데이트 및 그리기
        if ball.update():
            return
        screen.blit(ball.image, ball.rect)

        bricks_group.draw(screen)

        if len(bricks_group) == 0:
            if(game_start):
                initial_n += 1
                ball.start()
                stage += 1
                game_start = False
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

        # 홈 버튼 그리기
        home_button = create_home_button(screen, font, WHITE, BLACK)

        # 남은 블럭 개수 + 스테이지
        text_remaining_bricks = font.render(f'남은 벽돌: {len(bricks_group)}', True, BLACK)
        text_remaining_bricks_rect = text_remaining_bricks.get_rect(center=(ceiling_rect.centerx, ceiling_rect.centery))
        screen.blit(text_remaining_bricks, text_remaining_bricks_rect)

        text_stage = font.render(f'스테이지: {stage}', True, BLACK)
        text_stage_rect = text_stage.get_rect(midright=(ceiling_rect.right - 10, ceiling_rect.centery))
        screen.blit(text_stage, text_stage_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if home_button.collidepoint(event.pos):
                    return

        pygame.display.flip()
        clock.tick(60)

def create_home_button(screen, font, WHITE, BLACK):
    text_surface = font.render("홈", True, BLACK)
    text_rect = text_surface.get_rect(topleft=(5, 1))
    pygame.draw.rect(screen, WHITE, text_rect)
    screen.blit(text_surface, text_rect)
    return text_rect