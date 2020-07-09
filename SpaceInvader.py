import pygame, sys
from pygame import mixer
import math
from random import *
pygame.init()

win = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('alien.png')
space = pygame.image.load('background-black.png')
pygame.display.set_icon(icon)

# MUSIC
mixer.music.load('background.wav')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

click = False

def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        win.blit(space, (0, 0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255, 255, 255))
        win.blit(title_label, (800 / 2 - title_label.get_width() / 2, 250))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game()
    pygame.quit()

def game():
    # PLAYER
    playerImg = pygame.image.load('player2.png')
    playerX = 380
    playerY = 480
    playerX_change = 0

    def player(x, y):
        win.blit(playerImg, (x, y))

    # PLAYERHEALTH
    player_Health = 5
    Health_Text = pygame.font.SysFont('harrington.ttf', 36)

    def Health_Show(x, y, r, g, b):
        h = Health_Text.render("L I V E S : " + str(player_Health), True, (r, g, b), None)
        win.blit(h, (x, y))

    # SCORE
    score = 0
    score_text = pygame.font.SysFont('playbill.ttf', 32)

    def show_score(x, y):
        s = score_text.render("SCORE : " + str(score), True, (255, 255, 255), None)
        win.blit(s, (x, y))

    # GAME OVER
    game_over_text = pygame.font.SysFont('rage.ttf', 64)
    respawn_text = pygame.font.SysFont('palacescript.ttf', 48)

    def game_over():
        g = game_over_text.render("GAME OVER", True, (210, 210, 210))
        win.blit(g, (260, 200))
        r = respawn_text.render("PRESS 'R' TO RESPAWN", True, (170, 255, 128), None)
        win.blit(r, (200, 300))

    # ENEMY
    enemyY_change = 0.3
    enemyImg = []
    enemyX = []
    enemyY = []

    num_OF_enemies = randint(3,4)
    for i in range(num_OF_enemies):
        enemyImg.append(pygame.image.load('enemynew.png'))
        enemyImg.append(pygame.image.load('alien2.png'))
        enemyImg.append(pygame.image.load('enemynew2cropped.png'))
        enemyX.append(randint(20, 736))
        enemyY.append(randint(-200, -70))

    # BULLETFORENEMY
    enbulletX = []
    enbulletY = []
    bulletImg = []
    enbulletY_change = 0.5
    enbulletX_change = 0

    for i in range(num_OF_enemies):
        bulletImg.append(pygame.draw.rect(win, (0, 255, 255), (enemyX[i], enemyY[i], 4, 10)))
        enbulletX.append(enemyX[i])
        enbulletY.append(enemyY[i])

    def enemy(x, y, i):
        win.blit(enemyImg[i], (x, y))

    def enbullet(x, y, i):
        bulletImg[i] = (pygame.draw.rect(win, (0, 255, 255), (x + 32, y + 64, 4, 10)))

    # BULLETFORPLAYER
    bulletX = 380
    bulletY = 480
    bulletY_change = 2
    bulletX_change = 0
    bullet_state = "static"

    def bullet(x, y):
        bulletImg = pygame.draw.rect(win, (255, 255, 0), (x + 30, y, 4, 20))
        # bulletImg2 = pygame.draw.rect(win, (255, 255, 0), (x+2, y, 4, 20))
        # bulletImg2 = pygame.draw.rect(win, (255, 255, 0), (x+58, y, 4, 20))
        global bullet_state
        bullet_state = "dynamic"

    # COLLISIONWITHENEMY
    def isCollision(enemyX, bulletX, enemyY, bulletY):
        d = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
        if d < 40:
            return True
        else:
            return False

    # COLLISIONWITHPLAYER
    def pCollision(playerX, enbulletX, playerY, enbulletY):
        p1 = math.sqrt(math.pow(playerX - enbulletX, 2) + math.pow(playerY - enbulletY, 2))
        if p1 < 25:
            return True
        else:
            return False

    def playerEnemyCollision(playerX, enemyX, playerY, enemyY):
        p2 = math.sqrt(math.pow(playerX - enemyX, 2) + math.pow(playerY - enemyY, 2))
        if p2 < 45:
            return True
        else:
            return False

    #TIMER
    clock = pygame.time.Clock()

    counter, text = 3, '3'.rjust(3)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('Consolas', 64)
    ms = pygame.font.SysFont('Consolas', 36)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.USEREVENT:
                counter -= 1
                text = str(counter).rjust(3)
                if counter == 0:
                    break
        else:
            win.blit(space, (0, 0))
            win.blit(playerImg, (380, 480))
            win.blit(font.render(text, True, (0, 255, 0)), (310, 220))
            win.blit(ms.render('Stop The Enemies From Getting', True, (220,220,220)), (110, 340))
            win.blit(ms.render('To The End Point', True, (220,220,220)), (230, 390))
            pygame.display.flip()
            clock.tick(60)
            continue
        break

    run = True
    # GAMELOOP
    while run:
        win.fill((0,0,0))
        win.blit(space, (0,0))

        if player_Health == 0:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_r:
                        game()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    main_menu()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    playerX_change = 1
                if e.key == pygame.K_LEFT:
                    playerX_change = -1
                if e.key == pygame.K_SPACE or e.key == pygame.K_UP:
                    if bullet_state == "static":
                        laser_Sound = pygame.mixer.Sound('laser.wav')
                        laser_Sound.play()
                        bulletX = playerX
                        bullet_state = "dynamic"

            if e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT or e.key == pygame.K_LEFT:
                    playerX_change = 0
        #PLAYER MOVEMENT
        playerX += playerX_change

        if playerX >= 736:
            playerX = 736
        elif playerX <= 0:
            playerX = 0

        # BULLET MOVEMENT FOR PLAYER
        if bullet_state == "dynamic":
            bullet(bulletX, bulletY)
            bulletY -= bulletY_change
            if bulletY <= -10:
                bulletY = 480
                bullet_state = "static"

        #ENEMY MOVEMENT AND BULLET MOVEMENT FOR ENEMY
        for i in range(num_OF_enemies):
            enemyY[i] += enemyY_change
            enbulletY[i] += enbulletY_change
            if enemyY[i] >= 610:
                player_Health -= 1
                if player_Health <= 0:
                    player_Health = 0
                enemyY[i] = randint(-100, -70)
                enemyX[i] = randint(20, 720)
            if enbulletY[i] >= 600:
                enbulletY[i] = enemyY[i]
                enbulletX[i] = enemyX[i]

            # COLLISION OF ENEMY AND PLAYERBULLET
            iscol = isCollision(enemyX[i], bulletX, enemyY[i], bulletY)
            if iscol:
                score += 1
                enemyY[i] = randint(-100, -70)
                enemyX[i] = randint(20, 720)
                enbulletY[i] = enemyY[i]
                enbulletX[i] = enemyX[i]
                bulletY = 480
                bullet_state = "static"

            #COLLISION OF PLAYER AND ENEMYBULLET
            pcol = pCollision(playerX, enbulletX[i], playerY, enbulletY[i])

            if pcol:
                playerCollision_Sound = mixer.Sound('explosion.wav')
                playerCollision_Sound.play()
                player_Health -= 1
                enbulletY[i] = enemyY[i]
                enbulletX[i] = enemyX [i]

            #COLLISION OF PLAYER AND ENEMY
            ecol = playerEnemyCollision(playerX, enemyX[i], playerY, enemyY[i])

            if ecol:
                playerCollision_Sound = mixer.Sound('explosion.wav')
                playerCollision_Sound.play()
                player_Health -= 5

            enemy(enemyX[i], enemyY[i], i)
            enbullet(enbulletX[i], enbulletY[i], i)

        #SCORE DISPLAY
        show_score(10, 10)

        #HEALTH DISPLAY
        if player_Health < 3:
            Health_Show(650,560,255,0,0)
        elif player_Health < 5:
            Health_Show(650,560,255,255,0)
        else:
            Health_Show(650,560,0,255,0)

        if player_Health <= 0:
            player_Health = 0
            for j in range(num_OF_enemies):
                enemyY[j] = 2000
                enemyY_change = 0
                enbulletY[j] = enemyY[j]
                enbulletY_change = 0
                playerY = 1000
                bulletY = 1000
                bulletY_change = 0
            game_over()

        player(playerX, playerY)
        pygame.display.update()

main_menu()