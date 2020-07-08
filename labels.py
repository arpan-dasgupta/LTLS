import math
import numpy as np


def create_matrix(num_edges, num_labels):
    """
    Creates matrix to map a label to a edge
    TODO - Complete this
    TODO - Make this independent of graph structure?
    """
    mat = np.zeros((num_edges, num_labels))

    for i in range(num_labels):
        pass

    label_params = {"num_edges": num_edges, "matrix": mat}

    return label_params


def get_edges(label_num, label_params):
    """
    Given label number returns edges in a list
    """
    num_edges = label_params["num_edges"]
    matrix = label_params["matrix"]
    edges = []
    for i in range(num_edges):
        if matrix[i][label_num] == 1:
            edges.append(i)

    return edges


def get_label(edges, label_params):
    """
    Edge list to label number
    TODO Complete this
    """


def get_smallest_positive_path(paths, y_row, label_params):
    """
    Out of the paths given, find +ve path lowest in rank
    """


def get_largest_negative_path(paths, y_row, label_params):
    """
    Out of the paths given, find +ve path lowest in rank
    """


def update_values(positive_path, negative_path, output):
    """
    Given two sets of edges, update the edges in positive with +x and -ve with -x
    If no need of update, return 1 else 0
    """


if __name__ == "__main__":
    create_matrix(4, 10)
