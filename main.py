import pygame, sys, math, random

pygame.init()

windowSize = windowWidth, windowHeight = 640, 640
screen = pygame.display.set_mode(windowSize)
pygame.display.set_caption('fuck') #TODO: change

clock = pygame.time.Clock()

class Player:
    def __init__(self, posx, posy, lives):
        self.posx = posx
        self.posy = posy
        self.lives = lives
    graphics = []
    graphics.append(pygame.transform.scale(pygame.image.load('tenryuu0.png'), (80, 80)))
    graphics.append(pygame.transform.scale(pygame.image.load('tenryuu1.png'), (80, 80)))
    animationCycle = 0
    def draw(self, screen): #this thing right here slows down the animation
        screen.blit(self.graphics[self.animationCycle // 8], (self.posx, self.posy))
        self.animationCycle += 1
        self.animationCycle = self.animationCycle % 16
    def checkProjectileCollisions(self, projectiles):
        for projectile in projectiles.projectiles: #check collisions with projectiles, projectiles.projectiles is actual array inside Projectiles class
            if (self.graphics[0].get_rect().move(self.posx, self.posy).inflate(-50, -20).colliderect(projectile.graphics[0].get_rect().move(projectile.posx, projectile.posy))) and (not projectile.isPlayers): #holy fuck
                self.lives -= 1
                print('player hit, ' + str(self.lives) + ' lives left')
                projectiles.projectiles.remove(projectile)
        

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
    def update(self, projectiles):
        for enemy in self.enemies:
            enemy.updatePosition()
            if enemy.posx < -80: #TODO: sprite sizes
                self.enemies.remove(enemy)
            for projectile in projectiles.projectiles: #check collisions with projectiles, projectiles.projectiles is actual array inside Projectiles class
                if (enemy.graphics[0].get_rect().move(enemy.posx, enemy.posy).inflate(-20, -20).colliderect(projectile.graphics[0].get_rect().move(projectile.posx, projectile.posy))) and projectile.isPlayers: #holy fuck
                    print('enemy hit')
                    self.enemies.remove(enemy)
                    projectiles.projectiles.remove(projectile)
    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)
    def checkAndSpawn(self):
        print(len(self.enemies))
        if len(self.enemies) <= 2:
            self.spawnWave()
    def spawnWave(self):
        key = random.randint(0, 4)
        if key == 0:
            self.spawnWave0()
        elif key == 1:
            self.spawnWave1()
        elif key == 2:
            self.spawnWave2()
        elif key == 3:
            self.spawnWave3()
        elif key == 4:
            self.spawnWave4()
    def spawnWave0(self): #TODO: add more variations
        for index in range(0, 6):
            self.addEnemy(windowWidth, index * (windowHeight - 80)/5, -2, 0)
    def spawnWave1(self):
        for index in range(0, 6):
            self.addEnemy(windowWidth, index * (windowHeight - 80)/5, -2, (index-3)*(-1))
    def spawnWave2(self):
        for index in range(0, 6):
            self.addEnemy(index*50 + windowWidth, index * (windowHeight - 80)/5, -2, (index-3)*(-1))
    def spawnWave3(self):
        for index in range(0, 6):
            self.addEnemy(index*50 + windowWidth, (windowHeight - 80)/2, -2, 0)
    def spawnWave4(self):
        for index in range(0, 6):
            self.addEnemy(index*50 + windowWidth, (windowHeight - 80)/2, -2, (index-3)*(-1))

class Projectile:
    def __init__(self, posx, posy, speedx, speedy, isPlayers):
        self.posx = posx
        self.posy = posy
        self.speedx = speedx
        self.speedy = speedy
        self.isPlayers = isPlayers
    graphics = []
    graphics.append(pygame.transform.scale(pygame.image.load('projectile.png'), (30, 7)))
    graphics.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('projectile.png'), (30, 7)), True, False))
    def draw(self, screen):
        if self.isPlayers:
            screen.blit(self.graphics[0], (self.posx, self.posy))
        else:
            screen.blit(self.graphics[1], (self.posx, self.posy))
    def updatePosition(self): #TODO: update this so it complies with sprite sizes
        self.posx += self.speedx
        self.posy += self.speedy

class Projectiles:
    projectiles = []
    def addProjectile(self, posx, posy, speedx, speedy, isPlayers):
        self.projectiles.append(Projectile(posx, posy, speedx, speedy, isPlayers))
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
waveSpacing = 0.3 #majic numbers
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
    player = Player(50, 280, 3)

    enemies = Enemies()
    enemies.spawnWave()

    projectiles = Projectiles()
    projectiles.addProjectile(640, 300, -5, 0, False)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        dtime = clock.tick(60)

        screen.fill(pygame.Color('#496ddb'))
        drawWaves(screen)

        player.checkProjectileCollisions(projectiles)
        player.draw(screen)

        projectiles.update()
        projectiles.draw(screen)

        enemies.update(projectiles) #checking for collisions happens here
        enemies.checkAndSpawn()
        enemies.draw(screen)

        pygame.display.flip()
        #print(1000 // dtime)

loadResources()

pygame.mixer.music.load('music.ogg') #kickass tunes
pygame.mixer.music.play(-1) #it irritates me atm

gameLoop()
