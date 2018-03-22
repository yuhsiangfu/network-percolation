"""
Network percolation

@auth: Yu-Hsiang Fu
@date: 2015/12/13
@update 2018/03/21
"""
# --------------------------------------------------------------------------------
# 1.Import modular
# --------------------------------------------------------------------------------
# import modular
import networkx as nx
import numpy as np
import random as r

# import custom-modular
import util.handler.edgelist_handler as eh
import util.handler.pickle_handler as ph

# import constant
from util.constant.constant_folder import FOLDER_EDGELIST
from util.constant.constant_folder import FOLDER_FILE


# --------------------------------------------------------------------------------
# 2.Define variable
# --------------------------------------------------------------------------------
NEIGHBOR_SET = "neighbor-set"
NUM_SIMULATION = 100
PERCOLATION_MODE = "bond"
PERCOLATION_RATE = []


# --------------------------------------------------------------------------------
# 3.Define function
# --------------------------------------------------------------------------------
def create_network(edge_list):
    g = nx.parse_edgelist(edge_list, nodetype=int)
    g = g.to_undirected()
    g.remove_edges_from(g.selfloop_edges())
    return g


def percolation(g, p):
    # check p
    if p == 1.0:
        return g.number_of_nodes()
    elif p == 0:
        return 0
    else:
        pass

    # --------------------------------------------------
    h = nx.Graph()

    if PERCOLATION_MODE == "bond":
        # select p-% edges to occupy
        num_occupy_edges = int(round(g.number_of_edges() * p))
        occupy_edges = r.sample(g.edges(), num_occupy_edges)

        h.add_edges_from(occupy_edges)
    else:
        # remove p-% nodes from G
        num_occupy_nodes = int(round(g.number_of_nodes() * p))
        occupy_nodes = set(r.sample(g.nodes(), num_occupy_nodes))

        for i in occupy_nodes:
            for j in (g.node[i][NEIGHBOR_SET] & occupy_nodes):
                h.add_edge(i, j)

    # --------------------------------------------------
    # find largest-connected-component
    gcc = list(nx.connected_component_subgraphs(h))

    if gcc:
        return max([c.number_of_nodes() for c in gcc])
    else:
        return 0


def network_percolation(g):
    for i in g:
        g.node[i][NEIGHBOR_SET] = set(g.neighbors(i))

    # percolation
    percolated_result = {}

    for p in sorted(PERCOLATION_RATE):
        print(" --- [P]: {0}".format(p))
        sim_result = 0

        for s in range(0, NUM_SIMULATION):
            if s == 0:
                print(" ---- Simulation: {0}".format(s + 1))
                # print(" ---- Simulation: {0}".format(s + 1), end="")
            elif (s+1) % 10 == 0:
                print(" ---- Simulation: {0}".format(s + 1))
                # print(",{0}".format(s + 1), end="")
            else:
                pass

            sim_result += percolation(g, p)

        percolated_result[p] = (sim_result / (NUM_SIMULATION * g.number_of_nodes()))

        print(" --- [/P]")

    return percolated_result


def save_percolation_result(net_name, percolation_result):
    file_path = "{0}{1}, sim={2}, percolation-{3}.pickle"
    file_path = file_path.format(FOLDER_FILE, net_name, NUM_SIMULATION, PERCOLATION_MODE)
    ph.write_pickle_file(percolation_result, file_path)


# --------------------------------------------------------------------------------
# 4.Main function
# --------------------------------------------------------------------------------
def main_function():
    # test networks
    # filename_list = ["regular_n=1000_k=5"]
    filename_list = ["ba_n=1000_k=5",
                     "random_n=1000_k=5",
                     "regular_n=1000_k=5",
                     "sw_n=1000_k=5_p=0.1"]

    # percolation setting
    global NUM_SIMULATION, PERCOLATION_MODE, PERCOLATION_RATE
    NUM_SIMULATION = 100
    PERCOLATION_MODE = 'bond'  # bond(edges), site(nodes)
    PERCOLATION_RATE = [np.float(np.round(p, 3)) for p in np.arange(0.0, 1.0, 0.005)]
    PERCOLATION_RATE.append(1.0)

    for net_name in filename_list:
        print(" - [Net] {0}:".format(net_name))
        print(" -- Read edge-list file")

        # --------------------------------------------------
        file_path = "{0}{1}.txt".format(FOLDER_EDGELIST, net_name)
        g = create_network(eh.read_edgelist(file_path))

        # --------------------------------------------------
        print(" -- Network percolation ...")
        percolation_result = network_percolation(g)

        # --------------------------------------------------
        print(" -- Save percolation result")
        save_percolation_result(net_name, percolation_result)


if __name__ == '__main__':
    main_function()
