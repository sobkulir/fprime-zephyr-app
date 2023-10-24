import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

import seaborn as sns

def bytes_to_kilobytes(bytes, pos):
    kilobytes = bytes / 1024
    return f'{int(kilobytes)}KB'

# Use the Seaborn style
plt.style.use(['seaborn-v0_8'])

{'ram': {'Components': 45604, 'Component Stacks': 98816, 'F Prime Aux': 2156, 'Zephyr Aux': 1221, 'Zephyr drivers_fs_debug_etc': 9402, 'Zephyr stacks and threads': 14456, 'Heap': 36116}, 'flash': {'F Prime Drv,etc,Os,Topology': 27504, 'F Prime Components': 94671, 'Zephyr Aux': 42368, 'Zephyr Fs,deubg,logging,storage': 39420, 'Zephyr kernel,lib': 17108, 'String constants,other unnamed data': 25731}}
ram = np.array([
["Zephyr All",1221 + 9402 + 14456],
["F Prime\nComponents",45604],
["F Prime\nComponent Stacks\n(8 * 12KB)",98816],
# ["F Prime Aux",2156],
["Heap",36116 + 2156],
# ["Zephyr drivers_fs_debug_etc",9402],
# ["Zephyr stacks and threads",14456],


])

ram_names = ram[:, 0]
ram_values = list(map(lambda x: int(x), ram[:, 1]))

flash = np.array([
["Zephyr printf,\nmalloc, etc",42368],
["Zephyr LittleFS, Debug,\nLogging, Flash Storage",39420],
["Zephyr kernel, lib",17108],
["F Prime Framework",27504],
# The magic constant is there because we counted something twice,
# but it seems to make negligible difference so we remove the diff.
["F Prime\nComponents",94671 - 4800], 
["String constants, etc",25731],

])

flash_names = flash[:, 0]
flash_values = list(map(int, flash[:, 1]))

fig, ax = plt.subplots(figsize=(11, 8))

def plot_bars(tag, names, values, bar_x, colors, width=2):
  for i in range(len(values)):
    if tag == 'ram':
      c = colors[0 if i < 1 else 2]
    else:
      c = colors[0 if i < 3 else 2]
    ax.bar(bar_x, values[i], color=c, edgecolor='black', bottom = sum(values[:i]), width=width)
    plt.text(bar_x, sum(values[:i]) + values[i]/2, names[i], fontsize=14, fontweight='normal', ha='center', va='center')
    plt.text(bar_x + width/2 + 0.1, sum(values[:i]) + values[i]/2, bytes_to_kilobytes(values[i], None), fontsize=14, fontweight='normal', ha='left', va='center')


WIDTH=2.8
RAM_X=2.4
FLASH_X = 7
plot_bars('ram', ram_names, ram_values, RAM_X, sns.color_palette("dark:#5A9_r"), WIDTH)
plot_bars('flash', flash_names, flash_values, FLASH_X, sns.color_palette("flare"), WIDTH)

# ax.set_ylim(ymin=150*1024)
ax.set_xlim(xmin=0,xmax=10)

plt.title("RAM and Flash Usage Breakdown of Dev Build of LedBlinker", fontweight='bold' ,fontsize=17, pad=20)



# Set the custom tick formatter for y-axis
plt.gca().yaxis.set_major_formatter(FuncFormatter(bytes_to_kilobytes))


ram_prefix_sums = [sum(ram_values[:(i+1)]) for i in range(len(ram_values))]
flash_prefix_sums = [sum(flash_values[:(i+1)]) for i in range(len(flash_values))]
plt.yticks([
  *ram_prefix_sums,
  *flash_prefix_sums,
  0,
  ], fontsize=13)

# plt.text(-0.1, flash_prefix_sums[-1] + 16000, '[Size]', fontsize=13, fontweight='bold', ha='right')
plt.ylabel('Total Footprint', labelpad=12, fontsize=15, fontweight='bold')

plt.xticks([RAM_X, FLASH_X], ['RAM', 'Flash'], fontsize=13, fontweight='semibold')

plt.grid(axis='x')

plt.savefig('ram_flash_breakdown.pdf', bbox_inches='tight')
plt.show()

