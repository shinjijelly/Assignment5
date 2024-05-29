import pygame
import sys
import random
import time as t
import os

def game4_page(screen, font, WHITE, BLACK):
    pygame.init()
    FPS = 60

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (188, 0, 0)

    leftMouseHit = 1  # 왼쪽 마우스 클릭 확인 작업.
    pygame.display.set_caption('Whack A Mole')

    # HIT, MISS, LEVEL 정보 카운터를 생성하는 과정.
    scoreCounter = 0
    missCounter = 0
    levelCounter = 1

    frame = pygame.display.set_mode((900, 700), 0, 32)
    game_font = pygame.font.SysFont('Hursheys', 50)
    background = pygame.image.load(os.path.join("Molegame", "background.png"))

    # "mole.png" 이미지 로드
    mole_image = pygame.image.load(os.path.join("Molegame", "mole.png"))

    # 두더지 구멍의 위치를 지정하고 리스트에 저장하는 과정.
    holes = [
        (50, 108), (50, 308), (50, 508),
        (280, 108), (280, 308), (280, 508),
        (510, 108), (510, 308), (510, 508)
    ]

    def setup_background_with_holes():
        frame.blit(background, (0, 0))
        for hole in holes:
            pygame.draw.circle(frame, BLACK, (hole[0] + 70, hole[1] + 70), 85, 0)
        pygame.display.update()

    def lvlUpUpdate(initInterval):
        currentInterval = initInterval - levelCounter * 0.13
        return max(currentInterval, 0.05)

    def lvlInfo():
        return 1 + int(scoreCounter / 4)

    def showhammer():
        image3 = pygame.image.load(os.path.join("Molegame", "hammer.png"))
        x, y = pygame.mouse.get_pos()
        frame.blit(image3, [x - 20, y - 20])
        pygame.display.update()

    def moleHit(holePosition):
        x, y = pygame.mouse.get_pos()
        holeX, holeY = holePosition
        return holeX < x < holeX + 150 and holeY < y < holeY + 150

    def printStats():
        hitLabelTxt = game_font.render("HIT", True, WHITE)
        frame.blit(hitLabelTxt, [720, 25])
        scoreTxt = game_font.render(str(scoreCounter), True, WHITE)
        frame.blit(scoreTxt, [830, 25])

        missLabelTxt = game_font.render("MISS", True, WHITE)
        frame.blit(missLabelTxt, [720, 140])
        missTxt = game_font.render(str(missCounter), True, WHITE)
        frame.blit(missTxt, [830, 140])

        levelLabelTxt = game_font.render("LEVEL", True, WHITE)
        frame.blit(levelLabelTxt, [720, 248])
        lvlTxt = game_font.render(str(levelCounter), True, WHITE)
        frame.blit(lvlTxt, [830, 248])

        pygame.display.update()

    def ShutDownOrContinue(missNumber):
        if missNumber == 5:
            game_font_big = pygame.font.SysFont('Hursheys', 150)
            gameOverTxt = game_font_big.render("Game Over", True, RED)
            frame.blit(gameOverTxt, [100, 375])
            pygame.display.update()
            t.sleep(3)
            pygame.quit()
            return True
        return False

    def initialValues():
        nonlocal scoreCounter, missCounter, levelCounter

        gameLoopTimer = 0  # 루프 시간 카운터
        animationNumber = 0  # 애니메이션 번호 초기화
        gameLoop = True
        isMoleDown = False  # 두더지가 내려갔는지 확인하는 변수
        plusInterval = 0.1  # 레벨이 올라갈 때 두더지가 더 빨리 나타나게 하는 변수
        initialInterval = 1  # 두더지가 나타나는 초기 간격
        holeNumber = 0  # 구멍 번호

        timer = pygame.time.Clock()

        while gameLoop:
            if ShutDownOrContinue(missCounter):
                return

            printStats()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == leftMouseHit:
                    if moleHit(holes[holeNumber]) and animationNumber > 0:
                        for i in range(150):
                            showhammer()
                        animationNumber = 3
                        isMoleDown = False
                        plusInterval = 0
                        scoreCounter += 1
                        levelCounter = lvlInfo()
                    else:
                        missCounter += 1
                        for i in range(150):
                            showhammer()

            if animationNumber == 0:
                setup_background_with_holes()
                isMoleDown = False
                plusInterval = 0.5
                holeNumber = random.randint(0, len(holes) - 1)

            mil = timer.tick(FPS)
            sec = mil / 1000.0
            gameLoopTimer += sec

            if animationNumber > 5:
                setup_background_with_holes()
                animationNumber = 0

            if gameLoopTimer > plusInterval:
                pic = mole_image
                setup_background_with_holes()
                frame.blit(pic, (holes[holeNumber][0] + 20, holes[holeNumber][1]))

                if not isMoleDown:
                    animationNumber += 1
                else:
                    animationNumber -= 1

                if animationNumber == 4:
                    plusInterval = 0.3
                elif animationNumber == 3:
                    animationNumber -= 1
                    isMoleDown = True
                    plusInterval = lvlUpUpdate(initialInterval)
                else:
                    plusInterval = 0.1
                gameLoopTimer = 0

            pygame.display.flip()

    while True:
        screen.fill(WHITE)
        
        home_button = create_home_button(screen, font, WHITE, BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if home_button.collidepoint(event.pos):
                    return

        pygame.display.flip()

        # 게임 실행
        initialValues()

def create_home_button(screen, font, WHITE, BLACK):
    text_surface = font.render("홈", True, BLACK)
    text_rect = text_surface.get_rect(topleft=(10, 10))
    pygame.draw.rect(screen, WHITE, text_rect)
    screen.blit(text_surface, text_rect)
    return text_rect

if __name__ == "__main__":
    main()
