# from load_train_dot import get_train_data

# from graph import *
# from labels import *
# from config import *
# from model import *


# train_specs, x_train, y_train = get_train_data()

# graph_params = create_graph(train_specs)
# model = assign_edges(graph_params, train_specs)
# print(graph_params)
# print(train_specs)
# # print(create_matrix(train_specs['num_labels'], graph_params))
# # print(model)
# label_params = create_matrix(train_specs['num_labels'], graph_params)
# for i in label_params['matrix']:
#     for j in range(len(i)):
#         if i[j]:
#             print(list(graph_params['edge_map'].keys())[
#                   list(graph_params['edge_map'].values()).index(j)], end=", ")
#     print()


from load_train_dot import get_train_data

from graph import *
from model import *
from labels import *
from config import *

train_specs, x_train, y_train = get_train_data()

graph_params = create_graph(train_specs)
model = assign_edges(graph_params, train_specs)
# print(graph_params)
# print(train_specs)
label_params = create_matrix(train_specs['num_labels'], graph_params)
for i in range(train_specs['num_features']):
    x_row = x_train[i]
    y_row = y_train[i]
    num_positive = len(y_row)
    while True:
        weights = model.get_predictions(x_row)
        # print(weights)
        paths = get_top_k(graph_params, num_positive+1, weights)
        # print(paths)
        vp, pos = get_smallest_positive_path(y_row, label_params, weights)
        vn, neg = get_largest_negative_path(
            y_row, paths, label_params, weights)
        # print(pos)
        # print(pos,neg)
        if vp >= vn + ADD_VALUE:
            break
        update_values(pos, neg, weights)
        model.update(x_row, weights)
        print(vp, vn)
        # print(weights)
        # break
    break
