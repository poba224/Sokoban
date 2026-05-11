import time
import os
import matplotlib.pyplot as plt

import astar
import bfs
#import dfs


# Solverek listaja
solvers = [
    ("BFS", bfs.solve),
#    ("DFS", dfs.solve),
    ("A*", astar.solve),
]


def plot_results(ax, results, value_index, title, ylabel, level_names, tick_labels):
    for solver in solvers:
        name = solver[0]
        xs = []
        ys = []
        for result in results:
            if result[1] == name:
                xs.append(result[0])
                ys.append(result[value_index])
        ax.plot(xs, ys, marker="o", label=name)
    ax.set_title(title)
    ax.set_xlabel("pálya")
    ax.set_ylabel(ylabel)
    ax.set_xticks(level_names)
    ax.set_xticklabels(tick_labels)
    for index in range(len(level_names)):
        if (index + 1) % 5 == 0:
            ax.axvline(level_names[index], color="lightgray", linewidth=1.5, zorder=0)
    ax.legend()
    ax.grid(True, axis="y")


def main():
    results = []
    level_names = []

    # Csak a szamozott palyak
    for name in sorted(os.listdir("levels")):
        if name[:2].isdigit() and name.endswith(".txt"):
            level_names.append(name)

    tick_labels = []
    for index in range(len(level_names)):
        if (index + 1) % 5 == 0:
            short_name = level_names[index].replace(".txt", "")
            tick_labels.append(short_name)
        else:
            tick_labels.append("")

    # Palyamnkent lefuttatja a solvereket
    for level_name in level_names:
        level_path = "levels/" + level_name
        board = bfs.load_level(level_path)

        for name, solve_fn in solvers:
            print(name + " " + level_name)

            t0 = time.time()
            solution = solve_fn(board)
            elapsed = time.time() - t0
            hossz = 0
            if solution is not None:
                hossz = len(solution)
            results.append((level_name, name, elapsed, hossz))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Megoldasi idok
    plot_results(ax1, results, 2, "Megoldási idő solverenként", "idő (s)", level_names, tick_labels)

    # Megoldas hosszak
    plot_results(ax2, results, 3, "Megoldás hossza solverenként", "lépésszám", level_names, tick_labels)

    plt.tight_layout()
    plt.show()


main()
