import wfdb
from IPython.display import display
annotation=wfdb.rdann('mit-bih-arrhythmia-database-1.0.0/100', 'atr')
display(annotation.__dict__)

record=wfdb.rdrecord('mit-bih-arrhythmia-database-1.0.0/100', )
display(record.__dict__)
import numpy as np
from scipy import signal
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

plt.figure(1)
siglen=500
duration=siglen/record.fs
t = np.linspace(0, duration, siglen, False)  # 1秒，1000赫兹刻度
fig, (ax1, ax2,ax3) = plt.subplots(3, 1, sharex=True)  # 2行1列的图
sig0=record.p_signal[:siglen,0]
sig1=record.p_signal[:siglen,1]
ax1.plot(t, sig0)
ax1.plot(t, sig1)
ax1.set_title('ECG')
ax1.axis([0, duration, -2, 2])

plt.show(block=True)