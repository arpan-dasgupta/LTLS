import math
import numpy as np

from config import ADD_VALUE
from graph import get_top_k


def assign(u, mat, i, graph):
    if u == graph['num_nodes']-1:
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

    edge_to_label = {}
    for i in range(num_labels):
        cur_edges = mat[i].tolist()
        edges_hot = ""
        for j in range(num_edges):
            if cur_edges[j]:
                edges_hot += '1'
            else:
                edges_hot += '0'
        edge_to_label[edges_hot] = i

    label_params = {"num_edges": num_edges,
                    "matrix": mat, "edge_to_label": edge_to_label}

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
    edge_hot = ""
    for i in range(label_params['num_edges']):
        if i in edges:
            edge_hot += '1'
        else:
            edge_hot += '0'
    return label_params['edge_to_label'][edge_hot]


def get_smallest_positive_path(y_row, label_params, weights):
    """
    Out of the paths given, find +ve path lowest in rank
    """
    val, path = 10**7, []
    for label in y_row:
        cur_val, cur_path = get_path(label, label_params, weights)
        if cur_val < val:
            val, path = cur_val, cur_path
    return val, path


def get_largest_negative_path(y_row, paths, label_params, weights):
    """
    Out of the paths given, find +ve path lowest in rank
    """
    for path in paths:
        label = get_label(path, label_params)
        # print(label)
        if label not in y_row:
            return get_path(label, label_params, weights)


def update_values(positive_path, negative_path, output):
    """
    Given two sets of edges, update the edges in positive with +x and -ve with -x
    If no need of update, return 1 else 0
    """
    for edge in positive_path:
        output[edge] += ADD_VALUE
    for edge in negative_path:
        output[edge] -= ADD_VALUE


if __name__ == "__main__":
    print(create_matrix(4, 10))
