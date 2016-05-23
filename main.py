import pygame, sys, math

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('fuck')

clock = pygame.time.Clock()

while 1:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
    	sys.exit()
