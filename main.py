import pygame, sys, math, random

pygame.init()

windowSize = windowWidth, windowHeight = 640, 480
screen = pygame.display.set_mode(windowSize)
pygame.display.set_caption('fuck')

clock = pygame.time.Clock()


def loadResources():
    global waveSurface
    global tenryuuSurface0
    global tenryuuSurface1
    waveSurface = pygame.image.load('wave.png')
    tenryuuSurface0 = pygame.transform.scale(pygame.image.load('tenryuu0.png'), (80, 80))
    tenryuuSurface1 = pygame.transform.scale(pygame.image.load('tenryuu1.png'), (80, 80))

def drawWaves():
    for i in range(0, 10):
        waveX = random.randint(0, windowWidth)
        waveY = random.randint(0, windowHeight)
        screen.blit(waveSurface, (waveX, waveY))

tenryuuAnimationCycle = 0
def drawTenryuu(blitX, blitY):
    global tenryuuAnimationCycle
    if tenryuuAnimationCycle > 7:
        screen.blit(tenryuuSurface0, (blitX, blitY))
    if tenryuuAnimationCycle <= 7:
        screen.blit(tenryuuSurface1, (blitX, blitY))
    tenryuuAnimationCycle += 1
    tenryuuAnimationCycle = tenryuuAnimationCycle % 16

def gameLoop():
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        dtime = clock.tick(60)

        screen.fill(pygame.Color('#496ddb'))
        drawWaves()
        drawTenryuu(windowWidth/2, windowHeight/2)

        pygame.display.flip()
        print(dtime)

loadResources()

gameLoop()
