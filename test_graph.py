from graph import *

train_specs = {"num_labels": 10}
graph_params = create_graph(train_specs)
cgp = {'num_layers': 4, 'num_nodes': 9, 'adj_list': [[1, 2], [4, 3], [4, 3], [6, 5, 8], [6, 5], [7], [7], [8], []], 'edges': [[0, 1], [0, 2], [1, 4], [1, 3], [2, 4], [2, 3], [3, 6], [3, 5], [3, 8], [
    4, 6], [4, 5], [5, 7], [6, 7], [7, 8]], 'edge_map': {'0:1': 0, '0:2': 1, '1:4': 2, '1:3': 3, '2:4': 4, '2:3': 5, '3:6': 6, '3:5': 7, '3:8': 8, '4:6': 9, '4:5': 10, '5:7': 11, '6:7': 12, '7:8': 13}}
assert(graph_params == cgp)

weights = [5, 1, 1, 6, 1, 1, 4, 2, 20, 3, 4, 1, 1, 1]
paths = get_top_k(graph_params, 6, weights)
# print(paths)
assert(paths == [[8, 3, 0], [8, 5, 1], [13, 12, 6, 3, 0], [
       13, 11, 7, 3, 0], [13, 11, 10, 2, 0], [13, 12, 9, 2, 0]])
