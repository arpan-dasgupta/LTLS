
from sklearn import neural_network, linear_model
import numpy as np
from scipy import sparse

class Linear:
    """
    Model class 
    Can be replaced by any other model with same functions
    """

    def __init__(self, num_models, num_features):
        self.models = [linear_model.SGDRegressor()] * num_models
        self.num_models = num_models
        x_train_single = [np.random.random() for i in range(num_features)]
        for i in range(num_models):
            self.models[i].fit([x_train_single], [np.random.random()])

    def get_predictions(self, x_train_single):
        """
        Get predictions for a single row of features
        """

        x_row = x_train_single.toarray()
        h = []
        for i in range(self.num_models):
            h.append(self.models[i].predict(x_row)[0])

        return h

    def update(self, x_train_single, updated_h):
        """
        Train a single step with the updated_h as a list of expected output
        """
        x_row = x_train_single.toarray()
        for i in range(self.num_models):
            self.models[i].partial_fit(x_row, [updated_h[i]])


class SimpleLinear:
    """
    Model class 
    Can be replaced by any other model with same functions
    """
    learning_rate = 0.001

    def __init__(self, num_models, num_features):
        self.num_models = num_models
        self.num_features = num_features
        self.weights = np.random.rand(num_models, num_features)

    def get_predictions(self, x_train_single):
        """
        Get predictions for a single row of features
        """

        # x_row = x_train_single.toarray()
        x_row = x_train_single
        x_row = x_row.reshape(-1, 1)
        # print(np.shape(self.weights),x_row.shape)

        h = sparse.lil_matrix.dot(self.weights,x_row)
        y = []
        for val in h:
            y.append(val[0])
        # print(h,y)
        return y

    def update(self, x_train_single, updated_h):
        """
        Train a single step with the updated_h as a list of expected output
        """
        # x_row = np.array(x_train_single.toarray())
        x_row = x_train_single
        x_row = np.reshape(x_row, (1, self.num_features))
        updated_h = np.array(updated_h)
        updated_h = np.reshape(updated_h, (self.num_models, 1))
        update = sparse.lil_matrix.dot(updated_h, x_row) * self.learning_rate
        self.weights += update
        # self.biases += updated_h * self.learning_rate


class MLP:

    def __init__(self, num_models, num_features):
        self.models = [neural_network.MLPRegressor()
                       for i in range(num_models)]
        self.num_models = num_models
        x_train_single = [np.random.random() for i in range(num_features)]
        for i in range(num_models):
            self.models[i].fit(x_train_single, np.random.random())

    def get_predictions(self, x_train_single):
        h = list()
        for i in range(self.num_models):
            h.append(self.models[i].predict(x_train_single))

    def update(self, x_train_single, updated_h):
        for i in range(self.num_models):
            self.models[i].partial_fit(x_train_single, updated_h[i])


if __name__ == "__main__":
    s = SimpleLinear(10, 20)

