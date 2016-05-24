import pygame, sys, math, random
from settings import windowSize, windowWidth, windowHeight

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
