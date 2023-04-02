# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import json
import os

input_qps = []
# generate data from 100 to 5000
for i in range(0, 5001, 500):
    if i == 0:
        input_qps.append(100)
    else:
        input_qps.append(i)
sidecar_qps = [0] * len(input_qps)
no_sidecar_qps = [0] * len(input_qps)
p99_sidecar_latency = [0] * len(input_qps)
p99_no_sidecar_latency = [0] * len(input_qps)
folder_path = "./data"
for file_name in os.listdir(folder_path):
    if file_name.find("no") != -1:
        with open(folder_path + "/" + file_name, "r") as f:
            data = json.load(f)
            input = file_name.split("_")
            index = int(input[0]) //500
            no_sidecar_qps[index] = data["ActualQPS"]
            p99_no_sidecar_latency[index] = data["DurationHistogram"]["Percentiles"][3]["Value"] * 1000
    elif file_name.find("sidecar") != -1:
        with open(folder_path + "/" + file_name, "r") as f:
            data = json.load(f)
            input = file_name.split("_")
            index = int(input[0]) //500
            sidecar_qps[index] = data["ActualQPS"]
            p99_sidecar_latency[index] = data["DurationHistogram"]["Percentiles"][3]["Value"] * 1000

# # ms
actual_qps = {
    "sidecar": sidecar_qps,
    "no_sidecar":no_sidecar_qps
}

actual_p99_latency = {
    "p99_sidecar": p99_sidecar_latency,
    "p99_no_sidecar": p99_no_sidecar_latency
}

fig, ax = plt.subplots(1,2)
ax1 = ax[0]


x  = np.arange(len(input_qps)) # the label locations
barWidth = 0.25  # the width of the bars
multiplier = 0

for attribute, measurement in actual_qps.items():
    offset = barWidth * multiplier
    rects = ax1.bar(x + offset, measurement, barWidth, label=attribute)
    # ax1.bar_label(rects, padding=3)
    multiplier += 1



# ax1.set_title('10 connections',fontsize=15)
ax1.set_xlabel(u'Expected QPS',fontsize=20)
ax1.set_ylabel(u'Actual QPS',fontsize=20)
ax1.tick_params(axis='both', which='major', labelsize=15)
ax1.set_xticks(x + barWidth/2, input_qps)
ax1.grid(visible=True, axis='y', linestyle='--', linewidth=1, alpha=0.5)
ax1.legend(loc="upper left")


ax2 = ax[1]
# ax2.set_title('10 connections',fontsize=15)
ax2.set_xlabel(u'Expected QPS',fontsize=20)
ax2.set_ylabel(u'latency, 99th percentile (ms)',fontsize=20)
ax2.set_xticks(x + barWidth/2, input_qps)
ax2.tick_params(axis='both', which='major', labelsize=15)

for attribute, measurement in actual_p99_latency.items():
    ax2.plot(measurement,   label=attribute)



ax2.grid(visible=True, axis='y', linestyle='--', linewidth=1, alpha=0.5)
ax2.legend(loc="upper left", fontsize=15)

plt.show()

