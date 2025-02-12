import numpy as np
from sklearn import neural_network, linear_model
from scipy import sparse
#from numba import njit,jit
import cupy as cp
import cupyx

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

#@jit
def updater(x_row,updated_h,weights,num_features,num_models,learning_rate):
    x_row = cp.array(x_row.toarray())
    x_row = cp.reshape(x_row,(1,num_features))
    #x_row = x_row.reshape(1, num_features)
    #x_row = cupyx.scipy.sparse.csr_matrix(x_row)
    updated_h = cp.array(updated_h)
    updated_h = cp.reshape(updated_h, (num_models, 1))
    #update = cupyx.scipy.sparse.csr_matrix.dot(updated_h, x_row) * learning_rate
    update = cp.dot(updated_h,x_row) * learning_rate
    weights += update
    cp.cuda.Stream.null.synchronize()

class SimpleLinear:
    """
    Model class 
    Can be replaced by any other model with same functions
    """
    learning_rate = 0.03

    def __init__(self, num_models, num_features):
        self.num_models = num_models
        self.num_features = num_features
        self.weights = cp.random.rand(num_models, num_features)

    def get_predictions(self, x_train_single):
        """
        Get predictions for a single row of features
        """

        x_row = x_train_single.toarray()
        x_row = cp.array(x_row.reshape(-1, 1))
        #x_row = cupyx.scipy.sparse.csr_matrix(x_row)
	
        #h = cupyx.scipy.sparse.csr_matrix.dot(self.weights, x_row)
        h = cp.matmul(self.weights,x_row)
        h = cp.reshape(h,(self.num_models))
        h = cp.asnumpy(h)
        
        cp.cuda.Stream.null.synchronize()
        return h.tolist()
        #y = []
        #for val in h:
        #    y.append(val[0])
        
        #return y

    
    def update(self, x_train_single, updated_h):
        """
        Train a single step with the updated_h as a list of expected output
        """
        # x_row = cp.array(x_train_single.toarray())
        # cp.cuda.Stream.null.synchronize()
        updater(x_train_single,updated_h,self.weights,self.num_features,self.num_models,self.learning_rate)
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
