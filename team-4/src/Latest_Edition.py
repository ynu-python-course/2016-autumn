import sys
import pygame
from random import randint
from pygame.locals import *
#init pygame
pygame.init()


#init clock
clock = pygame.time.Clock()

#screen
screen = pygame.display.set_mode([800,710])

#voice
splat = pygame.mixer.Sound("splat.wav")
splat.set_volume(0.5)

pygame.mixer.music.load("ingg.mp3")
pygame.mixer.music.set_volume(0.1)

#background
background = pygame.Surface(screen.get_size())
bg_image = pygame.image.load("background.jpg")
background.blit(bg_image,[0,0])

#button
        
# key repeats
delay = 100

interval = 50
pygame.key.set_repeat(delay, interval)

class Ball1(pygame.sprite.Sprite):

    def restart(self):
        self.rect.left = randint(0,540)
        self.rect.top = 0
        self.speed = [0, 10]   #氧气速度从这里改

    def __init__(self,speed,location):
        pygame.sprite.Sprite.__init__(self)

        self.image=pygame.image.load('O2.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed

    def move(self):
        if self.rect.top<510:   #氧气碰撞位置从这里改
            newpos = self.rect.move(self.speed)
            self.rect = newpos
        else:
            self.restart()

class Ball2(pygame.sprite.Sprite):

    def restart(self):
        self.rect.left = randint(0,540)
        self.rect.top = 0
        self.speed = [0,8]    #氢气速度从这里改

    def __init__(self,speed,location):
        pygame.sprite.Sprite.__init__(self)

        self.image=pygame.image.load('H2.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed

    def move(self):
        if self.rect.top<510:   #氢气碰撞位置从这里改
            newpos = self.rect.move(self.speed)
            self.rect = newpos
        else:
            self.restart()

class Ball3(pygame.sprite.Sprite):

    def restart(self):
        self.rect.left = randint(0,540)
        self.rect.top = 0
        self.speed = [0,6]    #二氧化氮速度从这里改

    def __init__(self,speed,location):
        pygame.sprite.Sprite.__init__(self)

        self.image=pygame.image.load('No2.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed

    def move(self):
        if self.rect.top<510:    #二氧化氮碰撞位置从这里改
            newpos = self.rect.move(self.speed)
            self.rect = newpos
        else:
            self.restart()

class People(pygame.sprite.Sprite):

    #initializer
    def __init__(self,location):
        #call super initializer
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("people.png")
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = location
        
class Paddle(pygame.sprite.Sprite):
	# initializer
	def __init__(self, location):
		# call super initializer
		pygame.sprite.Sprite.__init__(self)

		image_surface = pygame.surface.Surface([120, 2])  # 设定绘制表面
		image_surface.fill([0, 0, 0,0])

		self.image = image_surface.convert()  # 将绘制表面转换成图像(球拍)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

my_ball1 = Ball1([0,8],[randint(0,540),0])   #随机生成的速度和位置
my_ball2 = Ball2([0,8],[randint(0,540),0])
my_ball3 = Ball3([0,7],[randint(0,540),0])

# create my objects

goodball_group = pygame.sprite.Group()
niceball_group = pygame.sprite.Group()
niceball_group.add(my_ball1)
goodball_group.add(my_ball2)

badball_group = pygame.sprite.Group()
badball_group.add(my_ball3)

# create my paddle
paddle = Paddle([(800-120)/2, 710-104])
people = People([(800-120)/2, 710-103])

score = 0

#set timer
pygame.time.set_timer(pygame.USEREVENT,1000)

#animate
def animate():
    global score
    screen.blit(background,(0,0))
    
# move ball one step
    my_ball1.move()

    my_ball2.move()
    
    my_ball3.move()

# detect collide
    if pygame.sprite.spritecollide(paddle, niceball_group, False):
            splat.play()
            score += 6
    if pygame.sprite.spritecollide(paddle, goodball_group, False):
            splat.play()
            score += 5
    if pygame.sprite.spritecollide(paddle, badball_group, False):
            splat.play()
            if score>=7:
                score -= 7
            else:
                score=0

    screen.blit(my_ball1.image, (my_ball1.rect.left, my_ball1.rect.top))
    screen.blit(my_ball2.image, (my_ball2.rect.left, my_ball2.rect.top))
    screen.blit(my_ball3.image, (my_ball3.rect.left, my_ball3.rect.top))
    screen.blit(paddle.image, paddle.rect)
    screen.blit(people.image, people.rect)


	# 创建显示文本到屏幕（文本在每一次击球后都会更新）
    font = pygame.font.Font(None, 50)
    if pygame.sprite.spritecollide(paddle, badball_group, False):
        score_text = font.render("%s" %score+"%",1,[150,0,0])
    elif pygame.sprite.spritecollide(paddle, goodball_group, False) or pygame.sprite.spritecollide(paddle, niceball_group, False) :
        score_text = font.render("%s" %score+"%",1,[0,255,0])
    else:
        score_text = font.render("%s" %score+"%",1,[255,255,255])

    text_pos = [44,250]
    screen.blit(score_text,text_pos)

#timer
    if 1 <= seconds and seconds <= 20:
        font = pygame.font.Font(None, 50)
        time_rect = pygame.Rect(800-130,193,97,-seconds*4.7)
        time_image = pygame.image.load("times.png")
        seconds_display = font.render("O2 "+str(seconds*5) +"%", 1, (255, 255, 255))
        display_pos =(800-130,49 )
        pygame.draw.rect(screen,[0,191,220],time_rect,0)
        screen.blit(seconds_display,display_pos)
        screen.blit(time_image,[800-130,97])
#end

#lifeline
    lifes_rect = pygame.Rect(42,222,47,-score*2)
    if 0 < score and score <=100:
        if 0 < score and score <=30:
            pygame.draw.rect(screen,[255,score * 5 + 4,25],lifes_rect,0)
        if 30 < score and score <=60:
            pygame.draw.rect(screen,[255,165,25],lifes_rect,0)
        if 60 < score and score <=100:
            pygame.draw.rect(screen,[255,165 + (score-40)*1.5,25],lifes_rect,0)
    elif score >100:
        lifes_rect = pygame.Rect(42,222,47,-200)
        pygame.draw.rect(screen,[230,255,25],lifes_rect,0)
    lives_image = pygame.image.load("lives.png")
    screen.blit(lives_image,[17,2])
    pygame.draw.line(screen,[0,0,0,100],[0,710-104],[960,710-104],1)
#end

    pygame.display.flip()

start_image = pygame.image.load("before.jpg")

def waitForPlayToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_s:
                    return 
            

screen.blit(start_image,(0,0))
pygame.display.flip()

pygame.display.update()  
waitForPlayToPressKey()


running = True
held_down =False

global seconds
seconds = 20

pygame.time.set_timer(USEREVENT + 1, 1000)
pygame.mixer.music.play(-1)
while running :
    #process events


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running =False
        if event.type == pygame.MOUSEMOTION:
            paddle.rect.centerx = event.pos[0]
            people.rect.centerx = event.pos[0]
        elif event.type == USEREVENT + 1:
            seconds-=1
    if seconds <= 0:
        if score >=100:
            sucess_image = pygame.image.load("success.jpg")
            screen.blit(sucess_image,[0,0])
            score_font = pygame.font.Font(None,50)
            score_text = score_font.render("SOCRE %d"%score,1,[200,20,0])
            width =screen.get_width()
            screen.blit(score_text,[(width - score_text.get_width() - 10)/2,60])

            pygame.display.flip()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    seconds = 20
                    score = 0
                    continue

        else:
            fail_image = pygame.image.load("fail.jpg")
            screen.blit(fail_image,[0,0])
            score_font = pygame.font.Font(None,50)
            score_text = score_font.render("SOCRE %d"%score,1,[200,20,0])
            width =screen.get_width()
            screen.blit(score_text,[(width - score_text.get_width() - 10)/2,60])

            pygame.display.flip()   
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    seconds = 20
                    score = 0
                continue
    else :
        animate()
    clock.tick(30)#30 frame


    
#exit program

pygame.quit()   #exit pygame
sys.exit()      #close window  




