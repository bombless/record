import numpy as np
import matplotlib.pyplot as plt

# 参数设置
fs = 1000  # 采样频率
f = 5      # 正弦波频率
T = 1      # 总时间
t = np.linspace(0, T, int(fs*T), endpoint=False)  # 时间向量

# 生成正弦波信号
y = np.sin(2 * np.pi * f * t)

# 应用窗函数
window = np.hanning(len(y))
yw = y * window

# 计算 FFT
Yw = np.fft.fft(yw)
f_values = np.fft.fftfreq(len(yw), d=1/fs)

# 绘制频谱
plt.figure(figsize=(12, 6))
plt.plot(f_values, np.abs(Yw))
plt.title('Frequency Spectrum')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.grid()
plt.show()
