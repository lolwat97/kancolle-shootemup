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
    animationCycle = 0
    def draw(self, screen):
        screen.blit(self.graphics[self.animationCycle // 8], (self.posx, self.posy))
        self.animationCycle += 1
        self.animationCycle = self.animationCycle % 16

class Enemy:
    def __init__(self, posx, posy, speedx, speedy):
        self.posx = posx
        self.posy = posy
        self.speedx = speedx
        self.speedy = speedy
    graphics = []
    graphics.append(pygame.transform.scale(pygame.image.load('tenryuu0.png'), (80, 80))) #TODO: add graphics for enemies
    graphics.append(pygame.transform.scale(pygame.image.load('tenryuu1.png'), (80, 80)))
    animationCycle = 0
    def draw(self, screen):
        screen.blit(self.graphics[self.animationCycle // 8], (self.posx, self.posy))
        self.animationCycle += 1
        self.animationCycle = self.animationCycle % 16
    def updatePosition(self): #TODO: update this so it complies with sprite sizes
        self.posx += self.speedx
        self.posy += self.speedy
        if (self.posy > windowHeight - 80) or (self.posy < 0): #TODO: again, sprite sizes
            self.speedy = -self.speedy

class Enemies:
    enemies = []
    def addEnemy(self, posx, posy, speedx, speedy):
        self.enemies.append(Enemy(posx, posy, speedx, speedy))
    def update(self):
        for enemy in self.enemies:
            enemy.updatePosition()
            if enemy.posy < -80: #TODO: sprite sizes
                self.enemies.remove(enemy)
    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)

class Projectile:
    def __init__(self, posx, posy, speedx, speedy):
        self.posx = posx
        self.posy = posy
        self.speedx = speedx
        self.speedy = speedy
    graphics = []
    graphics.append(pygame.transform.scale(pygame.image.load('tenryuu0.png'), (80, 80)))
    def draw(self, screen):
        screen.blit(self.graphics[0], (self.posx, self.posy))
    def updatePosition(self): #TODO: update this so it complies with sprite sizes
        self.posx += self.speedx
        self.posy += self.speedy

class Projectiles:
    projectiles = []
    def addProjectile(self, posx, posy, speedx, speedy):
        self.projectiles.append(Projectile(posx, posy, speedx, speedy))
    def update(self):
        for projectile in self.projectiles:
            projectile.updatePosition()
            if projectile.posy < -80: #TODO: sprite sizes
                self.projectiles.remove(enemy)
    def draw(self, screen):
        for projectile in self.projectiles:
            projectile.draw(screen)

def loadResources():
    global waveSurface
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
    player = Player(50, 280)

    enemies = Enemies();
    enemies.addEnemy(560, 280, -1, 2)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        dtime = clock.tick(60)

        screen.fill(pygame.Color('#496ddb'))
        drawWaves(screen)
        player.draw(screen)

        enemies.update()
        enemies.draw(screen)

        pygame.display.flip()
        #print(1000 // dtime)

loadResources()

pygame.mixer.music.load('music.ogg')
pygame.mixer.music.play(-1)

gameLoop()
