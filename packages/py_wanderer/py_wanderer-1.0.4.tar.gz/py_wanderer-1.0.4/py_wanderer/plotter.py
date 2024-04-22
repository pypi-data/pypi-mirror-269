try:
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
    from matplotlib.axes import Axes
    from matplotlib import cm
    from matplotlib.colors import Normalize

except ImportError:
    print("You need to install matplotlib to use this module.")
    exit(1)

from .maze import Maze


def plot_maze_with_paths(maze: Maze, paths: list[tuple[str, list[tuple[int, int]]]]) -> Figure:
    """Plot the maze with the paths."""
    fig, ax = plt.subplots()
    ax.axis('off')
    ax.matshow(maze.maze, cmap="gray")

    cmap = cm.get_cmap("tab20")
    norm = Normalize(0, len(paths))

    for i, (name, path) in enumerate(paths):
        color = cmap(norm(i))
        ax.plot([y for x, y in path], [x for x, y in path], color=color, linewidth=2)
        ax.plot(path[0][1], path[0][0], 'o', color=color, markersize=5, label=f"{name} ({len(path) - 1} steps)")

    ax.plot(maze.start[1], maze.start[0], "go", markersize=10, label="Start")
    ax.plot(maze.end[1], maze.end[0], "ro", markersize=10, label="End")

    ax.invert_yaxis()

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=3)

    return fig
