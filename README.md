# 미니게임 모음.zip

###### Requirements
![Laguage](https://img.shields.io/badge/python-3.12.3-blue.svg)
![Laguage](https://img.shields.io/badge/pygame-2.5.2-green.svg)


## 프로젝트 실행 방법

1. <https://github.com/shinjijelly/Assignment5> 
   
   위의 페이지의 프로젝트를 클론시킵니다.
2. CLI 환경에서 아래의 코드를 입력 해 주세요.

```
python -m pip install -r requirements.txt

python home.py
```

## 게임 실행 방법

### 1. 메인 페이지
<img src="https://github.com/soyun0904/Assignment5/raw/master/resources/mainscreen.png" alt="메인" width="500">

- 프로젝트 실행시 해당 화면을 볼 수 있습니다.
- 게임 선택을 클릭하여 총 4가지 게임을 플레이 할 수 있습니다.
- 각각의 선택 화면에 커서를 갖다대면 간략한 게임 설명을 볼 수 있습니다.


### 2. 벽돌깨기 게임
<img src="https://github.com/soyun0904/Assignment5/raw/master/resources/block_screen.png" alt="벽돌깨기" width="500">

- 좌우 방향키로 패들을 움직입니다.
- 패들로 공을 부딪혀 벽돌을 모두 부수게 되면 다음 스테이지로 진출합니다.
- 노란색 벽돌은 모두 두 번 부딪혀야 제거됩니다.
- 공이 화면 밖으로 나가게 되면 게임이 종료됩니다.
- 벽돌을 모두 부수면 다음 스테이지로 이동합니다.
- 게임 종료 후 다시 시작하고싶다면 ‘s’ 키를 누릅니다.


### 3. 오목 게임
<img src="https://github.com/soyun0904/Assignment5/raw/master/resources/omok_Screen.png" alt="오목" width="500">

- 두 명의 플레이어가 번갈아 가며 돌을 놓습니다.
- 흑돌이 먼저 시작합니다.
- 돌은 빈 칸에만 놓을 수 있습니다.
- 마우스로 보드 위의 빈 칸을 클릭하여 돌을 놓습니다.
- 먼저 가로, 세로, 대각선으로 5개의 돌을 연속으로 놓는 플레이어가 이깁니다.
- 게임 종료 후 다시 시작하고싶다면 ‘s’ 키를 누릅니다.


### 4. 2048 게임
<img src="https://github.com/soyun0904/Assignment5/raw/master/resources/2048_screen.png" alt="2048" width="500">

- 같은 숫자의 타일이 충돌하면 합쳐집니다.
- 방향키 이동 시 새로운 타일이 빈 칸에 나타납니다.
- 타일이 꽉 차서 더 이상 이동할 수 없으면 게임은 종료됩니다.
- 게임 종료 후 다시 시작하고싶다면 ‘s’ 키를 누릅니다.


### 5. 테트리스 게임
<img src="https://github.com/soyun0904/Assignment5/raw/master/resources/tetris_screen.png" alt="테트리스" width="500">

- 좌우 방향키를 이용하여 블록의 떨어지는 위치를 바꿀 수 있습니다.
- 위 방향키를 이용하여 블록을 회전시킬 수 있습니다.
- 아래 방향키를 이용하여 블록을 더 빠르게 낙하시킬 수 있습니다.
- 스페이스바를 누르면 블록이 바로 바닥으로 떨어집니다.
- 가로 한 줄이 가득 차면 해당 라인은 삭제됩니다.
- 점수 1000점 당 레벨이 증가합니다.
- 게임 종료 후 다시 시작하고싶다면 ‘s’ 키를 누릅니다.