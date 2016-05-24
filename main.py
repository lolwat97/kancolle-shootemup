#!/usr/bin/env python3

import pygame, sys, math, random

pygame.init()

windowSize = windowWidth, windowHeight = 1280, 640
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
    def checkCollisions(self, projectiles, enemies):
        self.checkProjectileCollisions(projectiles)
        self.checkEnemyCollisions(enemies)
    def checkProjectileCollisions(self, projectiles):
        for projectile in projectiles.projectiles: #check collisions with projectiles, projectiles.projectiles is actual array inside Projectiles class
            if (self.graphics[0].get_rect().move(self.posx, self.posy).inflate(-50, -20).colliderect(projectile.graphics[0].get_rect().move(projectile.posx, projectile.posy))) and (not projectile.isPlayers): #holy fuck
                self.lives -= 1
                projectiles.projectiles.remove(projectile)
    def checkEnemyCollisions(self, enemies):
        for enemy in enemies.enemies: #check collisions with projectiles, projectiles.projectiles is actual array inside Projectiles class
            if self.graphics[0].get_rect().move(self.posx, self.posy).inflate(-50, -20).colliderect(enemy.graphics[0].get_rect().move(enemy.posx, enemy.posy)): #holy fuck
                self.lives -= 3
                enemies.enemies.remove(enemy)
        
class Enemy:
    def __init__(self, posx, posy, speedx, speedy):
        self.posx = posx
        self.posy = posy
        self.speedx = speedx
        self.speedy = speedy
    graphics = []
    graphics.append(pygame.transform.scale(pygame.image.load('enemy0.png'), (80, 80))) #TODO: add graphics for enemies
    graphics.append(pygame.transform.scale(pygame.image.load('enemy1.png'), (80, 80)))
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
    def fireProjectile(self, projectiles, tox, toy):
        dx = tox - self.posx
        dy = toy - self.posy
        length = math.sqrt(dx**2 + dy**2)
        firex = dx / length * 10
        firey = dy / length * 10
        projectiles.addProjectile(self.posx + 40, self.posy + 40, firex, firey, False)

class Enemies:
    score = 0
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
                    try:
                        self.enemies.remove(enemy)
                        projectiles.projectiles.remove(projectile)
                        self.score += 10
                    except:
                        pass
    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)
    def checkAndSpawn(self):
        if len(self.enemies) <= 2:
            self.spawnWave()
    def checkAndFire(self, projectiles, tox, toy, fireTimer):
        for index in range(len(self.enemies)):
            if fireTimer % 60 == index * 3:
                self.enemies[index].fireProjectile(projectiles, tox, toy)
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
    graphics.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('projectile_enemy.png'), (30, 7)), True, False))
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
            if projectile.posx < -80 or projectile.posx > windowWidth+200 or projectile.posy < 60 or projectile.posy > windowHeight: #TODO: sprite sizes
                self.projectiles.remove(projectile)
    def draw(self, screen):
        for projectile in self.projectiles:
            projectile.draw(screen)

def loadResources():
    global waveSurface
    global grassSurface
    waveSurface = pygame.image.load('wave.png')
    grassSurface = pygame.transform.scale(pygame.image.load('grass.png'), (40,40))

baseWaveSpeed = 2 
waveSpacing = 0.3 #majic numbers
wavePositions = []
for i in range(64, windowHeight, 64):
    wavePositions.append([windowWidth, i])
    
def drawWaves(screen):
    pygame.draw.rect(screen, pygame.Color('#5adbff'), (0, 0, windowWidth, 40))
    for i in range(len(wavePositions)):
        wavePositions[i][0] -= (baseWaveSpeed * abs(wavePositions[i][1] - windowHeight/2 + 10)**0.3) 
        if wavePositions[i][0] < windowWidth - waveSpacing*(windowHeight - abs(wavePositions[i][1] - windowHeight/2)):
            wavePositions[i][0] = windowWidth
        for j in range(0, windowWidth, int(waveSpacing*(windowHeight - abs(wavePositions[i][1] - windowHeight/2)))):
            screen.blit(waveSurface, (wavePositions[i][0]-j, wavePositions[i][1]))

grassOffset = 0
def drawGrass(screen):
    global grassOffset
    grassOffset -= 5
    if grassOffset < -40:
        grassOffset = 0
    for i in range(0, windowWidth+40, 40):
        screen.blit(grassSurface, (grassOffset + i, 20))

def drawHealth(screen, health, font):
    pygame.draw.rect(screen, pygame.Color('#ff5555'), (5, 5, health*2 + 5, 10))
    pygame.draw.rect(screen, pygame.Color('#ff0000'), (5, 5, 205, 10), 1)

def drawScore(screen, score, font):
    screen.blit(font.render(str(score), False, pygame.Color('#aa8888')), (windowWidth - 30, 2))

def gameLoop():
    player = Player(50, 280, 100)
    autofireTimer = 14
    enemyFireTimer = 0

    enemies = Enemies()
    enemies.spawnWave()

    projectiles = Projectiles()
    enemies.enemies[0].fireProjectile(projectiles, player.posx, player.posy)

    moon = pygame.font.Font(pygame.font.match_font('moon'), 16)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        pressed = pygame.key.get_pressed()
        
        if pressed[pygame.K_LEFT]:
            if pressed[pygame.K_DOWN]:
                player.posx -= 3.5
                player.posy += 3.5
            if pressed[pygame.K_UP]:
                player.posx -= 3.5
                player.posy -= 3.5
            if not (pressed[pygame.K_DOWN] or pressed[pygame.K_UP]):
                player.posx -= 5
        if pressed[pygame.K_RIGHT]:
            if pressed[pygame.K_DOWN] and not pressed[pygame.K_LEFT]:
                player.posx += 3.5
                player.posy += 3.5
            if pressed[pygame.K_UP] and not pressed[pygame.K_LEFT]:
                player.posx += 3.5
                player.posy -= 3.5
            if not (pressed[pygame.K_DOWN] or pressed[pygame.K_UP]):
                player.posx += 5
        if not (pressed[pygame.K_LEFT] or pressed[pygame.K_RIGHT]):
            if pressed[pygame.K_UP]:
                player.posy -= 5
            if pressed[pygame.K_DOWN]:
                player.posy += 5
        if not pressed[pygame.K_z]:
            autofireTimer = 14
        else:
            autofireTimer += 1
            if autofireTimer % 15 == 0:
                projectiles.addProjectile(player.posx + 50, player.posy + 69, 8, 0, True)

        if player.posx < 0:
            player.posx = 0
        elif player.posx > windowWidth - 80:
            player.posx = windowWidth - 80
        if player.posy > windowHeight - 70:
            player.posy = windowHeight - 70
        elif player.posy < 0:
            player.posy = 0
            

        dtime = clock.tick(60)

        screen.fill(pygame.Color('#496ddb'))
        drawWaves(screen)
        drawGrass(screen)
        drawHealth(screen, player.lives, moon)
        drawScore(screen, enemies.score, moon)
        if player.lives <= 0:
            break

        player.checkCollisions(projectiles, enemies)
        player.draw(screen)

        projectiles.update()
        projectiles.draw(screen)

        enemyFireTimer += 1
        enemies.update(projectiles) #checking for collisions happens here
        enemies.checkAndSpawn()
        enemies.checkAndFire(projectiles, player.posx, player.posy, enemyFireTimer)
        enemies.draw(screen)

        pygame.display.flip()
        #print(1000 // dtime)

loadResources()

pygame.mixer.music.load('music.ogg') #kickass tunes
pygame.mixer.music.play(-1) #it irritates me atm

gameLoop()

gameover = pygame.font.Font(pygame.font.match_font('moon'), 64)
screen.blit(gameover.render('GAME OVER', True, pygame.Color('#aa3333')), (windowWidth/2 - 190, windowHeight/2 - 30))
pygame.display.flip()
pygame.time.wait(3000)
sys.exit()
