import os
import glob
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from collections import defaultdict
import json
from collections import defaultdict


csv_folder = os.path.join("graph-bench", "results_induscrial")
csv_files = glob.glob(os.path.join(csv_folder, "*.csv"))


data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
graph_names = []

for file in csv_files:
    with open(file, "r", encoding="utf-8") as f:
        current_algo = None
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split(",")]  # запихнули все в массивы, элементы делятся по запятой

            if len(parts) == 1:  # значит.  название алгоритма
                current_algo = parts[0]

            elif parts[0].lower() == "graph":
                continue
            elif len(parts) == 3 and current_algo is not None:
                graph_name = parts[0]
                spla_time = float(parts[1])
                lagraph_time = float(parts[2])
                graph_names.append(graph_name)
                data[current_algo][graph_name]["spla"].append(spla_time)
                data[current_algo][graph_name]["lagraph"].append(lagraph_time)


graph_names = set(graph_names)


algo_names = ["bfs", "sssp", "pr", "tc"]

for x in data.keys():
    for y in data[x].keys():
        # print(y)
        for z in data[x][y]:
            data[x][y][z] = round((sum(data[x][y][z]) / len(data[x][y][z])), 2)


print(json.dumps(data, ensure_ascii=False, indent=4)) # выводим среднее


datasets = sorted(list(graph_names))

colors = {
    "spla": "#4C72B0",
    "lagraph": "#DD8452",  }

fig, axs = plt.subplots(2, 2, figsize=(15, 11))
axs = (axs.flatten())

x = np.arange(len(datasets)) 
width = 0.35  # ширина одного столбц 

for i, algo in enumerate(algo_names):
    ax = axs[i]

    times_spla = [data[algo][dataset].get("spla", 0) for dataset in datasets]
    times_lagraph = [data[algo][dataset].get("lagraph", 0) for dataset in datasets]

    rects1 = ax.bar(x - width / 2,times_spla,width,label="SPLA",color=colors["spla"],edgecolor="#7f7f7f",linewidth=0.5,    )
    rects2 = ax.bar(x + width / 2, times_lagraph, width, label="LAGraph", color=colors["lagraph"], edgecolor="#7f7f7f", linewidth=0.5, )

    ax.set_facecolor("#ececec")
    ax.set_axisbelow(True)  
    ax.grid(True, which="both", color="white", linestyle="-", linewidth=0.8)
    ax.set_yscale("log")
    ax.set_title(algo.upper(), fontsize=14, fontweight="bold", pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(datasets, rotation=45, ha="right", fontsize=10)

    if i in [0, 2]:
        ax.set_ylabel("Speedup", fontsize=12, fontweight="semibold")

    if i == 3:
        ax.legend(loc="upper right", frameon=True, facecolor="white", edgecolor="none", fontsize=11,)

plt.tight_layout()
plt.show()
