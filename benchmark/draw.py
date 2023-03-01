# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np



barWidth = 0.25
fig = plt.figure(num=1, figsize =(8, 6))
plt.subplot(111)

plt.title('10 connections',fontsize=15)

sidecar_qps = [99.5,488.2,907.5,1805.6, 1259.8]
sidecar_99_latency = [3.85,4.14,13.1,45.63,58.62] # ms
no_sidecar_qps = [98.2,498.1,993.4,4384.9,6911.2]
no_sidecar_99_latency = [1,1.03,0.86,1.3,1.83]
input_qps = [100,500,1000,5000,10000]


br1 = np.arange(len(sidecar_qps))
b2 = [i + barWidth for i in br1]
# width：柱子的宽度；facecolor：柱子填充色；edgecolor：柱子轮廓色；lw：柱子轮廓的宽度；
plt.bar(br1, sidecar_qps,width = barWidth,  facecolor = 'deeppink', edgecolor = 'deeppink', lw=1, label ='sidecar')
plt.bar(b2, no_sidecar_qps,  width = barWidth,   facecolor = 'darkblue', edgecolor = 'darkblue', lw=1, label ='no_sidecar')

plt.xlabel(u'Input QPS',fontsize=10)
plt.ylabel(u'Output QPS',fontsize=10)
plt.xticks([r + barWidth for r in range(len(sidecar_qps))],
        input_qps)
plt.grid(visible=True, axis='y', linestyle='--', linewidth=1, alpha=0.5)

plt.legend(loc="upper left")


ax2 = plt.twinx()
ax2.set_ylabel(u'99th latency(ms)',fontsize=10)
plt.plot(sidecar_99_latency, color='deeppink',  label='sidecar')
plt.plot(no_sidecar_99_latency, color='darkblue',  label='no_sidecar')

plt.show()

