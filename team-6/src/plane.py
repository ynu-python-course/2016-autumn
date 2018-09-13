#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Filename:plane.py
# 2016/12/6
#Wang,Li,Kong

import pdb,sys,pygame,math,random

class enemy(pygame.sprite.Sprite):
    def __init__(self,image_file,speed1,location,speed2):
    	pygame.sprite.Sprite.__init__(self)
    	self.image = pygame.image.load('./enemy.png')
    	self.rect = self.image.get_rect()
    	self.rect.centerx, self.rect.top = location
    	self.speed = speed1
    	self.zidan_speed = speed2
    	pass

    def move(self):
        newpos = self.rect.move(self.speed)
        self.rect = newpos

class my_plane(pygame.sprite.Sprite):
    def __init__(self,image_file,location):
        pygame.sprite.Sprite.__init__(self)
    	self.image = pygame.image.load('./my_plane.png')
    	self.rect = self.image.get_rect()
    	self.rect.left, self.rect.top = location

class my_zidan(pygame.sprite.Sprite):
    def __init__(self,image_file,location):
    	pygame.sprite.Sprite.__init__(self)
    	self.image = pygame.image.load('./myzidan.jpg')
    	self.rect = self.image.get_rect()
    	self.rect.centerx, self.rect.top = location
    	pass

def gameover():
	font5 = pygame.font.Font(None, 90)
	font6 = pygame.font.Font(None, 30)
	over_text1 = font5.render('Game Over',1,[255,255,255])
	over_text2 = font6.render('press space to play again',1,[255,0,0])
	over_text3 = font6.render('press other key to exit',1,[255,0,0])
	bg = pygame.image.load('./bg_img.png')
	screen.blit(bg,[0,-244])
	screen.blit(over_text1, [100,230])
	screen.blit(over_text2, [140,310])
	screen.blit(over_text3, [155,350])
	pygame.display.flip()
	pygame.time.delay(1000)
	runing = True
	while runing:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					runing = False
				else:
					pygame.quit()
					sys.exit()
		pass	
	pass

def impact(sprite1,sprite2,distance):
	if math.sqrt((sprite1.rect.centerx - sprite2.rect.centerx) ** 2 + ((sprite1.rect.top + sprite1.rect.bottom - sprite2.rect.top - sprite2.rect.bottom)/2) ** 2) < distance :
		#impact_location = [(sprite1.rect.centerx - sprite2.rect.centerx) / 2, (sprite1.rect.top + sprite1.rect.bottom - sprite2.rect.top - sprite2.rect.bottom)/4]
		return True
	pass


def animate():
	global zidan_num
	global score
	global life
	global life_flip
	global num
	flip_delay = 0
	screen.blit(bg,(0,0))

	#draw my plane
	screen.blit(my_plane.image, my_plane.rect)

	#draw my zidan
	if num%12 == 0:		
		if zidan_num >= 12:
			del my_zidans[0]
			zidan_num -= 1
		new_zidan_location = [my_plane.rect.centerx,my_plane.rect.top + 5]
		my_zidans.append(my_zidan('./myzidan.jpg',new_zidan_location))
		zidan_num += 1	
	if_num3 = 0	
	for i in range(len(my_zidans)):
		k = i - if_num3
		my_zidans[k].rect.top -= 5
		if my_zidans[k].rect.top <= 5:
			del my_zidans[k]
			zidan_num -= 1
			if_num3 += 1
		else:
			screen.blit(my_zidans[k].image,my_zidans[k].rect)

	#draw enemy plane
	if_num1 = 0
	for i in range(len(enemy_plane)):
		k = i - if_num1
		if  enemy_plane[k].rect.top > 680:
			del enemy_plane[k]
			if_num1 += 1
		else:
			enemy_plane[k].move()
			if enemy_plane[k].rect.bottom >= 0:	
				screen.blit(enemy_plane[k].image,enemy_plane[k].rect)

				# collision	detection enemy_plane & my_plane
				if impact(enemy_plane[k],my_plane,60):
					impact_location = [(enemy_plane[k].rect.centerx + my_plane.rect.centerx) / 2, (enemy_plane[k].rect.top + enemy_plane[k].rect.bottom + my_plane.rect.top + my_plane.rect.bottom)/4]
					pygame.draw.circle(screen,[255,0,0],impact_location,15,0)
					flip_delay = 300
					life -= 1
					score -= 100
					del enemy_plane[k]
					if_num1 += 1

				# draw zidan
				# collision	detection zidan & my_plane
				for x in range(6):	
					enemy_zidan_location = [enemy_plane[k].rect.centerx,enemy_plane[k].rect.bottom + 100 + (x*30)]
					distance = math.sqrt((enemy_zidan_location[0] - my_plane.rect.centerx) ** 2 + ((2*enemy_zidan_location[1] - my_plane.rect.top - my_plane.rect.bottom)/2) ** 2)
					if distance <= 35:
						pygame.draw.circle(screen,[255,0,0],enemy_zidan_location,10,0)
						flip_delay = 300
						life -= 1
						score -= 100
						del enemy_plane[k]
						if_num1 += 1						
					else:
						pygame.draw.circle(screen,[255,255,255],enemy_zidan_location,2,0)

				# collision	detection my_zidan & eneny_plane
				if_num2 = 0
				for j in range(len(my_zidans)):
					z = j - if_num2
					if impact(my_zidans[z],enemy_plane[k],43):
						pygame.draw.circle(screen,[255,0,0],[my_zidans[z].rect.centerx,my_zidans[z].rect.top],10,0)
						score += 10
						del my_zidans[z]
						zidan_num -= 1
						if_num2 += 1
						del enemy_plane[k]
						if_num1 += 1

	font3 = pygame.font.Font(None,50)
	score_text = font3.render(u"score: %s"%score ,1,[255,255,255])
	screen.blit(score_text,[10,10])	
	font4 = pygame.font.Font(None,50)
	score_text = font4.render(u"Life: %s"%life ,1,[255,0,0])
	screen.blit(score_text,[400,10])

	#impcat
	if flip_delay != 0:
		pygame.display.flip()
		pygame.time.delay(flip_delay)
		flip_delay = 0
	#life + 1
	elif num - life_flip <= 50 and life_flip != 0:
		font7 = pygame.font.Font(None, 40)
		life_text = font7.render(u'Life + 1' ,1, [255,0,0])
		screen.blit(life_text, [220,320])
		pygame.display.flip()	
	else:
		pygame.display.flip()


pygame.init()
clock = pygame.time.Clock()
#设置按键长按
delay = 80
interval = 3
pygame.key.set_repeat(delay,interval)

screen = pygame.display.set_mode([520,680])

#bgm
pygame.mixer.music.load("bgm.mp3")
pygame.mixer.music.set_volume(0.40)
pygame.mixer.music.play(-1)

font1 = pygame.font.Font(None, 70)
font2 = pygame.font.Font(None, 40)
start_text1 = font1.render(u'Shoot 1000 planes' ,1, [255,255,255])
start_text2 = font2.render(u'press space to start',1,[255,0,0])
bg = pygame.image.load('./bg_img.png')
screen.blit(bg,[0,-244])
screen.blit(start_text1, [45,230])
screen.blit(start_text2, [130,320])
pygame.display.flip()
run = True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				run = False

#background
bg = pygame.Surface(screen.get_size())
bg_image = pygame.image.load('./bg_img.png')
bg_location = [0,-244]
bg.blit(bg_image,bg_location)

#my_flight
my_plane = my_plane('./my_plane.png',[235,605])

#enemy
enemy_num = 2000
enemy_plane = []
for i in range(enemy_num):
	enemy_location = [random.randint(25,495),random.randint(-150000,0)]
	enemy_plane.append(enemy('./enemy.png',[0,5],enemy_location,10))
	pass

score = 0
life = 5
life_add = 0
life_flip = 0
zidan_num = 0
zidan_location = []
my_zidans = []
num = 1
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				if my_plane.rect.left <= screen.get_rect().left:
					break
				else:
					my_plane.rect.left = my_plane.rect.left - 5
			elif event.key == pygame.K_RIGHT:
				if my_plane.rect.left + 50 >= screen.get_rect().right:
					break
				else:
					my_plane.rect.left = my_plane.rect.left + 5
			if event.key == pygame.K_UP:
				if my_plane.rect.top <= screen.get_rect().top:
					break
				else:
					my_plane.rect.top = my_plane.rect.top - 4
			elif event.key == pygame.K_DOWN:
				if my_plane.rect.top + 75 >= screen.get_rect().bottom:
					break
				else:
					my_plane.rect.top = my_plane.rect.top + 4

	if life <= 0:
		gameover()
		enemy_num = 2000
		enemy_plane = []
		for i in range(enemy_num):
			enemy_location = [random.randint(25,495),random.randint(-150000,0)]
			enemy_plane.append(enemy('./enemy.png',[0,5],enemy_location,10))
			pass
		score = 0
		life = 5
		zidan_num = 0
		zidan_location = []
		my_zidans = []
		num = 0

	#life + 1
	if score != 0 and score%500 == 0 and score != life_add and life < 8 :
		life_add = score
		life_flip = num
		life += 1

	num += 1
	animate()
	clock.tick(30)

pygame.quit()
sys.exit()