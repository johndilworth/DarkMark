import pygame
import time
from  pyomxplayer import OMXPlayer

pygame.init()
pygame.mouse.set_visible(False)

screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)

screen.fill((0,0,0))

done = False

player = OMXPlayer('videos/stag.mp4', '-o local')
player.toggle_pause() 

while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				done = True
	time.sleep(0.01)

pygame.quit()

