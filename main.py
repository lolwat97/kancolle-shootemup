#!/usr/bin/env python3

import pygame, sys, math, random
from classes import Player, Enemy, Enemies, Projectile, Projectiles
from settings import windowSize, windowWidth, windowHeight

pygame.init()

screen = pygame.display.set_mode(windowSize)
pygame.display.set_caption('fuck') #TODO: change

clock = pygame.time.Clock()

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

def processInput(pressed, player, projectiles, autofireTimer):
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
    return autofireTimer

def drawInterface(screen, player, enemies, moon):
    screen.fill(pygame.Color('#496ddb'))
    drawWaves(screen)
    drawGrass(screen)
    drawHealth(screen, player.lives, moon)
    drawScore(screen, enemies.score, moon)

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
        dtime = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        pressed = pygame.key.get_pressed()
        autofireTimer = processInput(pressed, player, projectiles, autofireTimer)
        
        if player.posx < 0:
            player.posx = 0
        elif player.posx > windowWidth - 80:
            player.posx = windowWidth - 80
        if player.posy > windowHeight - 70:
            player.posy = windowHeight - 70
        elif player.posy < 0:
            player.posy = 0
            
        player.checkCollisions(projectiles, enemies)
        projectiles.update()
        enemyFireTimer += 1
        enemies.update(projectiles) #checking for collisions happens here
        enemies.checkAndSpawn()
        enemies.checkAndFire(projectiles, player.posx, player.posy, enemyFireTimer)

        if player.lives <= 0:
            break

        drawInterface(screen, player, enemies, moon)

        player.draw(screen)

        projectiles.draw(screen)

        enemies.draw(screen)

        pygame.display.flip()
        1000 // dtime

loadResources()

pygame.mixer.music.load('music.ogg') #kickass tunes

gameLoop()

gameover = pygame.font.Font(pygame.font.match_font('moon'), 64)
screen.blit(gameover.render('GAME OVER', True, pygame.Color('#aa3333')), (windowWidth/2 - 190, windowHeight/2 - 30))
pygame.display.flip()
pygame.time.wait(3000)
sys.exit()
