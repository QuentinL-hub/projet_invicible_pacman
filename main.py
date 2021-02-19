import pygame, sys
from pygame.locals import *
import time
import random
import re
from map import Map
from end_window import *
def main():
	pygame.init()
 
# Assign FPS a value
	FPS = 30
	FramePerSec = pygame.time.Clock()
	 

	BLUE  = (0, 0, 255)
	RED   = (255, 0, 0)
	GREEN = (0, 255, 0)
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)

	BLOCK_SIZE = 30
	DISPLAYSURF = pygame.display.set_mode((1920,1080))
	pygame.display.set_caption("Impossible Pacman")
	M = Map()
	M.load_level(1)


	screen_rect = DISPLAYSURF.get_rect()
	window_rect = pygame.Rect(0, 0, 400, 250)
	window_rect.center = screen_rect.center
	font = pygame.font.SysFont('Arial', 24)
	message = 'Game Over'
	box = MessageBox(window_rect, font, message)
	while True:     
	    for event in pygame.event.get():              
	        if event.type == QUIT:
	            pygame.quit()
	            sys.exit()

	     
	    DISPLAYSURF.fill(BLACK)
	    su = M.update()
	    M.draw(DISPLAYSURF)

    # if(su == False):
    #   DISPLAYSURF.fill(BLACK)
    #   while True:
        
    #     box.update()
    #     DISPLAYSURF.fill(BLACK)
    #     if not box.should_exit:
    #       box.draw(DISPLAYSURF)

    #     pygame.display.update()
	    pygame.display.update()
	    FramePerSec.tick(FPS)


if __name__ == "__main__":
# execute only if run as a script
    main()