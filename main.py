from load_train_dot import get_train_data

from graph import *
from labels import *
from config import *
from model import *


train_specs, x_train, y_train = get_train_data()

graph_params = create_graph(train_specs)
model = assign_edges(graph_params, train_specs)
print(graph_params)
print(train_specs)
# print(create_matrix(train_specs['num_labels'], graph_params))
# print(model)
label_params = create_matrix(train_specs['num_labels'], graph_params)
for i in label_params['matrix']:
    for j in range(len(i)):
        if i[j]:
            print(list(graph_params['edge_map'].keys())[
                  list(graph_params['edge_map'].values()).index(j)], end=", ")
    print()
