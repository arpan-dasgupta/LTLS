from load_smaller_dot import get_data
import time

from graph import *
from model import *
from labels import *
from config import *

train_specs, x_train, y_train, test_specs, x_test, y_test = get_data()

graph_params = create_graph(train_specs)
model = assign_edges(graph_params, train_specs)
label_params = create_matrix(train_specs['num_labels'], graph_params)

loops_per_epoch = []
loss_per_epoch = []
times = [0 for i in range(6)]
for epoch in range(EPOCHS):
    sum_loops = 0
    sum_loss = 0
    for i in range(train_specs['train_length']):
        x_row = x_train[i]
        y_row = y_train[i]
        num_positive = len(y_row)
        count = 0
        loss_prev = 100
        loop_counter = 0
        while True:
            loop_counter += 1
            t1 = time.perf_counter()
            weights = model.get_predictions(x_row)
            t2 = time.perf_counter()
            paths = get_top_k(graph_params, num_positive+1, weights)
            t3 = time.perf_counter()
            vp, pos = get_smallest_positive_path(y_row, label_params, weights)
            t4 = time.perf_counter()
            vn, neg = get_largest_negative_path(
                y_row, paths, label_params, weights)
            t5 = time.perf_counter()
            loss = max(0, 1+vn-vp)
            if loss_prev-loss <= LOSS_THRESHOLD:
                count += 1
            if count > NUM_ANOMALIES:
                # print("exec")
                sum_loss += loss
                break
            # print(loss)
            # print(pos, neg)
            # print(get_label(pos, label_params), get_label(neg, label_params))
            # print(vp, vn)
            # if loss < 1.08:
            #     break
            temp = [0 for i in range(len(weights))]
            update_values(pos, neg, temp, loss)
            t6 = time.perf_counter()
            model.update(x_row, temp)
            t7 = time.perf_counter()
            times[0] += t2-t1
            times[1] += t3-t2
            times[2] += t4-t3
            times[3] += t5-t4
            times[4] += t6-t5
            times[5] += t7-t6
            loss_prev = loss
        # break
        sum_loops += loop_counter
        print(" ", (i/train_specs['train_length'])*100, end='\r')
    loops_per_epoch.append(sum_loops)
    loss_per_epoch.append(sum_loss/train_specs['train_length'])
    print()
    # break

    p_1 = 0
    for i in range(test_specs['test_length']):
        x_row = x_test[i]
        y_row = y_test[i]
        weights = model.get_predictions(x_row)
        paths = get_top_k(graph_params, 1, weights)
        label = get_label(paths[0], label_params)
        if label in y_row:
            p_1 += 1
    print("Score: ", (p_1/test_specs['test_length']))

print(loops_per_epoch)
print(loss_per_epoch)
print(times)
