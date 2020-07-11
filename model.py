from sklearn import neural_network, linear_model
import numpy as np


class Linear:
    """
    Model class 
    Can be replaced by any other model with same functions
    """

    def __init__(self, num_models, num_features):
        self.models = [linear_model.LinearRegression()] * num_models
        self.num_models = num_models
        x_train_single = [np.random.random()] * num_features
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
