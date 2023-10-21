import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import math

from collections import defaultdict

def sum_nested_dict(nested_dict):
    """Sums the values of nested dictionaries, keeping the structure intact."""

    result = defaultdict(list)
    for key, value in nested_dict.items():
        if isinstance(value, dict):
            result[key] = sum_nested_dict(value)
        else:
            result[key] = sum(value)

    return dict(result)

data = {
    'ObjBase': {'rom': {'Baseline': [134], 'Dev': [116], 'Min': [28]}, 'ram': {'Baseline': [84], 'Dev': [84], 'Min': [4]}},
    'ActiveLogger': {'rom': {'Baseline': [5384, 1024], 'Dev': [5384, 1024], 'Min': [3120, 966]}, 'ram': {'Baseline': [1860], 'Dev': [1784], 'Min': [812]}},
    'BufferManager': {'rom': {'Baseline': [2468, 1110], 'Dev': [2468, 1110], 'Min': [1492, 760]}, 'ram': {'Baseline': [968], 'Dev': [924], 'Min': [272]}}, 'CmdDispatcher': {'rom': {'Baseline': [8382, 1426], 'Dev': [8174, 1414], 'Min': [4372, 1248]}, 'ram': {'Baseline': [10184], 'Dev': [5856], 'Min': [2564]}}, 'CmdSequencer': {'rom': {'Baseline': [14526, 4834], 'Dev': [14526, 4834], 'Min': [8016, 4574]}, 'ram': {'Baseline': [2296], 'Dev': [2200], 'Min': [908]}}, 'Framer': {'rom': {'Baseline': [1288, 464], 'Dev': [1288, 464], 'Min': [584, 380]}, 'ram': {'Baseline': [3088], 'Dev': [3028], 'Min': [2228]}}, 'Deframer': {'rom': {'Baseline': [1632, 998], 'Dev': [1632, 998], 'Min': [710, 716]}, 'ram': {'Baseline': [824], 'Dev': [780], 'Min': [140]}}, 'FileManager': {'rom': {'Baseline': [10586, 1240], 'Dev': [10586, 1240], 'Min': [5716, 1220]}, 'ram': {'Baseline': [1216], 'Dev': [1152], 'Min': [340]}}, 'FileUplink': {'rom': {'Baseline': [4562, 1166], 'Dev': [4562, 1166], 'Min': [2456, 1124]}, 'ram': {'Baseline': [1284], 'Dev': [1228], 'Min': [496]}}, 'FileDownlink': {'rom': {'Baseline': [8340, 3216], 'Dev': [8190, 3216], 'Min': [4690, 2798]}, 'ram': {'Baseline': [2648], 'Dev': [2556], 'Min': [1344]}}, 'PassiveRateGroup': {'rom': {'Baseline': [1088, 382], 'Dev': [1088, 378], 'Min': [648, 264]}, 'ram': {'Baseline': [1456], 'Dev': [780], 'Min': [140]}}, 'TlmChan': {'rom': {'Baseline': [1740, 1028], 'Dev': [1740, 1028], 'Min': [934, 888]}, 'ram': {'Baseline': [17856], 'Dev': [12784], 'Min': [12224]}}}
data = sum_nested_dict(data)


def magic_plot(ax, components:list[str], memory_type:str, bar_width=0.2, spacing=0.02):
    assert memory_type in ['ram', 'rom'], memory_type


    ram_colors = [sns.color_palette("dark:#5A9_r")[idx] for idx in [0,1,2]]
    rom_colors = [sns.color_palette("flare")[idx] for idx in [0,1,3]]
    colors = (ram_colors if memory_type == "ram"
                    else rom_colors)

    baseline_data = [data[comp][memory_type]["Baseline"] for comp in components]
    dev_data = [data[comp][memory_type]["Dev"] for comp in components]
    min_data = [data[comp][memory_type]["Min"] for comp in components]

    x_axis = np.arange(len(components))
    ax.bar(x_axis - bar_width - spacing, baseline_data, bar_width, label = "Baseline", color=colors[0])
    ax.bar(x_axis, dev_data, bar_width, label = 'Dev', color=colors[1])
    ax.bar(x_axis + bar_width + spacing, min_data, bar_width, label = 'Min', color=colors[2])

    for x_off, cur_data in [(- bar_width - spacing, baseline_data), (0, dev_data), (bar_width + spacing, min_data)]:
        for i, val in enumerate(cur_data):
            ax.text(x_axis[i] + x_off + 0.01, 2**(math.log2(val) - 0.3), '{:,}'.format(val).replace(',', ' '), rotation=90, ha='center', va='top')

    ax.set_yscale('log') 
    ax.set_xticks(x_axis, components, fontsize=11, fontweight='semibold')
    title_mem_type = 'RAM' if memory_type == "ram" else "Flash"
    ax.set_ylabel(f"{title_mem_type} usage", fontsize=11, fontweight='semibold')

    custom_y_ticks = [2**i for i in range(1, 16)]  # Custom tick locations
    custom_y_tick_labels = [str(x) if x < 1000 else f'{x // 1024}KB' for x in custom_y_ticks]  # Custom tick labels

    # Set the custom y ticks
    ax.set_yticks(custom_y_ticks, custom_y_tick_labels)
    # plt.yticks([        0, 100, 1000
    #     ], fontsize=11)

    legend = ax.legend(
        #title=f'Build type',alignment='center', title_fontsize=10,
        fontsize=13, prop={'weight': 'bold'})
    ax.grid(axis='x')

components = [
    "TlmChan",
    "CmdSequencer", 
    "CmdDispatcher",
    "FileManager",
    "PassiveRateGroup",
    "ObjBase",
]

plt.style.use(['seaborn-v0_8'])
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))


magic_plot(ax1, components=components, memory_type='ram', bar_width=0.2)
magic_plot(ax2, components=components, memory_type='rom', bar_width=0.2)

ax1.set_title(f'RAM and Flash Usage of Standard Components in LedBlinker', fontweight='bold' ,fontsize=15, pad=18)
plt.savefig(f'ram_flash_components.pdf', bbox_inches='tight')
plt.show()