"""
Figure: network percolation

@auth: Yu-Hsiang Fu
@date: 2015/12/14
@update: 2018/03/21
"""
# --------------------------------------------------------------------------------
# 1.Import modular
# --------------------------------------------------------------------------------
# import modular
import matplotlib.pyplot as plt
import numpy as np

# import custom-modular
import util.handler.pickle_handler as ph

# import constant
from util.constant.constant_folder import FOLDER_FILE
from util.constant.constant_folder import FOLDER_IMAGE


# --------------------------------------------------------------------------------
# 2.Defile variable
# --------------------------------------------------------------------------------
NUM_SIMULATION = 100
PERCOLATION_MODE = "bond"

# plot
# COLOR_LIST = ['gray', 'orange', 'y', 'b', 'c', 'm', 'r', 'k']
# MARKER_LIST = ['o', '^', 'v', '8', 'H', 's', 'D', 'x', '+']
PLOT_DPI = 300
PLOT_FORMAT = 'png'
PLOT_LAYOUT_PAD = 0.1
PLOT_X_SIZE = 4
PLOT_Y_SIZE = 4


# --------------------------------------------------------------------------------
# 3.Defile function
# --------------------------------------------------------------------------------
def draw_percolation_result(filename_list, percolation_result):
    # prepare data
    data = {}
    xtick_labels = []

    for net_name in sorted(filename_list):
        if not xtick_labels:
            xtick_labels = [p for p in sorted(percolation_result[net_name].keys())]
        else:
            pass

        data[net_name] = [percolation_result[net_name][p] for p in xtick_labels]

    # --------------------------------------------------
    # create a figure
    fig, ax = plt.subplots(figsize=(PLOT_X_SIZE, PLOT_Y_SIZE), facecolor='w')

    # plot setting
    ax.grid(color="gray", linestyle="dotted", linewidth=0.5)
    ax.locator_params(axis="x", nbins=11)
    ax.set_xlim(-0.01, len(xtick_labels) + 0.01)
    ax.set_ylim(-0.01, 1.01)
    ax.set_xlabel("%-occupied, p", fontdict={'fontsize': 10})
    ax.set_ylabel("%-nodes of gcc, s", fontdict={'fontsize': 10})
    ax.set_xticklabels([str(round(p, 1)) for p in np.arange(-0.1, 1.1, 0.1)])
    ax.tick_params(axis="both", direction="in", which="major", labelsize=8)

    # draw plot
    # marker_index = 0

    for net_name in filename_list:
        _marker = "o"
        # _marker = MARKER_LIST[marker_index]
        # marker_index += 1
        ax.axes.plot(data[net_name], linewidth=1, marker=_marker, markersize=4, markevery=1, fillstyle="none")

    # legend-text
    ax.legend(filename_list, loc=2, fontsize='medium', prop={'size': 6}, ncol=1, framealpha=0.5)

    # save image
    image_path = '{0}network-percolation-{1}, sim={2}.{3}'
    image_path = image_path.format(FOLDER_IMAGE, PERCOLATION_MODE, NUM_SIMULATION, PLOT_FORMAT)
    plt.tight_layout(pad=PLOT_LAYOUT_PAD)
    plt.savefig(image_path, dpi=PLOT_DPI, format=PLOT_FORMAT)
    plt.close()


# --------------------------------------------------------------------------------
# 4.Main function
# --------------------------------------------------------------------------------
def main_function():
    # test networks
    # filename_list = ["regular_n=1000_k=5"]
    #
    filename_list = ["ba_n=1000_k=5",
                     "random_n=1000_k=5",
                     "regular_n=1000_k=5",
                     "sw_n=1000_k=5_p=0.1"]
    #
    # --------------------------------------------------
    # percolation variable
    print(" - Read pickle files:")
    global NUM_SIMULATION, PERCOLATION_MODE
    NUM_SIMULATION = 100
    PERCOLATION_MODE = "bond"

    percolation_result = {}

    for net_name in filename_list:
        print(" -- Network: {0}".format(net_name))
        file_path = '{0}{1}, sim={2}, percolation-{3}.pickle'
        file_path = file_path.format(FOLDER_FILE, net_name, NUM_SIMULATION, PERCOLATION_MODE)
        percolation_result[net_name] = ph.read_pickle_file(file_path)

    # --------------------------------------------------
    print(" - Draw percolation results")
    draw_percolation_result(filename_list, percolation_result)


if __name__ == '__main__':
    main_function()
