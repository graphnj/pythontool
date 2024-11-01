import numpy as np
from scipy import signal
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
'''b, a = signal.butter(4, 100, 'low', analog=True)  # 4阶低通临界频率为100Hz
w, h = signal.freqs(b, a)  # h为频率响应,w为频率'''
plt.figure(1)
'''plt.semilogx(w, 20 * np.log10(abs(h)))  # 用于绘制折线图，两个函数的 x 轴、y 轴分别是指数型的，并且转化为分贝
plt.title('Butterworth filter frequency response')
plt.xlabel('Frequency [radians / second]')
plt.ylabel('Amplitude [dB]')
plt.margins(0, 0.1)  # 去除画布四周白边
plt.grid(which='both', axis='both')  # 生成网格，matplotlin.pyplot.grid(b, which, axis, color, linestyle, linewidth， **kwargs)， which : 取值为'major', 'minor'， 'both'
plt.axvline(100, color='green')  # 绘制竖线
#plt.show()
'''

sample_rate=400
duration=1
t = np.linspace(0, duration, sample_rate*duration, False)  # 1秒，1000赫兹刻度
sig = np.sin(2*np.pi*5*t) + np.sin(2*np.pi*200*t)+np.sin(2*np.pi*80*t)# 合成信号

fig, (ax1, ax2,ax3) = plt.subplots(3, 1, sharex=True)  # 2行1列的图

ax1.plot(t, sig)
ax1.set_title('10 Hz and 20 Hz sinusoids')
ax1.set_xlim(0, duration)
ax1.set_ylim(-2, 2)  # 坐标范围



sample_count=len(sig)

xFFT = np.abs(np.fft.rfft(sig)/sample_count)  #快速傅里叶变换
xFreqs = np.linspace(0, sample_rate//2, sample_count//2+1) * 60




ax2.plot(xFreqs,xFFT)
ax2.set_title('10 Hz and 20 Hz sinusoids')
ax2.set_xlim(0, 600)
ax2.set_ylim(0, 0.6)  # 坐标范围
'''
x=xFreqs[40:52]
y=xFFT[40:52]
print(x,y)
start=x[0]
end=x[-1]
ax2.plot(x,y)
ax2.set_title('10 Hz and 20 Hz sinusoids')
ax2.axis([start, end, 0, 0.6])  # 坐标范围'''
#plt.show(block=True)

#sos = signal.butter(10, 15, 'hp', fs=1000, output='sos')  #10阶，15赫兹
sos = signal.butter(10, 100, btype='lowpass', analog=False, output='sos', fs=sample_rate)
filtered = signal.sosfilt(sos, sig)  # 滤波
ax3.plot(t, filtered)
ax3.set_title('After 15 Hz high-pass filter')
ax3.set_xlim(0, duration)
ax3.set_ylim(-2, 2)
ax3.set_xlabel('Time [seconds]')
#plt.tight_layout()
plt.show(block=True)
