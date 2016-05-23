import pygame, sys, math, random

pygame.init()

windowSize = windowWidth, windowHeight = 640, 640
screen = pygame.display.set_mode(windowSize)
pygame.display.set_caption('fuck')

clock = pygame.time.Clock()

class Player:
    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy
    graphics = []
    graphics.append(pygame.transform.scale(pygame.image.load('tenryuu0.png'), (80, 80)))
    graphics.append(pygame.transform.scale(pygame.image.load('tenryuu1.png'), (80, 80)))
    posx = 0
    posy = windowHeight // 2 - 80
    animationCycle = 0
    def drawPlayer(self, screen):
        screen.blit(self.graphics[self.animationCycle // 8], (self.posx, self.posy))
        self.animationCycle += 1
        self.animationCycle = self.animationCycle % 16
player = Player(50, 280)

def loadResources():
    global waveSurface
    global tenryuuSurface0
    global tenryuuSurface1
    waveSurface = pygame.image.load('wave.png')

baseWaveSpeed = 2 
waveSpacing = 0.3
wavePositions = []
for i in range(64, windowHeight, 64):
    wavePositions.append([windowWidth, i])
    
def drawWaves(screen):
    for i in range(len(wavePositions)):
        wavePositions[i][0] -= (baseWaveSpeed * abs(wavePositions[i][1] - windowHeight/2 + 10)**0.3) 
        if wavePositions[i][0] < windowWidth - waveSpacing*(windowHeight - abs(wavePositions[i][1] - windowHeight/2)):
            wavePositions[i][0] = windowWidth
        for j in range(0, windowWidth, int(waveSpacing*(windowHeight - abs(wavePositions[i][1] - windowHeight/2)))):
            screen.blit(waveSurface, (wavePositions[i][0]-j, wavePositions[i][1]))


def gameLoop():
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        dtime = clock.tick(60)

        screen.fill(pygame.Color('#496ddb'))
        drawWaves(screen)
        player.drawPlayer(screen)

        pygame.display.flip()
        print(dtime)

loadResources()

gameLoop()
