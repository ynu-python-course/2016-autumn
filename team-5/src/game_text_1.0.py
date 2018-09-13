#coding=gbk
#下面是一个判断输赢的基本方法： 
#如果超过了时间(90000毫秒或90秒)： 
#停止运行游戏 
#设置游戏的结果为赢了 
#如果城堡被摧毁了： 
#停止运行游戏 
#设置游戏结果为输了  

# 1 Import library
import pygame
from pygame.locals import *  # 引入pygame中的所有常量
import math
import random

# 2 Initialize the game
pygame.init()
width, height = 640, 480
screen=pygame.display.set_mode((width, height)) # 创建窗口

keys = [False, False, False, False]       #数组keys按WASD的顺序记录它们的状态。数组的每个元素对应一个键，第一个是W,第二个是A等等。 
playerpos=[200,100]                     #playerpos变量定义程序开始绘制游戏角色的起始位置

acc=[0,0]       #设置值
rockets=[]      #精度变量acc实际上是一个包含射击数量和命中獾 次数的列表。最后我们可以使用这些信息来计算精度的百分比

badtimer=100
badtimer1=0
badguys=[[640,100]]
healthvalue=194
pygame.mixer.init()

# 3  Load image
player = pygame.image.load("flybit/images/airplane.jpg")        #音乐与图像加载
en = pygame.image.load("flybit/images/sc.png")
castle = pygame.image.load("flybit/images/room.jpg")
rocket = pygame.image.load("flybit/images/rocket.png")
badguyimg1 = pygame.image.load("flybit/images/flybg.jpg")
badguyimg=badguyimg1

healthbar = pygame.image.load("flybit/images/healthbar.png")
health = pygame.image.load("flybit/images/health.png")
gameover = pygame.image.load("flybit/images/gameover.png")
youwin = pygame.image.load("flybit/images/youwin.png")

# 3.1 Load music
hit = pygame.mixer.Sound("flybit/musics/explode.wav")
enemy = pygame.mixer.Sound("flybit/musics/enemy.wav")
shoot = pygame.mixer.Sound("flybit/musics/shoot.wav")

hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)

pygame.mixer.music.load('flybit/musics/bg_music.mp3')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# 4 looping
running = 1
exitcode = 0
while running:                                                       # running变量跟踪游戏是否结束，exitcode变量跟踪玩家是赢了还是输了
    badtimer-=1
    # 5 clear the screen 
    screen.fill([255,255,255])
    for x in range(width/en.get_width()+1):
        for y in range(height/en.get_height()+1):
            screen.blit(en,(x*100,y*100))
    screen.blit(castle,(0,30))
    screen.blit(castle,(0,135))
    screen.blit(castle,(0,240))
    screen.blit(castle,(0,345 ))                                        #重复建筑物
    # 6 Set player position and rotation
    
    position = pygame.mouse.get_pos()
    
    angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
    playerrot = pygame.transform.rotate(player, 360-angle*57.29)
    playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)  #鼠标位置让飞机旋转使用三角函数来实现
    
    screen.blit(playerrot, playerpos1) 
    # 6.1 Draw rockets
    for bullet in rockets :
        index=0
        velx=math.cos(bullet[0])*10                                               #运用基本的三角函数可以计算出vely和velx。10是火箭的速度。 
        vely=math.sin(bullet[0])*10                                               #if语句检查弓箭是否飞出边界，如果是则删除该弓箭。第二个for语句循环过arrows数组并画出相应旋转的弓箭。
        bullet[1]+=velx
        bullet[2]+=vely
        if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
            rockets.pop(index)
        index+=1
        for projectile in rockets:
            rocket1 = pygame.transform.rotate(rocket, 360-projectile[0]*57.29)
            screen.blit(rocket1, (projectile[1], projectile[2]))
    # 6.2 Draw badgers
    if badtimer==0:
        badguys.append([640, random.randint(50,430)])
        badtimer=100-(badtimer1*2)
        if badtimer1>=35:
            badtimer1=35
        else:
            badtimer1+=5
    index=0
    for badguy in badguys:
        if badguy[0]<-64:
            badguys.pop(index)
        badguy[0]-=7
        # 6.3.1 - Attack castle
        badrect=pygame.Rect(badguyimg.get_rect())     
        badrect.top=badguy[1]
        badrect.left=badguy[0]
        if badrect.left<64:                                                          #如果飞碟的x坐标值小于64，则删除这家伙然后随机递减5到20点的城堡的生命值
            hit.play()
            healthvalue -= random.randint(5,20)
            badguys.pop(index)
        #6.3.2 - Check for collisions
        index1=0
        for bullet in rockets:
            bullrect=pygame.Rect(rocket.get_rect())
            bullrect.left=bullet[1]
            bullrect.top=bullet[2]
            if badrect.colliderect(bullrect):                                           #碰撞检测
                enemy.play()
                acc[0]+=1
                badguys.pop(index)
                rockets.pop(index1)
            index1+=1
        # 6.3.3 - Next bad guy
        index+=1
    for badguy in badguys:
        screen.blit(badguyimg, badguy)
    # 6.4 - Draw clock                                               #   使用PyGame默认字体创建字体并设置尺寸为24。然后使用字体渲染时间到表面上。之后被定位并绘制到屏幕上。 
    font = pygame.font.Font(None, 24)
    survivedtext = font.render(str((90000-pygame.time.get_ticks())/60000)+":"+str((90000-pygame.time.get_ticks())/1000%60).zfill(2), True, (0,0,0))
    textRect = survivedtext.get_rect()
    textRect.topright=[635,5]
    screen.blit(survivedtext, textRect)
    # 6.5 - Draw health bar
    screen.blit(healthbar, (5,5))
    for health1 in range(healthvalue):
        screen.blit(health, (health1+8,8))
    # 7 - update the screen
    pygame.display.flip()
    # 8 - loop through the events
    for event in pygame.event.get():
        # check if the event is the X button 
        if event.type==pygame.QUIT:
            # if it is quit the game
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key==K_w:
                keys[0]=True
            elif event.key==K_a:
                keys[1]=True
            elif event.key==K_s:
                keys[2]=True
            elif event.key==K_d:
                keys[3]=True
        if event.type == pygame.KEYUP:
            if event.key==pygame.K_w:
                keys[0]=False
            elif event.key==pygame.K_a:
                keys[1]=False
            elif event.key==pygame.K_s:
                keys[2]=False
            elif event.key==pygame.K_d:
                keys[3]=False
        if event.type==pygame.MOUSEBUTTONDOWN:       #这些代码检查是否有鼠标点击，如果有它会读取鼠标位置，并根据玩家的旋转和指针的位置计算出弓箭的旋转。这个旋转储存在rockets数组里
            shoot.play()
            position=pygame.mouse.get_pos()
            acc[1]+=1
            rockets.append([math.atan2(position[1]-(playerpos1[1]+32),position[0]-(playerpos1[0]+26)),playerpos1[0]+32,playerpos1[1]+32])
                
    # 9 - Move player
    if keys[0]:
        playerpos[1]-=5                #这段代码只是检查哪个键被按下，然后添加或减去游戏角色的x或y位置(取决于按下的键)来移动游戏角色
    elif keys[2]:
        playerpos[1]+=5
    if keys[1]:
        playerpos[0]-=5
    elif keys[3]:
        playerpos[0]+=5

    #10 - Win/Lose check
    if pygame.time.get_ticks()>=90000:
        running=0
        exitcode=1
    if healthvalue<=0:
        running=0
        exitcode=0
    if acc[1]!=0:
        accuracy=acc[0]*1.0/acc[1]*100
    else:
        accuracy=0
# 11 - Win/lose display        
if exitcode==0:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: "+str(accuracy)+"%", True, (255,0,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(gameover, (0,0))
    screen.blit(text, textRect)
else:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: "+str(accuracy)+"%", True, (0,255,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(youwin, (0,0))
    screen.blit(text, textRect)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()


