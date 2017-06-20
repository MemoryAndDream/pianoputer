# -*- coding: utf-8 -*-
import wave
import numpy
import pylab as pl

# 打开wav文件
# open返回一个的是一个Wave_read类的实例，通过调用它的方法读取WAV文件的格式和数据
f = wave.open(r"a1.wav", "rb")

# 读取格式信息
# 一次性返回所有的WAV文件的格式信息，它返回的是一个组元(tuple)：声道数, 量化位数（byte单位）, 采
# 样频率, 采样点数, 压缩类型, 压缩类型的描述。wave模块只支持非压缩的数据，因此可以忽略最后两个信息
params = f.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]

# 读取波形数据
# 读取声音数据，传递一个参数指定需要读取的长度（以取样点为单位）
str_data = f.readframes(nframes)
print(nchannels, sampwidth, framerate, nframes)#声道数, 量化位数（byte单位）, 采样频率, 采样点数
f.close()

# 将波形数据转换成数组
# 需要根据声道数和量化单位，将读取的二进制数据转换为一个可以计算的数组
wave_data = numpy.fromstring(str_data, dtype=numpy.short)#numpy.short短整型   这操作感觉是对付2声道的
wave_data.shape = -1, 2
wave_data = wave_data.T #这么操作相当于两点取一点

#另一种读取方式
#from scipy.io import wavfile
#fps, sound = wavfile.read('a1.wav')  # 返回rate和numpy格式data
#wave_data = sound.T
#print(wave_data.shape)

time = numpy.arange(0, nframes) * (1.0 / framerate)
len_time = len(time)
time = time[0:len_time]

##print "time length = ",len(time)
##print "wave_data[0] length = ",len(wave_data[0])

# 绘制波形

pl.subplot(311)#第一个参数为你要是实现的行数，一共两行图像，所以我们写2，第二个参数为列数，我们想实现的为一列，我们就写1，那第三个参数呢？第三个参数为该函数的标签
print time.shape,wave_data[0].shape#如果提示plot函数里的两个参数维度不同，说明要截取一半之类（修改时长len_time/2）的，不然不能一一对应作图
pl.plot(time, wave_data[0])
pl.subplot(312)
pl.plot(time, wave_data[1], c="r")
pl.subplot(313)
pl.plot(time, wave_data[1]-wave_data[0], c="r")#左右声道差距

pl.xlabel("time")
pl.show()