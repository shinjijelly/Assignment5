import pygame
import sys
import random

# 2048 게임 color 모음
color = {0: (180,180,180),
         2: (238,218,218),
         4: (235,225,205),
         8: (240,180,120),
         16: (245,150,100),
         32: (246,125,95),
         64: (246,95,60),
         128: (237,208,114),
         256: (240,225,100),
         512: (243,180,80),
         1024: (200,220,230),
         2048: (100,220,230),
         'bg': (250,248,239),
         'gamebg': (200,200,200)}


# 보드 판의 숫자
board_values = [ [0 for i in range(4)] for i in range(4)] 

score=0
file = open('resources/high_score','r')
init_score = int(file.readline())
file.close()
high_score = init_score

def game3_page(screen, font, WHITE, BLACK):
    pygame.display.set_caption("2048 게임")
    global board_values
    global score
    global high_score
    global init_score

    create= True
    create_count=0
    title = pygame.font.SysFont("resources/mainFont2.ttf" , 100,True)
    title_text = title.render("2048",True,(119,110,101))
    game_over = False
    game_clear = False
    board_values = [ [0 for i in range(4)] for i in range(4)]   
    score=0
    
    while True:
        screen.fill(color['bg'])

        home_button = create_home_button(screen, font, WHITE, BLACK)
        
        screen.blit(title_text, (360,0))            
        
        draw_board(screen)                          #보드 판을 그림
        draw_block(screen)                          #블록을 그림
        
        if(create or create_count < 2):              #처음 시작 시 블록 2개 생성
            board_values, game_over = create_block(board_values)
            create=False
            create_count+=1
        
        if game_over or game_clear:
            draw_over(screen, game_clear, game_over)
            if high_score > init_score:             #최고점 갱신했으면 업데이트
                file = open('resources/high_score', 'w')
                file.write(f'{high_score}')
                file.close()
                init_score=high_score


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if home_button.collidepoint(event.pos):
                    pygame.display.set_caption("미니게임 모음.zip")
                    return
            elif event.type == pygame.KEYUP:
                if game_over or game_clear:         # 게임 오버된 경우
                    if event.key == pygame.K_s:        # S 누르면 start
                        board_values = [ [0 for i in range(4)] for i in range(4)]   #초기화
                        create=True
                        create_count=0
                        score=0
                        game_over=False
                        game_clear=False
                else:
                    if event.key == pygame.K_UP:
                        board_values, game_clear  = move('UP', board_values)
                        create=True
                    elif event.key == pygame.K_DOWN:
                        board_values, game_clear = move('DOWN', board_values)
                        create=True
                    elif event.key == pygame.K_RIGHT:
                        board_values, game_clear = move('RIGHT', board_values)
                        create=True
                    elif event.key == pygame.K_LEFT:
                        board_values, game_clear = move('LEFT', board_values)
                        create=True

                

        if score > high_score:
            high_score = score

        pygame.display.flip()

# 보드 판을 그린다.
def draw_board(screen):

    pygame.draw.rect(screen,color['gamebg'],[250,200,400,400], 0,10)
    
    font = pygame.font.Font("resources/mainFont2.ttf" ,25)

    score_text = font.render(f'Score: {score}', True, 'black')
    high_score_text = font.render(f'High: {high_score}', True, 'black')
    help_text1 = font.render('조작방법 : 방향키', True, 'black')
    help_text2 = font.render('2048 만들면 승리!', True, 'black')
    help_text3 = font.render('보드 판이 꽉 차고', True, 'black')
    help_text4 = font.render('못 움직이면 패배!', True, 'black')

    screen.blit(score_text, (250, 120))
    screen.blit(high_score_text, (250, 150))
    screen.blit(help_text1, (20, 250))
    screen.blit(help_text2, (20, 300))
    screen.blit(help_text3, (20, 350))
    screen.blit(help_text4, (20, 400))

# 보드 판 안의 블록들을 그린다.
def draw_block(screen):
    for i in range(4):
        for j in range(4):
            value = board_values[i][j]              #  블록의 값
            block_color = color[value]              #  값에 맞는 색깔
            pygame.draw.rect(screen,block_color,[247 + j * 95 + 20, 197 + i * 95 + 20, 80, 80],0,10)    # 그리기
            if value > 0:
                font = pygame.font.SysFont("resources/mainFont2.ttf" ,30)
                value_text = font.render(str(value),True, 'black')
                text_rect = value_text.get_rect(center=(249 + j * 95 + 59, 198 + i * 95 + 57))          # 숫자 
                screen.blit(value_text,text_rect)
                pygame.draw.rect(screen, 'black', [247+ j * 95 + 20, 197+ i * 95 + 20, 80, 80], 2, 10)  # 검은 색 테두리 입히기
                
#블록을 생성
def create_block(board):
    full= True                              #꽉 찼으면
    empty_list = []
    for col in range(4):
        for row in range(4):
            if board[col][row] == 0:        #보드 판에 비어있는 곳이 있으면
                full=False
                empty_list.append([col,row])

    if not full:                            
        idx= random.randint(0,len(empty_list)-1)  #비어있는 곳 중 랜덤한 위치에 생성
        y,x = empty_list[idx]
        if random.randint(1,4) == 4:            #25% 확률로 4 등장
            board[y][x]=4
        else:
            board[y][x]=2
    if full:
        if check_board(board):
            return board, full
        
        full=False
    
    return board, full

def check_board(board):

    # 위로 합칠 수 있는 블록이 있는지
    for col in range(1,4):
        for row in range(4):
            if board[col][row] == board[col-1][row]:
                return False
    
    # 아래로 합칠 수 있는 블록이 있는지
    for col in range(2,-1,-1):
        for row in range(4):
            if board[col][row] == board[col+1][row]:
                return False
    
    # 왼쪽로 합칠 수 있는 블록이 있는지
    for col in range(4):
        for row in range(1,4):
            if board[col][row] == board[col][row-1]:
                return False
    
    # 오른쪽로 합칠 수 있는 블록이 있는지
    for col in range(4):
        for row in range(2,-1,-1):
            if board[col][row] == board[col][row+1]:
                return False

    return True

#블록을 움직임
def move(direction, board):
    global score
    clear = False

    merged = [[False for i in range(4)] for i in range(4)]
    if direction == 'UP':
        for i in range(1,4):
            for j in range(4):
                shift = 0        
                for k in range(i):
                    if board[k][j]==0:      #위로 움직일 수 있는 공간이 있을 때
                        shift+=1   

                if shift > 0:
                    board[i - shift][j]=board[i][j]         # 움직일 수 있는 공간만큼 움직임
                    board[i][j]=0

                if i - shift - 1 >= 0:                      # 범위를 벗어 나지 않고
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift - 1][j] and not merged[i - shift][j]:    # 다 움직인 후에 위의 블록과 합칠 수 있으면 합침.
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]          #합친 수만큼 점수 획득
                        if board[i - shift - 1][j] == 2048:       # 2048을 만들면 승리
                            clear = True
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True         #연속적으로 합칠 수 없기 때문에 True로 만들어 줌
    
    elif direction == 'DOWN':
        for i in range(2,-1,-1):            
            for j in range(4):
                shift = 0
                for k in range(3-i):
                    if board[3 - k][j] == 0:            #아래로 움직일 수 있는 공간이 있을 때
                        shift+=1

                if shift > 0:
                    board[i + shift][j] = board[i][j]   # 움직일 수 있는 공간만큼 움직임
                    board[i][j] = 0

                if i + shift + 1 <=3:                   # 범위를 벗어 나지 않고
                     if board[i + shift][j] == board[i + shift + 1][j] and not merged[i + shift + 1][j] and not merged[i + shift][j]:      #  다 움직인 후에 위의 블록과 합칠 수 있으면 합침.
                        board[i + shift + 1][j] *= 2
                        score += board[i + shift + 1][j]          #합친 수만큼 점수 획득
                        if board[i + shift + 1][j] == 2048:       # 2048을 만들면 승리
                            clear = True
                        board[i + shift][j] = 0
                        merged[i + shift + 1][j] = True #연속적으로 합칠 수 없기 때문에 True로 만들어 줌
    
    elif direction == 'LEFT':
        for i in range(4):
            for j in range(1,4):
                shift = 0
                for k in range(j):
                    if board[i][k] == 0:                #왼쪽으로 움직일 수 있는 공간이 있을 때
                        shift += 1

                if shift > 0:
                    board[i][j - shift] = board[i][j]   # 움직일 수 있는 공간만큼 움직임
                    board[i][j] = 0

                if j - shift - 1 >= 0:                  # 범위를 벗어 나지 않고
                    if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] and not merged[i][j - shift]:        #  다 움직인 후에 위의 블록과 합칠 수 있으면 합침.
                        board[i][j - shift - 1] *= 2
                        score += board[i][j - shift - 1]        #합친 수만큼 점수 획득
                        if board[i][j - shift - 1] == 2048:     # 2048을 만들면 승리
                            clear = True
                        board[i][j - shift] = 0
                        merged[i][j - shift - 1] = True #연속적으로 합칠 수 없기 때문에 True로 만들어 줌

    elif direction == 'RIGHT':
        for i in range(4):
            for j in range(2, -1, -1):       
                shift = 0
                for k in range(3- j):      
                    if board[i][3 - k] == 0:            #오른쪽으로 움직일 수 있는 공간이 있을 때
                        shift += 1

                if shift > 0:
                    board[i][j + shift] = board[i][j]   # 움직일 수 있는 공간만큼 움직임
                    board[i][j] = 0

                if j + shift + 1 <= 3:                  # 범위를 벗어 나지 않고
                    if board[i][j + shift + 1] == board[i][j + shift] and not merged[i][j + shift + 1] and not merged[i][j + shift]:        #  다 움직인 후에 위의 블록과 합칠 수 있으면 합침.
                        board[i][j + shift + 1] *= 2
                        score += board[i][j + shift + 1]        #합친 수만큼 점수 획득
                        if board[i][j + shift + 1] == 2048:     # 2048을 만들면 승리
                            clear = True
                        board[i][j + shift] = 0
                        merged[i][j + shift + 1] = True #연속적으로 합칠 수 없기 때문에 True로 만들어 줌

    return board, clear

def draw_over(screen, clear, over):                                  # 게임이 끝나면
    font_path = "resources/mainFont2.ttf" 
    font = pygame.font.Font(font_path, 28)
    pygame.draw.rect(screen, 'black', [300, 250, 320, 100], 0, 10)

    if clear:
        game_over_text1 = font.render('Game Clear!', True, 'white')
    elif over:
        game_over_text1 = font.render('Game Over!', True, 'white')

    game_over_text2 = font.render('Press S key to Restart', True, 'white')
    screen.blit(game_over_text1, (380, 265))
    screen.blit(game_over_text2, (310, 305))

def create_home_button(screen, font, WHITE, BLACK):
    image = pygame.image.load("resources/HomeButton2.png")
    button_width, button_height = 50,50
    image = pygame.transform.scale(image, (button_width, button_height))
    image_rect = image.get_rect(topleft=(10, 10))
    screen.blit(image, image_rect)

    return image_rect