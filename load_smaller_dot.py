import gc
from scipy import sparse
import pickle
from sklearn.preprocessing import normalize
from config import DATA_FILE_PATH, TRAIN_SPLITS, TEST_SPLITS


'''
The data files for all the datasets are in the following sparse representation format:
Header Line: Total_Points Num_Features Num_Labels
1 line per datapoint : label1,label2,...labelk ft1:ft1_val ft2:ft2_val ft3:ft3_val .. ftd:ftd_valsour
'''


def get_data():
    # READ TRAINING FILE

    f = open(DATA_FILE_PATH)
    size = f.readline()
    nrows, nfeature, nlabel = [int(s) for s in size.split()]

    x_m, pos, y_m = [[[]] * nrows] * 3

    for i in range(nrows):
        line = f.readline()
        temp = [s for s in line.split(sep=' ')]
        pos[i] = [int(s.split(':')[0]) for s in temp[1:]]
        x_m[i] = [float(s.split(':')[1]) for s in temp[1:]]
        for s in temp[0].split(','):
            try:
                int(s)
                y_m[i] = [int(s) for s in temp[0].split(',')]
            except ValueError:
                y_m[i] = []

    x_mod = sparse.lil_matrix((nrows, nfeature))
    for i in range(nrows):
        for j in range(len(pos[i])):
            x_mod[i, pos[i][j]] = x_m[i][j]

    del x_m, pos
    gc.collect()

    f.close()

    f1 = open(TRAIN_SPLITS)
    f2 = open(TEST_SPLITS)

    split_no = 4
    x_train = sparse.lil_matrix((4880, nfeature))
    y_train = []
    x_test = sparse.lil_matrix((2515, nfeature))
    y_test = []

    for i in range(4880):
        vals = f1.readline()
        vals = [int(s) for s in vals.split()]
        x_train[i] = x_mod[vals[split_no]-1]
        y_train.append(y_m[vals[split_no]-1])

    for i in range(2515):
        vals = f2.readline()
        vals = [int(s) for s in vals.split(sep=' ')]
        x_test[i] = x_mod[vals[split_no]-1]
        y_test.append(y_m[vals[split_no]-1])

    f1.close()
    f2.close()

    x_train = normalize(x_train, norm='l2', axis=1, copy=False)
    x_test = normalize(x_test, norm='l2', axis=1, copy=False)

    train_specs = {
        'train_length': x_train.shape[0],
        'num_features': x_train.shape[1],
        'num_labels': nlabel
    }

    test_specs = {
        'test_length': x_test.shape[0]
    }

    print("Training dataset is created")
    # print(y_m[0])

    return train_specs, x_train, y_train, test_specs, x_test, y_test


if __name__ == "__main__":
    get_data()
