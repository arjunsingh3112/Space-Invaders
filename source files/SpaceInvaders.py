
# Original Graphics :- self-made
# time.sleep(0.2) for buttons
# Add a timer maybe
# replace all text blits with text objects
# number of aliens could be a function of score. 
# can add play again button
# can also add pause button
# player speed at line 205 and 207
# enemy speed at line 166
# bullet speed at line 176
# 2 types of bullets - one normal, another which is twice as fast but gives half as much points

from pickletools import read_bytes1
import this
import pygame
import random
import math
from pygame import mixer
import time

pygame.init()
vec = pygame.math.Vector2 #Two dimensional vector

pause = False

clock = pygame.time.Clock()
FPS = 120
PLAYER_ACC_X = 0.5
PLAYER_FRIC_X = -0.08
#enemyAccX = 1
#ENEMY_FRIC_X = -0.08

#Theme
gameTheme = "Normal"

alienImg = pygame.image.load("alien.png")
dalekImg = pygame.image.load("dalek3.png")
enemyImg = alienImg

shipImg = pygame.image.load("ship.png")
tardisImg = pygame.image.load("tardis.png")
playerImg = shipImg

#Diffculty Variables
gameDifficulty = "Easy"
numEnemys = 4
enemyVelocity = 3
enemyVerticalGain = 20
bulletSpeed = -4
scoreIncrement = 1


#High Score
f = open("high_score.txt", "r")
highScore = int(f.readline())
f.close()

#colours
white = (255, 255, 255)
black = (0, 0, 0)
brightGreen = (0, 200, 0)
green = (0, 140, 0)
purple = (115, 16, 176)
brightPurple = (181, 7, 245)
greenish =(84, 181, 99)
red = (140, 0, 0)
brightRed = (255, 0, 0)
yellow = (140,140,0)
brightYellow = (200,200,0)

#Game Screen
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

#background
background = pygame.image.load("background_galaxy.jpg")

#background music
mixer.music.load("background_music3.mp3")
mixer.music.play(-1)

#Caption and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

class Button():
    buttonDrawState = True
    def __init__(self,msg,x,y,width,height,inactiveColor=green,activeColor=brightGreen,action=None):
        self.msg = msg
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.inactiveColor = inactiveColor
        self.activeColor = activeColor
        self.action = action
    
    def generateButton(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        clickSound = mixer.Sound('gameclick1.wav')

        if (self.buttonDrawState): 
            if self.x+self.width > mouse[0] > self.x and self.y+self.height > mouse[1] > self.y:
                pygame.draw.rect(screen, self.activeColor,(self.x,self.y,self.width,self.height))
                if click[0] == 1 and self.action != None:
                    clickSound.play()
                    time.sleep(0.2)
                    self.action()        
            else:
                pygame.draw.rect(screen, self.inactiveColor,(self.x,self.y,self.width,self.height))
            smallText = pygame.font.SysFont("comicsansms",20)
            textSurf, textRect = text_objects(self.msg, smallText, black)
            textRect.center = ( (self.x+(self.width/2)), (self.y+(self.height/2)) )
            screen.blit(textSurf, textRect)
    
    def turnOffButton(self):
        self.buttonDrawState = False

    def turnOnButton(self):
        self.buttonDrawState = True


#Enemy
enemyHeight = 64
enemyWidth = 64
enemySizeDefault = (enemyWidth, enemyHeight)

#enemyImgScaled = pygame.transform.scale(enemyImg, enemySizeDefault)

class Enemy(pygame.sprite.Sprite):
    #enemyX = random.randint(0, 735)
    #enemyY = random.randint(50, 150)
    def __init__(self,enemyImg=enemyImg,enemyWidth=64,enemyHeight=64):
        super().__init__()
        self.height = enemyHeight
        self.width = enemyWidth
        self.enemySize = (enemyWidth, enemyHeight)
        self.enemyImgScaled = pygame.transform.scale(enemyImg, self.enemySize)
        self.surf = self.enemyImgScaled
        self.rect = self.surf.get_rect()
        self.pos = vec(random.randint(0, 735), random.randint(50, 150))
        self.vel = vec(enemyVelocity,0)

        

    def move(self):
        #self.vel = vec(3,0)
        global gameOver
        self.pos += self.vel 

        if self.pos.x > SCREEN_WIDTH:   
            self.vel.x = -self.vel.x
            self.pos.y += enemyVerticalGain
        if self.pos.x < 0:
            self.vel.x = -self.vel.x
            self.pos.y += enemyVerticalGain

        self.rect.center = self.pos

        if self.pos.y + 64 > P1.pos.y:
            gameOver = True
        #print(self.pos)
        #print(self.pos.x>SCREEN_WIDTH)
        #print(pygame.time.get_ticks())

    def reset(self):
        self.pos.x = random.randint(0, 735)
        self.pos.y = random.randint(50, 150)
        self.vel.x = 3
        self.vel.y = 0

    def changeTheme(self):
        self.enemyImgScaled = pygame.transform.scale(enemyImg, self.enemySize)
        self.surf = self.enemyImgScaled
    
    

"""def enemy(x, y):
    screen.blit(enemyImgScaled, (x, y))"""

#Player
playerHeight = 64
playerWidth = 64
playerSizeDefault = (playerWidth, playerHeight)

#playerImgScaled = pygame.transform.scale(playerImg, playerSizeDefault)



"""def player(x, y):
    screen.blit(playerImg, (x, y))"""

class Player(pygame.sprite.Sprite):
    playerX = SCREEN_WIDTH/2
    playerY = SCREEN_HEIGHT * 0.85
    def __init__(self, playerImg=playerImg, playerWidth=64, playerHeight=64):
        super().__init__()
        self.width = playerWidth
        self.height = playerHeight
        self.playerSize = (playerWidth,playerHeight)
        self.playerImgScaled = pygame.transform.scale(playerImg, self.playerSize)
        self.surf = self.playerImgScaled
        self.rect = self.surf.get_rect()
        self.pos = vec(self.playerX, self.playerY)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    
    def move(self):
        self.acc = vec(0,0)
        pressed_keys = pygame.key.get_pressed()
                
        if pressed_keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC_X
            #screen.blit(self.surf, self.rect)
        if pressed_keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC_X
                 
        self.acc.x += self.vel.x * PLAYER_FRIC_X
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc


        if self.pos.x > SCREEN_WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = SCREEN_WIDTH

        
                    
             
        self.rect.center = self.pos
        #print("Player rect center: " + str(self.rect))
        #print("Player position: " + str(self.pos))
    
    def reset(self):
        self.pos.y = self.playerY
        self.pos.x = self.playerX
        self.vel.x = 0
        self.vel.y = 0
        self.acc.x = 0
        self.acc.y = 0
    
    def changeTheme(self):
        self.playerImgScaled = pygame.transform.scale(playerImg, self.playerSize)
        self.surf = self.playerImgScaled


#Bullet
bulletHeight = 32
bulletWidth = 32
bulletSizeDefault = (bulletWidth, bulletHeight)
bulletImg = pygame.image.load("bullet.png")
bulletImgScaled = pygame.transform.scale(bulletImg, bulletSizeDefault)
bullet_state = "ready"

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bulletImg=bulletImg, bulletWidth=32, bulletHeight=32):
        super().__init__()
        self.width = bulletWidth
        self.height = bulletHeight
        bulletSize = (self.width,self.height)
        bulletImgScaled = pygame.transform.scale(bulletImg, bulletSize)
        self.surf = bulletImgScaled
        self.rect = self.surf.get_rect()
        self.pos = vec(1200,1200)
        self.vel = vec(0,0)

    def move(self):
        global bullet_state
        #self.pos.y = P1.pos.y
        if(bullet_state is "ready"):
            self.pos.x = P1.pos.x
            self.pos.y = 1200
            self.vel = vec(0,0)
        if(bullet_state is "fire"):
            #self.vel.y = -4
            self.pos.x = P1.pos.x
            self.pos.y = P1.pos.y
            bullet_state = "in motion"
        if(bullet_state is "in motion"):
            self.vel.y = bulletSpeed

        self.pos += self.vel
        self.rect.center = self.pos
        #print(self.rect)
        #print("Bullet pos: "+str(self.pos))
        #print("Player Y pos:" +str(P1.pos.y))
        #print(bullet_state)

    def collide(self):
        hits = pygame.sprite.spritecollide(B1, enemys, False)
        global bullet_state
        global score_value
        explosionSound = mixer.Sound('explosion1.wav')
        if hits and (len(hits)==1):
            bullet_state = "ready"
            hits[0].pos.x = random.randint(0, 735) 
            hits[0].pos.y = random.randint(50, 150)
            explosionSound.play()
            score_value += scoreIncrement
            highScoreUpdate(score_value)
            #print(len(hits))
    
    def reset(self):
        self.pos.y = 1200
        self.pos.x = 1200
        self.vel.x = 0
        self.vel.y = 0

    def changeTheme(self):
        pass
            

"""def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    #screen.blit(bulletImg, (x + 16, y + 10))
    screen.blit(bulletImgScaled, (x, y))"""


"""def isCollision(enemyX, enemyY, bulletX, bulletY):
    x2 = enemyX + (enemyWidth/2)
    y2 = enemyY + (enemyHeight/2)
    x1 = bulletX + (bulletWidth/2)
    y1 = bulletY
    radius = (enemyHeight + enemyWidth)/4
    distance = math.sqrt(((x2-x1)**2)+((y2-y1)**2))
    return distance < radius"""

# Score
score_value = 0
scoreFont = pygame.font.SysFont('arial', 24)
scoreX = 10
scoreY = 10


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def show_score(x, y):
    score = scoreFont.render("Current Score: " + str(score_value), True, green)
    screen.blit(score, (x, y))

def game_over_message_display():
    messageFont = pygame.font.SysFont("impact", 72)
    message = messageFont.render("GAME OVER", True, purple)
    msg_rect = message.get_rect()
    msg_rect.center = (SCREEN_WIDTH/2, 240)
    screen.blit(message, msg_rect)

def final_score_display():
    messageFont = pygame.font.SysFont("impact", 32)
    message = messageFont.render("Final Score: " + str(score_value), True, greenish)
    msg_rect = message.get_rect()
    msg_rect.center = (SCREEN_WIDTH/2, 360)
    screen.blit(message, msg_rect)

def game_title_display():
    messageFont = pygame.font.SysFont("centurygothic", 64)
    message = messageFont.render("Space Invaders", True, white)
    msg_rect = message.get_rect()
    msg_rect.center = (SCREEN_WIDTH/2, 200)
    screen.blit(message, msg_rect)

def difficulty_display():
    messageFont = pygame.font.SysFont("centurygothic", 52)
    message = messageFont.render("Difficulty: " + gameDifficulty, True, white)
    msg_rect = message.get_rect()
    msg_rect.center = (SCREEN_WIDTH/2, 100)
    screen.blit(message, msg_rect)

def game_theme_display():
    messageFont = pygame.font.SysFont("centurygothic", 52)
    message = messageFont.render("Theme: " + gameTheme, True, white)
    msg_rect = message.get_rect()
    msg_rect.center = (SCREEN_WIDTH/2, 175)
    screen.blit(message, msg_rect)

def instructions_title_display():
    messageFont = pygame.font.SysFont("centurygothic", 52)
    message = messageFont.render("Instructions", True, white)
    msg_rect = message.get_rect()
    msg_rect.center = (SCREEN_WIDTH/2, 125)
    screen.blit(message, msg_rect)

def instructions_display():
    messageFont = pygame.font.SysFont("centurygothic", 28)
    InstructionsText = "Use left and right arrow keys to move your player. Press spacebar to fire at enemies. Press P to pause game. You can change difficulty and theme from settings menu. If aliens reach down to your player then game is over."
    message1Text = "Use left and right arrow keys to move your player."
    message1 = messageFont.render(message1Text, True, white)
    msg_rect1 = message1.get_rect()
    msg_rect1.center = (SCREEN_WIDTH/2, 200)
    screen.blit(message1, msg_rect1)

    message2Text = "Press spacebar to fire at enemies. Press P to pause game."
    message2 = messageFont.render(message2Text, True, white)
    msg_rect2 = message2.get_rect()
    msg_rect2.center = (SCREEN_WIDTH/2, 250)
    screen.blit(message2, msg_rect2)

    message3Text = "You can change difficulty and theme from settings menu."
    message3 = messageFont.render(message3Text, True, white)
    msg_rect3 = message3.get_rect()
    msg_rect3.center = (SCREEN_WIDTH/2, 300)
    screen.blit(message3, msg_rect3)

    message4Text = "If aliens reach down to your player then game is over."
    message4 = messageFont.render(message4Text, True, white)
    msg_rect4 = message4.get_rect()
    msg_rect4.center = (SCREEN_WIDTH/2, 350)
    screen.blit(message4, msg_rect4)

    

    #print(InstructionsText)


"""def button(msg,x,y,width,height,inactiveColor,activeColor,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+width > mouse[0] > x and y+height > mouse[1] > y:
        pygame.draw.rect(screen, activeColor,(x,y,width,height))
        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(screen, inactiveColor,(x,y,width,height))
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText, black)
    textRect.center = ( (x+(width/2)), (y+(height/2)) )
    screen.blit(textSurf, textRect)"""

def quit_game():
    pygame.quit()
    quit()

def pause_game():
    continueButton.turnOnButton()
    quitButton.turnOnButton()
    global highScore
    global score_value
    screen.blit(background, (0, 0))
    highScoreUpdate(score_value)
    pauseFont = pygame.font.SysFont("arial", 72)
    pauseMsgSurf, pauseMsgRect = text_objects("Game Paused", pauseFont, red)
    pauseMsgRect.center = ((SCREEN_WIDTH*0.5),(SCREEN_HEIGHT*0.3))
    screen.blit(pauseMsgSurf, pauseMsgRect)

    highScoreFont = pygame.font.SysFont("arial", 36)
    highScoreMsgSurf, highScoreMsgRect = text_objects("High Score:" + str(highScore), highScoreFont, white)
    highScoreMsgRect.center = ((SCREEN_WIDTH*0.5),(SCREEN_HEIGHT*0.5))
    screen.blit(highScoreMsgSurf, highScoreMsgRect)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        continueButton.generateButton()
        quitButton.generateButton()
        pygame.display.update()
    
def unpause_game():
    global pause
    pause = False
    continueButton.turnOffButton()
    quitButton.turnOffButton()

def highScoreUpdate(score_value):
    global highScore
    if(score_value>highScore):
        newHighScore = score_value
        highScore = newHighScore
        f = open("high_score.txt", "w")
        f.write(str(newHighScore))
        f.close()

def show_high_score(x, y):
    highScoreFont = pygame.font.SysFont('arial', 24)
    highScoreMsgSurf, highScoreMsgRect = text_objects("High Score: " + str(highScore), highScoreFont, green)
    highScoreMsgRect.center = (x, y)
    screen.blit(highScoreMsgSurf, highScoreMsgRect)


def restart_game():
    global score_value
    score_value = 0
    playAgainButton.turnOffButton()
    for entity in all_sprites:
        entity.reset()
    game_loop()

def gameOverScreen():
    playAgainButton.turnOnButton()
    mainMenuButton.turnOnButton()
    screen.fill(black)
    screen.blit(background, (0, 0))
    highScoreUpdate(score_value)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global running
            running = False
            pygame.quit()
            quit()
    game_over_message_display()
    final_score_display()
    playAgainButton.generateButton()
    mainMenuButton.generateButton()
    pygame.display.update()

def mainMenu():
    global score_value
    score_value = 0
    global gameOver
    gameOver = False
    global menu
    menu = True
    global optionsMenuBool
    optionsMenuBool = False
    playGameButton.turnOnButton()
    menuOptionsButton.turnOnButton()
    quitFromMenuButton.turnOnButton()
    backToMainMenuButton.turnOffButton()
    playAgainButton.turnOffButton()
    mainMenuButton.turnOffButton()
    while menu:
        screen.fill(black)
        screen.blit(background, (0, 0))
        game_title_display()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global running
                running = False
                pygame.quit()
                quit()
        playGameButton.generateButton()
        menuOptionsButton.generateButton()
        quitFromMenuButton.generateButton()
        pygame.display.update()

def optionsMenu():
    global menu
    menu = False
    global settingsMenuBool
    settingsMenuBool = False
    global optionsMenuBool
    optionsMenuBool = True
    settingsButton.turnOnButton()
    instructionsButton.turnOnButton()
    backToMainMenuButton.turnOnButton()
    playGameButton.turnOffButton()
    menuOptionsButton.turnOffButton()
    quitFromMenuButton.turnOffButton()
    changeDifficultyButton.turnOffButton()
    backToOptionsMenuButton.turnOffButton()
    changeThemeButton.turnOffButton()
    backToOptionsMenuFromInstructionsButton.turnOffButton()
    while optionsMenuBool:
        screen.fill(black)
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global running
                running = False
                pygame.quit()
                quit()
        settingsButton.generateButton()
        instructionsButton.generateButton()
        backToMainMenuButton.generateButton()
        pygame.display.update()

def settingsMenu():
    global optionsMenuBool
    optionsMenuBool = False
    global settingsMenuBool
    settingsMenuBool = True
    changeDifficultyButton.turnOnButton()
    changeThemeButton.turnOnButton()
    backToOptionsMenuButton.turnOnButton()
    settingsButton.turnOffButton()
    instructionsButton.turnOffButton()
    backToMainMenuButton.turnOffButton()
    while settingsMenuBool:
        screen.fill(black)
        screen.blit(background, (0, 0))
        difficulty_display()
        game_theme_display()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global running
                running = False
                pygame.quit()
                quit()
        changeDifficultyButton.generateButton()
        changeThemeButton.generateButton()
        backToOptionsMenuButton.generateButton()
        pygame.display.update()

def instructionsMenu():
    global optionsMenuBool
    optionsMenuBool = False
    global instructionsMenuBool
    instructionsMenuBool = True
    backToOptionsMenuFromInstructionsButton.turnOnButton()
    settingsButton.turnOffButton()
    instructionsButton.turnOffButton()
    backToMainMenuButton.turnOffButton()
    while instructionsMenuBool:
        screen.fill(black)
        screen.blit(background, (0, 0))
        instructions_title_display()
        instructions_display()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global running
                running = False
                pygame.quit()
                quit()
        backToOptionsMenuFromInstructionsButton.generateButton()
        pygame.display.update()    

def changeGameDifficulty():
    global gameDifficulty
    global numEnemys 
    global enemyVelocity 
    global enemyVerticalGain
    global bulletSpeed 
    global scoreIncrement
    if gameDifficulty == "Easy":
        gameDifficulty = "Normal"
        numEnemys = 6
        enemyVelocity = 6
        enemyVerticalGain = 25
        bulletSpeed = -8
        scoreIncrement = 2
    
    elif gameDifficulty == "Normal":
        gameDifficulty = "Hard"
        numEnemys = 8
        enemyVelocity = 9
        enemyVerticalGain = 30
        bulletSpeed = -12
        scoreIncrement = 3

    else:
        gameDifficulty = "Easy"
        numEnemys = 4
        enemyVelocity = 3
        enemyVerticalGain = 20
        bulletSpeed = -4
        scoreIncrement = 1

    #print(gameDifficulty)

def changeGameTheme():
    global gameTheme
    global playerImg
    global enemyImg
    
    if gameTheme is "Normal":
        gameTheme = "Doctor Who"
        playerImg = tardisImg
        enemyImg = dalekImg
    else:
        gameTheme = "Normal"
        playerImg = shipImg
        enemyImg = alienImg



# Game Loop
def game_loop():
    playGameButton.turnOffButton()
    menuOptionsButton.turnOffButton()
    quitFromMenuButton.turnOffButton()
    highScoreX = 270
    highScoreY = 23
    global highScore
    global score_value
    global running
    global menu
    menu = False
    running = True
    global gameOver
    gameOver = False

    #Sprite Initialisation
    global P1
    global B1
    global all_sprites
    global enemys
    P1 = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    enemys = pygame.sprite.Group() 
    for x in range(numEnemys):
        en = Enemy()
        enemys.add(en)
        all_sprites.add(en) 
    B1 = Bullet()
    all_sprites.add(B1)
    bullets = pygame.sprite.Group()
    bullets.add(B1)

    for entity in all_sprites:
        entity.changeTheme() 

    """enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = 20
    num_of_enemies = 5

    for i in range(num_of_enemies):
        enemyX.append(random.randint(0, 735))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(5)"""

    #Player
    playerX = (SCREEN_WIDTH - playerWidth)/2
    playerY = SCREEN_HEIGHT * 0.8
    playerX_change = 0

    #Bullet
    bulletX = 0
    bulletY = playerY 
    bulletY_change = 5
    global bullet_state
    bullet_state = "ready"

    while running:
        screen.fill(black)
        screen.blit(background, (0, 0))
        while gameOver:
            gameOverScreen()
        while not gameOver:
            screen.fill(black)
            screen.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    highScoreUpdate(score_value)
                    running = False
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        playerX_change = -4
                    if event.key == pygame.K_RIGHT:
                        playerX_change = 4
                    if event.key == pygame.K_SPACE:
                        #bullet_state = "fire"
                        if bullet_state == "ready":
                            bulletSound = mixer.Sound("laser1.wav")
                            bulletSound.play()
                            bullet_state = "fire"
                    if event.key == pygame.K_p:
                        global pause 
                        pause = True
                        pause_game()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        playerX_change = 0    

            #Player movement            
            playerX += playerX_change

            # Boundaries for player

            if playerX <= 0:
                playerX = 0
            elif playerX > (SCREEN_WIDTH - playerWidth):
                playerX = (SCREEN_WIDTH - playerWidth)    
            
            #Enemy movement
            """for i in range(num_of_enemies):
                if (enemyY[i] + enemyHeight) - playerY >= 0:
                    gameOver = True
                    break

                enemyX[i] += enemyX_change[i]
                if enemyX[i] <= 0 or enemyX[i] > (SCREEN_WIDTH - enemyWidth):
                    enemyX_change[i] = - enemyX_change[i]
                    enemyY[i] += enemyY_change
                
                #Collision of bullet with enemy
                collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
                if collision:
                    explosionSound = mixer.Sound('explosion1.wav')
                    explosionSound.play()
                    bulletY = playerY
                    bullet_state = "ready"
                    score_value += 1
                    highScoreUpdate(score_value)
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(50, 150)
                #enemy(enemyX[i], enemyY[i])"""
            if gameOver:
                break
        

            #Bullet movement
            if B1.pos.y <= 0:
                bullet_state = "ready"


            """if bullet_state is "fire":
                fire_bullet(bulletX, bulletY)
                bulletY -= bulletY_change""" 
            
            show_high_score(highScoreX, highScoreY)
            show_score(scoreX, scoreY)
            #player(playerX, playerY)
            #P1.move()
            B1.collide()
            for entity in all_sprites:
                screen.blit(entity.surf, entity.rect)
                entity.move()
            pygame.display.update()
            clock.tick(FPS)

# Pause Screen 
continueButton = Button("Continue", 350, 375, 100, 50, green, brightGreen, unpause_game)
quitButton = Button("Quit", 350, 450, 100, 50, red, brightRed, quit_game)

#Game Over Screen
playAgainButton = Button("Play Again", 350, 450, 100, 50, purple, brightPurple, restart_game)
mainMenuButton = Button("Main menu", 350, 525, 100, 50, red, brightRed, mainMenu)

#Main menu Screen
playGameButton = Button("Play", 350, 325, 100, 50, green, brightGreen, game_loop)
menuOptionsButton = Button("Options", 350, 400, 100, 50, yellow, brightYellow, optionsMenu)
quitFromMenuButton = Button("Quit", 350, 475, 100, 50, red, brightRed, quit_game)

#Options menu Screen
settingsButton = Button("Settings", 350, 250, 100, 50, green, brightGreen, settingsMenu)
instructionsButton = Button("Instructions", 325, 325, 150, 50, yellow, brightYellow, instructionsMenu)
backToMainMenuButton = Button("Back", 350, 400, 100, 50, red, brightRed, mainMenu)

#Settings Menu Screen
changeDifficultyButton = Button("Change Difficulty", 313, 250, 175, 50, green, brightGreen, changeGameDifficulty)
changeThemeButton = Button("Change Theme", 313, 325, 175, 50, yellow, brightYellow, changeGameTheme)

backToOptionsMenuButton = Button("Back", 350, 400, 100, 50, red, brightRed, optionsMenu)

#Instructions Screen
backToOptionsMenuFromInstructionsButton = Button("Back", 350, 400, 100, 50, red, brightRed, optionsMenu)

mainMenu()
pygame.quit()
quit()