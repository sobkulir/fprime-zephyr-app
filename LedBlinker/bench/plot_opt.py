import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

import seaborn as sns

# Use the Seaborn style
plt.style.use(['seaborn'])

ram = np.array([
    ['baseline', 267678],
    ['No Object/Port Tracing\nNo Port Serialization', 266049],
    # ['rtgr', 244009],
    # ['cmd', 243369],
    # ['buf', 237145],
    ['Tighter Buffer Sizes', 248825],
    ['Tighter Heap Size', 223825],
    ['No Object Names', 206965],
])

ram_names = ram[:, 0]
ram_values = list(map(lambda x: int(x) - (16 * 1024), ram[:, 1]))

flash = np.array([
    ['baseline', 247686],
    ['No Port Serialization', 242414],
    ['CRC Assert', 232782],
    ['No Text Logging', 214246],
    ['No Object Names', 206926],
    ['No Assert', 175466]
])

flash_names = flash[:, 0]
flash_values = list(map(int, flash[:, 1]))

fig, ax = plt.subplots(figsize=(12, 8))

# Stacked bar chart with loop
RAM_X=1.7
RAM_colors = sns.color_palette("dark:#5A9_r")
for i in range(ram.shape[0]):
  ax.bar(RAM_X, ram_values[i], color=RAM_colors[ram.shape[0]-1-i], bottom = 0, width=2)
  if i != 0:
    plt.text(RAM_X + 1.1, ram_values[i] - (2000 if i == 1 else 0), ram_names[i], rotation=15, fontsize=14, fontweight='normal', ha='left')

plt.text(RAM_X, ram_values[0]+1000, 'Baseline', fontsize=12, fontweight='bold', ha='center')
plt.text(RAM_X, ram_values[3]+1000, 'Dev', fontsize=12, fontweight='bold', ha='center')
plt.text(RAM_X, ram_values[-1]+1000, 'Min', fontsize=12, fontweight='bold', ha='center')

FLASH_X = 6.7
FLASH_colors = sns.color_palette("flare")
for i in range(flash.shape[0]):
  ax.bar(FLASH_X, flash_values[i], color=FLASH_colors[flash.shape[0]-1-i], bottom = 0, width=2)
  if i != 0:
    plt.text(FLASH_X + 1.1, flash_values[i], flash_names[i], rotation=15, fontsize=14, fontweight='normal', ha='left')

plt.text(FLASH_X, flash_values[0]+1000, 'Baseline', fontsize=12, fontweight='bold', ha='center')
plt.text(FLASH_X, flash_values[1]+1000, 'Dev', color='white', alpha=0.6, fontsize=12, fontweight='bold', ha='center')
plt.text(FLASH_X, flash_values[-1]+1000, 'Min', fontsize=12, fontweight='bold', ha='center')


ax.set_ylim(ymin=150*1024)
ax.set_xlim(xmin=0,xmax=10)

plt.title("RAM and Flash Usage Optimization of LedBlinker", fontweight='bold' ,fontsize=17, pad=20)

def bytes_to_kilobytes(bytes, pos):
    kilobytes = bytes / 1024
    return f'{int(kilobytes)}KB'

# Set the custom tick formatter for y-axis
plt.gca().yaxis.set_major_formatter(FuncFormatter(bytes_to_kilobytes))

plt.text(-0.1, ram_values[0] + 10000, '[Size]', fontsize=13, fontweight='bold', ha='right')
plt.yticks([
  ram_values[0],
  *ram_values[2:],
  *flash_values[:2],
  flash_values[3],
  *flash_values[5:],
  150*1024,
  ], fontsize=13)
plt.xticks([RAM_X, FLASH_X], ['RAM', 'Flash'], fontsize=13, fontweight='semibold')

plt.grid(axis='x')

# plt.savefig('ram_flash_opt.pdf', bbox_inches='tight')
plt.show()

