#!/usr/bin/env python
#coding=utf8
from scipy.io import wavfile
import argparse
import numpy as np
import pygame
import sys
import warnings
import Queue


myQueue = Queue.Queue()
#music=[0,0,0,0,0,0]
#music=[1,2,3,4,5,6,7,8,8,7,6,5,4,3,2,1]
#music=[-2,1,3,5,1,0,3,5,5,6,7,8,6,6,5,5,3,2,1,1,1,3,2,1,1,1,2,3,2,1,-1,2,3,2]

music=[1,1,5,5,6,6,5,4,4,3,3,2,2,1,5,5,4,4,3,3,2,5,5,4,4,3,3,2,1,1,5,5,6,6,5,4,4,3,3,2,2,1]#小星星
#music=[5,3,3,4,2,2,1,2,3,4,5,5,5,5,3,3,4,2,2,1,3,5,3,3,3,3,3,3,3,4,5,4,4,4,4,4,5,6,5,3,3,4,2,2,1,3,5,3,1]

for i in music:
    myQueue.put(i*2+24)#差一位差半个音
'''
后续：长音处理，长音不能拼接(基准是开头音强)，需要拉长
增加乐谱，用queue
增加提示？提示长音短音
声音的音质
'''

def speedx(snd_array, factor):#通过删除点和重复采样点改变频率，同时改变长度  factor加快的系数    越高声音修正的越不对
    """ Speeds up / slows down a sound, by some factor. """
    indices = np.round(np.arange(0, len(snd_array), factor)) #得到一个数列
    #print(factor)
    indices = indices[indices < len(snd_array)].astype(int)        #通过布尔数列截取
    return snd_array[indices]       #返回np队列


def stretch(snd_array, factor, window_size, h):#变速  改变速度的同时保持音频   这个好像用起来不太对劲
    """ Stretches/shortens a sound, by some factor. """
    phase = np.zeros(window_size)
    hanning_window = np.hanning(window_size)
    result = np.zeros(int(len(snd_array)/ factor) + window_size)

    for i in np.arange(0, len(snd_array) - (window_size + h), h*factor):
        # Two potentially overlapping subarrays
        i=int(i)
        a1 = snd_array[i: i + window_size]
        a2 = snd_array[i + h: i + window_size + h]

        # The spectra of these arrays
        s1 = np.fft.fft(hanning_window * a1)
        s2 = np.fft.fft(hanning_window * a2)

        # Rephase all frequencies
        phase = (phase + np.angle(s2/s1)) % 2*np.pi

        a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))
        i2 = int(i/factor)
        result[i2: i2 + window_size] += hanning_window*a2_rephased.real

    # normalize (16bit)
    result = ((2**(16-4)) * result/result.max())

    return result.astype('int16')


def pitchshift(snd_array, n, window_size=2**13, h=2**11):#整合以上两功能实现变频率的同时保持长度
    """ Changes the pitch of a sound by ``n`` semitones. """
    factor = 2**(1.0 * n / 12.0) #要将音高提高n个半音的话，我们需要将频率乘上系数2^(n/12)   **和pow一个效果
    stretched = stretch(snd_array, 1.0/factor, window_size, h)
    return speedx(stretched[window_size:], factor)  #反正最后获得的是一串等长的numpy数列


def parse_arguments():   #这里的基准声音是敲碗的。。。。
    description = ('Use your computer keyboard as a "piano"')

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '--wav', '-w',
        metavar='FILE',
        type=argparse.FileType('r'),
        default='bowl.wav',
        help='WAV file (default: bowl.wav)')  #a1.wav好像是2声道的。。。
    parser.add_argument(
        '--keyboard', '-k',
        metavar='FILE',
        type=argparse.FileType('r'),
        default='typewriter.kb',
        help='keyboard file (default: typewriter.kb)')
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='verbose mode')#verbose 详细

    return (parser.parse_args(), parser)


def main():
    # Parse command line arguments
    (args, parser) = parse_arguments()

    # Enable warnings from scipy if requested
    if not args.verbose:
        warnings.simplefilter('ignore')

    fps, sound = wavfile.read(args.wav.name)#返回rate和numpy格式data

    print(sound.shape)
    try:
        sound = sound[:,0]  #取单声道
    except:
        pass#单声道
    tones = range(-25, 25)
    sys.stdout.write('Transponding sound file... ')
    sys.stdout.flush()
    transposed_sounds = [pitchshift(sound, n) for n in tones]  #列表式要用[xxx]
    #transposed_sounds = [sound.astype('int16')  for n in tones]  #列表式要用[xxx]

    print('DONE')

    # So flexible ;)
    pygame.mixer.init(fps, -16, 1, 4096) #这里只能放1个声道的
    # For the focus
    screen = pygame.display.set_mode((150, 150))

    keys = args.keyboard.read().split('\n')  #获取所有按键
    sounds = map(pygame.sndarray.make_sound, transposed_sounds)#map()函数接收两个参数，一个是函数，一个是序列，map将传入的函数依次作用到序列的每个元素，并把结果作为新的list返回。
    key_sound = dict(zip(keys, sounds))  #zip是二维数组，可以直接转成dict
    is_playing = {k: False for k in keys}

    while True:
        event = pygame.event.wait()
        #if event.type in (pygame.KEYDOWN, pygame.KEYUP):
        if event.type in (pygame.KEYDOWN,):
            key = pygame.key.name(event.key)
            #print(key,type(key))
            if myQueue.empty():
                raise KeyboardInterrupt
            i = myQueue.get()
            key = str(keys[i])
            print('press'+key)
        if event.type == pygame.KEYDOWN:
            if (key in key_sound.keys()) and (not is_playing[key]):
                key_sound[key].play(fade_ms=2000)
                is_playing[key] = True

            if event.key == pygame.K_ESCAPE:  #按esc退出
                print('exit')
                pygame.quit()
                raise KeyboardInterrupt#退出游戏

        elif event.type == pygame.KEYUP and key in key_sound.keys():
            # Stops with 50ms fadeout
            key_sound[key].fadeout(100)#这里的逻辑是按下最多响2秒，
            is_playing[key] = False


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Goodbye')
