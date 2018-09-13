import pygame,sys,random,time

#初始化
pygame.init()
pygame.mixer.init()

#时间控制
clock=pygame.time.Clock()

#重复按键设置
pygame.key.set_repeat(100,15)

#取得历史最高分
highest=open('highest.txt', 'r')
line = highest.readline()
h_result=int(line)
highest.close()

ding_splat = pygame.mixer.Sound("ding.wav")

#动画精灵
class ImgClass (pygame.sprite.Sprite):
    def __init__(self,image_file,location,speed):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(image_file)
        self.rect=self.image.get_rect()
        self.rect.left,self.rect.top=location
        self.speed=speed
    def move(self):
        self.rect=self.rect.move(self.speed)

#游戏开始界面
def show_start():
    people=pygame.image.load("people.jpg")
    screen.blit(people,[302,150])
    people=pygame.image.load("black.jpg")
    screen.blit(people,[152,199])
    people=pygame.image.load("red.jpg")
    screen.blit(people,[452,199])
    
    font=pygame.font.Font(None,50)
    score_text = font.render("Press space to start to play the game!",1,[0,0,0])
    screen.blit(score_text, [10,250])

#游戏时文字
def show_result(result):
    #暂停提示
    p_font=pygame.font.Font(None,20)
    score_text = p_font.render("Press space to pause!",1,[0,0,0])
    screen.blit(score_text, [20,20])
    #显示分数
    font=pygame.font.Font(None,20)
    text="result:"+str(result)
    score_text = font.render(text,1,[0,0,0])
    screen.blit(score_text, [550,20])

#游戏结束界面
def show_over(result):
    global h_result
    if result>h_result:
        h_result=result
        new_highest=open('highest.txt', 'w')
        new_highest.write(str(result))
        new_highest.close()
    over_font=pygame.font.Font(None,100)
    score_text = over_font.render("GAME OVER!",1,[255,0,0])
    screen.blit(score_text, [100,150])
    
    font=pygame.font.Font(None,50)
    text="result:"+str(result)
    score_text = font.render(text,1,[0,0,0])
    screen.blit(score_text, [230,250])
    
    h_font=pygame.font.Font(None,50)
    text="highest:"+str(h_result)
    score_text = h_font.render(text,1,[0,0,0])
    screen.blit(score_text, [205,300])
    
    f_font=pygame.font.Font(None,50)
    score_text = f_font.render("Press space to go on!",1,[0,0,0])
    screen.blit(score_text, [150,350])


#窗口
screen =pygame.display.set_mode([640,480])

#游戏主体函数
def game():
    result=0
    #绘制纯白色背景
    screen.fill([255,255,255])
    #加载背景音乐并循环播放
    pygame.mixer.music.load("BGM.mp3")
    pygame.mixer.music.set_volume(0.60)
    pygame.mixer.music.play(-1)
    #加载人物图片于窗口正下方
    people_file="people.jpg"
    p_location=[302,396]
    people=ImgClass(people_file,p_location,[0,0])
    #定义红球组和黑球组
    red_balls=pygame.sprite.Group()
    black_balls=pygame.sprite.Group()
    #获取当前时间
    s_time=time.time()

    pause=False
    play=True
    while play:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:  #用于在游戏进行中退出
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN:  #用于控制人物左右移动
                if event.key==pygame.K_LEFT:
                    if people.rect.left>10:   
                        people.rect.left-=10
                    else:                      #当人物抵达最左边则无法继续向左移动
                        pass
                elif event.key==pygame.K_RIGHT:
                    if people.rect.left<600:
                        people.rect.left+=10
                    else:
                        pass                   #当人物抵达最右边则无法继续向右移动
                elif event.key==pygame.K_SPACE:
                    pause=True
                    font=pygame.font.Font(None,50)
                    score_text = font.render("Press space to go on!",1,[0,0,0])
                    screen.blit(score_text, [150,200])
                    pygame.display.flip()    #翻转显示暂停信息
                    while pause:
                        for event in pygame.event.get():
                            if event.type==pygame.QUIT:   #用于在游戏暂停时退出
                                pygame.quit()
                                sys.exit()
                            elif event.type==pygame.KEYDOWN:
                                if event.key==pygame.K_SPACE:   #按下空格键继续游戏
                                    pause=False
        
        clock.tick(100)    #设置fps为100
        #根据玩家当前分数改变出现球的频率范围
        if result<100:
            mintime=0.5
            maxtime=3
        elif result<200:
            mintime=0.4
            maxtime=2.5
        elif result<400:
            mintime=0.3
            maxtime=2
        elif result<600:
            mintime=0.2
            maxtime=1.5
        else:
            mintime=0.1
            maxtime=1
        #根据频率范围产生新的球
        if time.time()-s_time>random.uniform(mintime,maxtime):
            s_time=time.time()
            #根据玩家当前分数确定新产生球的下落速度范围
            if result<0:
                 minspeed=1
                 maxspeed=5
            else:
                minspeed=result/100+1
                maxspeed=result/100+5
            #生成随机数，根据随机数确定生成的球的颜色
            i=random.randint(0,1)
            if i==0:      #生成红球
                ball_file="red.jpg"
                location=[random.randint(0,605),-35]  #设置球的初始位置，x轴位置随机，y轴位置位于窗口上方
                speed=[0,random.uniform(minspeed,maxspeed)] #设置球的下落速度
                ball=ImgClass(ball_file,location,speed)   #产生球对象
                red_balls.add(ball)    #将球加入红球组
            else:         #生成黑球
                ball_file="black.jpg"
                location=[random.randint(0,605),-35]
                speed=[0,random.uniform(minspeed,maxspeed)]
                ball=ImgClass(ball_file,location,speed)
                black_balls.add(ball)   #将球加入黑球组
        #重新绘制背景
        screen.fill([255,255,255])
        #绘制人物
        screen.blit(people.image,people.rect)
        #使各个球根据自身速度下落
        for ball in red_balls:
            ball.move()
            screen.blit(ball.image,ball.rect)
            if ball.rect.top>480:    #若红球落入窗口外则将该球从组中删除
                red_balls.remove(ball)
        for ball in black_balls:
            ball.move()
            screen.blit(ball.image,ball.rect)
            if ball.rect.top>480:   #若黑球落入窗口外则扣除玩家5分并将该球从组中删除
                result-=5
                black_balls.remove(ball)
        #碰撞检测
        if pygame.sprite.spritecollide(people,red_balls,False):
            #若人物碰到红球，停止背景音乐，播放死亡音效，延时一秒后结束游戏跳出循环
            pygame.mixer.music.stop()
            splat = pygame.mixer.Sound("DIE.wav")
            splat.play()
            pygame.time.delay(1000)
            play=False
        if pygame.sprite.spritecollide(people,black_balls,True):
            #若人物碰到黑球则删除黑球、播放等分音效并为玩家加10分
            ding_splat.play()
            result+=10
        #显示玩家分数
        show_result(result)
        #翻转显示
        pygame.display.flip()
    #游戏结束画面
    screen.fill([255,255,255]) #重新绘制白色背景
    show_over(result)         #绘制游戏结束画面
    pygame.display.flip()    #翻转显示

    #游戏结束时循环
    #加载开场音乐
    pygame.mixer.music.load("BGM1.mp3")
    pygame.mixer.music.set_volume(0.80)
    pygame.mixer.music.play(-1)
    play=True
    while play:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:   #用于在游戏结束时退出
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:   #按下空格键停止开场音乐重新开始游戏
                    pygame.mixer.music.stop()
                    game()

#执行游戏主体
screen.fill([255,255,255]) #绘制白色背景
show_start()         #绘制游戏开始前画面
pygame.display.flip()    #翻转显示

#加载开场音乐
pygame.mixer.music.load("BGM1.mp3")
pygame.mixer.music.set_volume(0.80)
pygame.mixer.music.play(-1)
while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:   #用于在游戏开始前退出
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:   #按下空格键停止开场音乐并开始游戏
                    pygame.mixer.music.stop()
                    game()
    
