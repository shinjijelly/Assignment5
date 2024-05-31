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
# board_values = [ 
#     [0,0,0,2] , 
#     [0,0,2,2] , 
#     [0,2,0,0 ] ,
#     [2,2,2,2]]

game_over = False

score=0
file = open('high_score','r')
init_score = int(file.readline())
file.close()
high_score = init_score

def game3_page(screen, font, WHITE, BLACK):
    global board_values
    global score
    global high_score
    
    create= True
    create_count=0
    while True:
        screen.fill(color['bg'])

        home_button = create_home_button(screen, font, WHITE, BLACK)

        draw_board(screen)
        draw_block(screen)
        
        if(create or create_count < 2):              #처음 시작 시 블록 2개 생성
            board_values, game_over = create_block(board_values)
            create=False
            create_count+=1


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if home_button.collidepoint(event.pos):
                    return
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    board_values = move('UP', board_values)
                    create=True
                elif event.key == pygame.K_DOWN:
                    board_values = move('DOWN', board_values)
                    create=True
                elif event.key == pygame.K_RIGHT:
                    board_values = move('RIGHT', board_values)
                    create=True
                elif event.key == pygame.K_LEFT:
                    board_values = move('LEFT', board_values)
                    create=True
        
        if score > high_score:
            high_score = score

        pygame.display.flip()

# 보드 판을 그린다.
def draw_board(screen):
    pygame.draw.rect(screen,color['gamebg'],[250,200,400,400], 0,10)
    
    font = pygame.font.SysFont('arial',30)
    score_text = font.render(f'Score: {score}', True, 'black')
    high_score_text = font.render(f'High: {high_score}', True, 'black')
    screen.blit(score_text, (250, 120))
    screen.blit(high_score_text, (250, 150))
    pass

# 보드 판 안의 블록들을 그린다.
def draw_block(screen):
    for i in range(4):
        for j in range(4):
            value = board_values[i][j]              #  블록의 값
            block_color = color[value]              #  값에 맞는 색깔
            pygame.draw.rect(screen,block_color,[247 + j * 95 + 20, 197 + i * 95 + 20, 80, 80],0,10)    # 그리기
            if value > 0:
                font = pygame.font.SysFont('arial',30)
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
        print("꽉 참")
    return board, full

#블록을 움직임
def move(direction, board):
    global score
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
                        board[i][j + shift] = 0
                        merged[i][j + shift + 1] = True #연속적으로 합칠 수 없기 때문에 True로 만들어 줌


    return board

def create_home_button(screen, font, WHITE, BLACK):
    text_surface = font.render("홈", True, BLACK)
    text_rect = text_surface.get_rect(topleft=(10, 10))
    pygame.draw.rect(screen, WHITE, text_rect)
    screen.blit(text_surface, text_rect)
    return text_rect
