import math
import numpy as np

from graph import get_top_k


def assign(u, mat, i, graph):
    if u == graph['num_nodes']:
        return [i]
    ret = []
    for index in range(len(graph['adj_list'][u])):
        nxt = graph['adj_list'][u][index]
        nxt_index = max(ret + [i-1]) + 1
        new_ret = assign(nxt, mat, nxt_index, graph)
        for n_index in new_ret:
            mat[n_index][graph['edge_map'][str(u) + ":" + str(nxt)]] = 1
        ret += new_ret
    return ret


def create_matrix(num_labels, graph):
    """
    Creates matrix to map a label to a edge
    TODO - Complete this
    TODO - Make this independent of graph structure?
    Note: Assuming 1
    """
    num_edges = len(graph['edges'])
    mat = np.zeros((num_labels, num_edges))

    assign(0, mat, 0, graph)

    label_params = {"num_edges": num_edges, "matrix": mat}

    return label_params


def get_path(label, label_params, weights):
    """
    Given label number returns edges in a list
    """
    matrix = label_params["matrix"]
    path = []
    val = 0
    for i in range(len(matrix[label])):
        if matrix[label][i]:
            path.append(i)
            val += weights[i]

    return val, path


def get_label(edges, label_params):
    """
    Edge list to label number
    TODO Complete this
    """


def get_smallest_positive_path(y_row, label_params, weights):
    """
    Out of the paths given, find +ve path lowest in rank
    """
    val, path = 0, []
    for label in y_row:
        cur_val, cur_path = get_path(label, label_params, weights)
        if cur_val < val:
            val, path = cur_val, cur_path
    return val, path


def get_largest_negative_path(y_row, graph, weights):
    """
    Out of the paths given, find +ve path lowest in rank
    """
    res = get_top_k(graph, len(y_row) + 1, weights)
    print(res)


def update_values(positive_path, negative_path, output):
    """
    Given two sets of edges, update the edges in positive with +x and -ve with -x
    If no need of update, return 1 else 0
    """


if __name__ == "__main__":
    print(create_matrix(4, 10))
