#coding=utf8
import time
import pygame
import Queue
import os

rawPath='/home/vobile/meng/raw'
#files=os.listdir(rawPath)
files=['c2.ogg','d2.ogg','e2.ogg','f2.ogg','g2.ogg','a2.ogg','b2.ogg','c3.ogg']#对应表https://wenku.baidu.com/view/99b7a5194431b90d6c85c7b0.html
oggfilelist = []
for file in files:
    file_path = os.path.join(rawPath, file)
    #先不加半音吧
    if not 'm' in  file:
        oggfilelist.append(file_path)

'''设计：采用乐谱文件 pygame 长音和短音时间不同'''
myQueue = Queue.Queue()
#music=[0,0,0,0,0,0]
#music=[1,2,3,4,5,6,7,8,8,7,6,5,4,3,2,1]
#music=[-2,1,3,5,1,0,3,5,5,6,7,8,6,6,5,5,3,2,1,1,1,3,2,1,1,1,2,3,2,1,-1,2,3,2]
#music=[5,5,5,5,3,4,5,7,6,6,6,6,4,6,5,5,5,5,5,5,7,6,5,4,4,4,4,4,4,3,2,1,1,5,5,5,5,3,4,5,7,6,6,6,6,4,6,5,5,5,5,5,5,7,6,5,4,4,4,4,4,4,3,2,1]#同桌的你
music=[1,1,5,5,6,6,5,4,4,3,3,2,2,1,5,5,4,4,3,3,2,5,5,4,4,3,3,2,1,1,5,5,6,6,5,4,4,3,3,2,2,1]#小星星
#music=[5,3,3,4,2,2,1,2,3,4,5,5,5,5,3,3,4,2,2,1,3,5,3,3,3,3,3,3,3,4,5,4,4,4,4,4,5,6,5,3,3,4,2,2,1,3,5,3,1]

for i in music:
    myQueue.put(i)#差一位差半个音

def main():
	# So flexible ;)
	pygame.mixer.init() #只初始化声音
	# For the focus
	screen = pygame.display.set_mode((150, 150))
	while True:
		event = pygame.event.wait()
		if event.type == pygame.KEYDOWN:
			if myQueue.empty():
				raise KeyboardInterrupt
			i = myQueue.get()
			#track = pygame.mixer.Sound(oggfilelist[i])#sound音质很不好
			track1 = pygame.mixer.music.load(oggfilelist[i])
			pygame.mixer.music.stop()
			pygame.mixer.music.play()

			print oggfilelist[i]
			#track.play(fade_ms=2000)
			if event.key == pygame.K_ESCAPE:  # 按esc退出
				print('exit')
				pygame.quit()
				raise KeyboardInterrupt  # 退出游戏





if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Goodbye')
