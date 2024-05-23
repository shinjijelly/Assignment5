import pygame
import sys
from game1 import game1_page
from game2 import game2_page
from game3 import game3_page
from game4 import game4_page

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Group 11 Assignment')


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    screen.fill((255, 255, 255))
   
    pygame.display.flip()

#종료
pygame.quit()
sys.exit()
