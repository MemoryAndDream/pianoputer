# -*- coding: utf8 -*-
import pygame
import time
pygame.mixer.init()
print("播放音乐1")
track = pygame.mixer.music.load("a1.wav")
pygame.mixer.music.play()
time.sleep(5)
pygame.mixer.music.stop()

#print("播放音乐2")
#track1 = pygame.mixer.music.load("bowl.wav")
#pygame.mixer.music.play()

#print("播放音乐3")
track2 = pygame.mixer.Sound("f1.wav")
track2.play()
time.sleep(2)