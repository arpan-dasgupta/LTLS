from load_train_dot import get_train_data

from graph import *
from model import *
from labels import *
from config import *

train_specs, x, y = get_train_data()

x_train = x[0:5991]
y_train = y[0:5991]
x_test = x[5991:]
y_test = y[5991:]
test_specs = {}
test_specs['test_length'] = train_specs['train_length'] - 5991
train_specs['train_length'] = 5991


graph_params = create_graph(train_specs)
model = assign_edges(graph_params, train_specs)
# print(graph_params)
# print(train_specs)
label_params = create_matrix(train_specs['num_labels'], graph_params)
for i in range(train_specs['train_length']):
    x_row = x_train[i]
    y_row = y_train[i]
    num_positive = len(y_row)
    count = 0
    loss_prev = 100
    while True:
        weights = model.get_predictions(x_row)
        paths = get_top_k(graph_params, num_positive+1, weights)
        vp, pos = get_smallest_positive_path(y_row, label_params, weights)
        vn, neg = get_largest_negative_path(
            y_row, paths, label_params, weights)
        loss = max(0, 1+vn-vp)
        if loss > loss_prev:
            count += 1
        if count > 100:
            print("exec")
            break
        # print(loss)
        if loss < 1.1:
            break
        temp = [0 for i in range(len(weights))]
        update_values(pos, neg, temp)
        model.update(x_row, temp)
        loss_prev = loss
    print(" ", (i/train_specs['train_length'])*100, end='\r')
print()


p_1 = 0
for i in range(test_specs['test_length']):
    x_row = x_test[i]
    y_row = y_test[i]
    weights = model.get_predictions(x_row)
    paths = get_top_k(graph_params, 1, weights)
    label = get_label(paths[0], label_params)
    if label in y_row:
        p_1 += 1
print((p_1/test_specs['test_length']))
