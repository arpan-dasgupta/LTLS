from sklearn import neural_network
import numpy as np


class Linear:

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
